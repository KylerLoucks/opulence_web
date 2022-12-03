const AmazonCognitoIdentity = require('amazon-cognito-identity-js');

const poolData = {	UserPoolId: "us-east-1_oE6xNLqlz", // cognito user pool id
                    ClientId: "6v0nmvata8lpjt8crpj5jc69bf", // cognito client id
                    };
export const userPool = new AmazonCognitoIdentity.CognitoUserPool(poolData);

