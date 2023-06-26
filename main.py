# Required for redis to work
from gevent import monkey
monkey.patch_all()

# import eventlet
# eventlet.monkey_patch()

import traceback
import flask
from flask import Flask, request
from flask_socketio import SocketIO, send, emit, join_room, leave_room
import json
from opulence import Opulence
from Config import Config
from GlobalMethods import log, error
from dynamodb_controller import DynamoDBController
import pprint
import os
# from dynamodb_controller import DynamoDBController

# Set url to use localhost if the environment variable isn't found
redis_host = os.environ.get("REDIS_HOST", "localhost:6379/")
redis_url = f"redis://{redis_host}"

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'

# Logger= True to show emit logs
# message_queue=redis_url, <- put in SocketIO params to use redis
socketio = SocketIO(app, cors_allowed_origins='*', message_queue=redis_url, logger=True, async_mode='gevent')

games_dict={} # local games, this doesn't get sent to the front-end

# TODO: Replace this with Dynamo query function that emits games
games_list={} # emitted to clients


# @app.route('/')
# def index():
#     return flask.render_template('index.html')
authenticated_users = {}

ddb = DynamoDBController()

@socketio.on("redis-test")
def redis_test(data):
    print(f"Retrieved redis test data: {data}")
    join_room("redis")
    emit("redis-test", data, room="redis")

# built-in 'connect' event for socket io which gets called every time a user loads the webpage
@socketio.on('connect')
def client_connect():
    print("user connected: ", request.sid)
    sid = str(request.sid)
    flask.session['sid'] = sid
    flask.session['gameID'] = None
    flask.session['displayName'] = ''
    emit('user-sid', sid)
    #  # TODO: Remove this call completely and instead create a function/API that queries dynamo and emits the games_list from the response.
    # emit('list-games', games_list, broadcast=True)
    # emit('Connection', 'Connected!') # Send 'Connection' data to the client
    
    log('client loaded the webpage: ' + str(sid))

@socketio.on('query-games')
def query():

    response = ddb.find_games(limit=1)
    pprint.pp(response)
    last_key = response.get('LastEvaluatedKey')
    deserialized = ddb.deserialize(data=response['Items'])
    data = ddb.convert_decimal_to_int(deserialized) # Convert 'Decimal' objects to ints
    emit('list-games', {"games": data, "last_key": last_key})

@socketio.on('auth')
def authenticate(data):
    sub = data.get('sub')
    user_name = data.get('username')
    print("user was authenticated: ", data)
    if sub != None:
        flask.session['sub'] = sub
        flask.session['displayName'] = user_name

        if authenticated_users.get(sub) == None:
            authenticated_users[sub] = flask.session['sid']
        emit('user-sid', authenticated_users[sub])

# # built-in 'disconnect' event for socket io which gets called every time a user refreshes/closes the browser tab
@socketio.on('disconnect')
def on_client_disconnect():
    # if the user isn't an authenticated user, remove them from the game
    if flask.session.get('sub') == None:
        sid = str(flask.session['sid'])
        gameID = str(flask.session['gameID'])
        name = flask.session['displayName']
        # if the player isn't in a game when they disconnect, return
        if gameID == 'None':
            return
        # TODO replace opulence ref w/ Opulence(game_id=game_id), opulence._load_game_state()
        opulence = games_dict[gameID]
        log(f"Player is Disconnecting....: {name}")
        if opulence.remove_player(sid, name, disconnected=True):
            print(f"Player Disconnected: {name}")
            leave_room(gameID) 
            flask.session['gameID'] = None
            # remove the game if nobody is in it
            if len(opulence.players) <= 0:
                # TODO: Remove game from dynamodb instead. Also remove the user.
                del games_list[gameID]
                del games_dict[gameID]
                # TODO: test this
                ddb.delete_game(game_id=gameID, users=opulence.player_sids)
                turn_timer = 0
                emit('turn-timer', turn_timer, room=gameID)
            elif len(opulence.players) > 0:
                emit('game-logs', opulence.game_logs.logs, room=gameID)
                emit('game-data', opulence._get_game_data(), room=gameID) # send the new game-data
                # if the game is started, emit the next persons turn. It could have been the turn of the person who left
                if opulence.game_started and not opulence.game_over: 
                    emit('current-turn-sid', opulence._get_current_turn_sid(), room=gameID)
                    emit('turn-timer', opulence.config.turn_timer, room=gameID)
            opulence.game_logs.logs = [] # clear logs for next action

