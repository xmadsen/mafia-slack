import boto3
from botocore.exceptions import ClientError

if __name__ == '__main__':
    dynamo = boto3.resource("dynamodb", endpoint_url="http://localhost:8000")
    try:
        #TODO this should really get stood up in cloud formation or the console
        print("creating players table")
        player_table = dynamo.create_table(
            AttributeDefinitions=[
                {
                    'AttributeName': '_id',
                    'AttributeType': 'S'
                },
            ],
            TableName='players',
            KeySchema=[
                {
                    'AttributeName': '_id',
                    'KeyType': 'HASH'
                },
            ],
            BillingMode='PAY_PER_REQUEST'
        )
        
        player_table.meta.client.get_waiter('table_exists').wait(TableName='players')
    except ClientError:
        print("table already exists")

    try:
        #TODO this should really get stood up in cloud formation or the console
        print("creating gameState table")
        player_table = dynamo.create_table(
            AttributeDefinitions=[
                {
                    'AttributeName': '_id',
                    'AttributeType': 'S'
                },
            ],
            TableName='gameState',
            KeySchema=[
                {
                    'AttributeName': '_id',
                    'KeyType': 'HASH'
                },
            ],
            BillingMode='PAY_PER_REQUEST'
        )
        
        player_table.meta.client.get_waiter('table_exists').wait(TableName='gameState')
    except ClientError:
        print("table already exists")