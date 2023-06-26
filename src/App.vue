<template>
  <div id="app">
    <PageLoader></PageLoader>

    <span id="mobile-hamburger" class="material-icons">menu</span>

    <div v-if="!ingame && !tutorial" class="opulence-banner-container">
      <img src="./assets/OPULENCE.png" class="opulence-banner" draggable="false"/>
    </div>
    
    <Authenticate v-if="!AuthState.state.isAuthenticated && !AuthState.state.skipAuthentication"></Authenticate>

 
    <button v-if="AuthState.state.isAuthenticated && !ingame" class="create-game-button" v-on:click="signOut()">Sign Out</button>
    
    
    <div v-if="!AuthState.state.isAuthenticated && AuthState.state.skipAuthentication && !playing" class="play-container" >
      <input class="input-name" v-model="userName" type="text" placeholder="[username]" maxlength="20" pattern="[A-z0-9\s]">
      
      <button  class="create-game-button"  v-on:click="play">Play</button>
      
      <!-- REDIS TEST -->
      <!-- <input class="input-name" v-model="redisData" type="text" placeholder="Enter Redis Data" maxlength="20" pattern="[A-z0-9\s]">
      <button  class="create-game-button"  v-on:click="emitRedisTest()">Test Data</button>
      <h2 class="gameid-text">Redis Test Data: {{redisOtherUserData}}</h2> -->


      <!-- <button  class="create-game-button"  v-on:click="showTutorial()">How To Play</button> -->
    </div>

    <div v-if="!ingame && !playing && tutorial" class="tutorial-container" >
    
      <img src="./assets/tutorial_bg.png" style="max-width: 90%; position: fixed; top:50%; left:50%;max-height: 100%;transform:translate(-50%, -50%)" class="tutorial-bg" draggable="false" v-on:click="tutorial = false"/>
    </div>
  
    
    <div v-if="(!ingame && AuthState.state.isAuthenticated || playing && !ingame)" class="games-parent-container" >
      <h2>Select a game from the list or create one</h2>
      <button class="create-game-button"  v-on:click="showGameConfigModal = true">Create Game</button>
      <GamesMenu :games="gamesList" :next-token="nextToken" @joinRoom="joinRoom"></GamesMenu>
    </div>
    
    
    <transition name="config-fade" appear>
      <div class="game-config-overlay" v-if="showGameConfigModal" @click="showGameConfigModal = false"></div>
    </transition>
    <transition name="config-slide" appear>
      <div class="game-config-modal" v-if="showGameConfigModal">
        <h1>Game Config</h1>
        <div class="game-config-modal-inputs-container">
          <div class="input-game-config">
            <span>Max Players</span>
            <input class="config-input" v-model="configMaxPlayers" type="number" placeholder="8" maxlength="2" min="2">
          </div>
          <div class="input-game-config">
            <span>Legendary Cards In Shop
              <img draggable="false" src="@/assets/sword.png" style="width:20px; height: 20px;"/>
            </span>
            <input class="config-input" v-model="configShopSize" type="number" placeholder="5" maxlength="2" min="0">
          </div>
          <div class="input-game-config">
            <span>Dragons In Shop
              <img draggable="false" src="@/assets/dragons/icons/LAVAdragon-icon.png" style="width:20px; height: 20px;"/>
            </span>
            <input class="config-input" v-model="configTotalDragons" type="number" placeholder="2" maxlength="2" min="0">
          </div>
          <div class="input-game-config">
            <span>Runes-Per-Turn
              <img draggable="false" :src="iconPath(`NATURE.png`)" style="width:20px; height: 20px;"/>
            </span>
            <input class="config-input" v-model="configRunesPerTurn" type="number" placeholder="5" maxlength="2" min="1">
          </div>
          <div class="input-game-config">
            <span>Player Starting Health
              <img draggable="false" :src="iconPath(health_icon)" style="width:20px; height: 20px;"/>
            </span>
            <input class="config-input" v-model="configPlayerStartHealth" type="number" placeholder="10" maxlength="3" min="1">
          </div>
          <div class="input-game-config">
            <span>Turn Timer (Seconds)
              <fa icon="fa-solid fa-stopwatch" size="lg" class="timer-icon" />
            </span>
            <input class="config-input" v-model="configTurnTimer" type="number" placeholder="30" maxlength="4" min="10">
          </div>
        </div>
        <button class="game-config-modal-button" v-on:click="createGame(), showGameConfigModal = false">Create Lobby</button>
      </div>
    </transition>



    <div v-if="ingame" class="game-banner">
        <template v-for="(user, index) in current_game_users" :key="index">
          <template v-if="user.sid == this.currentTurnSid">
            <span class="banner-current-turn">Current Turn: {{user.display_name}}</span>
            <fa icon="fa-solid fa-stopwatch" size="lg" class="timer-icon" />
            <span class="banner-turn-timer"> {{ this.turnHour !== '0' && this.turnHour !== '00' ? `${this.turnHour} : ${this.turnMinute} : ${this.turnSecond} ` : `${this.turnMinute} : ${this.turnSecond}` }}</span>
          </template>
        </template>
    </div>


    <div v-if="ingame" class="master-container">

      <div class="shop-parent-container">
        <div v-show="buyingShopCards" class="shop-container">
              <h2 class="shop-title">Legendary Card Shop</h2>
              <LegendaryShopCards class="shop-cards" v-for="(key, index) in current_game_card_shop" :cost="key.cost" :power="key.card.power" :affinity="key.card.affinity" :runeType="key.card.rune" :spellType="key.card.type" :currentTurnSid="this.currentTurnSid" :users="this.current_game_users" :key="index" @buyCard="buyCard(index)"></LegendaryShopCards>
        </div>
        <div v-show="buyingDragonCards" class="shop-container">
              <h2 class="shop-title">Dragon Shop</h2>
              <DragonCards class="shop-cards" v-for="(key,index) in current_game_dragon_shop" :cost="key.cost" :dragonType="key.dragon.type" :currentTurnSid="this.currentTurnSid" :users="this.current_game_users" :key="index" @buyDragon="buyDragon(index)"></DragonCards>
        </div>

        <div v-show="crafting" class="shop-container">
              <h2 class="shop-title">Craft a basic card</h2>
              <Crafting class="shop-cards" :currentTurnSid="this.currentTurnSid" :users="this.current_game_users" @craftCard="craftCard"></Crafting>
        </div>
        
  
  
        <div v-show="showHand" class="shop-container">
            <template v-for="(user,userIndex) in current_game_users" :key="userIndex">
              <template v-if="user.sid == this.currentTurnSid">
                <h2 class="shop-title">{{user.display_name}}'s Hand</h2>
                <PlayerCards class="shop-cards" v-for="(card, index) in current_game_users[userIndex].cards" :power="card.card.power" :affinity="card.card.affinity" :runeType="card.card.rune" :spellType="card.card.type" :key="index" @playCard="playCard(index, card.card.type)"></PlayerCards>
              </template>
            </template>
        </div>



        <transition name="other-player-hand-slide" v-show="showHandModal" appear>
          <div v-if="current_game_users[showHandModalIndex] != null" class="player-hand-modal"  @click="showHandModal = false" @touchend="showHandModal">
            <h2 v-if="current_game_users[showHandModalIndex].sid != this.sid" style="font-size: clamp(1em, 1vw, 2em);">{{current_game_users[showHandModalIndex].display_name}}'s Hand</h2>
            <h2 v-else style="font-size: clamp(1em, 1vw, 2em);">Your Hand</h2>
            <div class="player-hand-modal-cards">
                <ClientSidePlayerCards class="shop-cards" v-for="(card) in current_game_users[showHandModalIndex].cards" :power="card.card.power" :affinity="card.card.affinity" :runeType="card.card.rune" :spellType="card.card.type" :key="card"></ClientSidePlayerCards>
            </div>
          </div>
        </transition>
  
  
        <div class="shop-button-container">
          <button class="shop-button" :disabled="!isTurn" v-on:click="openCraftShop">craft</button>
          <button class="shop-button" :disabled="!isTurn" v-on:click="openCardShop">shop</button>
          <button class="shop-button" :disabled="!isTurn" v-on:click="openDragonShop">dragon</button>
          <button class="shop-button" :disabled="!isTurn" v-on:click="openPlayersHand">hand</button>
        </div>
      </div>
  
      <div class="player-statistics-container">
        <div class="other-player-statistics">
          <div class="other-player" v-for="(user, userIndex) in current_game_users" :key="userIndex">
            <!-- render other player health/stats together -->
            <div v-if="user.sid != this.sid">
              <div class="hp-shield-bars">
                <h3 class="player-name">Name: {{user.display_name}}</h3>
                <div class="dragons-owned-container" >
                  <div class="dragons-owned-icons" v-for="dragon in user.dragons" :key="dragon">
                    <img draggable="false" :src="iconPath(`dragons/icons/${dragon.dragon.type}dragon-icon.png`)" style="width: 100%; max-width: 2em; height: 100%; max-height: 2em;"/>
                    <div class="dragons-owned-icons-runes">
                      <img draggable="false" :src="iconPath(`${dragon.dragon.runes[0]}.png`)" style="width: 100%; max-width: 1em; height: 100%; max-height: 1em;"/>
                      <img draggable="false" :src="iconPath(`${dragon.dragon.runes[1]}.png`)" style="width: 100%; max-width: 1em; height: 100%; max-height: 1em;"/>
                    </div>
                  </div>
                </div>
                <span v-show="user.vines > 0" class="status-effect-text" style="color:#5ec234">vines: {{user.vines}}</span>
                <span v-show="user.burn > 0" class="status-effect-text" style="color:#dd221e">burn: {{user.burn}}</span>
                <div class="hp-bar">
                  <div class="hp-image">
                
                    <img v-show="attacking && !user.isDead" src="./assets/attack.png" style="width: 100%; min-width: 2em; max-width: 2em; height: 100%; max-height: 2em;" class="attack-button" v-on:click="attackPlayer(user.sid)"/>
                    
                    <img v-if="user.isDead" draggable="false" :src="iconPath(death_icon)" style="width: 100%; max-width: 2em; height: 100%; max-height: 2em;">
                    <img v-else draggable="false" :src="iconPath(health_icon)" style="width: 100%; max-width: 2em; height: 100%; max-height: 2em;"> 
                  </div>
                    <HpBar :bgcolor="'#880808'" :value="user.hp" :vines="user.vines"/>
                </div>

                <div class="shield-bar">
                  <div class="shield-image">
                    <img v-if="user.shield.rune == null" draggable="false" :src="iconPath(shield_icon)" style="width: 100%; max-width: 2em; height: 100%; max-height: 2em;"/>
                    <img v-else-if="user.shield.rune == 'FIRE'" draggable="false" :src="iconPath('fire-shield.png')" style="width: 100%; max-width: 2em; height: 100%; max-height: 2em;"/>
                    <img v-else-if="user.shield.rune == 'WATER'" draggable="false" :src="iconPath('water-shield.png')" style="width: 100%; max-width: 2em; height: 100%; max-height: 2em;"/>
                    <img v-else-if="user.shield.rune == 'DARK'" draggable="false" :src="iconPath('dark-shield.png')" style="width: 100%; max-width: 2em; height: 100%; max-height: 2em;"/>
                    <img v-else-if="user.shield.rune == 'ARCANE'" draggable="false" :src="iconPath('arcane-shield.png')" style="width: 100%; max-width: 2em; height: 100%; max-height: 2em;"/>
                    <img v-else-if="user.shield.rune == 'EARTH'" draggable="false" :src="iconPath('earth-shield.png')" style="width: 100%; max-width: 2em; height: 100%; max-height: 2em;"/>
                    <img v-else-if="user.shield.rune == 'NATURE'" draggable="false" :src="iconPath('nature-shield.png')" style="width: 100%; max-width: 2em; height: 100%; max-height: 2em;"/>
                    <img v-else-if="user.shield.rune == 'SOLAR'" draggable="false" :src="iconPath('solar-shield.png')" style="width: 100%; max-width: 2em; height: 100%; max-height: 2em;"/>
                    <img v-else-if="user.shield.rune == 'WIND'" draggable="false" :src="iconPath('wind-shield.png')" style="width: 100%; max-width: 2em; height: 100%; max-height: 2em;"/>
                  </div>
                    <ShieldBar :bgcolor="shield_color" :value="user.shield.power" :shieldType="user.shield.rune"/>
                </div>
              </div>



              
              <img class="other-player-hand-button" draggable="false" :src="iconPath('logo.png')" style="width: 100%; max-width: 1em; height: 100%; max-height: 1em;"  v-on:click="openPlayersHandModal(userIndex)"/>
              
              <div class="player-runes">
                  <div class="rune-button">
                    <img draggable="false" src="./assets/FIRE.png" style="width:100%; height: 100%; max-width: 1em; max-height: 1em;"/>
                    <h3 class="total-runes-text"> <span style="color:#dd221e">{{user.runes.FIRE}}</span> (<span style="color:#f5c441">{{user.affinities.FIRE}}</span>)</h3>
                  </div> 
                  <div class="rune-button">
                    <img draggable="false" src="./assets/WATER.png" style="width:100%; height: 100%; max-width: 1em; max-height: 1em;"/>
                    <h3 class="total-runes-text"><span style="color:#3f7ab6">{{user.runes.WATER}}</span> (<span style="color:#f5c441">{{user.affinities.WATER}}</span>)</h3>
                  </div>
                  <div class="rune-button">
                    <img draggable="false" src="./assets/EARTH.png" style="width:100%; height: 100%; max-width: 1em; max-height: 1em;"/>
                    <h3 class="total-runes-text"><span style="color:#865b38">{{user.runes.EARTH}}</span> (<span style="color:#f5c441">{{user.affinities.EARTH}}</span>)</h3>
                  </div>
                  <div class="rune-button">
                    <img draggable="false" src="./assets/ARCANE.png" style="width:100%; height: 100%; max-width: 1em; max-height: 1em;"/>
                    <h3 class="total-runes-text"><span style="color:#7332b7">{{user.runes.ARCANE}}</span> (<span style="color:#f5c441">{{user.affinities.ARCANE}}</span>)</h3>
                  </div>
                  <div class="rune-button">
                    <img draggable="false" src="./assets/NATURE.png" style="width:100%; height: 100%; max-width: 1em; max-height: 1em;"/>
                    <h3 class="total-runes-text"><span style="color:#5ec234">{{user.runes.NATURE}}</span> (<span style="color:#f5c441">{{user.affinities.NATURE}}</span>)</h3>
                  </div>
                  <div class="rune-button">
                    <img draggable="false" src="./assets/SOLAR.png" style="width:100%; height: 100%; max-width: 1em; max-height: 1em;"/>
                    <h3 class="total-runes-text"><span style="color:#c9721f">{{user.runes.SOLAR}}</span> (<span style="color:#f5c441">{{user.affinities.SOLAR}}</span>)</h3>
                  </div>
                  <div class="rune-button">
                    <img draggable="false" src="./assets/DARK.png" style="width:100%; height: 100%; max-width: 1em; max-height: 1em;"/>
                    <h3 class="total-runes-text"><span style="color:#200f34">{{user.runes.DARK}}</span> (<span style="color:#f5c441">{{user.affinities.DARK}}</span>)</h3>
                  </div>
                  <div class="rune-button">
                    <img draggable="false" src="./assets/WIND.png" style="width:100%; height: 100%; max-width: 1em; max-height: 1em;"/>
                    <h3 class="total-runes-text"><span style="color:#b7b7b7">{{user.runes.WIND}}</span> (<span style="color:#f5c441">{{user.affinities.WIND}}</span>)</h3>
                  </div>
              </div>
            </div>
            
        </div>
      </div>
  
      <!-- render client health bars in another location -->
      <div v-if="ingame" class="client-player-statistics">
        <div class="client-player" v-for="(user, index) in current_game_users" :key="index">
          <div v-if="user.sid == this.sid" class="client-player">

            <div class="hp-shield-bars">
              <h3 class="player-name">Name: {{user.display_name}}</h3>
              <div class="dragons-owned-container" >
                <div class="dragons-owned-icons" v-for="dragon in user.dragons" :key="dragon">
                  <img draggable="false" :src="iconPath(`dragons/icons/${dragon.dragon.type}dragon-icon.png`)" style="width: 100%; max-width: 2em; height: 100%; max-height: 2em;"/>
                  <div class="dragons-owned-icons-runes">
                    <img draggable="false" :src="iconPath(`${dragon.dragon.runes[0]}.png`)" style="width: 100%; max-width: 1em; height: 100%; max-height: 1em;"/>
                    <img draggable="false" :src="iconPath(`${dragon.dragon.runes[1]}.png`)" style="width: 100%; max-width: 1em; height: 100%; max-height: 1em;"/>
                  </div>
                </div>
              </div>
              <span v-show="user.vines > 0" class="status-effect-text" style="color:#5ec234">vines: {{user.vines}}</span>
              <span v-show="user.burn > 0" class="status-effect-text" style="color:#dd221e">burn: {{user.burn}}</span>
              <div class="hp-bar">
                <div class="hp-image">
                  <img v-if="user.isDead" draggable="false" :src="iconPath(death_icon)" style="width: 100%; max-width: 2em; height: 100%; max-height: 2em;">
                  <img v-else draggable="false" :src="iconPath(health_icon)" style="width: 100%; max-width: 2em; height: 100%; max-height: 2em;"> 
                </div>
                    <HpBar :bgcolor="'#880808'" :value="user.hp" :vines="user.vines"/>
              </div>
              <div class="shield-bar">
                <div class="shield-image">
                  <img v-if="user.shield.rune == null" draggable="false" :src="iconPath(shield_icon)" style="width: 100%; max-width: 2em; height: 100%; max-height: 2em;"/>
                  <img v-else-if="user.shield.rune == 'FIRE'" draggable="false" :src="iconPath('fire-shield.png')" style="width: 100%; max-width: 2em; height: 100%; max-height: 2em;"/>
                  <img v-else-if="user.shield.rune == 'WATER'" draggable="false" :src="iconPath('water-shield.png')" style="width: 100%; max-width: 2em; height: 100%; max-height: 2em;"/>
                  <img v-else-if="user.shield.rune == 'DARK'" draggable="false" :src="iconPath('dark-shield.png')" style="width: 100%; max-width: 2em; height: 100%; max-height: 2em;"/>
                  <img v-else-if="user.shield.rune == 'ARCANE'" draggable="false" :src="iconPath('arcane-shield.png')" style="width: 100%; max-width: 2em; height: 100%; max-height: 2em;"/>
                  <img v-else-if="user.shield.rune == 'EARTH'" draggable="false" :src="iconPath('earth-shield.png')" style="width: 100%; max-width: 2em; height: 100%; max-height: 2em;"/>
                  <img v-else-if="user.shield.rune == 'NATURE'" draggable="false" :src="iconPath('nature-shield.png')" style="width: 100%; max-width: 2em; height: 100%; max-height: 2em;"/>
                  <img v-else-if="user.shield.rune == 'SOLAR'" draggable="false" :src="iconPath('solar-shield.png')" style="width: 100%; max-width: 2em; height: 100%; max-height: 2em;"/>
                  <img v-else-if="user.shield.rune == 'WIND'" draggable="false" :src="iconPath('wind-shield.png')" style="width: 100%; max-width: 2em; height: 100%; max-height: 2em;"/>
                </div>
                  <ShieldBar :bgcolor="shield_color" :value="user.shield.power" :shieldType="user.shield.rune"/>
              </div>
            </div>

            <img class="other-player-hand-button" draggable="false" :src="iconPath('logo.png')" style="width: 100%; max-width: 1em; height: 100%; max-height: 1em;"  v-on:click="openPlayersHandModal(index)"/>

            <div class="player-runes">
                <div class="rune-button">
                  <span class="tooltip" data-hover="Fire damage lights the target on fire, dealing full damage on hit, then full damage again after the target's turn ends. Super effective against nature shield and poison vines."><img src="./assets/FIRE.png" draggable="false" :class="isTurn ? 'rune-btn-img' : 'rune-btn-img-notturn'" style="width: 100%; min-width: .5em; max-width: 2em; height: 100%; min-height: .5em; max-height: 2em;" v-on:click="isTurn ? takeRune('FIRE') : ''"/></span>
                  <h3 class="total-runes-text"> <span style="color:#dd221e">{{user.runes.FIRE}}</span> (<span style="color:#f5c441">{{user.affinities.FIRE}}</span>)</h3>
                </div>
                <div class="rune-button">
                  <span class="tooltip" data-hover="Water damage has no select target, but hits between 1-4 enemies for full damage. Super effective against fire shield."> <img src="./assets/WATER.png" draggable="false" :class="isTurn ? 'rune-btn-img' : 'rune-btn-img-notturn'" style="width: 100%; min-width: .5em; max-width: 2em; height: 100%; min-height: .5em; max-height: 2em;" v-on:click="isTurn ? takeRune('WATER') : ''"/></span>
                  <h3 class="total-runes-text"><span style="color:#3f7ab6">{{user.runes.WATER}}</span> (<span style="color:#f5c441">{{user.affinities.WATER}}</span>)</h3>
                </div>
                <div class="rune-button">
                  <span class="tooltip" data-hover="Earth damage has a 25% chance to crit for triple damage. Super effective against wind shield."><img src="./assets/EARTH.png" draggable="false" :class="isTurn ? 'rune-btn-img' : 'rune-btn-img-notturn'" style="width: 100%; min-width: .5em; max-width: 2em; height: 100%; min-height: .5em; max-height: 2em;" v-on:click="isTurn ? takeRune('EARTH') : ''"/></span>
                  <h3 class="total-runes-text"><span style="color:#865b38">{{user.runes.EARTH}}</span> (<span style="color:#f5c441">{{user.affinities.EARTH}}</span>)</h3>
                </div>
                <div class="rune-button">
                  <span class="tooltip" data-hover="Arcane damage ignores shields altogether, dealing full damage to healthbar."><img src="./assets/ARCANE.png" draggable="false" :class="isTurn ? 'rune-btn-img' : 'rune-btn-img-notturn'" style="width: 100%; min-width: .5em; max-width: 2em; height: 100%; min-height: .5em; max-height: 2em;" v-on:click="isTurn ? takeRune('ARCANE') : ''"/></span> 
                  <h3 class="total-runes-text"><span style="color:#7332b7">{{user.runes.ARCANE}}</span> (<span style="color:#f5c441">{{user.affinities.ARCANE}}</span>)</h3>
                </div>
                <div class="rune-button">
                  <span class="tooltip" data-hover="Nature always deals 1 damage, then traps the target in poison vines, which absorb damage from the target's attacks and deal 1 damage per turn until they're killed. Super effective against earth shield."><img src="./assets/NATURE.png" :class="isTurn ? 'rune-btn-img' : 'rune-btn-img-notturn'" style="width: 100%; min-width: .5em; max-width: 2em; height: 100%; min-height: .5em; max-height: 2em;" v-on:click="isTurn ? takeRune('NATURE') : ''"/></span>
                  <h3 class="total-runes-text"><span style="color:#5ec234">{{user.runes.NATURE}}</span> (<span style="color:#f5c441">{{user.affinities.NATURE}}</span>)</h3>
                </div>
                <div class="rune-button">
                  <span class="tooltip" data-hover="Solar damage hits everyone in the game, including the user. Super effective against solar shield."><img src="./assets/SOLAR.png" draggable="false" :class="isTurn ? 'rune-btn-img' : 'rune-btn-img-notturn'" style="width: 100%; min-width: .5em; max-width: 2em; height: 100%; min-height: .5em; max-height: 2em;" v-on:click="isTurn ? takeRune('SOLAR') : ''"/></span>
                  <h3 class="total-runes-text"><span style="color:#c9721f">{{user.runes.SOLAR}}</span> (<span style="color:#f5c441">{{user.affinities.SOLAR}}</span>)</h3>
                </div>
                <div class="rune-button">
                  <span class="tooltip" data-hover="Darkness damage heals the caster for all damage done to health (not shield). Super effective against darkness shield."><img src="./assets/DARK.png" draggable="false" :class="isTurn ? 'rune-btn-img' : 'rune-btn-img-notturn'" style="width: 100%; min-width: .5em; max-width: 2em; height: 100%; min-height: .5em; max-height: 2em;" v-on:click="isTurn ? takeRune('DARK') : ''"/></span>
                  <h3 class="total-runes-text"><span style="color:#200f34">{{user.runes.DARK}}</span> (<span style="color:#f5c441">{{user.affinities.DARK}}</span>)</h3>
                </div>
                <div class="rune-button">
                  <span class="tooltip" data-hover="Wind damage is twice as effective against all shields. Super effective against water shield."><img src="./assets/WIND.png" draggable="false" :class="isTurn ? 'rune-btn-img' : 'rune-btn-img-notturn'" style="width: 100%; min-width: .5em; max-width: 2em; height: 100%; min-height: .5em; max-height: 2em;" v-on:click="isTurn ? takeRune('WIND') : ''"/></span>
                  <h3 class="total-runes-text"><span style="color:#b7b7b7">{{user.runes.WIND}}</span> (<span style="color:#f5c441">{{user.affinities.WIND}}</span>)</h3>
                </div>
            </div>
          </div>
        </div>
        <div class="start-game-button-container">
          <button v-if="!gameStarted" class="start-game-button" v-on:click="startGame()">Start Game</button>
        </div>
      </div>

      </div>
      <Sidebar :logs="logs" @leaveRoom="leaveRoom()"></Sidebar>
    
    
    
      <!-- <div v-if="ingame" :class="'chat-logs-parent-container'">
        <h2 class="sidebar-title">Game Logs</h2>
        <ChatLog class="chat-logs" :logs="logs"></ChatLog>
        <div class="leave-room-container">
          <h2 class="gameid-text">GameID: {{current_room_id}}</h2>
          <button class="leave-room-button" v-on:click="leaveRoom()">Leave Room</button>
        </div>
      </div> -->
    </div>
  
  


  
  
