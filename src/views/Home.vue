<template>
    <div id="home">
      <PageLoader></PageLoader>
  
  
      <transition name="settings" v-show="GameState.state.showSettings" appear>
          <div class="settings">
            <fa v-if="GameState.state.showSettings" icon="fa-solid fa-close" size="lg" class="settings-close-btn" v-on:click="GameState.state.showSettings = false" />
          </div>
      </transition>
      <span v-if="!GameState.state.showSettings" id="mobile-hamburger" class="material-icons" v-on:click="GameState.state.showSettings = true">menu</span>
    
      
      <div class="games-parent-container" >
        <GamesMenu :games="GameState.state.gamesList" @joinRoom="joinRoom" @signOut="signOut()" @name="setDisplayName()" @showGameModal="GameState.state.showGameConfigModal = true"></GamesMenu>
      </div>

      <transition name="config-fade" appear>
        <div class="game-config-overlay" v-if="GameState.state.showGameConfigModal" @click="GameState.state.showGameConfigModal = false"></div>
      </transition>
      <transition name="config-slide" appear>
        <div class="game-config-modal" v-if="GameState.state.showGameConfigModal">
          <h1>Game Config</h1>
          <div class="game-config-modal-inputs-container">
            <div class="input-game-config">
              <span>Max Players</span>
              <input class="config-input" v-model="GameState.state.configMaxPlayers" type="number" placeholder="8" maxlength="2" min="2">
            </div>
            <div class="input-game-config">
              <span>Legendary Cards In Shop
                <img draggable="false" src="@/assets/sword.png" style="width:20px; height: 20px;"/>
              </span>
              <input class="config-input" v-model="GameState.state.configShopSize" type="number" placeholder="5" maxlength="2" min="0">
            </div>
            <div class="input-game-config">
              <span>Dragons In Shop
                <img draggable="false" src="@/assets/dragons/icons/LAVAdragon-icon.png" style="width:20px; height: 20px;"/>
              </span>
              <input class="config-input" v-model="GameState.state.configTotalDragons" type="number" placeholder="2" maxlength="2" min="0">
            </div>
            <div class="input-game-config">
              <span>Runes-Per-Turn
                <img draggable="false" :src="iconPath(`NATURE.png`)" style="width:20px; height: 20px;"/>
              </span>
              <input class="config-input" v-model="GameState.state.configRunesPerTurn" type="number" placeholder="5" maxlength="2" min="1">
            </div>
            <div class="input-game-config">
              <span>Player Starting Health
                <img draggable="false" :src="iconPath(health_icon)" style="width:20px; height: 20px;"/>
              </span>
              <input class="config-input" v-model="GameState.state.configPlayerStartHealth" type="number" placeholder="10" maxlength="3" min="1">
            </div>
            <div class="input-game-config">
              <span>Turn Timer (Seconds)
                <fa icon="fa-solid fa-stopwatch" size="lg" class="timer-icon" />
              </span>
              <input class="config-input" v-model="GameState.state.configTurnTimer" type="number" placeholder="30" maxlength="4" min="10">
            </div>
          </div>
          <button class="game-config-modal-button" v-on:click="createGame(), GameState.state.showGameConfigModal = false">Create Lobby</button>
        </div>
      </transition>
      
      
 
  
    
    
  
  
    
    
  </div>
    
  </template>
    
    <script>
    // import { ref } from "vue";
    
    // import Authenticate from "@/components/authenticate/Authenticate.vue"
    import PageLoader from "@/components/PageLoader.vue";
    import GamesMenu from "@/components/pagination/GamesMenu.vue";

  
    import { userPool } from "@/components/authenticate/UserPool"
  
    import { socket } from "@/websocket"
  
    import AuthState from "@/components/authenticate/AuthState"
    import GameState from "@/GameState";
  
    import utils from "@/utils";
    
    export default {
      name: 'HomeView',
      components: {

        // Games,

        // Authenticate,
        PageLoader,
        GamesMenu,

      },
      setup() {
        // const hp = ref(0);
        // setInterval(() => (hp.value = Math.floor(Math.random() * 35)),2000);
        
        // return {hp}
        
      },
      data: function() {
        return {
          shield: 10,
          health_icon: "heart.png",
          death_icon: "death.png",
          shield_icon: "shield.png",
          shield_color: "#dd221e",
          utils,
          AuthState,
          GameState,
          socket,
        }
      },
      methods: {

        // rooms with socket io
        joinRoom: function(gameid) {
          try {
            console.log("Attempting to join game: ", gameid);
            this.socket.emit('join-room', { 'gameid': gameid }, (response) => {
                console.log("RESPONSE:", response);
                if (response.success) {
                    this.utils.setJoinSuccessful(true)
                    this.GameState.state.ingame = true;
                    this.GameState.state.current_room_id = gameid;
                    // this.GameState.state.gameStarted = this.GameState.state.gamesList[gameid].started;
                    console.log("SUCCESS RESPONSE!!");
                    this.$router.push({ name: 'game', params: { gameid: gameid } });
                } else {
                    console.log("RESPONSE WAS NOT SUCCESSFUL");
                }
            });
          } catch (error) {
              console.log('Error while joining room:', error);
          }
        },
  
        checkScreenSize() {
            
            // Update isMobile based on the current screen size
            if (window.innerWidth <= 768) {
              this.utils.setMobile(true)
            } else {
              this.utils.setMobile(false)
            }
        },
  
        viewSettings() {
          if (this.showSettings == true) {
            this.showSettings = false
          } else {
            this.showSettings = true
          }
          
        },
  
  
        pickRandomBackgroundOnDOMLoad() {
          var backgrounds = ['bg_1.png', 'bg_2.png', 'bg_3.png', 'bg_4.png', 'bg_5.png', 'bg_6.png', 'bg_7.png', 'bg_8.png', 'bg_9.png', 'bg_10.png']
          document.body.style.backgroundImage = 'url(' + require('@/assets/backgrounds/'+backgrounds[Math.floor(Math.random() * backgrounds.length)]) + ')'
        },
    
        // sendMessage: function() {
        //   console.log("sending message")
          
        //   this.shield = Math.floor(Math.random() * 10) // remove this later
    
        //   let random = Math.floor(Math.random() * 7) // num between 0 and 7
        //   this.updateShield(this.shield_icons[random].color, this.shield_icons[random].icon) // remove this later
    
        //   let data = {icon: this.shield_icon, color: this.shield_color, shield_value: this.shield}
        //   this.socket.emit('icon', data)
        //   console.log(`sent message data: ${data}`)
          
          
        //   this.fire_rune_count++
        // },
  

    
        // KEEP ME ALIVE AT ALL COSTS
        iconPath(value) {
          return require(`@/assets/${value}`)
        },
    
  
        // sign out of cognito
        signOut() {
            var cognitoUser = userPool.getCurrentUser()
            if (cognitoUser != null) { 
                cognitoUser.signOut(() => {
                  this.AuthState.setAuthenticated(false)
                  this.$router.push('/login')
              });
            }
        },
    
        setDisplayName() {
          this.socket.emit('play-button', {'username': String(this.GameState.state.userName)})
          console.log(this.GameState.state.userName)
        },
    
        createGame: function() {
          this.socket.emit('create-game', 
          {maxplayers: this.GameState.state.configMaxPlayers,
          cardsinshop: this.GameState.state.configShopSize,
          runesperturn: this.GameState.state.configRunesPerTurn,
          totaldragons: this.GameState.state.configTotalDragons,
          startinghealth: this.GameState.state.configPlayerStartHealth,
          turntimer: this.GameState.state.configTurnTimer}, (response) => {
            if (response.success) {
              const gameid = response.gameid
              console.log('created a game')
              console.log('player health: ' + this.GameState.state.configPlayerStartHealth)
              GameState.state.current_game_users = response.game_data.user_data
              GameState.state.current_game_card_shop = response.game_data.card_shop.cards
              GameState.state.current_turn_sid = response.current_turn_sid
              GameState.state.logs = response.logs
              GameState.state.sid = response.sid
              GameState.state.ingame = true
              utils.setCreatedGame(true)
              this.$router.push({ name: 'game', params: { gameid: gameid} });
            } else {
              console.log("RESPONSE WAS NOT SUCCESSFUL");
            }
          })
          
          
        },
    
        showTutorial: function() {
          console.log('showing tutorial')
          this.tutorial = true;
      
        },
    
      },
    
  
      // before the DOM is mounted
      beforeMount: function() {

        // Grab cognito user from local storage
        const cognitoUser = userPool.getCurrentUser()
        console.log("current_user: ", userPool.getCurrentUser())
        if (cognitoUser != null) {

          // check if user is authenticated
          cognitoUser.getSession((err, session) => {
            if (err) {
            alert(err.message || JSON.stringify(err))
            }
            // user is valid
            this.AuthState.setAuthenticated(session.isValid())

            cognitoUser.getUserAttributes((err, attributes) => {
            if (err) {
                console.log("Error when getting user attributes: ", err)
            }
            let sub = attributes[0].getValue()
            let username = cognitoUser.getUsername()
            // console.log("Attributes: ", attributes)
            this.socket.emit('auth', {'sub': sub, 'username': username})
            })
          })
        }
      },
  
      
      created: function() {
  
        // connect socket handling
        // this.socket.on('user-sid', (res) => {
        //   this.GameState.state.sid = res
        //   console.log('your sid equals ' + this.GameState.state.sid)
        // });
    
        // this.socket.on('current-turn-sid', (res) => {
        //   this.GameState.state.currentTurnSid = res
    
        //   // if the sid that came back from the server matches
        //   if (this.GameState.state.sid == this.GameState.state.currentTurnSid) {
        //     this.GameState.state.isTurn = true // make buttons visible
        //     var audio = new Audio(require('@/assets/mp3s/notification.mp3'))
        //     audio.play()
        //   } else {
        //     this.GameState.state.isTurn = false
        //   }
        //   console.log('it is ' + this.GameState.state.currentTurnSid + ' turn')
        // });
    
        // receive list of active games
        // this.socket.on('list-games', (res) => {
        //   console.log('Active Games: ' + JSON.stringify(this.GameState.state.gamesList))
        //   for (let i = 0; i < res.games.length; i++) {
        //     this.GameState.state.gamesList.push(res.games[i])
        //   }
  
        //   // this.gamesList = res.games
        //   this.GameState.state.nextToken = res.last_key
        //   console.log('Active Games: ' + JSON.stringify(this.GameState.state.gamesList))
        // });
    
        // this.socket.on('join-room', () => {
        //   this.GameState.state.ingame = true
        //   console.log('In game?: ' + this.GameState.state.ingame)
        // });
    

        // this.socket.on('game-logs', (res) => {
        //   res.map((log) => {
        //     this.GameState.state.logs.push(log)
        //   })
        //   // old implementation
        //   // this.GameState.state.logs = res
        // });
  

        // // grab dict of user and card shop game data from server
        // this.socket.on('game-data', (res) => {
        //   console.log("got game data:", res)
        //   this.GameState.state.current_game_users = res['user_data']
        //   this.GameState.state.current_game_card_shop = res['card_shop']['cards']
        //   console.log("grabbing game data")
        // });
    
    
        // // // dragon shop data
        // this.socket.on('dragon-shop-data', (res) => {
        //   this.GameState.state.current_game_dragon_shop = res['dragons']
        // });
        
      },
    
      // do things on first load of the DOM
      mounted: function() {
  
        this.pickRandomBackgroundOnDOMLoad()
  
        this.checkScreenSize();
  
        // Add a window resize event listener to continuously monitor screen size changes
        window.addEventListener("resize", this.checkScreenSize);
  
  
        // mobile touch events
        // this.$el.addEventListener('touchstart', () => {
        //   console.log("started")
        // });
        // this.$el.addEventListener('touchmove', e => {
        //   console.log(e)
        // });
        
      },
    
      // do things for when the DOM is already loaded
      updated: function() {
        
        
      },
    }
    
    
    
    
    
    
    
    
    </script>
    
    <style>
    :root{
        --game-banner-height: 2.5em;
        --game-footer-height: 4em;
    }
  
    body {
      background-color: rgb(42, 42, 42);
      background-size: cover;
      background-repeat: no-repeat;
      background-position-x: center;
      background-position-y: center;
      background-attachment: fixed;
      overscroll-behavior: contain; /**Disable Refreshing on screen pull-down for mobile */
    }
  
  
  
  
  
    #home {
      font-family: Avenir, Helvetica, Arial, sans-serif;
      -webkit-font-smoothing: antialiased;
      -moz-osx-font-smoothing: grayscale;
      text-align: center;
      color: grey;
  
      position: absolute;
      bottom: 0;
      top: 0;
      left: 0;
      right: 0;
  
    }
  
    .game-config-modal {
      position: fixed;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
  
      z-index: 99; /**higher than game-config-overlay */
  
      width: 100%;
      max-width: 25em;
      height: 100%;
      max-height: 30em;
      padding: 1em;
      background-color: #FFF;
      border-radius: .5em;
      overflow: auto;
  
    }
  
    .game-config-modal-inputs-container {
      display: flex;
      flex-direction: column;
      margin: 5px;
      max-height: 20em;
      overflow-y: auto;
    }
  
    .input-game-config {
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      margin: .5em;
    }
  
    .game-config-modal-button {
      appearance: none;
      border: 2px solid #294129;
      outline: none;
      background: none;
      background-image: linear-gradient(to right, #81ce71, rgb(58, 176, 154));
      border-radius: .5rem;
  
      padding: 1rem;
      cursor: pointer;
      font-size: 1em;
      font-weight:400;
      color: #FFF;
    }
  
    .config-input{
      height: 1em;
      max-width: 50%;
      background-color: rgba(114, 130, 153, 0.74);
      border-radius: .2em;
      font-size: 1em;
      font-weight:400;
      color: #FFF;
    }
  
    .game-config-overlay {
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      z-index: 98;
      background-color: rgba(0,0,0,0.3);
    }
  
    .config-slide-enter-from, .config-slide-leave-to {
      transform: translateY(-100vh) translateX(-50%);
    }
  
    .config-slide-enter-active, .config-slide-leave-active {
      transition: transform 1.0s ease;
    }
  
    .config-fade-enter-active, .config-fade-leave-active {
      transition: opacity 0.5s ease;
    }
  
    .config-fade-enter-from, .config-fade-leave-to {
      opacity: 0;
    }
  
  
  
    .game-banner{
      max-height: var(--game-banner-height);
      position: absolute;
      width: 100%;
      height: 100%;
      color: white;
      background: linear-gradient(to right, #711282, rgb(12, 66, 132));
      /* z-index: 1; */
      display: flex;
      align-items: center;
      justify-content: center;
    }
  
    .game-banner .banner-current-turn {
      margin-right: 5em;
    }
  
    .game-banner .banner-turn-timer {
      margin-left: .5em;
    }
  
    .opulence-banner{
      max-width: 100vw;
      width: min(75vw, 20em);
    }
  
    /* play section */
    .play-container {
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      margin-top: 8vh;
    }
    

    
    .play-button {
      width: 200px;
      height: 46px;
      margin: 10px;
    }
    
    .create-game-button {
      width: 50%;
      height: 3em;
      margin: 1em;
      font-size: 1em;
      background-color: #1eab4800; 
      border: 2px solid #1eab48;
      color: white;
      transition: background-color .3s ease-in-out;
    }
    .create-game-button:hover {
      background-color: #1eab48
    }
    
    /* in-game containers */
    .master-container {
      display: flex;
      flex-direction: row;
      gap: 0.5em;
      width: 100%;
      height: 100%;
      box-sizing: border-box;
      padding-top: var(--game-banner-height);
    }

    .games {
      margin: 4px;
    }
    

    #mobile-hamburger {
      visibility: hidden;
      position: absolute;
      z-index: 1;
    }
  
    
    ::-webkit-scrollbar {
      width: .5em;
      height: .5em;
    }
    
    ::-webkit-scrollbar-track { /* background of scrollbar */
      background: rgba(28, 28, 28, 0.317);
      
    }
    
    ::-webkit-scrollbar-thumb { /* scrollbar scroller */
      background: rgb(124, 124, 124);
      
     
    }
    
    @supports (scrollbar-color: red blue) {
      * {
        scrollbar-color: rgba(66, 66, 66, 0);
        scrollbar-width: thin;
      }
    }
  
  
    /* MOBILE */
    @media screen and (max-width: 768px) {
      #mobile-hamburger{
        visibility: visible;
        position: absolute;
        top:10px;
        left:10px;
        color:rgb(255, 255, 255);
        z-index: 99;
      }
  
      /* CSS for the animation transition */
      .settings-enter-active,
      .settings-leave-active {
        transition: transform 0.4s ease-in-out;
      }
  
      .settings-enter-from, .settings-leave-to {
        transform: translateX(-100%); /* Start offscreen at the bottom */
      }
  
      .settings {
        position: absolute;
        background-color: #222222;
        width: 18em;
        height: 100vh;
        z-index: 999;
      }
      
      .settings-close-btn {
        position: absolute;
        color: white;
        width: 1.5em;
        height: 1.5em;
        top: 0;
        right: 0;
        padding: 25px;
        padding-top: 15px;
      }
  
  

  


      
 
      .master-container {
        display: flex;
        flex-direction: column;
        width: 100%;
        height: 100%;
        box-sizing: border-box;
        padding-top: var(--game-banner-height);
        padding-bottom: var(--game-footer-height);
      }

  
      .game-config-modal {
        max-width: 35em;
        max-height: 35em;
  
      }
  
  
  
  
    }
  
    /* DESKTOP */
    @media screen and (min-width: 1024px) {
      
    }
  
  
    
    </style>
    