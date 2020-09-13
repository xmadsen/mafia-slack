import json
def lambda_handler(event, context):
    print(f"Received event:\n{json.dumps(event)}\nWith context:\n{context}")
    response = {
        'statusCode': 200,
        'headers' : {},
        'body': {}
    }
    return response