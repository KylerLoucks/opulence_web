import json
import boto3
import os

table_name = os.environ['DDB_TABLE']
ddb = boto3.client('dynamodb', region_name="us-east-1")
def lambda_handler(event, context):
    print(json.dumps(event))

    if 'email_verified' in event['request']['userAttributes']:

        userid = event['request']['userAttributes']['sub']
        username = event['userName']
        email = event['request']['userAttributes']['email']

        try:
            response = ddb.update_item(
                TableName=table_name,
                Key={
                    'PK': {"S": f"USER#{userid}"},
                    'SK': {"S": f"USER#{userid}"}
                },
                UpdateExpression="SET email_address = :email, #username = :name, \
                                owned_icons = :icons, dragons_owned = :drag_own, leg_cards_bought = :leg_cards, \
                                #inv = :inv, #level = :lvl, xp = :xp, required_xp = :req_xp, \
                                games_won = :wins",
                ExpressionAttributeNames={
                    "#username": "username",
                    "#level": "level",
                    "#inv": "inventory",
                },
                ExpressionAttributeValues={
                    ":name": {"S": username},
                    ":email": {"S": email},
                    ":icons": {"SS": ['default']},
                    ":drag_own": {"N": "0"},
                    ":leg_cards": {"N": "0"},
                    ":lvl": {"N": "1"},
                    ":xp": {"N": "0"},
                    ":req_xp": {"N": "375"},
                    ":wins": {"N": "0"},
                    ":inv": {"M": {
                            "keys": {"N": "0"},
                            "common_crates": {"N": "0"}
                        }
                    }
                }
            )
            print(json.dumps(response))
        except Exception as e:
            print("failed to add user to the database: ", e)
    # returning event is required unless you want the `Verify Email` link to show a "Invalid lambda function output: Invalid JSON" msg.
    return event
