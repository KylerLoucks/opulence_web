import { socket } from "./websocket";
import GameState from "./GameState";



socket.on('user-sid', (res) => {
    GameState.state.sid = res
    console.log('your sid equals ' + GameState.state.sid)
});


socket.on('current-turn-sid', (res) => {
    GameState.state.currentTurnSid = res

    // if the sid that came back from the server matches
    if (GameState.state.sid == GameState.state.currentTurnSid) {
      GameState.state.isTurn = true // make buttons visible
      var audio = new Audio(require('@/assets/mp3s/notification.mp3'))
      audio.play()
    } else {
      GameState.state.isTurn = false
    }
    console.log('it is ' + GameState.state.currentTurnSid + ' turn')
});



socket.on('list-games', (res) => {
    for (let i = 0; i < res.games.length; i++) {
        const newGamePK = res.games[i].PK;
    
        // Check if the PK already exists in GameState.state.gamesList
        const gameExists = GameState.state.gamesList.some(game => game.PK === newGamePK);
    
        if (!gameExists) {
          GameState.state.gamesList.push(res.games[i]);
        }
    }

    // gamesList = res.games
    GameState.state.nextToken = res.last_key
    console.log('Active Games: ' + JSON.stringify(GameState.state.gamesList))
});

socket.on('join-room', () => {
    GameState.state.ingame = true
    console.log('In game?: ' + GameState.state.ingame)
});


socket.on('game-logs', (res) => {
    res.map((log) => {
      GameState.state.logs.push(log)
    })
    // old implementation
    // GameState.state.logs = res
});


  // grab dict of user and card shop game data from server
socket.on('game-data', (res) => {
    console.log("got game data:", res)
    GameState.state.current_game_users = res['user_data']
    GameState.state.current_game_card_shop = res['card_shop']['cards']
    console.log("grabbing game data")
});


// // dragon shop data
socket.on('dragon-shop-data', (res) => {
    GameState.state.current_game_dragon_shop = res['dragons']
});



/**
 * clear the countdown timer (reset to 0)
 */
export function clearTurnTimer() {
if (GameState.state.timerId) {
    console.log("CLEARING TIMER")
    clearInterval(this.GameState.state.timerId)
}
    GameState.state.turnSecond = '0',
    GameState.state.turnMinute = '0',
    GameState.state.turnHour = '0',
    GameState.state.turnDay = '0',
    GameState.state.countDate = null
}

/**
 * Starts a countdown timer
 * @param {*} countDate unix epoch formatted date (e.g. 1687110770)
 */
function countDown(countDate) {

const now = new Date().getTime();

// Check if the countdown has finished
if (now >= countDate) {
    console.log('Countdown finished!');
    clearInterval(this.GameState.state.timerId)
    return;
}

const diff = countDate - now;

const second = 1000;
const minute = second * 60;
const hour = minute * 60;
const day = hour * 24;

const m = Math.floor((diff % hour) / minute);
const s = Math.floor((diff % minute) / second);
const h = Math.floor((diff % day) / hour);
const d = Math.floor((diff / day));
m < 10 ? GameState.state.turnMinute = '0' + m : GameState.state.turnMinute = m;
s < 10 ? GameState.state.turnSecond = '0' + s : GameState.state.turnSecond = s;
h < 10 ? GameState.state.turnHour = '0' + h : GameState.state.turnHour = h;
GameState.state.turnDay = d;

}

socket.on('turn-timer', (timer) => {
    GameState.state.countDate = new Date().getTime() + (timer > 0 ? timer + 1 : timer) * 1000;
    GameState.state.timerId = setInterval(() => {
      countDown(GameState.state.countDate)
    }, 1000);
})



socket.on('Connection', (msg) => { // retrieve 'Connection' data from the server
    const connectedMsg = msg
    console.log(connectedMsg)
});

  // receive boolean that a user is about to pick who to attack
socket.on('user-playing-attack-card', (res) => {
    if (res == "true") {
      GameState.state.attacking = true
    } else if (res == "false") {
      GameState.state.attacking = false
    }
    
});

// receive string of the element that killed a player | play the relevant sound effect
socket.on('player-died', (res) => {
    var audio = new Audio(require('@/assets/mp3s/player_died_by_' + res + '.mp3'))
    audio.play()
});

socket.on('game-over', (res) => {
    var audio = new Audio(require('@/assets/mp3s/victory.mp3'))
    // var audio_tie_game = new Audio(require('@/assets/mp3s/reeverb.mp3'))
    console.log('Player won the game: ' + res)
    if (res == null) {
      audio.play()
    } else audio.play()
   

});

  // receive misc sound effect from the server and play it
socket.on('play-sound', (res) => {
    var audio = new Audio(require('@/assets/mp3s/' + res + '.mp3'))
    audio.play()
});

  // receive the current room id that you are in from the server
socket.on('current-room-id', (res) => {
    GameState.state.current_room_id = res
    console.log('Received current game ID as: ' + res)
});

  // receive button pressed data when another player opens the shop, etc.
socket.on('button-pressed', (res) => {
    if (res == "shop") {
      GameState.state.buyingShopCards = true
      GameState.state.buyingDragonCards = false
      GameState.state.showHand = false
      GameState.state.crafting = false
      GameState.state.showChat = false
    } else if (res == "dragon") {
      GameState.state.buyingDragonCards = true
      GameState.state.buyingShopCards = false
      GameState.state.showHand = false
      GameState.state.crafting = false
      GameState.state.showChat = false
    } else if (res == "hand") {
      GameState.state.showHand = true
      GameState.state.buyingShopCards = false
      GameState.state.buyingDragonCards = false
      GameState.state.crafting = false
      GameState.state.showChat = false
    } else if (res == "craft") {
      GameState.state.crafting = true
      GameState.state.buyingShopCards = false
      GameState.state.buyingDragonCards = false
      GameState.state.showHand = false
      GameState.state.showChat = false
    } else if (res == "logs") {
      GameState.state.showChat = true
      GameState.state.crafting = false
      GameState.state.buyingShopCards = false
      GameState.state.buyingDragonCards = false
      GameState.state.showHand = false
      GameState.state.showChat = false
    }
});

    // receive (boolean) if game started
socket.on('game-started', (res) => {
      GameState.state.gameStarted = res
      console.log("from server: Game started ? " + res)
});