# emit to the clients when a user selects an attack card they want to play
@socketio.on('attack-card-selected')
def attack_card_selected(data):
    gameID = str(flask.session['gameID'])
    sid = authenticated_users.get(flask.session.get('sub'), str(flask.session['sid']))
    # TODO replace opulence ref w/ Opulence(game_id=game_id), opulence._load_game_state()
    opulence = games_dict[gameID]

    # make sure the button only disapears if it's the turn of the player that clicks the attack button 
    if opulence._get_current_turn_sid() == sid:
        if data == "true":
            emit('user-playing-attack-card', "true", room=gameID)
        elif data == "false":
            emit('user-playing-attack-card', "false", room=gameID)
    
    


# handle when the card shop, dragon shop, and users 'hand' buttons get pressed
@socketio.on('shop-buttons-pressed')
def shop_button_pressed(data):
    sid = authenticated_users.get(flask.session.get('sub'), str(flask.session['sid']))
    gameID = str(flask.session['gameID'])
    # TODO replace opulence ref w/ Opulence(game_id=game_id), opulence._load_game_state()
    opulence = games_dict[gameID]

    print(data)
    # if it's the players turn who's pushing the buttons
    if opulence._get_current_turn_sid() == sid:
        if data['button'] == "shop":
            emit('button-pressed', "shop", room=gameID)
            # make sure if the user changes their mind on playing an attack card, the attack swords are removed.
            emit('user-playing-attack-card', "false", room=gameID)
        elif data['button'] == "dragon":
            emit('button-pressed', "dragon", room=gameID)
            emit('user-playing-attack-card', "false", room=gameID)
        elif data['button'] == "hand":
            emit('button-pressed', "hand", room=gameID)
            emit('user-playing-attack-card', "false", room=gameID)
        elif data['button'] == "craft":
            emit('button-pressed', "craft", room=gameID)
            emit('user-playing-attack-card', "false", room=gameID) 
        
        emit('play-sound', 'muted_click', room=gameID)

# taking runes
@socketio.on('take-rune')
def take_rune(data):
    try:
        sid = authenticated_users.get(flask.session.get('sub'), str(flask.session['sid']))
        gameID = str(flask.session['gameID'])
        # TODO replace opulence ref w/ Opulence(game_id=game_id), opulence._load_game_state()
        opulence = games_dict[gameID]
        rune = str(data)
        runes_taken = opulence.runes_taken
        print(f"player {sid} tried taking {rune}")
        if opulence.take_rune(sid, rune):
            emit('game-logs', opulence.game_logs.logs, room=gameID)
            emit('game-data', opulence._get_game_data(), room=gameID) # send the current_game_data to the client
            emit('play-sound', 'soft_click', room=gameID)
            if runes_taken == opulence.config.runes_per_turn - 1: # if before taking another rune the amount taken would cause a change in turns:
                emit('current-turn-sid', opulence._get_current_turn_sid(), room=gameID) # emit whose turn it is
                turn_timer = opulence.config.turn_timer
                # notify the front end if someone died
                if opulence.game_logs.new_death:    
                    emit('player-died', opulence.game_logs.new_death, room=gameID)
                    opulence.game_logs.new_death = None
                # notify the front end if gameover
                if opulence.game_over:
                    emit('game-over', opulence.game_logs.winner, room=gameID)
                    turn_timer = 0
                emit('turn-timer', turn_timer, room=gameID)
            opulence.game_logs.logs = [] # clear logs for next action

    except Exception as e:
        error(f"❌ {e}\n```{traceback.format_exc()[:1900]}```")

