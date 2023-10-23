<template>
  <div id="app">
    <PageLoader></PageLoader>


    <transition name="settings" v-show="GameState.state.showSettings" appear>
        <div class="settings">
          <fa v-if="GameState.state.showSettings" icon="fa-solid fa-close" size="lg" class="settings-close-btn" v-on:click="GameState.state.showSettings = false" />
        </div>
    </Transition>
    <span v-if="!GameState.state.showSettings" id="mobile-hamburger" class="material-icons" v-on:click="GameState.state.showSettings = true">menu</span>
    
    
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



    <div class="game-banner">
        <template v-for="(user, index) in GameState.state.current_game_users" :key="index">
          <template v-if="user.sid == this.GameState.state.currentTurnSid">
            <span class="banner-current-turn">Current Turn: {{user.display_name}}</span>
            <fa icon="fa-solid fa-stopwatch" size="lg" class="timer-icon" />
            <span class="banner-turn-timer"> {{ this.GameState.state.turnHour !== '0' && this.GameState.state.turnHour !== '00' ? `${this.GameState.state.turnHour} : ${this.GameState.state.turnMinute} : ${this.GameState.state.turnSecond} ` : `${this.GameState.state.turnMinute} : ${this.GameState.state.turnSecond}` }}</span>
          </template>
        </template>
    </div>

    <!-- DESKTOP -->
    <div v-if="!utils.state.isMobile" class="master-container">

      <div class="shop-parent-container">
        <div v-show="GameState.state.buyingShopCards" class="shop-container">
              <h2 class="shop-title">Legendary Card Shop</h2>
              <LegendaryShopCards class="shop-cards" v-for="(key, index) in GameState.state.current_game_card_shop" :cost="key.cost" :power="key.card.power" :affinity="key.card.affinity" :runeType="key.card.rune" :spellType="key.card.type" :currentTurnSid="this.GameState.state.currentTurnSid" :users="this.GameState.state.current_game_users" :key="index" @buyCard="buyCard(index)"></LegendaryShopCards>
        </div>
        <div v-show="GameState.state.buyingDragonCards" class="shop-container">
              <h2 class="shop-title">Dragon Shop</h2>
              <DragonCards class="shop-cards" v-for="(key,index) in GameState.state.current_game_dragon_shop" :cost="key.cost" :dragonType="key.dragon.type" :currentTurnSid="this.GameState.state.currentTurnSid" :users="this.GameState.state.current_game_users" :key="index" @buyDragon="buyDragon(index)"></DragonCards>
        </div>

        <div v-show="GameState.state.crafting" class="shop-container">
              <h2 class="shop-title">Craft a basic card</h2>
              <Crafting class="shop-cards" :currentTurnSid="this.GameState.state.currentTurnSid" :users="this.GameState.state.current_game_users" @craftCard="craftCard"></Crafting>
        </div>
        
  
  
        <div v-show="GameState.state.showHand" class="shop-container">
            <template v-for="(user,userIndex) in GameState.state.current_game_users" :key="userIndex">
              <template v-if="user.sid == this.GameState.state.currentTurnSid">
                <h2 class="shop-title">{{user.display_name}}'s Hand</h2>
                <PlayerCards class="shop-cards" v-for="(card, index) in GameState.state.current_game_users[userIndex].cards" :power="card.card.power" :affinity="card.card.affinity" :runeType="card.card.rune" :spellType="card.card.type" :key="index" @playCard="playCard(index, card.card.type)"></PlayerCards>
              </template>
            </template>
        </div>



        <transition name="other-player-hand-slide" v-show="GameState.state.showHandModal" appear>
          <div v-if="GameState.state.current_game_users[GameState.state.showHandModalIndex] != null" class="player-hand-modal"  @click="GameState.state.showHandModal = false" @touchend="GameState.state.showHandModal">
            <h2 v-if="GameState.state.current_game_users[GameState.state.showHandModalIndex].sid != this.GameState.state.sid" style="font-size: clamp(1em, 1vw, 2em);">{{GameState.state.current_game_users[GameState.state.showHandModalIndex].display_name}}'s Hand</h2>
            <h2 v-else style="font-size: clamp(1em, 1vw, 2em);">Your Hand</h2>
            <div class="player-hand-modal-cards">
                <ClientSidePlayerCards class="shop-cards" v-for="(card) in GameState.state.current_game_users[GameState.state.showHandModalIndex].cards" :power="card.card.power" :affinity="card.card.affinity" :runeType="card.card.rune" :spellType="card.card.type" :key="card"></ClientSidePlayerCards>
            </div>
          </div>
        </transition>
  
  
        <div class="shop-button-container">
          <button class="shop-button" :disabled="!GameState.state.isTurn" v-on:click="openCraftShop">craft <fa icon="fa-solid fa-hammer" size="lg" class="button-icons"></fa></button>
          <button class="shop-button" :disabled="!GameState.state.isTurn" v-on:click="openCardShop">shop <fa icon="fa-solid fa-coins" size="lg" class="button-icons"></fa></button>
          <button class="shop-button" :disabled="!GameState.state.isTurn" v-on:click="openDragonShop">dragon <fa icon="fa-solid fa-dragon" size="lg" class="button-icons"></fa></button>
          <button class="shop-button" :disabled="!GameState.state.isTurn" v-on:click="openPlayersHand">hand <fa icon="fa-solid fa-layer-group" size="lg" class="button-icons"></fa></button>
        </div>
      </div>
  
      <div class="player-statistics-container">
        <div class="other-player-statistics">
          <template v-for="(user, userIndex) in GameState.state.current_game_users" :key="userIndex">
            <!-- render other player health/stats together -->
            <div v-if="user.sid != GameState.state.sid" class="divider"></div>
            <div class="other-player" v-if="user.sid != GameState.state.sid">
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
                
                    <img v-show="GameState.state.attacking && !user.isDead" src="@/assets/attack.png" style="width: 100%; min-width: 2em; max-width: 2em; height: 100%; max-height: 2em;" class="attack-button" v-on:click="attackPlayer(user.sid)"/>
                    
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
                    <img draggable="false" src="@/assets/FIRE.png" style="width:100%; height: 100%; max-width: 1em; max-height: 1em;"/>
                    <h3 class="total-runes-text"> <span style="color:#dd221e">{{user.runes.FIRE}}</span> (<span style="color:#f5c441">{{user.affinities.FIRE}}</span>)</h3>
                  </div> 
                  <div class="rune-button">
                    <img draggable="false" src="@/assets/WATER.png" style="width:100%; height: 100%; max-width: 1em; max-height: 1em;"/>
                    <h3 class="total-runes-text"><span style="color:#3f7ab6">{{user.runes.WATER}}</span> (<span style="color:#f5c441">{{user.affinities.WATER}}</span>)</h3>
                  </div>
                  <div class="rune-button">
                    <img draggable="false" src="@/assets/EARTH.png" style="width:100%; height: 100%; max-width: 1em; max-height: 1em;"/>
                    <h3 class="total-runes-text"><span style="color:#865b38">{{user.runes.EARTH}}</span> (<span style="color:#f5c441">{{user.affinities.EARTH}}</span>)</h3>
                  </div>
                  <div class="rune-button">
                    <img draggable="false" src="@/assets/ARCANE.png" style="width:100%; height: 100%; max-width: 1em; max-height: 1em;"/>
                    <h3 class="total-runes-text"><span style="color:#7332b7">{{user.runes.ARCANE}}</span> (<span style="color:#f5c441">{{user.affinities.ARCANE}}</span>)</h3>
                  </div>
                  <div class="rune-button">
                    <img draggable="false" src="@/assets/NATURE.png" style="width:100%; height: 100%; max-width: 1em; max-height: 1em;"/>
                    <h3 class="total-runes-text"><span style="color:#5ec234">{{user.runes.NATURE}}</span> (<span style="color:#f5c441">{{user.affinities.NATURE}}</span>)</h3>
                  </div>
                  <div class="rune-button">
                    <img draggable="false" src="@/assets/SOLAR.png" style="width:100%; height: 100%; max-width: 1em; max-height: 1em;"/>
                    <h3 class="total-runes-text"><span style="color:#c9721f">{{user.runes.SOLAR}}</span> (<span style="color:#f5c441">{{user.affinities.SOLAR}}</span>)</h3>
                  </div>
                  <div class="rune-button">
                    <img draggable="false" src="@/assets/DARK.png" style="width:100%; height: 100%; max-width: 1em; max-height: 1em;"/>
                    <h3 class="total-runes-text"><span style="color:#200f34">{{user.runes.DARK}}</span> (<span style="color:#f5c441">{{user.affinities.DARK}}</span>)</h3>
                  </div>
                  <div class="rune-button">
                    <img draggable="false" src="@/assets/WIND.png" style="width:100%; height: 100%; max-width: 1em; max-height: 1em;"/>
                    <h3 class="total-runes-text"><span style="color:#b7b7b7">{{user.runes.WIND}}</span> (<span style="color:#f5c441">{{user.affinities.WIND}}</span>)</h3>
                  </div>
              </div>
            </div>
            
        </template>
      </div>
  
      <!-- render client health bars in another location -->
      <div v-if="GameState.state.ingame" class="client-player-statistics">
        <div class="client-player" v-for="(user, index) in GameState.state.current_game_users" :key="index">
          <div v-if="user.sid == this.GameState.state.sid" class="client-player">

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
                  <span class="tooltip" data-hover="Fire damage lights the target on fire, dealing full damage on hit, then full damage again after the target's turn ends. Super effective against nature shield and poison vines."><img src="@/assets/FIRE.png" draggable="false" :class="GameState.state.isTurn ? 'rune-btn-img' : 'rune-btn-img-notturn'" style="width: 100%; min-width: .5em; max-width: 2em; height: 100%; min-height: .5em; max-height: 2em;" v-on:click="GameState.state.isTurn ? takeRune('FIRE') : ''"/></span>
                  <h3 class="total-runes-text"> <span style="color:#dd221e">{{user.runes.FIRE}}</span> (<span style="color:#f5c441">{{user.affinities.FIRE}}</span>)</h3>
                </div>
                <div class="rune-button">
                  <span class="tooltip" data-hover="Water damage has no select target, but hits between 1-4 enemies for full damage. Super effective against fire shield."> <img src="@/assets/WATER.png" draggable="false" :class="GameState.state.isTurn ? 'rune-btn-img' : 'rune-btn-img-notturn'" style="width: 100%; min-width: .5em; max-width: 2em; height: 100%; min-height: .5em; max-height: 2em;" v-on:click="GameState.state.isTurn ? takeRune('WATER') : ''"/></span>
                  <h3 class="total-runes-text"><span style="color:#3f7ab6">{{user.runes.WATER}}</span> (<span style="color:#f5c441">{{user.affinities.WATER}}</span>)</h3>
                </div>
                <div class="rune-button">
                  <span class="tooltip" data-hover="Earth damage has a 25% chance to crit for triple damage. Super effective against wind shield."><img src="@/assets/EARTH.png" draggable="false" :class="GameState.state.isTurn ? 'rune-btn-img' : 'rune-btn-img-notturn'" style="width: 100%; min-width: .5em; max-width: 2em; height: 100%; min-height: .5em; max-height: 2em;" v-on:click="GameState.state.isTurn ? takeRune('EARTH') : ''"/></span>
                  <h3 class="total-runes-text"><span style="color:#865b38">{{user.runes.EARTH}}</span> (<span style="color:#f5c441">{{user.affinities.EARTH}}</span>)</h3>
                </div>
                <div class="rune-button">
                  <span class="tooltip" data-hover="Arcane damage ignores shields altogether, dealing full damage to healthbar."><img src="@/assets/ARCANE.png" draggable="false" :class="GameState.state.isTurn ? 'rune-btn-img' : 'rune-btn-img-notturn'" style="width: 100%; min-width: .5em; max-width: 2em; height: 100%; min-height: .5em; max-height: 2em;" v-on:click="GameState.state.isTurn ? takeRune('ARCANE') : ''"/></span> 
                  <h3 class="total-runes-text"><span style="color:#7332b7">{{user.runes.ARCANE}}</span> (<span style="color:#f5c441">{{user.affinities.ARCANE}}</span>)</h3>
                </div>
                <div class="rune-button">
                  <span class="tooltip" data-hover="Nature always deals 1 damage, then traps the target in poison vines, which absorb damage from the target's attacks and deal 1 damage per turn until they're killed. Super effective against earth shield."><img src="@/assets/NATURE.png" :class="GameState.state.isTurn ? 'rune-btn-img' : 'rune-btn-img-notturn'" style="width: 100%; min-width: .5em; max-width: 2em; height: 100%; min-height: .5em; max-height: 2em;" v-on:click="GameState.state.isTurn ? takeRune('NATURE') : ''"/></span>
                  <h3 class="total-runes-text"><span style="color:#5ec234">{{user.runes.NATURE}}</span> (<span style="color:#f5c441">{{user.affinities.NATURE}}</span>)</h3>
                </div>
                <div class="rune-button">
                  <span class="tooltip" data-hover="Solar damage hits everyone in the game, including the user. Super effective against solar shield."><img src="@/assets/SOLAR.png" draggable="false" :class="GameState.state.isTurn ? 'rune-btn-img' : 'rune-btn-img-notturn'" style="width: 100%; min-width: .5em; max-width: 2em; height: 100%; min-height: .5em; max-height: 2em;" v-on:click="GameState.state.isTurn ? takeRune('SOLAR') : ''"/></span>
                  <h3 class="total-runes-text"><span style="color:#c9721f">{{user.runes.SOLAR}}</span> (<span style="color:#f5c441">{{user.affinities.SOLAR}}</span>)</h3>
                </div>
                <div class="rune-button">
                  <span class="tooltip" data-hover="Darkness damage heals the caster for all damage done to health (not shield). Super effective against darkness shield."><img src="@/assets/DARK.png" draggable="false" :class="GameState.state.isTurn ? 'rune-btn-img' : 'rune-btn-img-notturn'" style="width: 100%; min-width: .5em; max-width: 2em; height: 100%; min-height: .5em; max-height: 2em;" v-on:click="GameState.state.isTurn ? takeRune('DARK') : ''"/></span>
                  <h3 class="total-runes-text"><span style="color:#200f34">{{user.runes.DARK}}</span> (<span style="color:#f5c441">{{user.affinities.DARK}}</span>)</h3>
                </div>
                <div class="rune-button">
                  <span class="tooltip" data-hover="Wind damage is twice as effective against all shields. Super effective against water shield."><img src="@/assets/WIND.png" draggable="false" :class="GameState.state.isTurn ? 'rune-btn-img' : 'rune-btn-img-notturn'" style="width: 100%; min-width: .5em; max-width: 2em; height: 100%; min-height: .5em; max-height: 2em;" v-on:click="GameState.state.isTurn ? takeRune('WIND') : ''"/></span>
                  <h3 class="total-runes-text"><span style="color:#b7b7b7">{{user.runes.WIND}}</span> (<span style="color:#f5c441">{{user.affinities.WIND}}</span>)</h3>
                </div>
            </div>
          </div>
        </div>
        <div class="start-game-button-container">
          <button v-if="!GameState.state.gameStarted" class="start-game-button" v-on:click="startGame()">Start Game</button>
        </div>
      </div>

      </div>
      <Sidebar :logs="GameState.state.logs" @leaveRoom="leaveRoom()"></Sidebar>
    
    
    
      <!-- <div v-if="GameState.state.ingame" :class="'chat-logs-parent-container'">
        <h2 class="sidebar-title">Game Logs</h2>
        <ChatLog class="chat-logs" :logs="logs"></ChatLog>
        <div class="leave-room-container">
          <h2 class="gameid-text">GameID: {{GameState.state.current_room_id}}</h2>
          <button class="leave-room-button" v-on:click="leaveRoom()">Leave Room</button>
        </div>
      </div> -->
    </div>

    <!-- MOBILE -->
    <div v-if="utils.state.isMobile" class="master-container">
      
      
      <transition name="mobile-card-shops" v-show="GameState.state.buyingShopCards" appear>
        
        <div class="mobile-card-shop">
          <div class="mobile-shop-exit-btn">
            <fa icon="fa-solid fa-close" size="lg" class="close-icon" v-on:click="closeMobileShopModal()" />
          </div>
          <div class="mobile-shop-exit-btn"></div>
          <div class="shop-container">
              <h2 class="shop-title">Legendary Card Shop</h2>
              <button class="shop-button" :disabled="!GameState.state.isTurn" v-on:click="openDragonShop">
                <fa icon="fa-solid fa-dragon" size="lg" class="button-icons"></fa>
              </button>
              <LegendaryShopCards class="shop-cards" v-for="(key, index) in GameState.state.current_game_card_shop" :cost="key.cost" :power="key.card.power" :affinity="key.card.affinity" :runeType="key.card.rune" :spellType="key.card.type" :currentTurnSid="this.GameState.state.currentTurnSid" :users="this.GameState.state.current_game_users" :key="index" @buyCard="buyCard(index)"></LegendaryShopCards>
          </div>
        </div>
      </transition>

      <transition name="mobile-card-shops" v-show="GameState.state.buyingDragonCards" appear>
        
        <div class="mobile-card-shop">
          <div class="mobile-shop-exit-btn">
            <fa icon="fa-solid fa-close" size="lg" class="close-icon" v-on:click="closeMobileShopModal()" />
          </div>
          <div class="shop-container">
            <h2 class="shop-title">Dragon Shop</h2>
            <button class="shop-button" :disabled="!GameState.state.isTurn" v-on:click="openCardShop()">
              <fa icon="fa-solid fa-undo" size="lg" class="button-icons"></fa>
              <fa icon="fa-solid fa-coins" size="lg" class="button-icons"></fa>
            </button>
            <DragonCards class="shop-cards" v-for="(key,index) in GameState.state.current_game_dragon_shop" :cost="key.cost" :dragonType="key.dragon.type" :currentTurnSid="this.GameState.state.currentTurnSid" :users="this.GameState.state.current_game_users" :key="index" @buyDragon="buyDragon(index)"></DragonCards>
          </div>
        </div>
      </transition>

      <transition name="mobile-card-shops" v-show="GameState.state.showHand" appear>
        <div class="mobile-card-shop">
          <div class="mobile-shop-exit-btn">
            <fa icon="fa-solid fa-close" size="lg" class="close-icon" v-on:click="closeMobileShopModal()" />
          </div>
          <div class="mobile-shop-exit-btn"></div>
          <div class="shop-container">
            <template v-for="(user,userIndex) in GameState.state.current_game_users" :key="userIndex">
              <template v-if="user.sid == this.GameState.state.currentTurnSid">
                <h2 class="shop-title">{{user.display_name}}'s Hand</h2>
                <PlayerCards class="shop-cards" v-for="(card, index) in GameState.state.current_game_users[userIndex].cards" :power="card.card.power" :affinity="card.card.affinity" :runeType="card.card.rune" :spellType="card.card.type" :key="index" @playCard="playCard(index, card.card.type)"></PlayerCards>
              </template>
            </template>
          </div>
        </div>
      </transition>

      <transition name="mobile-card-shops" v-show="GameState.state.crafting" appear>
        <div class="mobile-card-shop">
          <div class="mobile-shop-exit-btn">
            <fa icon="fa-solid fa-close" size="lg" class="close-icon" v-on:click="closeMobileShopModal()" />
          </div>
          <div class="mobile-shop-exit-btn"></div>
          <div class="shop-container">
            <h2 class="shop-title">Craft a basic card</h2>
            <Crafting class="shop-cards" :currentTurnSid="this.GameState.state.currentTurnSid" :users="this.GameState.state.current_game_users" @craftCard="craftCard"></Crafting>
          </div>
        </div>
      </transition>

      <transition name="mobile-card-shops" v-show="GameState.state.showChat" appear>
        <div class="mobile-card-shop">
          <div class="mobile-shop-exit-btn">
            <fa icon="fa-solid fa-close" size="lg" class="close-icon" v-on:click="closeMobileShopModal()" />
          </div>
          <div class="mobile-shop-exit-btn"></div>
          <div class="shop-container">
            <h2 class="shop-title">Game Logs</h2>
            <ChatLog :logs="GameState.state.logs"></ChatLog>
          </div>
        </div>
      </transition>

      <!-- PLAYER STATS -->
      <transition name="mobile-card-shops" v-show="GameState.state.showHandModal" appear>
        <div class="mobile-card-shop">
          <div class="mobile-shop-exit-btn">
            <fa icon="fa-solid fa-close" size="lg" class="close-icon" v-on:click="closeMobileShopModal()" />
          </div>
          <div class="shop-container">
            <div v-if="GameState.state.current_game_users[GameState.state.showHandModalIndex] != null">
              <h2 v-if="GameState.state.current_game_users[GameState.state.showHandModalIndex].sid != this.GameState.state.sid" style="font-size: clamp(1em, 1vw, 2em);">{{GameState.state.current_game_users[GameState.state.showHandModalIndex].display_name}}'s Stats</h2>
              <h2 v-else style="font-size: clamp(1em, 1vw, 2em);">Your Stats</h2>


              <div class="hp-shield-bars">
                <div class="dragons-owned-container" >
                  <div class="dragons-owned-icons" v-for="dragon in GameState.state.current_game_users[GameState.state.showHandModalIndex].dragons" :key="dragon">
                    <img draggable="false" :src="iconPath(`dragons/icons/${dragon.dragon.type}dragon-icon.png`)" style="width: 100%; max-width: 2em; height: 100%; max-height: 2em;"/>
                    <div class="dragons-owned-icons-runes">
                      <img draggable="false" :src="iconPath(`${dragon.dragon.runes[0]}.png`)" style="width: 100%; max-width: 1em; height: 100%; max-height: 1em;"/>
                      <img draggable="false" :src="iconPath(`${dragon.dragon.runes[1]}.png`)" style="width: 100%; max-width: 1em; height: 100%; max-height: 1em;"/>
                    </div>
                  </div>
                </div>
                <span v-show="GameState.state.current_game_users[GameState.state.showHandModalIndex].vines > 0" class="status-effect-text" style="color:#5ec234">vines: {{GameState.state.current_game_users[GameState.state.showHandModalIndex].vines}}</span>
                <span v-show="GameState.state.current_game_users[GameState.state.showHandModalIndex].burn > 0" class="status-effect-text" style="color:#dd221e">burn: {{GameState.state.current_game_users[GameState.state.showHandModalIndex].burn}}</span>
                <div class="hp-bar">
                  <div class="hp-image">
                
                    <img v-show="GameState.state.attacking && !GameState.state.current_game_users[GameState.state.showHandModalIndex].isDead" src="@/assets/attack.png" style="width: 100%; min-width: 2em; max-width: 2em; height: 100%; max-height: 2em;" class="attack-button" v-on:click="attackPlayer(user.sid)"/>
                    
                    <img v-if="GameState.state.current_game_users[GameState.state.showHandModalIndex].isDead" draggable="false" :src="iconPath(death_icon)" style="width: 100%; max-width: 2em; height: 100%; max-height: 2em;">
                    <img v-else draggable="false" :src="iconPath(health_icon)" style="width: 100%; max-width: 2em; height: 100%; max-height: 2em;"> 
                  </div>
                    <HpBar :bgcolor="'#880808'" :value="GameState.state.current_game_users[GameState.state.showHandModalIndex].hp" :vines="GameState.state.current_game_users[GameState.state.showHandModalIndex].vines"/>
                </div>

                <div class="shield-bar">
                  <div class="shield-image">
                    <img v-if="GameState.state.current_game_users[GameState.state.showHandModalIndex].shield.rune == null" draggable="false" :src="iconPath(shield_icon)" style="width: 100%; max-width: 2em; height: 100%; max-height: 2em;"/>
                    <img v-else-if="GameState.state.current_game_users[GameState.state.showHandModalIndex].shield.rune == 'FIRE'" draggable="false" :src="iconPath('fire-shield.png')" style="width: 100%; max-width: 2em; height: 100%; max-height: 2em;"/>
                    <img v-else-if="GameState.state.current_game_users[GameState.state.showHandModalIndex].shield.rune == 'WATER'" draggable="false" :src="iconPath('water-shield.png')" style="width: 100%; max-width: 2em; height: 100%; max-height: 2em;"/>
                    <img v-else-if="GameState.state.current_game_users[GameState.state.showHandModalIndex].shield.rune == 'DARK'" draggable="false" :src="iconPath('dark-shield.png')" style="width: 100%; max-width: 2em; height: 100%; max-height: 2em;"/>
                    <img v-else-if="GameState.state.current_game_users[GameState.state.showHandModalIndex].shield.rune == 'ARCANE'" draggable="false" :src="iconPath('arcane-shield.png')" style="width: 100%; max-width: 2em; height: 100%; max-height: 2em;"/>
                    <img v-else-if="GameState.state.current_game_users[GameState.state.showHandModalIndex].shield.rune == 'EARTH'" draggable="false" :src="iconPath('earth-shield.png')" style="width: 100%; max-width: 2em; height: 100%; max-height: 2em;"/>
                    <img v-else-if="GameState.state.current_game_users[GameState.state.showHandModalIndex].shield.rune == 'NATURE'" draggable="false" :src="iconPath('nature-shield.png')" style="width: 100%; max-width: 2em; height: 100%; max-height: 2em;"/>
                    <img v-else-if="GameState.state.current_game_users[GameState.state.showHandModalIndex].shield.rune == 'SOLAR'" draggable="false" :src="iconPath('solar-shield.png')" style="width: 100%; max-width: 2em; height: 100%; max-height: 2em;"/>
                    <img v-else-if="GameState.state.current_game_users[GameState.state.showHandModalIndex].shield.rune == 'WIND'" draggable="false" :src="iconPath('wind-shield.png')" style="width: 100%; max-width: 2em; height: 100%; max-height: 2em;"/>
                  </div>
                    <ShieldBar :bgcolor="shield_color" :value="GameState.state.current_game_users[GameState.state.showHandModalIndex].shield.power" :shieldType="GameState.state.current_game_users[GameState.state.showHandModalIndex].shield.rune"/>
                </div>
              </div>
              
              <div class="player-runes">
                <div class="rune-button">
                  <img draggable="false" src="@/assets/FIRE.png" style="width:100%; height: 100%; max-width: 2em; max-height: 2em;"/>
                  <h3 class="total-runes-text"> <span style="color:#dd221e">{{GameState.state.current_game_users[GameState.state.showHandModalIndex].runes.FIRE}}</span> (<span style="color:#f5c441">{{GameState.state.current_game_users[GameState.state.showHandModalIndex].affinities.FIRE}}</span>)</h3>
                </div> 
                <div class="rune-button">
                  <img draggable="false" src="@/assets/WATER.png" style="width:100%; height: 100%; max-width: 2em; max-height: 2em;"/>
                  <h3 class="total-runes-text"><span style="color:#3f7ab6">{{GameState.state.current_game_users[GameState.state.showHandModalIndex].runes.WATER}}</span> (<span style="color:#f5c441">{{GameState.state.current_game_users[GameState.state.showHandModalIndex].affinities.WATER}}</span>)</h3>
                </div>
                <div class="rune-button">
                  <img draggable="false" src="@/assets/EARTH.png" style="width:100%; height: 100%; max-width: 2em; max-height: 2em;"/>
                  <h3 class="total-runes-text"><span style="color:#865b38">{{GameState.state.current_game_users[GameState.state.showHandModalIndex].runes.EARTH}}</span> (<span style="color:#f5c441">{{GameState.state.current_game_users[GameState.state.showHandModalIndex].affinities.EARTH}}</span>)</h3>
                </div>
                <div class="rune-button">
                  <img draggable="false" src="@/assets/ARCANE.png" style="width:100%; height: 100%; max-width: 2em; max-height: 2em;"/>
                  <h3 class="total-runes-text"><span style="color:#7332b7">{{GameState.state.current_game_users[GameState.state.showHandModalIndex].runes.ARCANE}}</span> (<span style="color:#f5c441">{{GameState.state.current_game_users[GameState.state.showHandModalIndex].affinities.ARCANE}}</span>)</h3>
                </div>
                <div class="rune-button">
                  <img draggable="false" src="@/assets/NATURE.png" style="width:100%; height: 100%; max-width: 2em; max-height: 2em;"/>
                  <h3 class="total-runes-text"><span style="color:#5ec234">{{GameState.state.current_game_users[GameState.state.showHandModalIndex].runes.NATURE}}</span> (<span style="color:#f5c441">{{GameState.state.current_game_users[GameState.state.showHandModalIndex].affinities.NATURE}}</span>)</h3>
                </div>
                <div class="rune-button">
                  <img draggable="false" src="@/assets/SOLAR.png" style="width:100%; height: 100%; max-width: 2em; max-height: 2em;"/>
                  <h3 class="total-runes-text"><span style="color:#c9721f">{{GameState.state.current_game_users[GameState.state.showHandModalIndex].runes.SOLAR}}</span> (<span style="color:#f5c441">{{GameState.state.current_game_users[GameState.state.showHandModalIndex].affinities.SOLAR}}</span>)</h3>
                </div>
                <div class="rune-button">
                  <img draggable="false" src="@/assets/DARK.png" style="width:100%; height: 100%; max-width: 2em; max-height: 2em;"/>
                  <h3 class="total-runes-text"><span style="color:#200f34">{{GameState.state.current_game_users[GameState.state.showHandModalIndex].runes.DARK}}</span> (<span style="color:#f5c441">{{GameState.state.current_game_users[GameState.state.showHandModalIndex].affinities.DARK}}</span>)</h3>
                </div>
                <div class="rune-button">
                  <img draggable="false" src="@/assets/WIND.png" style="width:100%; height: 100%; max-width: 2em; max-height: 2em;"/>
                  <h3 class="total-runes-text"><span style="color:#b7b7b7">{{GameState.state.current_game_users[GameState.state.showHandModalIndex].runes.WIND}}</span> (<span style="color:#f5c441">{{GameState.state.current_game_users[GameState.state.showHandModalIndex].affinities.WIND}}</span>)</h3>
                </div>
              </div>
              <div class="divider"></div>
              <div class="player-hand-modal-cards">
                <h2>Hand</h2>
                <ClientSidePlayerCards class="shop-cards" v-for="(card) in GameState.state.current_game_users[GameState.state.showHandModalIndex].cards" :power="card.card.power" :affinity="card.card.affinity" :runeType="card.card.rune" :spellType="card.card.type" :key="card"></ClientSidePlayerCards>
              </div>
            </div>
          </div>
        </div>
      </transition>
    

      <div class="player-statistics-container">
        <div class="other-player-statistics">
          <template v-for="(user, userIndex) in GameState.state.current_game_users" :key="userIndex">
            <!-- render other player health/stats together -->
            <div class="divider" v-if="user.sid != this.GameState.state.sid"></div>
            <div class="other-player" v-if="user.sid != this.GameState.state.sid" v-on:click="openPlayersHandModal(userIndex)" >
              
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
                
                    <img v-show="GameState.state.attacking && !user.isDead" src="@/assets/attack.png" style="width: 100%; min-width: 2em; max-width: 2em; height: 100%; max-height: 2em;" class="attack-button" v-on:click="attackPlayer(user.sid)"/>
                    
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
            </div>
          </template>
        </div>
      </div>


      <!-- render client health bars in another location -->
      <div class="client-player-statistics">
        <div class="client-player" v-for="(user, index) in GameState.state.current_game_users" :key="index">
          <div v-if="user.sid == this.GameState.state.sid" class="client-player">

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

            <!-- <img class="other-player-hand-button" draggable="false" :src="iconPath('logo.png')" style="width: 100%; max-width: 1em; height: 100%; max-height: 1em;"  v-on:click="openPlayersHandModal(index)"/> -->

            <div class="player-runes">
                <div class="rune-button">
                  <span class="tooltip" data-hover="Fire damage lights the target on fire, dealing full damage on hit, then full damage again after the target's turn ends. Super effective against nature shield and poison vines."><img src="@/assets/FIRE.png" draggable="false" :class="GameState.state.isTurn ? 'rune-btn-img' : 'rune-btn-img-notturn'" style="width: 100%; min-width: .5em; max-width: 3em; height: 100%; min-height: .5em; max-height: 3em;" v-on:click="GameState.state.isTurn ? takeRune('FIRE') : ''"/></span>
                  <h3 class="total-runes-text"> <span style="color:#dd221e">{{user.runes.FIRE}}</span> (<span style="color:#f5c441">{{user.affinities.FIRE}}</span>)</h3>
                </div>
                <div class="rune-button">
                  <span class="tooltip" data-hover="Water damage has no select target, but hits between 1-4 enemies for full damage. Super effective against fire shield."> <img src="@/assets/WATER.png" draggable="false" :class="GameState.state.isTurn ? 'rune-btn-img' : 'rune-btn-img-notturn'" style="width: 100%; min-width: .5em; max-width: 3em; height: 100%; min-height: .5em; max-height: 3em;" v-on:click="GameState.state.isTurn ? takeRune('WATER') : ''"/></span>
                  <h3 class="total-runes-text"><span style="color:#3f7ab6">{{user.runes.WATER}}</span> (<span style="color:#f5c441">{{user.affinities.WATER}}</span>)</h3>
                </div>
                <div class="rune-button">
                  <span class="tooltip" data-hover="Earth damage has a 25% chance to crit for triple damage. Super effective against wind shield."><img src="@/assets/EARTH.png" draggable="false" :class="GameState.state.isTurn ? 'rune-btn-img' : 'rune-btn-img-notturn'" style="width: 100%; min-width: .5em; max-width: 3em; height: 100%; min-height: .5em; max-height: 3em;" v-on:click="GameState.state.isTurn ? takeRune('EARTH') : ''"/></span>
                  <h3 class="total-runes-text"><span style="color:#865b38">{{user.runes.EARTH}}</span> (<span style="color:#f5c441">{{user.affinities.EARTH}}</span>)</h3>
                </div>
                <div class="rune-button">
                  <span class="tooltip" data-hover="Arcane damage ignores shields altogether, dealing full damage to healthbar."><img src="@/assets/ARCANE.png" draggable="false" :class="GameState.state.isTurn ? 'rune-btn-img' : 'rune-btn-img-notturn'" style="width: 100%; min-width: .5em; max-width: 3em; height: 100%; min-height: .5em; max-height: 3em;" v-on:click="GameState.state.isTurn ? takeRune('ARCANE') : ''"/></span> 
                  <h3 class="total-runes-text"><span style="color:#7332b7">{{user.runes.ARCANE}}</span> (<span style="color:#f5c441">{{user.affinities.ARCANE}}</span>)</h3>
                </div>
                <div class="rune-button">
                  <span class="tooltip" data-hover="Nature always deals 1 damage, then traps the target in poison vines, which absorb damage from the target's attacks and deal 1 damage per turn until they're killed. Super effective against earth shield."><img src="@/assets/NATURE.png" :class="GameState.state.isTurn ? 'rune-btn-img' : 'rune-btn-img-notturn'" style="width: 100%; min-width: .5em; max-width: 3em; height: 100%; min-height: .5em; max-height: 3em;" v-on:click="GameState.state.isTurn ? takeRune('NATURE') : ''"/></span>
                  <h3 class="total-runes-text"><span style="color:#5ec234">{{user.runes.NATURE}}</span> (<span style="color:#f5c441">{{user.affinities.NATURE}}</span>)</h3>
                </div>
                <div class="rune-button">
                  <span class="tooltip" data-hover="Solar damage hits everyone in the game, including the user. Super effective against solar shield."><img src="@/assets/SOLAR.png" draggable="false" :class="GameState.state.isTurn ? 'rune-btn-img' : 'rune-btn-img-notturn'" style="width: 100%; min-width: .5em; max-width: 3em; height: 100%; min-height: .5em; max-height: 3em;" v-on:click="GameState.state.isTurn ? takeRune('SOLAR') : ''"/></span>
                  <h3 class="total-runes-text"><span style="color:#c9721f">{{user.runes.SOLAR}}</span> (<span style="color:#f5c441">{{user.affinities.SOLAR}}</span>)</h3>
                </div>
                <div class="rune-button">
                  <span class="tooltip" data-hover="Darkness damage heals the caster for all damage done to health (not shield). Super effective against darkness shield."><img src="@/assets/DARK.png" draggable="false" :class="GameState.state.isTurn ? 'rune-btn-img' : 'rune-btn-img-notturn'" style="width: 100%; min-width: .5em; max-width: 3em; height: 100%; min-height: .5em; max-height: 3em;" v-on:click="GameState.state.isTurn ? takeRune('DARK') : ''"/></span>
                  <h3 class="total-runes-text"><span style="color:#200f34">{{user.runes.DARK}}</span> (<span style="color:#f5c441">{{user.affinities.DARK}}</span>)</h3>
                </div>
                <div class="rune-button">
                  <span class="tooltip" data-hover="Wind damage is twice as effective against all shields. Super effective against water shield."><img src="@/assets/WIND.png" draggable="false" :class="GameState.state.isTurn ? 'rune-btn-img' : 'rune-btn-img-notturn'" style="width: 100%; min-width: .5em; max-width: 3em; height: 100%; min-height: .5em; max-height: 3em;" v-on:click="GameState.state.isTurn ? takeRune('WIND') : ''"/></span>
                  <h3 class="total-runes-text"><span style="color:#b7b7b7">{{user.runes.WIND}}</span> (<span style="color:#f5c441">{{user.affinities.WIND}}</span>)</h3>
                </div>
            </div>
          </div>
        </div>

      </div>










    
    </div>

  
    <div v-if="utils.state.isMobile && GameState.state.ingame" class="shop-button-container">
      <div class="start-game-button-container">
        <button v-if="!GameState.state.gameStarted" class="start-game-button" v-on:click="startGame()">Start Game</button>
      </div>
      <template v-if="GameState.state.gameStarted">
        <button class="shop-button" :disabled="!GameState.state.isTurn" v-on:click="openCraftShop()">
          <fa icon="fa-solid fa-hammer" size="lg" class="button-icons"></fa>
        </button>
        <button class="shop-button" :disabled="!GameState.state.isTurn" v-on:click="openCardShop()">
          <fa icon="fa-solid fa-coins" size="lg" class="button-icons"></fa>
        </button>
        <button class="shop-button" :disabled="!GameState.state.isTurn" v-on:click="openPlayersHand()">
          <fa icon="fa-solid fa-layer-group" size="lg" class="button-icons"></fa>
        </button>
        <button class="shop-button" :disabled="!GameState.state.isTurn" v-on:click="openChatLogs()">
          <fa icon="fa-solid fa-comment-dots" size="lg" class="button-icons"></fa>
        </button>
      </template>
    </div>

  
  


  
  
