<template>
  <Authenticate></Authenticate>
</template>


<script>
// import { ref } from "vue";
import Authenticate from "@/components/authenticate/Authenticate.vue"

import { userPool } from "@/components/authenticate/UserPool"

import { socket } from "@/websocket"

import AuthState from "@/components/authenticate/AuthState"

import GameState from "@/GameState"

// import utils from "./utils";

export default {
  name: "LoginView",
  components: {
    Authenticate,
  },
  setup() {
    
  },
  data: function() {
    return {
      AuthState,
      userPool,
      GameState,
      socket
    }
  },

  created: function() {
  
  },

  beforeMount: function() {

  }
}
</script>