# playing a card
@socketio.on('play-card')
def play_card(data):
    try:
        sid1 = authenticated_users.get(flask.session.get('sub'), str(flask.session['sid']))
        if data.get('attackedPlayer'):
            sid2 = str(data['attackedPlayer'])
        else:
            sid2 = None
        card_idx = data.get('index', 0)
        gameID = str(flask.session['gameID'])
        # TODO replace opulence ref w/ Opulence(game_id=game_id) \ opulence._load_game_state()
        opulence = games_dict[gameID]

        # record the number of living players
        alive_count = len(opulence._get_living_players())

        if card_idx == None:
            return

        if opulence.game_over:
            return
        # if it's the players turn who's trying to play a card
        if opulence._get_current_turn_sid() == sid1:
            log(f"card at index: {card_idx} was attempted to be played")
            if opulence.play_card(card_idx, sid1, sid2):
                log('playing the card was successful')
                emit('game-logs', opulence.game_logs.logs, room=gameID)
                emit('game-data', opulence._get_game_data(), room=gameID) # send the current_game_data to the client
                emit('current-turn-sid', opulence._get_current_turn_sid(), room=gameID)
                turn_timer =  opulence.config.turn_timer

                # notify the front end if someone died
                if opulence.game_logs.new_death:    
                    emit('player-died', opulence.game_logs.new_death, room=gameID)
                    opulence.game_logs.new_death = None
                # notify the front end if gameover
                if opulence.game_over:
                    emit('game-over', opulence.game_logs.winner, room=gameID)
                    turn_timer = 0
                # play a sound if a card was played
                elif opulence.game_logs.played_card:
                    if opulence.game_logs.played_card == "ATTACK":
                        emit('play-sound', 'play_attack', room=gameID)
                    elif opulence.game_logs.played_card == "SHIELD":
                        emit('play-sound', 'play_shield', room=gameID)
                    opulence.game_logs.played_card = None
                emit('turn-timer', turn_timer, room=gameID)
                opulence.game_logs.logs = [] # clear logs for next action

    except Exception as e:
        error(f"❌ {e}\n```{traceback.format_exc()[:1900]}```")

# buying a card
@socketio.on('buy-card')
def buy_card(data):
    try:
        sid = authenticated_users.get(flask.session.get('sub'), str(flask.session['sid']))
        gameID = str(flask.session['gameID'])
        # TODO replace opulence ref w/ Opulence(game_id=game_id), opulence._load_game_state()
        opulence = games_dict[gameID]
        card_idx = data['index']
        log(f"card at index: {card_idx} was attempted to be purchased")
        if opulence.buy_card(sid, card_idx):
            log('buying the card was successful')
            emit('game-logs', opulence.game_logs.logs, room=gameID)
            emit('game-data', opulence._get_game_data(), room=gameID) # send the current_game_data to the client
            emit('current-turn-sid', opulence._get_current_turn_sid(), room=gameID)
            emit('play-sound', 'purchase_legendary', room=gameID)
            turn_timer =  opulence.config.turn_timer
            # notify the front end if someone died
            if opulence.game_logs.new_death:    
                emit('player-died', opulence.game_logs.new_death, room=gameID)
                opulence.game_logs.new_death = None
            # notify the front end if gameover
            if opulence.game_over:
                emit('game-over', opulence.game_logs.winner, room=gameID)
                turn_timer = 0

            emit('turn-timer', turn_timer, room=gameID)
            opulence.game_logs.logs = [] # clear logs for next action

    except Exception as e:
        error(f"❌ {e}\n```{traceback.format_exc()[:1900]}```")

# crafting a card
@socketio.on('craft-card')
def craft_card(data):
    try:
        sid = authenticated_users.get(flask.session.get('sub'), str(flask.session['sid']))
        gameID = str(flask.session['gameID'])
        
        element1 = data['element1']
        element2 = data['element2']
        # TODO replace opulence ref w/ Opulence(game_id=game_id), opulence._load_game_state()
        opulence = games_dict[gameID]
        if opulence.buy_basic_card(sid, element1=element1, element2=element2):
            log('crafting the card was successful')
            emit('game-logs', opulence.game_logs.logs, room=gameID)
            emit('game-data', opulence._get_game_data(), room=gameID) # send the current_game_data to the client
            emit('current-turn-sid', opulence._get_current_turn_sid(), room=gameID)
            emit('play-sound', 'purchase', room=gameID)
            turn_timer =  opulence.config.turn_timer
            
            # notify the front end if someone died
            if opulence.game_logs.new_death:    
                emit('player-died', opulence.game_logs.new_death, room=gameID)
                opulence.game_logs.new_death = None
            # notify the front end if gameover
            if opulence.game_over:
                emit('game-over', opulence.game_logs.winner, room=gameID)
                turn_timer = 0

            emit('turn-timer', turn_timer, room=gameID)
            opulence.game_logs.logs = [] # clear logs for next action

    except Exception as e:
        error(f"❌ {e}\n```{traceback.format_exc()[:1900]}```")

