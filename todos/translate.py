import json
import logging
import boto3
import os
from todos import decimalencoder

dynamodb = boto3.resource('dynamodb')


def get(event, context):
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    # fetch todo from the database
    result = table.get_item(
        Key={
            'id': event['pathParameters']['id']
        }
    )

    #translate
    translate = boto3.client(service_name='translate', region_name='eu-west-1', use_ssl=True)
    source_language = "auto"
    

    if event['pathParameters']['lg'] == 'en':
        target_language = 'en'
    elif event['pathParameters']['lg'] == 'fr':
        target_language = 'fr'
    else:
        target_language = 'auto'

    result['Item']["text"] = translate.translate_text(Text=result['Item']["text"], SourceLanguageCode=source_language, TargetLanguageCode=target_language)
    
    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(result['Item'],
                           cls=decimalencoder.DecimalEncoder)
    }

    return response