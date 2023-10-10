<template>

    <div v-show="showSignInForm" class="container"> 
        <form @submit.prevent="signIn()">
            <h2 class="head-text">Sign In</h2>
            <input class="input" v-model="userName" type="text" placeholder="Username/Email" autocomplete="on">
            <input class="input" v-model="password" type="password" placeholder="Password" autocomplete="on" maxlength="20">
            <span id="forgot-pass" class="clickable-text" v-on:click="showForgotPassword()">Forgot Password?</span>
            <h5 v-if="signInError" id="error">{{signInError}}</h5>
            <h5 v-if="registrationSuccessMsg" id="error">{{registrationSuccessMsg}}</h5>

            <button class="confirm-input-btn">Sign In</button>
            
            <div class="lower-text-container">
                <a>Need an account? <span class="clickable-text" v-on:click="showRegistration()">Sign Up</span> | or <span class="clickable-text" v-on:click="AuthState.skipAuth(true)">Skip Authentication</span></a>
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

            <h5 v-if="registerError" id="error">{{registerError}}</h5>
            <button class="confirm-input-btn">Sign Up</button>
            <div class="lower-text-container">
                <a>Already have an account? <span class="clickable-text" v-on:click="showSignIn()">Sign in</span> | or <span class="clickable-text" v-on:click="AuthState.skipAuth(true)">Skip Authentication</span></a>
            </div>
        </form>
    </div>

    
    <div v-show="showResetPasswordForm" class="container"> 
        <form @submit.prevent="resetPassword()">
            <h2 class="head-text">Forgot Password</h2>
            <input class="input" v-model="userName" type="text" placeholder="Username/Email" autocomplete="off">

            <h5 v-if="forgotPasswordError" id="error">{{forgotPasswordError}}</h5>
            <button class="confirm-input-btn">Reset My Password</button>
            <div class="lower-text-container">
                <a>Remember your password? <span class="clickable-text" v-on:click="showSignIn()">Sign in</span></a>
            </div>
        </form>
    </div>

    <div v-show="showConfirmPasswordResetForm" class="container"> 
        <form @submit.prevent="confirmResetPassword()">
            <h2 class="head-text">Confirm Password Reset</h2>
            <h5 id="error">A password reset code has been sent to {{destinationEmail}}. Enter the code below to reset your password.</h5>
            <label for="#code">Code</label>
            <input class="input" v-model="verificationCode" type="text" placeholder="123456" autocomplete="off">
            <label for="#new_password">New Password</label>
            <input class="input" v-model="newPassword" type="password" placeholder="" autocomplete="off">
            <label for="#enter_new password_again">Enter New Password Again</label>
            <input class="input" v-model="confirmNewPassword" type="password" placeholder="" autocomplete="off">
            
            <h5 v-if="changePasswordError" id="error">{{changePasswordError}}</h5>
            <button class="confirm-input-btn">Change Password</button>
        </form>
    </div>

    <!-- <a>Didn't receive a code? <span class="clickable-text" v-on:click="resendConfirmation()">Resend it</span></a> -->