# buying a dragon
@socketio.on('buy-dragon')
def buy_dragon(data):
    try:
        sid = authenticated_users.get(flask.session.get('sub'), str(flask.session['sid']))
        gameID = str(flask.session['gameID'])
        
        # TODO replace opulence ref w/ Opulence(game_id=game_id), opulence._load_game_state()
        opulence = games_dict[gameID]
        dragon_idx = data['index']
        log(f"dragon at index: {dragon_idx} was attempted to be purchased")
        if opulence.buy_dragon(sid, dragon_idx):
            log('buying the dragon was successful')
            emit('game-logs', opulence.game_logs.logs, room=gameID)
            emit('game-data', opulence._get_game_data(), room=gameID) # send the current_game_data to the client
            emit('dragon-shop-data', opulence._get_dragon_shop_data(), room=gameID)
            emit('current-turn-sid', opulence._get_current_turn_sid(), room=gameID)
            emit('play-sound', 'dragon_growl', room=gameID)
            turn_timer =  opulence.config.turn_timer
            # notify the front end if someone died
            if opulence.game_logs.new_death:    
                emit('player-died', opulence.game_logs.new_death, room=gameID)
                opulence.game_logs.new_death = None
            # notify the front end if gameover
            if opulence.game_over:
                emit('game-over', opulence.game_logs.winner, room=gameID)
                turn_timer = 0
            
            emit('turn-timer', turn_timer, room=gameID)
            opulence.game_logs.logs = [] # clear logs for next action
    except Exception as e:
        error(f"❌ {e}\n```{traceback.format_exc()[:1900]}```")


@socketio.on('play-button')
def play_button(data):
    try:
        display_name = data.get('username', '') if isinstance(data.get('username', ''), str) and len(data.get('username', '')) <= 20 else ''
        if display_name == '':
            display_name = flask.session['sid']
        flask.session['displayName'] = display_name
        log('client set their display name as: ' + str(display_name))
    except Exception as e:
        error(f"❌ {e}\n```{traceback.format_exc()[:1900]}```")

@socketio.on('create-game')
def create_game(data):
    try:
        max_players = min(99, max(2, data.get('maxplayers', 8))) if isinstance(data.get('maxplayers'), int) else 8
        runes_per_turn = min(99, max(1, data.get('runesperturn', 5))) if isinstance(data.get('runesperturn'), int) else 5
        dragons_in_shop = min(99, max(0, data.get('totaldragons', 2))) if isinstance(data.get('totaldragons'), int) else 2
        cards_in_shop = min(20, max(0, data.get('cardsinshop', 5))) if isinstance(data.get('cardsinshop'), int) else 5
        player_starting_hp = min(99, max(1, data.get('startinghealth', 10))) if isinstance(data.get('startinghealth'), int) else 10
        turn_timer = min(10000, max(1, data.get('turntimer', 30))) if isinstance(data.get('turntimer'), int) else 30

        sid = authenticated_users.get(flask.session.get('sub'), str(flask.session['sid']))
        name = flask.session['displayName']
        opulence = Opulence(
            Config(max_players=max_players,
            runes_per_turn=runes_per_turn,
            dragons_in_shop=dragons_in_shop,
            cards_in_shop=cards_in_shop,
            player_starting_health=player_starting_hp,
            turn_timer=turn_timer
            ))
        game_id = opulence.game_id
        opulence.game_logs.create_game_log(name, game_id)
        opulence.add_player(sid, flask.session['displayName'])
        opulence._save_state()         # Add game and user to dynamodb.


        games_dict[game_id] = opulence # add the game to the games dict
        flask.session['gameID'] = game_id # add the gameid to the clients flask session dict

        games_list[game_id] = {"gameID": game_id, "started": opulence.game_started, "users": opulence.player_names}
        join_room(game_id) # join the flask room corresponding to the gameID of the newly created game
        emit('current-room-id', str(flask.session['gameID'])) # send the client what their current gameID is
        emit('game-logs', opulence.game_logs.logs, room=game_id)
        emit('game-data', opulence._get_game_data(), room=game_id)
        emit('dragon-shop-data', opulence._get_dragon_shop_data(), room=game_id)
        emit('user-sid', sid)
        opulence.game_logs.logs = [] # clear logs for next action
    except Exception as e:
        error(f"❌ {e}\n```{traceback.format_exc()[:1900]}```")

