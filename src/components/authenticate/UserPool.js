const AmazonCognitoIdentity = require('amazon-cognito-identity-js');

const poolData = {	UserPoolId: process.env.VUE_APP_USERPOOLID, // cognito user pool id
                    ClientId: process.env.VUE_APP_USERPOOLCLIENTID, // cognito client id
                    };
export const userPool = new AmazonCognitoIdentity.CognitoUserPool(poolData);

