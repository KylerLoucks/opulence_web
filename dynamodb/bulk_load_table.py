import boto3
import json

dynamodb = boto3.resource('dynamodb')

table = dynamodb.Table("testdatapksk")


# Read from the items.json file and add to the list
items = []
with open('dynamodb/items.json', 'r') as file:
    for row in file:
        items.append(json.loads(row))

# Batch write the items from the 'items' list
with table.batch_writer() as batch:
    for item in items:
        batch.put_item(Item=item)
        print(f"Put item in database:")
        print(item)