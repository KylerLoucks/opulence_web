<template>

<div v-if="games && games.length > 0" class="parent-container">
  <Games class='games' v-for="game in displayedDict" :id="game.PK" :started="game.started" :key="game.PK" @joinRoom="joinRoom" ></Games>
  <Pagination
    v-model="page"
    :page-count="maxPages"
    :margin-pages="1"
    :page-range="2"
    :no-li-surround="true"
    :first-last-button="true"
    @page-change="handlePageChange"
  ></Pagination>
</div>

</template>
  
  
<script>
import Games from "@/components/Games.vue"
import Pagination from "./Pagination.vue"

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
      itemsPerPage: 2,
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
    }
  },
  
  created: function() { // debugging the props
      
  },

  updated() {
    console.log(`${this.page} ${this.maxPages}`)
    if (this.page == this.maxPages) {
      console.log("reached max page, querying for more items...")
    }
  }
};
</script>
  
<style scoped>
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