</template>
  
  
<script>
    import { userPool } from './UserPool';
    import { socket } from '@/websocket';
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
            showConfirmAccountForm: false,
            showResetPasswordForm: false,
            showConfirmPasswordResetForm: false,
            userName: "",
            password: "",
            registerUserName: "",
            registerEmail: "",
            registerPassword: "",
            confirmPassword: "",

            signInError: "",
            registerError: "",
            registrationSuccessMsg: "",
            
            verificationCode: "",
            newPassword: "",
            confirmNewPassword: "",
            forgotPasswordError: "",
            changePasswordError: "",
            destinationEmail: "",



            AuthState,
            socket
        }
        
    },

    methods: {
        showSignIn: function() {
            this.showSignInForm = true
            this.showRegistrationForm = false
            this.showConfirmAccountForm = false
            this.showResetPasswordForm = false
            this.showConfirmAccountForm = false
        },

        showRegistration: function() {
            this.showRegistrationForm = true
            this.showSignInForm = false
            this.showConfirmAccountForm = false
        },

        showForgotPassword: function() {
            this.showResetPasswordForm = true
            this.showConfirmAccountForm = false
            this.showRegistrationForm = false
            this.showSignInForm = false
        },

        showConfirmPasswordReset: function() {
            this.showConfirmPasswordResetForm = true
            this.showResetPasswordForm = false
            this.showConfirmAccountForm = false
            this.showRegistrationForm = false
            this.showSignInForm = false
        },

        showConfirmAccount: function() {
            this.showConfirmAccountForm = true
            this.showRegistrationForm = false
            this.showSignInForm = false
        },

        signIn: function() {
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
                        // console.log("onSuccess: ", result)
                        this.AuthState.setAuthenticated(true)

                        let sub = result.getIdToken().decodePayload()['sub']
                        let username = result.getIdToken().decodePayload()['cognito:username']
                        this.socket.emit('auth', {'sub': sub, 'username': username})
                    },
                    // login failed
                    onFailure: (err) => {
                        // if the user isn't confirmed yet.
                        if (err.code === "UserNotConfirmedException") {
                            this.signInError = `${err.message} You should have received an email to confirm your account.`
                        } else {
                            this.password = ""
                            this.signInError = err.message
                        }
                        
                    }
                });
        },

        register: function() {
            if (this.confirmPassword != this.registerPassword) {
                this.registerError = "Passwords do not match."
                return
            }

            if (this.confirmPassword.length < 6) {
                this.registerError = "Password length must be at least 6 characters long."
                return;
            }

            var attributeList = [];

            var dataEmail = {
                Name: 'email',
                Value: this.registerEmail,
            };

            var attributeEmail = new AmazonCognitoIdentity.CognitoUserAttribute(dataEmail);

            attributeList.push(attributeEmail)

            userPool.signUp(this.registerUserName, this.registerPassword, attributeList, null, (err,result) => {
                if (err) {
                    this.registerError = err.message.split(';').length < 2 ? err.message : "Registration Failed."
                    return;
                }
                this.registerError = ""
                this.registrationSuccessMsg = `Registration Successful! A confirmation email has been sent to ${result.codeDeliveryDetails.Destination}. Please confirm the email before signing in.`
                this.showSignIn()
                var cognitoUser = result.user;
                console.log('user name is ' + cognitoUser.getUsername());
            });
        },


        resendConfirmation: function() {
            var userData = {
                Username: this.userName,
                Pool: userPool,
            };

            var cognitoUser = new AmazonCognitoIdentity.CognitoUser(userData);
            cognitoUser.resendConfirmationCode((err, result) => {
                if (err) {
                    alert(err.message || JSON.stringify(err));
                    return;
                }
                console.log('resending confirmation call result: ' + result);
            });

        },

        resetPassword: function() {
            var userData = {
                Username: this.userName,
                Pool: userPool,
            };

            var cognitoUser = new AmazonCognitoIdentity.CognitoUser(userData);
            cognitoUser.forgotPassword(
                {
                    // sent password reset code
                    onSuccess: (result) => {
                        this.destinationEmail = result.CodeDeliveryDetails.Destination // destination email
                        this.showConfirmPasswordReset()
                    },
                    onFailure: () => {
                        this.forgotPasswordError = "Please enter a valid Username or Email address."
                    }
                });

        },
        confirmResetPassword: function() {
            if (this.newPassword != this.confirmNewPassword) {
                this.changePasswordError = "Passwords do not match"
                return
            }
            var userData = {
                Username: this.userName,
                Pool: userPool,
            };

            var cognitoUser = new AmazonCognitoIdentity.CognitoUser(userData);
            cognitoUser.confirmPassword(
                this.verificationCode,
                this.newPassword,
                {
                    // sent password reset code
                    onSuccess: (result) => {
                        console.log("Password Confirmed! " + JSON.stringify(result))
                    },
                    onFailure: (err) => {
                        console.log("Password not confirmed! " + JSON.stringify(err))
                    }
                });

        }




    },

    created: function() {

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
        margin-top: 12vh;
        
    }

    form {
        width: 100%;
        max-width: 50vw;
        display: flex;
        flex-direction: column;
        justify-content: center;
        padding: 1em;
        background-color: rgba(17, 17, 17, 0.609);
        border-radius: 1em;
    }

    label {
        display: flex;
        justify-content: flex-start;
        color: white;
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

    #error {
        color: #d26a5c;
        word-wrap: break-word;
        
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