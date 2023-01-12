import boto3

dynamodb = boto3.client('dynamodb')

table_name = ""

# Grab first line from table_name.txt config to grab the table name
with open('dynamodb/table_name.txt', 'r') as file:
    table_name = file.readlines()[0]

try:
    dynamodb.update_table(
        TableName=table_name,
        # Specify attribute types for PK and SK of GSI
        AttributeDefinitions=[
            {
                "AttributeName": "started",
                "AttributeType": "S"
            },
            {
                "AttributeName": "players",
                "AttributeType": "N"
            }
        ],
        GlobalSecondaryIndexUpdates=[
            {
                "Create": {
                    "IndexName": "OpenGamesIndex",
                    "KeySchema": [
                        {
                            "AttributeName": "started",
                            "KeyType": "HASH"
                        },
                        {
                            "AttributeName": "players",
                            "KeyType": "RANGE"
                        }
                    ],
                    "Projection": {
                        "ProjectionType": "ALL"
                    },
                    "ProvisionedThroughput": {
                        "ReadCapacityUnits": 5,
                        "WriteCapacityUnits": 5
                    }
                }
            }
        ],
    )
    print("Table updated successfully.")
except Exception as e:
    print("Could not update table. Error:")
    print(e)