@socketio.on('start-game')
def start_game():
    try:
        gameID = str(flask.session['gameID'])
        sid = authenticated_users.get(flask.session.get('sub'), str(flask.session['sid']))
        # TODO replace opulence ref w/ Opulence(game_id=game_id), opulence._load_game_state()
        opulence = games_dict[gameID]
        
        if opulence.start_game(sid):
            games_list[gameID]['started'] = True
            emit('game-logs', opulence.game_logs.logs, room=gameID)
            emit('current-turn-sid', opulence._get_current_turn_sid(), room=gameID)
            emit('game-started', True, room=gameID)
            emit('turn-timer', opulence.config.turn_timer, room=gameID)
            opulence.game_logs.logs = [] # clear logs for next action
    except Exception as e:
        error(f"❌ {e}\n```{traceback.format_exc()[:1900]}```")


#rooms (join/leave room)
@socketio.on('join-room')
def on_join(data):
    try:
        gameID = str(data['gameid'])
        sid = authenticated_users.get(flask.session.get('sub'), str(flask.session['sid']))
        name = flask.session['displayName']
        # TODO replace opulence ref w/ Opulence(game_id=game_id), opulence._load_game_state()
        if games_dict.get(gameID):
            opulence = games_dict[gameID]
        else:
            opulence = Opulence(
                config=Config(),
                game_id=gameID
            )
            opulence._load_game_state()
            games_dict[gameID] = opulence

        # join as a spectator
        if opulence.game_started:
            flask.session['gameID'] = gameID        # put the gameID in the users flask session
            join_room(gameID)                       # join the flask_room corresponding to the gameID
            emit('join-room')
            emit('game-logs', opulence.game_logs.logs, room=gameID)
            emit('game-data', opulence._get_game_data(), room=gameID) # send the new game-data
            emit('dragon-shop-data', opulence._get_dragon_shop_data(), room=gameID)
            emit('current-turn-sid', opulence._get_current_turn_sid(), room=gameID)
            opulence.game_logs.logs = [] # clear logs for next action

        elif opulence.add_player(sid, name):
            log(f"added {name} to game")
            flask.session['gameID'] = gameID        # put the gameID in the users flask session
            join_room(gameID)                       # join the flask_room corresponding to the gameID
            emit('join-room')
            emit('game-logs', opulence.game_logs.logs, room=gameID)
            emit('game-data', opulence._get_game_data(), room=gameID) # send the new game-data
            emit('dragon-shop-data', opulence._get_dragon_shop_data(), room=gameID)
            opulence.game_logs.logs = [] # clear logs for next action
    except Exception as e:
        error(f"❌ {e}\n```{traceback.format_exc()[:1900]}```")

    

@socketio.on('leave-room')
def on_leave():
    try:
        sid = authenticated_users.get(flask.session.get('sub'), str(flask.session['sid']))
        gameID = str(flask.session['gameID'])
        name = flask.session['displayName']
        # TODO replace opulence ref w/ Opulence(game_id=game_id), opulence._load_game_state()
        opulence = games_dict[gameID]
        log("user left the room " + name)
        if opulence.remove_player(sid, name):
            leave_room(gameID) 
            flask.session['gameID'] = None
            # remove the game if nobody is in it
            if len(opulence.players) <= 0:
                del games_list[gameID]
                del games_dict[gameID]
            elif len(opulence.players) > 0:
                emit('game-logs', opulence.game_logs.logs, room=gameID)
                emit('game-data', opulence._get_game_data(), room=gameID) # send the new game-data
                # if the game is started, emit the next persons turn. It could have been the turn of the person who left
                if opulence.game_started and not opulence.game_over:
                    emit('current-turn-sid', opulence._get_current_turn_sid(), room=gameID)
            opulence.game_logs.logs = [] # clear logs for next action
    except Exception as e:
        error(f"❌ {e}\n```{traceback.format_exc()[:1900]}```")


def emit_game_turn(opulence: Opulence, game_id):
    # Helper function. Can't emit 'game-data'. payload too big.
    socketio.emit('current-turn-sid', opulence._get_current_turn_sid(), room=game_id)
    socketio.emit('game-logs', opulence.game_logs.logs, room=game_id)
    socketio.emit('turn-timer', opulence.config.turn_timer, room=game_id)


if __name__ == '__main__':
    
    try:
        # app.debug = True
        print("Flask server listening on port 5000!")
        # Set host="0.0.0.0" to be able to connect to docker container running this app externally (make the server externally visible). Default is 127.0.0.1
        socketio.run(app, host="0.0.0.0", port=5000)
        

    except Exception as e:
        error(f"❌ {e}\n```{traceback.format_exc()[:1900]}```")