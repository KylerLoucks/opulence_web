<template>

    <div v-show="showSignInForm" class="container"> 
        <form @submit.prevent="signIn()">
            <h2 class="head-text">Sign In</h2>
            <input class="input" v-model="userName" type="text" placeholder="Username/email" autocomplete="on" maxlength="20">
            <input class="input" v-model="password" type="password" placeholder="Password" autocomplete="on" maxlength="20">
            <span id="forgot-pass" class="clickable-text" v-on:click="(showRegistrationForm = true, showSignInForm = false)">Forgot Password?</span>
            <h5 v-if="signInError" id="signIn-error">{{signInError}}</h5>
            <button class="confirm-input-btn">Sign In</button>
            
            <div class="lower-text-container">
                <a>Haven't got an account? <span class="clickable-text" v-on:click="(showRegistrationForm = true, showSignInForm = false)">Register here</span></a>
            </div>
        </form>

    </div>

    <div v-show="showRegistrationForm" class="container"> 
        <form @submit.prevent="register()">
            <h2 class="head-text">Register</h2>
            <input class="input" v-model="registerUserName" type="text" placeholder="Username" autocomplete="off">
            <input class="input" v-model="registerEmail" type="text" placeholder="Email"  autocomplete="off">
            <input class="input" v-model="registerPassword" type="password" placeholder="Password" autocomplete="off">
            <input class="input" v-model="confirmPassword" type="password" placeholder="Confirm Password" autocomplete="off">

            <h5 v-if="registerError" id="signIn-error">{{registerError}}</h5>
            <button class="confirm-input-btn">Register</button>
            <div class="lower-text-container">
                <a>Already registered? <span class="clickable-text" v-on:click="(showSignInForm = true, showRegistrationForm = false)">Login</span></a>
            </div>
        </form>
    </div>
    
</template>
  
  
<script>
    import {userPool} from './UserPool';
    import AuthState from './AuthState';
    const AmazonCognitoIdentity = require('amazon-cognito-identity-js');

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
            showSignInForm: false,
            showRegistrationForm: true,
            userName: "",
            password: "",
            registerUserName: "",
            registerEmail: "",
            registerPassword: "",
            confirmPassword: "",

            signInError: "",
            registerError: "",
            AuthState
        }
        
    },

    methods: {
        signIn() {
            var authenticationData = {
                Username: this.userName,
                Password: this.password,
            };

            var authenticationDetails = new AmazonCognitoIdentity.AuthenticationDetails(authenticationData);

            var userData = {
                Username: this.userName,
                Pool: userPool,
            };

            var cognitoUser = new AmazonCognitoIdentity.CognitoUser(userData);
            // Authenticate user sign-in
            cognitoUser.authenticateUser(
                authenticationDetails, 
                {
                    // login was successful
                    onSuccess: (result) => {
                        console.log("onSuccess: ", result)
                        this.AuthState.setAuthenticated(true)
                    },
                    // login failed
                    onFailure: (err) => {
                        // alert(err.message || JSON.stringify(err))
                        console.log("login failed: ", err)
                        this.password = ""
                        this.signInError = err.message
                    }
                });
        },

        register() {
            if (this.confirmPassword != this.registerPassword) {
                this.registerError = "Passwords do not match"
                return
            }

            var attributeList = [];

            var dataEmail = {
                Name: 'email',
                Value: this.registerEmail,
            };

            var attributeEmail = new AmazonCognitoIdentity.CognitoUserAttribute(dataEmail);

            attributeList.push(attributeEmail)

            userPool.signUp(this.registerUserName, this.registerPassword, attributeList, null, function(err,result) {
                if (err) {
                    console.log("Registration failed: ", err)
                    alert(err.message || JSON.stringify(err));
                    return;
                }
                console.log("result: " + JSON.stringify(result))
                var cognitoUser = result.user;
                console.log('user name is ' + cognitoUser.getUsername());
            });
        }


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
        align-items: center;
        margin: 0 auto;
        justify-content: center;
    }

    form {
        justify-content: center;
        display: flex;
        flex-direction: column;
        max-width: fit-content;
    }

    .input {
        background-color: rgba(205, 226, 255, 0.74);
        border-radius: .5em;
        color: rgba(255, 255, 255, 0.8);
        font-size: 2em;

        margin-bottom: .25em;
    }

    .confirm-input-btn {
        width: 100%;
        justify-content: center;
        background-color: rgb(47, 83, 134);
        border-radius: .5em;
        color: rgba(255, 255, 255, 0.8);
        font-size: 2em;

        margin-bottom: .25em;
    }

    .head-text {
        color:white;
    }

    .lower-text-container {
        text-align: center;
        color: white;
    }

    #forgot-pass{
        margin-bottom: .5em;
        display: flex;
        justify-content: flex-end;
    }

    #signIn-error {
        color: #d26a5c
    }

    .clickable-text {
        color: rgb(71, 110, 172);
    }

    .clickable-text:hover {
        color: rgb(36, 71, 126);
        transition: 0.25s ease-in-out;
        cursor: pointer;
    }



</style>