</div>
  
</template>
  
  <script>
  // import { ref } from "vue";
  
  import HpBar from "./components/HpBar.vue";
  // import Games from "./components/Games.vue";
  import LegendaryShopCards from "./components/LegendaryShopCards.vue";
  import DragonCards from "./components/DragonCards.vue";
  import Crafting from "./components/Crafting.vue";
  import PlayerCards from "./components/PlayerCards.vue";
  import ShieldBar from "./components/ShieldBar.vue";
  import Sidebar from "./components/sidebar/Sidebar.vue";
  import ClientSidePlayerCards from "./components/ClientSidePlayerCards.vue";
  import Authenticate from "./components/authenticate/Authenticate.vue"
  import PageLoader from "./components/PageLoader.vue";
  import GamesMenu from "./components/pagination/GamesMenu.vue";

  import { userPool } from "./components/authenticate/UserPool"

  import { socket } from "./websocket"

  import AuthState from "./components/authenticate/AuthState"

  
  export default {
    name: 'App',
    components: {
      HpBar,
      ShieldBar,
      // Games,
      LegendaryShopCards,
      DragonCards,
      Crafting,
      PlayerCards,
      Sidebar,
      ClientSidePlayerCards,
      Authenticate,
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

        
        
        AuthState,
        socket,
        
        shield_colors: [{"FIRE": "#dd221e"}, {"WATER":"#3f7ab6"}, {"DARK": "#200f34"}, {"WIND": "#b7b7b7"}, {"ARCANE": "#7332b7"}, {"EARTH": "#865b38"}, {"SOLAR": "#c9721f"}, {"NATURE":"#5ec234"}],
  
        gamesList: {"1": {"gameID": "1", "started": "False", "users": ['2304820348', '202308402834', '20384023840328', '2081023823048208', '20384023804']}, "2": {"gameID": "2", "started": "True", "users": ['2304820348', '202308402834', '20384023840328', '2081023823048208', '20384023804']},
                  "5": {"gameID": "5", "started": "False", "users": ['2304820348', '202308402834', '20384023840328', '2081023823048208', '20384023804']}, "6": {"gameID": "6", "started": "True", "users": ['2304820348', '202308402834', '20384023840328', '2081023823048208', '20384023804']},
                  "8": {"gameID": "8", "started": "False", "users": ['2304820348', '202308402834', '20384023840328', '2081023823048208', '20384023804']}, "9": {"gameID": "2", "started": "True", "users": ['2304820348', '202308402834', '20384023840328', '2081023823048208', '20384023804']},
                  "10": {"gameID": "10", "started": "False", "users": ['2304820348', '202308402834', '20384023840328', '2081023823048208', '20384023804']}, "11": {"gameID": "11", "started": "True", "users": ['2304820348', '202308402834', '20384023840328', '2081023823048208', '20384023804']}
        },
        // gamesList: null,
        nextToken: null,
  
        // cards: {"1":{"runeVal":5,"spellVal":3,"runeType":"fire","spellType":1,"cost":{"wind":2,"fire":5,"earth":10,"water":2,"nature":3,"solar":8}},"2":{"runeVal":7,"spellVal":6,"runeType":"solar","spellType":2,"cost":{"wind":2,"solar":7,"water":3}},"3":{"runeVal":9,"spellVal":10,"runeType":"water","spellType":1,"cost":{"wind":2,"nature":10}},"4":{"runeVal":8,"spellVal":8,"runeType":"arcane","spellType":2,"cost":{"arcane":8,"solar":5,"water":3}},"5":{"runeVal":10,"spellVal":4,"runeType":"nature","spellType":1,"cost":{"earth":10,"water":3,"solar":5,"dark":6}},"6":{"runeVal":3,"spellVal":1,"runeType":"wind","spellType":1,"cost":{"dark":8,"water":11}},"7":{"runeVal":6,"spellVal":9,"runeType":"wind","spellType":1,"cost":{"wind":2}},"8":{"runeVal":4,"spellVal":5,"runeType":"wind","spellType":1,"cost":{"dark":10,"solar":5,"fire":11,"wind":2}}},
        // dragons: {"Deep-sea Dragon": {"cost": {"water": 20,"dark": 20},"icon": "Deep-sea_Dragon.png","shield": 8,"damage": 2}, "Nova Dragon": {"cost": {"fire": 20,"solar": 20},"icon": "Nova_Dragon.png","shield": 8,"damage": 2}, "Swamp Dragon": {"cost": {"water": 20,"nature": 20},"icon": "Swamp_Dragon.png","shield": 8,"damage": 2},"Cloud Dragon": {"cost": {"water": 20,"wind": 20},"icon": "Cloud_Dragon.png","shield": 8,"damage": 2},},
        // users: {"1822372397923":{"health":12,"shield":5,"shieldType":"fire","runes":{"fire":1,"water":2,"earth":5,"arcane":3,"nature":3,"solar":6,"dark":2,"wind":2},"timer":80},"391234972397":{"health":10,"shield":5,"shieldType":"water","runes":{"fire":1,"water":2,"earth":5,"arcane":3,"nature":3,"solar":6,"dark":2,"wind":2},"timer":80}, "59123492397":{"health":10,"shield":5,"shieldType":"water","runes":{"fire":1,"water":2,"earth":5,"arcane":3,"nature":3,"solar":6,"dark":2,"wind":2},"timer":80}, "15123492397":{"health":10,"shield":5,"shieldType":"water","runes":{"fire":1,"water":2,"earth":5,"arcane":3,"nature":3,"solar":6,"dark":2,"wind":2},"timer":80}, "11113492397":{"health":10,"shield":5,"shieldType":"water","runes":{"fire":1,"water":2,"earth":5,"arcane":3,"nature":3,"solar":6,"dark":2,"wind":2},"timer":80}, "2222492397":{"health":10,"shield":5,"shieldType":"water","runes":{"fire":1,"water":2,"earth":5,"arcane":3,"nature":3,"solar":6,"dark":2,"wind":2},"timer":80}},
        logs: [":arcane:", ":fire: runes", 'log2', 'log3', 'log4', 'log5 took a :fire: rune worth x6 affinity and played a card to deal x5 :solar: to everyone', 'log6', 'log7', 'log8', 'log9', 'log10', 'log11', 'log12', 'log13', 'log14',
        ":fire: runes"],
        
        
        isTurn: false,
        
        connectedMsg: 'Disconnected',
        redisData: "",
        redisOtherUserData: "",

        turnSecond: '0',
        turnMinute: '0',
        turnHour: '0',
        turnDay: '0',
        countDate: null,
        timerId: null,
        

      
        current_game_card_shop: [{'card': {'rune': 'ARCANE', 'type': 'SHIELD', 'affinity': 8, 'power': 4}, 'cost': {'NATURE': 2, 'DARK': 8, 'ARCANE': 7, 'SOLAR': 5}}],
        current_game_dragon_shop: [{'dragon': {'type': 'THORN', 'runes': ['NATURE', 'ARCANE']}, 'cost': {'NATURE': 20, 'ARCANE': 20}}],
        current_game_users: [{"sid":"WWxbPZRWHvr_L7lNAAAF","hp":10,"shield":{"rune":null,"power":0},"runes":{"ARCANE":0,"SOLAR":0,"DARK":0,"NATURE":0,"EARTH":0,"WIND":0,"WATER":0,"FIRE":0}, "cards": [{"card": {"rune": "EARTH", "type": "ATTACK", "affinity": 7, "power": 7}}],"affinities":{"ARCANE":0,"SOLAR":0,"DARK":0,"NATURE":0,"EARTH":0,"WIND":0,"WATER":0,"FIRE":0},"dragons":[{"dragon": {"type": "VOID", "runes": ["ARCANE", "DARK"]}}, {"dragon": {"type": "CLOUD", "runes": ["WIND", "WATER"]}}],"isDead":false, "vines": 0, "burn": 0, "display_name": "client-player"}, {"sid":"other_sid1","hp":5,"shield":{"rune":null,"power":0},"runes":{"ARCANE":0,"SOLAR":0,"DARK":0,"NATURE":2,"EARTH":0,"WIND":0,"WATER":0,"FIRE":0}, "cards": [{"card": {"rune": "EARTH", "type": "ATTACK", "affinity": 7, "power": 7}}],"affinities":{"ARCANE":7,"SOLAR":0,"DARK":0,"NATURE":0,"EARTH":0,"WIND":0,"WATER":0,"FIRE":0},"dragons":[],"isDead":true, "vines": 10, "burn": 1, "display_name": "other-player1"}, {"sid":"other_sid2","hp":10,"shield":{"rune":null,"power":0},"runes":{"ARCANE":0,"SOLAR":0,"DARK":0,"NATURE":2,"EARTH":0,"WIND":0,"WATER":0,"FIRE":0}, "cards": [{"card": {"rune": "EARTH", "type": "ATTACK", "affinity": 7, "power": 7}}, {"card": {"rune": "ARCANE", "type": "ATTACK", "affinity": 7, "power": 7}}, {"card": {"rune": "ARCANE", "type": "ATTACK", "affinity": 7, "power": 7}}],"affinities":{"ARCANE":7,"SOLAR":0,"DARK":0,"NATURE":0,"EARTH":0,"WIND":0,"WATER":0,"FIRE":0},"dragons":[],"isDead":false, "vines": 0, "display_name": "other-player2"}],
        current_room_id: '0',
        ingame: false,
        tutorial: false,
        gameStarted: false,
  
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
        
  
      }
    },
    methods: {


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
      openPlayersHandModal(index) {
        this.showHandModalIndex = index
        this.showHandModal = true
      },
      

      // emitRedisTest() {
      //   let data = this.redisData
      //   this.redisData = ""
      //   this.socket.emit('redis-test', data)

      // },

      takeRune(element) {
        let data = element
        this.socket.emit('take-rune', data)
      },
  
      // KEEP ME ALIVE AT ALL COSTS
      iconPath(value) {
        return require(`./assets/${value}`)
      },
  
      updateShield(color, icon) {
        this.shield_color = color
        this.shield_icon = icon
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
        this.socket.emit('query-games')
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
  
      buyCard: function(index) {
        this.socket.emit('buy-card', {'index': index})
      },
  
      buyDragon: function(index) {
        this.socket.emit('buy-dragon', {'index': index})
      },
      
      // rooms with socket io
      joinRoom: function(id) { // emits to the server with the roomId to join (only handled on server side)
        this.socket.emit('join-room', {'gameid': id})
        this.ingame = true
        this.current_room_id = id
        this.gameStarted = this.gamesList[id].started
        console.log(`"joined room id: ${id}"`)
      },

      leaveRoom: function() { // emits to the server with the roomId to leave (only handled on server side)
        this.clearTurnTimer()
        this.socket.emit('leave-room')
        this.ingame = false
        this.current_room_id = null
        this.showHandModal = false
        this.gameStarted = false
        this.isTurn = false // make buttons greyed-out
        this.logs = [];
      },

      startGame: function() { // emits to the server with the roomId to leave (only handled on server side)
        this.socket.emit('start-game')
        this.gameStarted = true
        
      },
  
      playCard: function(cardIdx, type) {
        if (type == "SHIELD") {
          // remove the sword buttons from showing
          this.socket.emit('attack-card-selected', "false")
          // play the card immediately if it is a shield card
          this.socket.emit('play-card', {'index': cardIdx}) 
        } else if (type == "ATTACK") {
          this.socket.emit('attack-card-selected', "true")
          this.cardIdxBeingPlayed = cardIdx
        }
      },
  
      attackPlayer: function(sid) {
        this.socket.emit('attack-card-selected', "false") // attack-button visible = false; emit to make sure the attack buttons disappear
        this.socket.emit('play-card', {'index': this.cardIdxBeingPlayed, 'attackedPlayer': sid})
        this.cardIdxBeingPlayed = null
        
        
      },

      craftCard: function(rune1, rune2) {
        console.log(`rune 1: ${rune1}`)
        console.log(`rune 2: ${rune2}`)
        this.socket.emit('craft-card', {'element1':rune1, 'element2': rune2})

      },
  
      openDragonShop: function() {
        // this.buyingDragonCards = true
        // this.buyingShopCards = false
        // this.showHand = false
        this.socket.emit('shop-buttons-pressed', {'button': "dragon"})
      },
  
      openCardShop: function() {
        // this.buyingShopCards = true
        // this.buyingDragonCards = false
        // this.showHand = false
        this.socket.emit('shop-buttons-pressed', {'button': "shop"})
      },
      openCraftShop: function() {
        // this.buyingShopCards = true
        // this.buyingDragonCards = false
        // this.showHand = false
        this.socket.emit('shop-buttons-pressed', {'button': "craft"})
      },
      openPlayersHand: function() {
        // this.buyingShopCards = false
        // this.buyingDragonCards = false
        // this.showHand = true
        this.socket.emit('shop-buttons-pressed', {'button': "hand"})
      },

      /**
       * clear the countdown timer (reset to 0)
       */
      clearTurnTimer() {
        if (this.timerId) {
          console.log("CLEARING TIMER")
          clearInterval(this.timerId)
        }
        this.turnSecond = '0',
        this.turnMinute = '0',
        this.turnHour = '0',
        this.turnDay = '0',
        this.countDate = null
      },

      /**
       * Starts a countdown timer
       * @param {*} countDate unix epoch formatted date (e.g. 1687110770)
       */
      countDown(countDate) {
        
        const now = new Date().getTime();
  
        // Check if the countdown has finished
        if (now >= countDate) {
          console.log('Countdown finished!');
          clearInterval(this.timerId)
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
        m < 10 ? this.turnMinute = '0' + m : this.turnMinute = m;
        s < 10 ? this.turnSecond = '0' + s : this.turnSecond = s;
        h < 10 ? this.turnHour = '0' + h : this.turnHour = h;
        this.turnDay = d;
        
      }
  
    },
  

    // before the DOM is mounted
    beforeMount: function() {

      // Grab cognito user from local storage
      var cognitoUser = userPool.getCurrentUser()
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
      // window.setInterval(function() {
      //     var elem = document.getElementsByClassName('chat-log-container');
      //     elem.scrollTop = elem.scrollHeight;
      // }, 2000);

      // this.socket.on('redis-test', (msg) => {
      //   this.redisOtherUserData = msg
      //   console.log(this.redisOtherUserData)
      // });

      // Handle turn timer
      this.socket.on('turn-timer', (timer) => {
        this.countDate = new Date().getTime() + (timer > 0 ? timer + 1 : timer) * 1000;
        this.timerId = setInterval(() => {
          this.countDown(this.countDate)
        }, 1000);
      })



      this.socket.on('Connection', (msg) => { // retrieve 'Connection' data from the server
        this.connectedMsg = msg
        console.log(this.connectedMsg)
      });
  
      // connect socket handling
      this.socket.on('user-sid', (res) => {
        this.sid = res
        console.log('your sid equals ' + this.sid)
      });
  
      this.socket.on('current-turn-sid', (res) => {
        this.currentTurnSid = res
  
        // if the sid that came back from the server matches
        if (this.sid == this.currentTurnSid) {
          this.isTurn = true // make buttons visible
          var audio = new Audio(require('./assets/mp3s/notification.mp3'))
          audio.play()
        } else {
          this.isTurn = false
        }
        console.log('it is ' + this.currentTurnSid + ' turn')
      });
  
      // receive boolean that a user is about to pick who to attack
      this.socket.on('user-playing-attack-card', (res) => {
        if (res == "true") {
          this.attacking = true
        } else if (res == "false") {
          this.attacking = false
        }
        
      });

      // receive string of the element that killed a player | play the relevant sound effect
      this.socket.on('player-died', (res) => {
        var audio = new Audio(require('./assets/mp3s/player_died_by_' + res + '.mp3'))
        audio.play()
      });

      this.socket.on('game-over', (res) => {
        var audio = new Audio(require('./assets/mp3s/victory.mp3'))
        // var audio_tie_game = new Audio(require('./assets/mp3s/reeverb.mp3'))
        console.log('Player won the game: ' + res)
        if (res == null) {
          audio.play()
        } else audio.play()
       

      });

      // receive misc sound effect from the server and play it
      this.socket.on('play-sound', (res) => {
        var audio = new Audio(require('./assets/mp3s/' + res + '.mp3'))
        audio.play()
      });
  
      // receive the current room id that you are in from the server
      this.socket.on('current-room-id', (res) => {
        this.current_room_id = res
        console.log('Received current game ID as: ' + res)
      });
  
      // receive button pressed data when another player opens the shop, etc.
      this.socket.on('button-pressed', (res) => {
        if (res == "shop") {
          this.buyingShopCards = true
          this.buyingDragonCards = false
          this.showHand = false
          this.crafting = false
        } else if (res == "dragon") {
          this.buyingDragonCards = true
          this.buyingShopCards = false
          this.showHand = false
          this.crafting = false
        } else if (res == "hand") {
          this.buyingShopCards = false
          this.buyingDragonCards = false
          this.crafting = false
          this.showHand = true
        } else if (res == "craft") {
          this.buyingShopCards = false
          this.buyingDragonCards = false
          this.showHand = false
          this.crafting = true
        }
      });
  
        // receive (boolean) if game started
        this.socket.on('game-started', (res) => {
          this.gameStarted = res
          console.log("from server: Game started ? " + res)
      });
  
      // receive list of active games
      this.socket.on('list-games', (res) => {
        this.gamesList = res.games
        this.nextToken = res.last_key
        console.log('Active Games: ' + JSON.stringify(res))
      });
  
      this.socket.on('join-room', () => {
        this.ingame = true
        console.log('In game?: ' + this.ingame)
      });
  
  
      this.socket.on('game-logs', (res) => {
        res.map((log) => {
          this.logs.push(log)
        })
        // old implementation
        // this.logs = res
      });
  
      // grab dict of user and card shop game data from server
      this.socket.on('game-data', (res) => {
        console.log("got game data:", res)
        this.current_game_users = res['user_data']
        this.current_game_card_shop = res['card_shop']['cards']
        console.log("grabbing game data")
      });
  
  
      // dragon shop data
      this.socket.on('dragon-shop-data', (res) => {
        this.current_game_dragon_shop = res['dragons']
      });
      
    },
  
    // do things on first load of the DOM
    mounted: function() {
      this.pickRandomBackgroundOnDOMLoad()




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





  #app {
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



  .game-banner{
    max-height: var(--game-banner-height);
    position: absolute;
    width: 100%;
    height: 100%;
    color: white;
    background: linear-gradient(to right, #711282, rgb(12, 66, 132));
    z-index: 1;
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
  
  .other-player {
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: flex-start;
   
  }
  
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
  @media screen and (max-width: 640px) {
  }


    /* MOBILE */
  @media screen and (max-width: 740px) {
    #mobile-hamburger{
      visibility: visible;
      position: absolute;
      top:10px;
      left:10px;
      color:rgb(255, 255, 255);
      z-index: 99;
    }

    .shop-container {
      width: 100%;
      overflow-y:auto;
      height: 75vh;
    }

    .player-statistics-container{
      width: 100%;
      /* height: 85vh; */
      display: flex;
      flex-direction: column;
      align-items: center;
    }


    .shop-button-container {
      display: block;
      justify-content: center;
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
  }

  /* DESKTOP */
  @media screen and (min-width: 1024px) {
    
  }
  
  </style>
  