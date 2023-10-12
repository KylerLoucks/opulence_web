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
  
    // connect socket handling
    this.socket.on('user-sid', (res) => {
      this.GameState.state.sid = res
      console.log('your sid equals ' + this.GameState.state.sid)
    });
  },

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
  }
}
</script>