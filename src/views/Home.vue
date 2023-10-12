<template>
    <div id="home">
      <PageLoader></PageLoader>
  
  
      <transition name="settings" v-show="GameState.state.showSettings" appear>
          <div class="settings">
            <fa v-if="GameState.state.showSettings" icon="fa-solid fa-close" size="lg" class="settings-close-btn" v-on:click="GameState.state.showSettings = false" />
          </div>
      </Transition>
      <span v-if="!GameState.state.showSettings" id="mobile-hamburger" class="material-icons" v-on:click="GameState.state.showSettings = true">menu</span>
  
  
  
      <div v-if="!GameState.state.ingame && !tutorial" class="opulence-banner-container">
        <img src="@/assets/OPULENCE.png" class="opulence-banner" draggable="false"/>
      </div>
      
      <!-- <Authenticate v-if="!AuthState.state.isAuthenticated && !AuthState.state.skipAuthentication"></Authenticate> -->
  
   
      <button v-if="AuthState.state.isAuthenticated && !GameState.state.ingame" class="create-game-button" v-on:click="signOut()">Sign Out</button>
      
      
      <div v-if="!AuthState.state.isAuthenticated && AuthState.state.skipAuthentication && !playing" class="play-container" >
        <input class="input-name" v-model="userName" type="text" placeholder="[username]" maxlength="20" pattern="[A-z0-9\s]">
        
        <button  class="create-game-button"  v-on:click="play">Play</button>
        
        <!-- REDIS TEST -->
        <!-- <input class="input-name" v-model="redisData" type="text" placeholder="Enter Redis Data" maxlength="20" pattern="[A-z0-9\s]">
        <button  class="create-game-button"  v-on:click="emitRedisTest()">Test Data</button>
        <h2 class="gameid-text">Redis Test Data: {{redisOtherUserData}}</h2> -->
  
  
        <!-- <button  class="create-game-button"  v-on:click="showTutorial()">How To Play</button> -->
      </div>
  
      <div v-if="!GameState.state.ingame && !GameState.state.playing && tutorial" class="tutorial-container" >
      
        <img src="@/assets/tutorial_bg.png" style="max-width: 90%; position: fixed; top:50%; left:50%;max-height: 100%;transform:translate(-50%, -50%)" class="tutorial-bg" draggable="false" v-on:click="tutorial = false"/>
      </div>
    
      
      <div class="games-parent-container" >
        <GamesMenu :games="GameState.state.gamesList" :next-token="GameState.state.nextToken" @joinRoom="joinRoom" @showGameModal="GameState.state.showGameConfigModal = true"></GamesMenu>
      </div>
      
      
 
  
    
    
  
  
    
    
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
          
          shield_colors: [{"FIRE": "#dd221e"}, {"WATER":"#3f7ab6"}, {"DARK": "#200f34"}, {"WIND": "#b7b7b7"}, {"ARCANE": "#7332b7"}, {"EARTH": "#865b38"}, {"SOLAR": "#c9721f"}, {"NATURE":"#5ec234"}],
    
          // gamesList: {"1": {"gameID": "1", "started": "False", "users": ['2304820348', '202308402834', '20384023840328', '2081023823048208', '20384023804']}, "2": {"gameID": "2", "started": "True", "users": ['2304820348', '202308402834', '20384023840328', '2081023823048208', '20384023804']},
          //           "5": {"gameID": "5", "started": "False", "users": ['2304820348', '202308402834', '20384023840328', '2081023823048208', '20384023804']}, "6": {"gameID": "6", "started": "True", "users": ['2304820348', '202308402834', '20384023840328', '2081023823048208', '20384023804']},
          //           "8": {"gameID": "8", "started": "False", "users": ['2304820348', '202308402834', '20384023840328', '2081023823048208', '20384023804']}, "9": {"gameID": "2", "started": "True", "users": ['2304820348', '202308402834', '20384023840328', '2081023823048208', '20384023804']},
          //           "10": {"gameID": "10", "started": "False", "users": ['2304820348', '202308402834', '20384023840328', '2081023823048208', '20384023804']}, "11": {"gameID": "11", "started": "True", "users": ['2304820348', '202308402834', '20384023840328', '2081023823048208', '20384023804']}
          // },
          gamesList: [],
          nextToken: null,
    
          // cards: {"1":{"runeVal":5,"spellVal":3,"runeType":"fire","spellType":1,"cost":{"wind":2,"fire":5,"earth":10,"water":2,"nature":3,"solar":8}},"2":{"runeVal":7,"spellVal":6,"runeType":"solar","spellType":2,"cost":{"wind":2,"solar":7,"water":3}},"3":{"runeVal":9,"spellVal":10,"runeType":"water","spellType":1,"cost":{"wind":2,"nature":10}},"4":{"runeVal":8,"spellVal":8,"runeType":"arcane","spellType":2,"cost":{"arcane":8,"solar":5,"water":3}},"5":{"runeVal":10,"spellVal":4,"runeType":"nature","spellType":1,"cost":{"earth":10,"water":3,"solar":5,"dark":6}},"6":{"runeVal":3,"spellVal":1,"runeType":"wind","spellType":1,"cost":{"dark":8,"water":11}},"7":{"runeVal":6,"spellVal":9,"runeType":"wind","spellType":1,"cost":{"wind":2}},"8":{"runeVal":4,"spellVal":5,"runeType":"wind","spellType":1,"cost":{"dark":10,"solar":5,"fire":11,"wind":2}}},
          // dragons: {"Deep-sea Dragon": {"cost": {"water": 20,"dark": 20},"icon": "Deep-sea_Dragon.png","shield": 8,"damage": 2}, "Nova Dragon": {"cost": {"fire": 20,"solar": 20},"icon": "Nova_Dragon.png","shield": 8,"damage": 2}, "Swamp Dragon": {"cost": {"water": 20,"nature": 20},"icon": "Swamp_Dragon.png","shield": 8,"damage": 2},"Cloud Dragon": {"cost": {"water": 20,"wind": 20},"icon": "Cloud_Dragon.png","shield": 8,"damage": 2},},
          // users: {"1822372397923":{"health":12,"shield":5,"shieldType":"fire","runes":{"fire":1,"water":2,"earth":5,"arcane":3,"nature":3,"solar":6,"dark":2,"wind":2},"timer":80},"391234972397":{"health":10,"shield":5,"shieldType":"water","runes":{"fire":1,"water":2,"earth":5,"arcane":3,"nature":3,"solar":6,"dark":2,"wind":2},"timer":80}, "59123492397":{"health":10,"shield":5,"shieldType":"water","runes":{"fire":1,"water":2,"earth":5,"arcane":3,"nature":3,"solar":6,"dark":2,"wind":2},"timer":80}, "15123492397":{"health":10,"shield":5,"shieldType":"water","runes":{"fire":1,"water":2,"earth":5,"arcane":3,"nature":3,"solar":6,"dark":2,"wind":2},"timer":80}, "11113492397":{"health":10,"shield":5,"shieldType":"water","runes":{"fire":1,"water":2,"earth":5,"arcane":3,"nature":3,"solar":6,"dark":2,"wind":2},"timer":80}, "2222492397":{"health":10,"shield":5,"shieldType":"water","runes":{"fire":1,"water":2,"earth":5,"arcane":3,"nature":3,"solar":6,"dark":2,"wind":2},"timer":80}},
          logs: [":arcane:", ":fire: runes", 'log2', 'log3', 'log4', 'log5 took a :fire: rune worth x6 affinity and played a card to deal x5 :solar: to everyone', 'log6', 'log7', 'log8', 'log9', 'log10', 'log11', 'log12', 'log13', 'log14',
          ":fire: runes"],
          
          
          isTurn: true,
          
          connectedMsg: 'Disconnected',
          redisData: "",
          redisOtherUserData: "",
  
          turnSecond: '0',
          turnMinute: '0',
          turnHour: '0',
          turnDay: '0',
          countDate: null,
          timerId: null,
          
  
        
          current_game_card_shop: [{'card': {'rune': 'FIRE', 'type': 'SHIELD', 'affinity': 8, 'power': 4}, 'cost': {'NATURE': 2, 'DARK': 8, 'ARCANE': 7, 'SOLAR': 5}}, {'card': {'rune': 'ARCANE', 'type': 'SHIELD', 'affinity': 8, 'power': 4}, 'cost': {'NATURE': 2, 'DARK': 8, 'ARCANE': 7, 'SOLAR': 5}}, {'card': {'rune': 'ARCANE', 'type': 'SHIELD', 'affinity': 8, 'power': 4}, 'cost': {'NATURE': 2, 'DARK': 8, 'ARCANE': 7, 'SOLAR': 5}}, {'card': {'rune': 'ARCANE', 'type': 'SHIELD', 'affinity': 8, 'power': 4}, 'cost': {'NATURE': 2, 'DARK': 8, 'ARCANE': 7, 'SOLAR': 5}}, {'card': {'rune': 'EARTH', 'type': 'SHIELD', 'affinity': 8, 'power': 4}, 'cost': {'NATURE': 2, 'DARK': 8, 'ARCANE': 7, 'SOLAR': 5}}],
          current_game_dragon_shop: [{'dragon': {'type': 'THORN', 'runes': ['NATURE', 'ARCANE']}, 'cost': {'NATURE': 20, 'ARCANE': 20}}],
        //   current_game_users: [
        //     {
        //       "sid": "WWxbPZRWHvr_L7lNAAAF",
        //       "hp": 10,
        //       "shield": {
        //         "rune": null,
        //         "power": 0
        //       },
        //       "runes": {
        //         "ARCANE": 0,
        //         "SOLAR": 2,
        //         "DARK": 0,
        //         "NATURE": 2,
        //         "EARTH": 0,
        //         "WIND": 0,
        //         "WATER": 0,
        //         "FIRE": 0
        //       },
        //       "cards": [
        //         {
        //           "card": {
        //             "rune": "EARTH",
        //             "type": "ATTACK",
        //             "affinity": 7,
        //             "power": 7
        //           }
        //         }
        //       ],
        //       "affinities": {
        //         "ARCANE": 0,
        //         "SOLAR": 0,
        //         "DARK": 0,
        //         "NATURE": 0,
        //         "EARTH": 0,
        //         "WIND": 0,
        //         "WATER": 0,
        //         "FIRE": 0
        //       },
        //       "dragons": [
        //         {
        //           "dragon": {
        //             "type": "VOID",
        //             "runes": ["ARCANE", "DARK"]
        //           }
        //         },
        //         {
        //           "dragon": {
        //             "type": "CLOUD",
        //             "runes": ["WIND", "WATER"]
        //           }
        //         }
        //       ],
        //       "isDead": false,
        //       "vines": 0,
        //       "burn": 0,
        //       "display_name": "client-player"
        //     },
        //     {
        //       "sid": "other_sid1",
        //       "hp": 5,
        //       "shield": {
        //         "rune": null,
        //         "power": 0
        //       },
        //       "runes": {
        //         "ARCANE": 0,
        //         "SOLAR": 0,
        //         "DARK": 0,
        //         "NATURE": 2,
        //         "EARTH": 0,
        //         "WIND": 0,
        //         "WATER": 0,
        //         "FIRE": 0
        //       },
        //       "cards": [
        //         {
        //           "card": {
        //             "rune": "EARTH",
        //             "type": "ATTACK",
        //             "affinity": 7,
        //             "power": 7
        //           }
        //         }
        //       ],
        //       "affinities": {
        //         "ARCANE": 7,
        //         "SOLAR": 0,
        //         "DARK": 0,
        //         "NATURE": 0,
        //         "EARTH": 0,
        //         "WIND": 0,
        //         "WATER": 0,
        //         "FIRE": 0
        //       },
        //       "dragons": [],
        //       "isDead": true,
        //       "vines": 10,
        //       "burn": 1,
        //       "display_name": "other-player1"
        //     },
        //     {
        //       "sid": "other_sid2",
        //       "hp": 10,
        //       "shield": {
        //         "rune": null,
        //         "power": 0
        //       },
        //       "runes": {
        //         "ARCANE": 0,
        //         "SOLAR": 0,
        //         "DARK": 0,
        //         "NATURE": 2,
        //         "EARTH": 0,
        //         "WIND": 0,
        //         "WATER": 0,
        //         "FIRE": 0
        //       },
        //       "cards": [
        //         {
        //           "card": {
        //             "rune": "EARTH",
        //             "type": "ATTACK",
        //             "affinity": 7,
        //             "power": 7
        //           }
        //         },
        //         {
        //           "card": {
        //             "rune": "ARCANE",
        //             "type": "ATTACK",
        //             "affinity": 7,
        //             "power": 7
        //           }
        //         },
        //         {
        //           "card": {
        //             "rune": "ARCANE",
        //             "type": "ATTACK",
        //             "affinity": 7,
        //             "power": 7
        //           }
        //         }
        //       ],
        //       "affinities": {
        //         "ARCANE": 7,
        //         "SOLAR": 0,
        //         "DARK": 0,
        //         "NATURE": 0,
        //         "EARTH": 0,
        //         "WIND": 0,
        //         "WATER": 0,
        //         "FIRE": 0
        //       },
        //       "dragons": [],
        //       "isDead": false,
        //       "vines": 0,
        //       "display_name": "other-player2"
        //     },
        //     {
        //       "sid": "other_sid3",
        //       "hp": 10,
        //       "shield": {
        //         "rune": null,
        //         "power": 0
        //       },
        //       "runes": {
        //         "ARCANE": 0,
        //         "SOLAR": 0,
        //         "DARK": 0,
        //         "NATURE": 2,
        //         "EARTH": 0,
        //         "WIND": 0,
        //         "WATER": 0,
        //         "FIRE": 0
        //       },
        //       "cards": [
        //         {
        //           "card": {
        //             "rune": "EARTH",
        //             "type": "ATTACK",
        //             "affinity": 7,
        //             "power": 7
        //           }
        //         },
        //         {
        //           "card": {
        //             "rune": "ARCANE",
        //             "type": "ATTACK",
        //             "affinity": 7,
        //             "power": 7
        //           }
        //         },
        //         {
        //           "card": {
        //             "rune": "ARCANE",
        //             "type": "ATTACK",
        //             "affinity": 7,
        //             "power": 7
        //           }
        //         }
        //       ],
        //       "affinities": {
        //         "ARCANE": 7,
        //         "SOLAR": 0,
        //         "DARK": 0,
        //         "NATURE": 0,
        //         "EARTH": 0,
        //         "WIND": 0,
        //         "WATER": 0,
        //         "FIRE": 0
        //       },
        //       "dragons": [],
        //       "isDead": false,
        //       "vines": 0,
        //       "display_name": "other-player3"
        //     },
        //     {
        //       "sid": "other_sid4",
        //       "hp": 10,
        //       "shield": {
        //         "rune": null,
        //         "power": 0
        //       },
        //       "runes": {
        //         "ARCANE": 0,
        //         "SOLAR": 0,
        //         "DARK": 0,
        //         "NATURE": 2,
        //         "EARTH": 0,
        //         "WIND": 0,
        //         "WATER": 0,
        //         "FIRE": 0
        //       },
        //       "cards": [
        //         {
        //           "card": {
        //             "rune": "EARTH",
        //             "type": "ATTACK",
        //             "affinity": 7,
        //             "power": 7
        //           }
        //         },
        //         {
        //           "card": {
        //             "rune": "ARCANE",
        //             "type": "ATTACK",
        //             "affinity": 7,
        //             "power": 7
        //           }
        //         },
        //         {
        //           "card": {
        //             "rune": "ARCANE",
        //             "type": "ATTACK",
        //             "affinity": 7,
        //             "power": 7
        //           }
        //         }
        //       ],
        //       "affinities": {
        //         "ARCANE": 7,
        //         "SOLAR": 0,
        //         "DARK": 0,
        //         "NATURE": 0,
        //         "EARTH": 0,
        //         "WIND": 0,
        //         "WATER": 0,
        //         "FIRE": 0
        //       },
        //       "dragons": [],
        //       "isDead": false,
        //       "vines": 0,
        //       "display_name": "other-player4"
        //     }
        //   ],
          current_room_id: '0',
          ingame: false,
          tutorial: false,
    
          playing: false,
  
          userName: '',
          attacking: false,
  
  
          skipLogin: false,
          crafting: true,
          buyingDragonCards: false,
          buyingShopCards: false,
          showHand: false,
          showHandModal: false,
          showHandModalIndex: 0,
          
    
          currentTurnSid: 'WWxbPZRWHvr_L7lNAAAF', // the sid of the player whose turn it is
          sid: 'WWxbPZRWHvr_L7lNAAAF',
  
  
          showGameConfigModal: false,
          configShopSize: 5,
          configTotalDragons: 2,
          configRunesPerTurn: 5,
          configPlayerStartHealth: 10,
          configMaxPlayers: 8,
          configTurnTimer: 30,
          
          showChat: false,
          showSettings: false,
    
        }
      },
      methods: {

        joinRoom: function(gameid) {
            this.$router.push({ name: 'game', params: { gameid: gameid } });

        },
  
        checkScreenSize() {
            
            // Update isMobile based on the current screen size
            if (window.innerWidth <= 768) {
              this.utils.setMobile(true)
            } else {
              this.utils.setMobile(false)
            }
            console.log(`Is Mobile?: ${this.utils.state.isMobile}`)
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
              });
            }
        },
    
        play() {
          this.playing = true
          this.socket.emit('play-button', {'username': String(this.userName)})
          console.log(this.userName)
          const lastKey = this.nextToken
          this.socket.emit('query-games', {lastKey})
        },
    
        createGame: function() {
          this.socket.emit('create-game', 
          {maxplayers: this.configMaxPlayers,
          cardsinshop: this.configShopSize,
          runesperturn: this.configRunesPerTurn,
          totaldragons: this.configTotalDragons,
          startinghealth: this.configPlayerStartHealth,
          turntimer: this.configTurnTimer})
          
          console.log('created a game')
          console.log('player health: ' + this.configPlayerStartHealth)
          this.ingame = true;
          
        },
    
        showTutorial: function() {
          console.log('showing tutorial')
          this.tutorial = true;
      
        },
    
      },
    
  
      // before the DOM is mounted
      beforeMount: function() {
      },
  
      
      created: function() {
  
        // connect socket handling
        this.socket.on('user-sid', (res) => {
          this.GameState.state.sid = res
          console.log('your sid equals ' + this.GameState.state.sid)
        });
    
        this.socket.on('current-turn-sid', (res) => {
          this.GameState.state.currentTurnSid = res
    
          // if the sid that came back from the server matches
          if (this.GameState.state.sid == this.GameState.state.currentTurnSid) {
            this.GameState.state.isTurn = true // make buttons visible
            var audio = new Audio(require('@/assets/mp3s/notification.mp3'))
            audio.play()
          } else {
            this.GameState.state.isTurn = false
          }
          console.log('it is ' + this.GameState.state.currentTurnSid + ' turn')
        });
    
        // receive list of active games
        this.socket.on('list-games', (res) => {
          console.log('Active Games: ' + JSON.stringify(this.GameState.state.gamesList))
          for (let i = 0; i < res.games.length; i++) {
            this.GameState.state.gamesList.push(res.games[i])
          }
  
          // this.gamesList = res.games
          this.GameState.state.nextToken = res.last_key
          console.log('Active Games: ' + JSON.stringify(this.GameState.state.gamesList))
        });
    
        this.socket.on('join-room', () => {
          this.GameState.state.ingame = true
          console.log('In game?: ' + this.GameState.state.ingame)
        });
    

        this.socket.on('game-logs', (res) => {
          res.map((log) => {
            this.GameState.state.logs.push(log)
          })
          // old implementation
          // this.GameState.state.logs = res
        });
  

        // grab dict of user and card shop game data from server
        this.socket.on('game-data', (res) => {
          console.log("got game data:", res)
          this.GameState.state.current_game_users = res['user_data']
          this.GameState.state.current_game_card_shop = res['card_shop']['cards']
          console.log("grabbing game data")
        });
    
    
        // // dragon shop data
        this.socket.on('dragon-shop-data', (res) => {
          this.GameState.state.current_game_dragon_shop = res['dragons']
        });
        
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
  
  
    .opulence-banner-container {
      position: absolute;
      display: flex;
      justify-content: center;
      align-items: center;
      left: 0;
      top: 0;
      right: 0;
      height: 8vh;
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
    
    .input-name {
      height: 2em;
      width: 100%;
      max-width: fit-content;
      background-color: rgba(205, 226, 255, 0.74);
      border-radius: .5em;
      color: rgba(255, 255, 255, 0.8);
      font-size: 2em;
      text-align: center;
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
    
    .leave-room-button {
      background-color: #7d4646; 
      border: 2px solid #412929;
      border-radius: 6px;
      color: white;
      padding: .5rem .5rem;
      text-align: center;
      text-decoration: none;
      
      font-size: clamp(.5em, 1vw, 2em);
    }
    .leave-room-button:hover {
      background-color: #946767
    }
  
    .gameid-text {
      font-size: min(1.5vw, 1.17em);
      color: #e0e0e0
    }
  
    .start-game-button {
      width: 10em;
      background-color: #467d46;
      border: 2px solid #294129;
      border-radius: 6px;
      color: white;
      
      text-align: center;
      text-decoration: none;
      
      font-size: clamp(.75em, 1vw, 2em);
    }
    .start-game-button:hover {
      background-color: #28a24d
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
    
    
    /* player stats */
    .player-statistics-container {
      width: 100%;
      height: 85vh;
      display: flex;
      flex-direction: column;
      align-items: center;
  
    }
  
    .status-effect-text{
      margin: .5rem;
      font-size: clamp(1em, 1vw 1.2em);
      font-family: monospace;
      font-weight: bold;
    }
    
    .player-hand-modal {
      position: fixed;
      /* background: linear-gradient(45deg, #cccccc, #acacac); */
      top: 50%;
      left: 75vw;
      transform: translate(-50%, -50%);
  
      z-index: 99; /**higher than game-config-overlay */
  
      width: 100%;
      max-width: min(30vw, 20em);
      max-height: 50vh;
      min-height: 20vh;
      padding: 1em;
      background-color: #FFF;
      border-radius: .5em;
      overflow-y: auto;
      overflow-x: hidden;
  
    }
  
    .other-player-hand-overlay {
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      z-index: 98;
      background-color: rgba(0,0,0,0.3);
    }
  
    .other-player-hand-slide-enter-from, .other-player-hand-slide-leave-to {
      transform: translateY(-50%) translateX(100vw);
    }
  
    .other-player-hand-slide-enter-active, .other-player-hand-slide-leave-active {
      transition: transform 1.0s ease;
    }
  
    .other-player-hand-fade-enter-active, .other-player-hand-fade-leave-active {
      transition: opacity 0.5s ease;
    }
  
    .other-player-hand-fade-enter-from, .other-player-hand-fade-leave-to {
      opacity: 0;
    }
    
    .hp-shield-bars {
      width: 100%;
      height: 100%;
    }
    
    .hp-image {
      margin-right: 5px;
    }
    
    .hp-bar{
      display: flex;
      justify-content: center;
      align-items: center;
    }
    
    .shield-image {
      margin-right: 5px;
      display: flex;
    }
    
    .shield-bar{
      display: flex;
      justify-content: center;
      align-items: center;
    }
    
    .player-runes{
      display: flex;
      justify-content: center;
      align-items: center;
    }
  
    .player-name{
      font-size: min(2vh, 1.17em)
    }
    
    .other-player-statistics {
      overflow: auto;
      height: 80%;
      min-height: 200px;
      background-color: rgba(44, 67, 77, 0.362);
      border-style: solid;
      box-sizing: border-box;
  
      width: 100%;
    }
  
    .other-player-hand-button {
      cursor: pointer;
      width: 100%;
    }
  
    .other-player-hand-button:active {
      cursor:pointer;
      transform: translateY(1px);
      opacity: 70%;
    }
    
    /* .other-player {
      width: 100%;
      display: flex;
      flex-direction: column;
      align-items: flex-start;
     
    } */
    
    /* client player stats */
    .client-player-statistics {
      width: 100%;
      position: relative;
      justify-content: center;
      align-items: center;
      /* height: 20%; */
    }
    .client-player {
      margin: 0;
    }
    
    .dragons-owned-container{
      display: flex;
      justify-content: center;
      align-items: center;
  
    }
    .dragons-owned-icons{
      margin: 5px;
    }
  
  
    
    
    
    .total-runes-text {
      margin-left: .15em;
      font-size: clamp(1vh, 1vw, 2em);
    }
    
    
    
    
    
    
    .attack-button {
      cursor:pointer;
    }
    .attack-button:active {
      cursor:pointer;
      transform: translateY(1px);
      opacity: 70%;
    }
    
    .rune-button{
      display: flex;
      justify-content: center;
      align-items: center;
      margin: 6px;
    }
    
    .rune-btn-img {
      cursor:pointer;
    }
    
    /* animate the rune image button during press */
    .rune-btn-img:active {
      transform: translateY(1px);
      opacity: 70%;
    }
    
    .rune-btn-img-notturn {
      opacity: 50%;
    }
  
    
  
    
    
    .shop-parent-container {
      width: min(20rem, 60vw);
      height: 100%;
    }
    
    .shop-title {
      font-size: clamp(1em, 1vw, 2em);
      word-break: break-all; /* wrap text to fit within the confines of parent*/
      color: white;
    }
  
    .shop-container {
      overflow: auto;
      height: 85vh;
      width: 100%; /*needs 'width' so it can be centered within the parent container */
      padding: .2em;
      box-sizing: border-box;
    }
    
    .shop-cards {
      margin-top: 30px;
    }
    
    .shop-button-container{
      display: flex;
      margin-top: 1em;
      justify-content: center;
      align-items: center;
      width: 100%;
    }
    
    .shop-button {
      margin: .1rem;
      background-color: #64572d;
      border: 2px solid #4a4226;
      border-radius: 6px;
      color: white;
      padding: .4rem .9rem;
      text-align: center;
      text-decoration: none;
      display: inline-block;
      font-size: min(2vw, 14px);
    }
    
    /* before joining a game containers */
    .games-container {
      /* display: flex;
      flex-direction: column; */
      justify-content: center;
      align-items: center;
    }
    
    .games {
      margin: 4px;
    }
    
    
    
    
    /* mouse over tooltip for runes */
    .tooltip {
      position: relative;
    }
  
    .tooltip:before {
      content: attr(data-hover);
      visibility: hidden;
      opacity: 0;
      width: 256px;
      height: max-content;
    
      border-radius: .3rem;
      border-color: aqua;
      border-style: solid;
      border-width: 1px;
      background-color: rgb(25, 25, 25);
      color: #fff;
      text-align: center;
      padding: 5px 0;
      transition: opacity .55s ease-in-out;
      
      position: absolute;
      
      top: -.25rem;
      left: 50%;
      transform: translateX(-50%) translateY(-100%);
      
      padding: .5rem;
    }
    
    .tooltip:hover:before {
      opacity: 1;
      visibility: visible;
      
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
  
    .button-icons {
      width: 1em;
      height: 1em;
    }
  
  
    .divider {
      width: 100%;
      height: 1px; /* Set a height for the divider line */
      background-color: #ccc; /* Customize the divider line color */
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
  
  
      .mobile-chat-logs {
        position: absolute
  
      }
  
      .button-icons {
        width: 2em;
        height: 2em;
      }
      .start-game-button {
        width: 15em;
        height: 4em;
        
        /* background-color: #467d46;
        border: 2px solid #294129;
        border-radius: 6px;
        color: white;
        
        text-align: center;
        text-decoration: none; */
        
        font-size: clamp(.75em, 2vw, 2em);
      }
      
  
  
      .shop-button-container {
        justify-content: center;
        max-height: var(--game-footer-height);
        position: absolute;
        width: 100%;
        height: 100%;
        color: white;
        background: linear-gradient(to right, #711282, rgb(12, 66, 132));
        z-index: 997;
        bottom: 0;
  
      }
  
      .shop-button {
        margin: 1.5em;
        background-color: #64572d00;
        border: 1px solid #ffffff;
        border-radius: 6px;
        color: white;
      }
  
      .tooltip:before{
        content: none;
      }
  
      .player-runes {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        justify-content: center;
        align-items: center;
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
  
      /* client player stats */
      .client-player-statistics {
        width: 100%;
        position: relative;
        justify-content: center;
        align-items: center;
        height: 100%;
        overflow: auto;
      }
  
      .player-statistics-container{
        width: 100%;
        display: flex;
        flex-direction: column;
        align-items: center;
        height: calc(100% - 50px);
        max-height: 40vh;
      }
  
      .other-player {
        width: 100%;
        display: flex;
        flex-direction: column;
        align-items: flex-start;
        margin-bottom: 2em;
    }
  
    .other-player-statistics {
      overflow: auto;
      height: 100%;
      min-height: 200px;
      background-color: rgba(44, 67, 77, 0.362);
      border-style: solid;
      box-sizing: border-box;
  
      width: 100%;
    }
  
  
      /* CSS for the animation transition */
      .mobile-card-shops-enter-active,
      .mobile-card-shops-leave-active {
        transition: transform 0.3s ease-in-out;
      }
  
      .mobile-card-shops-enter-from, .mobile-card-shops-leave-to /* .mobile-card-shop-leave-active in <2.1.8 */ {
        transform: translateY(100%); /* Start offscreen at the bottom */
      }
  
      .mobile-card-shop {
        position: fixed;
        overflow: auto;
        height: 100%;
        width: 100%;
        background-color: #222222; /* Lavender */
  
        padding-bottom: 50px;
        z-index: 2;
      }
  
      .shop-cards {
        margin-top: 30px;
      }
  
      .mobile-shop-exit-btn {
        position: absolute;
        color: white;
        margin: 1em;
  
      }
  
      .shop-container {
        height: 100vh;
        box-sizing: border-box;
        padding-bottom: 150px;
      }
  
      .total-runes-text {
        margin-left: .15em;
        font-size: clamp(1vh, 4vw, 2.5em);
      }
  
  
      .game-config-modal {
        max-width: 35em;
        max-height: 35em;
  
      }
  
      .close-icon {
        width: 1.5em;
        height: 1.5em;
        cursor: pointer;
      }
  
  
  
  
    }
  
    /* DESKTOP */
    @media screen and (min-width: 1024px) {
      
    }
  
  
    
    </style>
    