<template>

<div class="parent">





  <div class="hero-container">

    <div class="opulence-banner-container">
      <img src="@/assets/OPULENCE.png" class="opulence-banner-img" draggable="false"/>
    </div>

    <div v-if="showStats" class="stats-container">
      <table class="table">
        <thead>
        </thead>
        <tbody>
          <tr>
            <td class="stats-txt">Skill Level</td>
            <th class="stats-txt">0</th>
          </tr>
          <tr>
            <td class="stats-txt">Total Wins</td>
            <th class="stats-txt">0</th>
          </tr>
          <tr class="stats-txt">
            <td class="stats-txt">Current XP</td>
            <th class="stats-txt">200</th>
          </tr>
          <tr class="stats-txt">
            <td class="stats-txt">XP Required for Next Level</td>
            <th class="stats-txt">200</th>
          </tr>
          <tr class="stats-txt">
            <td class="stats-txt">Legendary Cards Bought</td>
            <th class="stats-txt">100</th>
          </tr>
          <tr class="stats-txt">
            <td class="stats-txt">Dragons Bought</td>
            <th class="stats-txt">2</th>
          </tr>
        </tbody>

      </table>

      <div class="player-icon" >
        <img v-on:click="selectIcon = !selectIcon" draggable="false" :src="iconPath(selectedIcon)" style="width: 100%; height: 100%;"/>
          
        <div v-if="selectIcon" class="icon-selection">
          <div v-for="(img) in ownedIcons" :key="img">
            <img
              v-if="img !== selectedIcon"
              class="icons"
              v-on:click="setIcon(img)"
              :alt="img"
              :src="iconPath(img)"
              :style="{ borderColor: iconMappings.state[img] }"
              draggable="false"
            />
          </div>
        </div>

        <img>
      </div>

    </div>

    

    <div v-if="!AuthState.state.isAuthenticated && !showStats" class="play-container" >
        <input class="input-name" v-model="GameState.state.userName" type="text" placeholder="[username]" maxlength="20" pattern="[A-z0-9\s]">
        
        <button  class="classic-btn" v-on:click="$emit('name')">Set your display name</button>
        
    </div>

    <button v-if="!showStats" class="classic-btn" v-on:click="AuthState.state.isAuthenticated ? $emit('signOut') : $router.push('/login')">
      {{ AuthState.state.isAuthenticated ? 'Sign Out' : 'Sign In' }}
    </button>
    <button class="classic-btn" v-on:click="showStats = !showStats, selectIcon = false">{{ showStats ? 'Back' : 'Stats' }}</button>

    <button class="classic-btn" v-if="isDevEnvironment && !showStats" v-on:click="utils.setCreatedGame(true), GameState.state.ingame = true; $router.push({ name: 'game', params: { gameid: 'TESTGAME'} })">Development Game</button>
  </div>


  <div class="game-selection">
    <h2>Select a game from the list or create one</h2>
    <button class="create-game-button" v-on:click="$emit('showGameModal')" >Create Game</button>
    
    <div v-if="games && games.length > 0" >
      <div class="games-container">
        <Games class='games' v-for="game in displayedDict" :id="game.PK" :started="game.started" :players="game.players" :key="game.PK" @joinRoom="joinRoom" ></Games>
      </div>
      
      <!-- Pagination buttons -->
      <Pagination
        class="pagination"
        v-model="page"
        :page-count="maxPages"
        :margin-pages="1"
        :page-range="2"
        :no-li-surround="true"
        :first-last-button="true"
        @page-change="handlePageChange"
      ></Pagination>
    </div>
  </div>
</div>
</template>
  
  
<script>
import Games from "@/components/Games.vue"
import Pagination from "./Pagination.vue"
import AuthState from "../authenticate/AuthState";
import { socket } from "@/websocket"
import GameState from "@/GameState";
import utils from "@/utils";
import iconMappings from "@/iconMappings"

