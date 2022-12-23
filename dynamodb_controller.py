import boto3

dynamodb = boto3.resource('dynamodb')

table = dynamodb.Table("testdata")

# logs = []

# for i in range(5):
#     logs.append(f"averageplayername took 10x :arcane: damage to their shield and 20x :arcane: damage to their health.{i}")
def update_logs():
    try:
        response = table.update_item(
                Key={
                    'PK': 'GAME#12345'
                },
                # Append :logValue list to 'game_logs' attribute list
                UpdateExpression="SET gameLogs = list_append(if_not_exists(gameLogs, :emptyVal), :logVal)", 
                ExpressionAttributeValues={
                    ':logVal': ['log1'],
                    ':emptyVal': []
                },
                ReturnConsumedCapacity='TOTAL',
                ConditionExpression='attribute_exists(logs)'
            )
    except Exception as e:
        return "Couldn't update item"
    return response

# get a game by ID
def get_game(id: str=None):
    response = table.get_item(
        Key={
            'PK': f'GAME#{id}'
        },
        
        ReturnConsumedCapacity='TOTAL',

    )
    return response

# print(get_game("12345"))
print(update_logs())



# doing any action in-game:
    # read game from db

    # create Opulence object with config and and pass config dict from db read
    # opulence.players = db.players
    # opulence.turn = db.turn_index
    # opulence.card_shop.items = db.card_shop_items
    # opulence.dragon_shop.items = db.card_shop_items