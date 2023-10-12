<template>
  <div id="app">
    <router-view></router-view>
  </div>
  
</template>
  
  <script>
  // import { ref } from "vue";
  
  export default {
    name: 'App',
    components: {
    },
    setup() {
      // const hp = ref(0);
      // setInterval(() => (hp.value = Math.floor(Math.random() * 35)),2000);
      
      // return {hp}
      
    },
    data: function() {
      return {
      }
    },
    methods: {
      pickRandomBackgroundOnDOMLoad() {
        var backgrounds = ['bg_1.png', 'bg_2.png', 'bg_3.png', 'bg_4.png', 'bg_5.png', 'bg_6.png', 'bg_7.png', 'bg_8.png', 'bg_9.png', 'bg_10.png']
        document.body.style.backgroundImage = 'url(' + require('@/assets/backgrounds/'+backgrounds[Math.floor(Math.random() * backgrounds.length)]) + ')'
      },
    },
  

    // before the DOM is mounted
    beforeMount: function() {
    },

    
    created: function() {

      
    },
  
    // do things on first load of the DOM
    mounted: function() {
      this.pickRandomBackgroundOnDOMLoad()
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


  
  </style>
  