export default {
  name: "GamesMenu",
  components: {
    Games,
    Pagination,
  },
  props: { // variables when instantiating this component
    games: Object,
  },
  setup() {
    return {
        
    };
  },

  data() {
    return {
      page: 1,
      itemsPerPage: 4,
      socket,
      AuthState,
      GameState,
      utils,
      iconMappings,
      isDevEnvironment: process.env.VUE_APP_ENVIRONMENT === 'dev',
      showStats: true,
      selectIcon: false,
      selectedIcon: "default",
      ownedIcons: ['default', 'aether_sword', 'dark_staff', 'elemental_scroll', 'arcane_arrow', 'arcane_elixir', 'arcane_key', 'arcane_rune', 'arcane_sphere', 'dust_sphere', 'elemental_scroll', 'fire_ember', 'light_sphere', 'nature_elixir', 'pixel_elixir']
    }
  },
  computed: {
    // Slice the list of values depending on the page index
    displayedDict() {
      const itemArray = Object.values(this.games);
      const start = (this.page - 1) * this.itemsPerPage;
      const end = start + this.itemsPerPage;
      return itemArray.slice(start, end);
    },

    // computed prop to update and calc the max amount of pages to display
    maxPages() {
      if (this.GameState.state.nextToken) {
        return Math.ceil(Object.keys(this.games).length / this.itemsPerPage) + 1;
      }
      return Math.ceil(Object.keys(this.games).length / this.itemsPerPage);
    }
  },

  methods: {
    joinRoom(gameId) {
      // Handle join room logic with gameId
      console.log(`Join room from GamesMenu.vue with game ID: ${gameId}`);
      this.$emit('joinRoom', gameId);
    },

    handlePageChange(pageNumber) {
      this.page = pageNumber
    },

    queryGames() {
      const lastKey = this.GameState.state.nextToken
      this.socket.emit('query-games', {lastKey})
    },

    iconPath(value) {
      return require(`@/assets/icons/${value}.png`)
    },

    setIcon(img) {
      this.selectedIcon = img
    },
  },
  
  created: function() {
    this.queryGames()
  },

  updated() {
    console.log(`${this.page} ${this.maxPages}`)
    console.log(`LAST KEY: ${this.GameState.state.nextToken}`)
    if (this.page == this.maxPages && this.GameState.state.nextToken != null) {
      console.log("reached max page, querying for more items...")
      this.queryGames()
    }
  }
};
</script>
  
<style scoped>

  .parent {
    display: flex;
    gap: 2em;
    z-index: 1;
  }

  .classic-btn {
    cursor: pointer;
    padding: 1em;
    width: 100%;
    max-width: 15em;
    color: #8E9092;
    background-color: #24272C;
    border-color: #2d3036;
    margin-top: 5em;
  }

  .opulence-banner-container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 8vh;
    width:100%;
  }

  .opulence-banner-img {
    width: 100%;
    max-width: 20em;
  }


  
  .hero-container {
      background-color: rgba(0, 0, 0, 0.75);
      height: 100%;
      width: 100%;
      min-height: 100vh;
      min-width: 35vw;
      max-width: 35vw;
      padding-top: 0.5em;
      box-sizing: border-box;
  }

  .game-selection {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    width: 100%;
    height: 100%;
    margin-top: 8vh;
  }

  .games-container {
    overflow: auto;
    padding: 2em;
    height: 50vh;
    max-width: 35vw;
  }

  .games {
    background-color: rgb(30, 30, 30);
  }
  

  .pagination {
    margin-top: 0em;
  }

  .page-item {
    margin: 5px;
    background: linear-gradient(rgb(236, 75, 80));
  }
  .page-link-item {
    background: linear-gradient(rgb(236, 75, 80));
    color: linear-gradient(rgb(76, 191, 9));
  }
  .prev-item {
    margin: 20px;

  }
  .prev-link-item {
  }
  .next-item {
    margin: 20px;

  }
  .next-link-item {
  }
  .break-view {
  }
  .break-view-item {
  }

  .page-class {
    margin: 20px;
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


  .stats-container {
    position: relative;
    display: flex;
    padding: 1.25em;
    gap: 0.5em;
  }

  .player-icon {
    position: relative;
    width: 6em;
    height: 6em;
    min-width: 6em;
    border: 1px solid #e89b4e;
    display: flex;
    justify-content: center;
    align-items: center;
    cursor: pointer;

  }

  .icon-selection {
    position: absolute;
    width: 16em;
    max-height: 16em;
    background-color: #2d3036;
    overflow-y: auto;
    
    margin-top: 0.5em;
    top: 100%; /* Display below the player-icon */
    left: 50%;
    transform: translateX(-50%);
    
    display: flex;
    padding: 1em;
    gap: .25em;
    flex-wrap: wrap;
    justify-content: center;
    box-sizing: border-box;
  }

  .icons {
    transition: 0.3s ease-in-out;
    width: 4em;
    height: 4em;
    cursor: pointer;
    border: 2px solid #e89b4e;
    
  }

  .icons:hover {
    transform: scale(1.1);
    border: 2px solid #e89b4e;
  }

  .icons:active {
    transition: 0.1s ease-in-out;
    cursor:pointer;
    transform: translateY(1px);
    transform: scale(1.05);
    opacity: 70%;
  }
  

  .table {
    width: 100%;
    border-collapse: collapse;
    box-sizing: border-box;
  }

  .table th, td {
    border-top: 1px solid #e89b4e;
    padding: 0.5rem;
  }


  .stats-txt {
    color: rgb(255, 255, 255);
  }

</style>