</div>
  
</template>
  
  <script>
  // import { ref } from "vue";
  
  import HpBar from "@/components/HpBar.vue";
  // import Games from "@/components/Games.vue";
  import LegendaryShopCards from "@/components/LegendaryShopCards.vue";
  import DragonCards from "@/components/DragonCards.vue";
  import Crafting from "@/components/Crafting.vue";
  import PlayerCards from "@/components/PlayerCards.vue";
  import ShieldBar from "@/components/ShieldBar.vue";
  import Sidebar from "@/components/sidebar/Sidebar.vue";
  import ClientSidePlayerCards from "@/components/ClientSidePlayerCards.vue";
  import PageLoader from "@/components/PageLoader.vue";
  import ChatLog from "@/components/ChatLog.vue";

  import { userPool } from "@/components/authenticate/UserPool"

  import { socket } from "@/websocket"

  import AuthState from "@/components/authenticate/AuthState"

	import GameState from "@/GameState";

  import utils from "@/utils";

  import { clearTurnTimer } from "@/socketListeners";
  import emitter from '@/EventBus';
  
  export default {
    name: 'GameView',
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
      PageLoader,
      ChatLog,
    },
    props: {
        gameid: String,
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

      checkScreenSize() {
          
          // Update isMobile based on the current screen size
          if (window.innerWidth <= 768) {
            this.utils.setMobile(true)
          } else {
            this.utils.setMobile(false)
          }
      },

      viewSettings() {
        if (this.GameState.state.showSettings == true) {
          this.GameState.state.showSettings = false
        } else {
          this.GameState.state.showSettings = true
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
      openPlayersHandModal(index) {
        this.GameState.state.showHandModalIndex = index
        this.GameState.state.showHandModal = true
      },

      closeMobileShopModal() {
        this.GameState.state.crafting = false;
        this.GameState.state.buyingShopCards = false;
        this.GameState.state.buyingDragonCards = false;
        this.GameState.state.showHand = false;
        this.GameState.state.showChat = false;
        this.GameState.state.showHandModal = false;
      },
      

      // emitRedisTest() {
      //   let data = this.redisData
      //   this.redisData = ""
      //   this.socket.emit('redis-test', data)

      // },

      takeRune(element) {
        let data = element
        emitter.emit('showPopup', {message: `Took +1 ${element.toLowerCase()} rune.`, icon: "logo", borderColor: "#2799ff"});
        this.socket.emit('take-rune', data)
      },
  
      // KEEP ME ALIVE AT ALL COSTS
      iconPath(value) {
        return require(`@/assets/${value}`)
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
        this.socket.emit('play-button', {'username': String(this.GameState.state.userName)})
        console.log(this.GameState.state.userName)
        const lastKey = this.GameState.state.nextToken
        this.socket.emit('query-games', {lastKey})
      },
  
      createGame: function() {
        this.socket.emit('create-game', 
        {maxplayers: this.GameState.state.configMaxPlayers,
        cardsinshop: this.GameState.state.configShopSize,
        runesperturn: this.GameState.state.configRunesPerTurn,
        totaldragons: this.GameState.state.configTotalDragons,
        startinghealth: this.GameState.state.configPlayerStartHealth,
        turntimer: this.GameState.state.configTurnTimer})
        
        console.log('created a game')
        console.log('player health: ' + this.GameState.state.configPlayerStartHealth)
        this.GameState.state.ingame = true;
        
      },
  
      showTutorial: function() {
        console.log('showing tutorial')
        this.tutorial = true;
    
      },
      
      // TODO: Add callback from ws to show popup if the player can't afford.
      buyCard: function(index) {
        this.socket.emit('buy-card', {'index': index})
      },
  
      buyDragon: function(index) {
        this.socket.emit('buy-dragon', {'index': index})
      },
      
			// rooms with socket io
			joinRoom: async function(gameid) {
					return new Promise(( resolve, reject) => {
						try {
							console.log("Attempting to join game");
							this.socket.emit('join-room', { 'gameid': gameid }, (response) => {
									console.log("RESPONSE:", response);
									if (response.success) {
											
											this.GameState.state.ingame = true;
											this.GameState.state.current_room_id = gameid;
											this.GameState.state.gameStarted = this.GameState.state.gamesList[gameid].started;
											console.log("SUCCESS RESPONSE!!");
											resolve(true); // WebSocket join successful
									} else {
											console.log("RESPONSE WAS NOT SUCCESSFUL");
											reject(false); // WebSocket join failed
									}
							});
							} catch (error) {
									console.error('Error while joining room:', error);
									reject(false); // WebSocket join failed
							}
					});
			},

      leaveRoom: function() { // emits to the server with the roomId to leave (only handled on server side)
        clearTurnTimer()
        this.socket.emit('leave-room')
        this.GameState.state.ingame = false
        this.GameState.state.current_room_id = null
        this.GameState.state.showHandModal = false
        this.GameState.state.gameStarted = false
        this.GameState.state.isTurn = false // make buttons greyed-out
        this.GameState.state.logs = [];
        this.$router.push('/home');
      },

      startGame: function() { // emits to the server with the roomId to leave (only handled on server side)
        this.socket.emit('start-game')
        this.GameState.state.gameStarted = true
        
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

        if (this.utils.state.isMobile) {
          this.GameState.state.showHand = false;
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
        // TODO: REMOVE THESE. FOR TESTING ONLY. USE WEBSOCKET SERVER.
        this.GameState.state.buyingDragonCards = true
        this.GameState.state.buyingShopCards = false
        this.GameState.state.showHand = false
        this.GameState.state.crafting = false
        this.GameState.state.showChat = false;

        this.socket.emit('shop-buttons-pressed', {'button': "dragon"})
      },
  
      openCardShop: function() {
        // TODO: REMOVE THESE. FOR TESTING ONLY. USE WEBSOCKET SERVER.
        this.GameState.state.buyingShopCards = true
        this.GameState.state.buyingDragonCards = false
        this.GameState.state.showHand = false
        this.GameState.state.crafting = false
        this.GameState.state.showChat = false;
        
        this.socket.emit('shop-buttons-pressed', {'button': "shop"})
      },
      openCraftShop: function() {
        // TODO: REMOVE THESE. FOR TESTING ONLY. USE WEBSOCKET SERVER.
        this.GameState.state.buyingShopCards = false
        this.GameState.state.buyingDragonCards = false
        this.GameState.state.showHand = false
        this.GameState.state.crafting = true
        
        this.GameState.state.showChat = false;
        
        this.socket.emit('shop-buttons-pressed', {'button': "craft"})
      },

      openPlayersHand: function() {
        // TODO: REMOVE THESE. FOR TESTING ONLY. USE WEBSOCKET SERVER.
        this.GameState.state.showHand = true
        this.GameState.state.buyingShopCards = false
        this.GameState.state.buyingDragonCards = false
        this.GameState.state.crafting = false
        this.GameState.state.showChat = false;
        
        this.socket.emit('shop-buttons-pressed', {'button': "hand"})
      },


      openChatLogs: function() {
        // TODO: REMOVE THESE. FOR TESTING ONLY. USE WEBSOCKET SERVER.
        this.GameState.state.showChat = true;
        this.GameState.state.buyingShopCards = false
        this.GameState.state.buyingDragonCards = false
        this.GameState.state.showHand = false
        this.GameState.state.crafting = false

        this.socket.emit('shop-buttons-pressed', {'button': "hand"})
      },

      // /**
      //  * clear the countdown timer (reset to 0)
      //  */
      // clearTurnTimer() {
      //   if (this.GameState.state.timerId) {
      //     console.log("CLEARING TIMER")
      //     clearInterval(this.GameState.state.timerId)
      //   }
      //   this.GameState.state.turnSecond = '0',
      //   this.GameState.state.turnMinute = '0',
      //   this.GameState.state.turnHour = '0',
      //   this.GameState.state.turnDay = '0',
      //   this.GameState.state.countDate = null
      // },

      // /**
      //  * Starts a countdown timer
      //  * @param {*} countDate unix epoch formatted date (e.g. 1687110770)
      //  */
      // countDown(countDate) {
        
      //   const now = new Date().getTime();
  
      //   // Check if the countdown has finished
      //   if (now >= countDate) {
      //     console.log('Countdown finished!');
      //     clearInterval(this.GameState.state.timerId)
      //     return;
      //   }

      //   const diff = countDate - now;

      //   const second = 1000;
      //   const minute = second * 60;
      //   const hour = minute * 60;
      //   const day = hour * 24;

      //   const m = Math.floor((diff % hour) / minute);
      //   const s = Math.floor((diff % minute) / second);
      //   const h = Math.floor((diff % day) / hour);
      //   const d = Math.floor((diff / day));
      //   m < 10 ? this.GameState.state.turnMinute = '0' + m : this.GameState.state.turnMinute = m;
      //   s < 10 ? this.GameState.state.turnSecond = '0' + s : this.GameState.state.turnSecond = s;
      //   h < 10 ? this.GameState.state.turnHour = '0' + h : this.GameState.state.turnHour = h;
      //   this.GameState.state.turnDay = d;
        
      // }
  
    },
  

    // before the DOM is mounted
    beforeMount: function() {


      if (window.innerWidth <= 768) {
        this.GameState.state.crafting = false;
      } else {
        this.GameState.state.crafting = true;
      }

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
      // this.socket.on('turn-timer', (timer) => {
      //   this.GameState.state.countDate = new Date().getTime() + (timer > 0 ? timer + 1 : timer) * 1000;
      //   this.GameState.state.timerId = setInterval(() => {
      //     this.countDown(this.GameState.state.countDate)
      //   }, 1000);
      // })



      // this.socket.on('Connection', (msg) => { // retrieve 'Connection' data from the server
      //   this.connectedMsg = msg
      //   console.log(this.connectedMsg)
      // });
  
      // // connect socket handling
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
  
      // // receive boolean that a user is about to pick who to attack
      // this.socket.on('user-playing-attack-card', (res) => {
      //   if (res == "true") {
      //     this.GameState.state.attacking = true
      //   } else if (res == "false") {
      //     this.GameState.state.attacking = false
      //   }
        
      // });

      // // receive string of the element that killed a player | play the relevant sound effect
      // this.socket.on('player-died', (res) => {
      //   var audio = new Audio(require('@/assets/mp3s/player_died_by_' + res + '.mp3'))
      //   audio.play()
      // });

      // this.socket.on('game-over', (res) => {
      //   var audio = new Audio(require('@/assets/mp3s/victory.mp3'))
      //   // var audio_tie_game = new Audio(require('@/assets/mp3s/reeverb.mp3'))
      //   console.log('Player won the game: ' + res)
      //   if (res == null) {
      //     audio.play()
      //   } else audio.play()
       

      // });

      // // receive misc sound effect from the server and play it
      // this.socket.on('play-sound', (res) => {
      //   var audio = new Audio(require('@/assets/mp3s/' + res + '.mp3'))
      //   audio.play()
      // });
  
      // // receive the current room id that you are in from the server
      // this.socket.on('current-room-id', (res) => {
      //   this.GameState.state.current_room_id = res
      //   console.log('Received current game ID as: ' + res)
      // });
  
      // // receive button pressed data when another player opens the shop, etc.
      // this.socket.on('button-pressed', (res) => {
      //   if (res == "shop") {
      //     this.GameState.state.buyingShopCards = true
      //     this.GameState.state.buyingDragonCards = false
      //     this.GameState.state.showHand = false
      //     this.GameState.state.crafting = false
      //     this.GameState.state.showChat = false
      //   } else if (res == "dragon") {
      //     this.GameState.state.buyingDragonCards = true
      //     this.GameState.state.buyingShopCards = false
      //     this.GameState.state.showHand = false
      //     this.GameState.state.crafting = false
      //     this.GameState.state.showChat = false
      //   } else if (res == "hand") {
      //     this.GameState.state.showHand = true
      //     this.GameState.state.buyingShopCards = false
      //     this.GameState.state.buyingDragonCards = false
      //     this.GameState.state.crafting = false
      //     this.GameState.state.showChat = false
      //   } else if (res == "craft") {
      //     this.GameState.state.crafting = true
      //     this.GameState.state.buyingShopCards = false
      //     this.GameState.state.buyingDragonCards = false
      //     this.GameState.state.showHand = false
      //     this.GameState.state.showChat = false
      //   } else if (res == "logs") {
      //     this.GameState.state.showChat = true
      //     this.GameState.state.crafting = false
      //     this.GameState.state.buyingShopCards = false
      //     this.GameState.state.buyingDragonCards = false
      //     this.GameState.state.showHand = false
      //     this.GameState.state.showChat = false
      //   }
      // });
  
      //   // receive (boolean) if game started
      //   this.socket.on('game-started', (res) => {
      //     this.GameState.state.gameStarted = res
      //     console.log("from server: Game started ? " + res)
      // });
  
      // // receive list of active games
      // this.socket.on('list-games', (res) => {
      //   console.log('Active Games: ' + JSON.stringify(this.GameState.state.gamesList))
      //   for (let i = 0; i < res.games.length; i++) {
      //     this.GameState.state.gamesList.push(res.games[i])
      //   }

      //   // this.GameState.state.gamesList = res.games
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
  
  
      // // dragon shop data
      // this.socket.on('dragon-shop-data', (res) => {
      //   this.GameState.state.current_game_dragon_shop = res['dragons']
      // });
      
    },
  
    // do things on first load of the DOM
    mounted: function() {
      console.log("STARTED??", this.GameState.state.gameStarted)
      console.log("CURRENT SID: ", this.GameState.state.sid)
      console.log("CURRENT TURN SID: ", this.GameState.state.currentTurnSid)
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
  
  <style scoped>
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

  /* play section */
  .play-container {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    margin-top: 8vh;
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
  