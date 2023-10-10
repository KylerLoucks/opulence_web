<template>

<div class="parent">
  <div class="hero-container"></div>



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

import { socket } from "@/websocket"

export default {
  name: "GamesMenu",
  components: {
    Games,
    Pagination,
  },
  props: { // variables when instantiating this component
    games: Object,
    nextToken: Object,
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
      if (this.nextToken) {
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
      const lastKey = this.nextToken
      this.socket.emit('query-games', {lastKey})
    }
  },
  
  created: function() { // debugging the props
      
  },

  updated() {
    console.log(`${this.page} ${this.maxPages}`)
    console.log(`LAST KEY: ${this.nextToken}`)
    if (this.page == this.maxPages && this.nextToken != null) {
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
  }
  .hero-container {
      background-color: rgba(0, 0, 0, 0.75);
      height: 100%;
      width: 100%;
      min-height: 100vh;
      min-width: 35vw;
      max-width: 35vw;
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

</style>