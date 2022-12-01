<template>

    <div v-show="signIn" class="container"> 
        <h2 class="head-text">Sign In</h2>
        <input :id="signIn-username" class="input" v-model="userName" type="text" placeholder="Username/email" maxlength="20" pattern="[A-z0-9\s]">
        <input :id="signIn-pasword" class="input" v-model="password" type="password" placeholder="Password" maxlength="20" pattern="[A-z0-9\s]">
        <button class="confirm-input-btn"  v-on:click="play">Sign In</button>
        <div class="lower-text-container">
            <a>Haven't got an account? <span class="clickable-text" v-on:click="(register = true, signIn = false)">Register here</span></a>
        </div>
    </div>
    <div v-show="register" class="container"> 
        <h2 class="head-text">Register</h2>
        <input class="input" v-model="registerUserName" type="text" placeholder="Username" maxlength="20" pattern="[A-z0-9\s]">
        <input class="input" v-model="registerEmail" type="text" placeholder="Email" maxlength="20" pattern="[A-z0-9\s]">
        <input class="input" v-model="registerPassword" type="password" placeholder="Password" maxlength="20" pattern="[A-z0-9\s]">
        <input class="input" v-model="confirmPassword" type="password" placeholder="Confirm Password" maxlength="20" pattern="[A-z0-9\s]">
        <button class="confirm-input-btn"  v-on:click="play">Register</button>
        <div class="lower-text-container">
            <a>Already registered? <span class="clickable-text" v-on:click="(signIn = true, register = false)">Login</span></a>
        </div>
    </div>
    
</template>
  
  
<script>
    // import {userPool} from './UserPool';


    // const user = new CognitoUser({
    //     Username: this.userName,
    //     Pool: userPool
    // })
    export default {
    name: "AuthenticateUsers",
    props: {

    },
    setup() {
        return {
        };
    },
    data: function() {
        return {
            signIn: false,
            register: true,
            userName: "",
            password: "",
            registerUserName: "",
            registerEmail: "",
            registerPassword: "",
            confirmPassword: "",


        }
        
    },

    methods: {

    },

    created: function() { // debugging the props
        // console.log(this.logs)

    },

    mounted: function() {
    },

    updated: function() {
    }
};
</script>
  
<style>

</style>

<style scoped>
    .container {
        display: flex;
        flex-direction: column;
        
        align-items: center;
        margin: 0 auto;
        max-width: 50vw;
    }

    .input {
        height: 2em;
        width: 100%;
       
        background-color: rgba(205, 226, 255, 0.74);
        border-radius: .5em;
        color: rgba(255, 255, 255, 0.8);
        font-size: 2em;

        margin: .25em;
    }

    .confirm-input-btn{
        height: 2em;
        width: 100%;
        
        background-color: rgb(47, 83, 134);
        border-radius: .5em;
        color: rgba(255, 255, 255, 0.8);
        font-size: 2em;

        margin: .25em;
    }

    .head-text {
        color:white;
    }

    .lower-text-container {
        text-align: center;
        color: white;
    }

    .lower-text-container .clickable-text {
        color: rgb(71, 110, 172);
    }

    .lower-text-container .clickable-text:hover {
        color: rgb(36, 71, 126);
        transition: 0.25s ease-in-out;
        cursor: pointer;
    }



</style>