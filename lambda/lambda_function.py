import json
import os
import string
import random
import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['TABLE_NAME'])

def generate_short_code(length=6):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choices(chars, k=length))

def lambda_handler(event, context):
    http_method = event.get('httpMethod', '')
    path = event.get('path', '')

    if http_method == 'POST' and path == '/shorten':
        body = json.loads(event.get('body', '{}'))
        long_url = body.get('url')
        if not long_url:
            return response(400, {'error': 'Missing url field'})
        short_code = generate_short_code()
        table.put_item(Item={'short_code': short_code, 'long_url': long_url})
        return response(200, {'short_code': short_code, 'short_url': f"Use GET /{short_code} to redirect"})

    elif http_method == 'GET' and len(path) > 1:
        short_code = path.lstrip('/')
        result = table.get_item(Key={'short_code': short_code})
        item = result.get('Item')
        if not item:
            return response(404, {'error': 'Short code not found'})
        return {
            'statusCode': 301,
            'headers': {'Location': item['long_url']},
            'body': ''
        }

    return response(400, {'error': 'Invalid request'})

def response(status_code, body):
    return {
        'statusCode': status_code,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps(body)
    }