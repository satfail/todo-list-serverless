import json
import logging
import boto3
import os
from todos import decimalencoder

dynamodb = boto3.resource('dynamodb')
translate = boto3.client('translate')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def get(event, context):
    logger.info(event)
    
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    # fetch todo from the database
    result = table.get_item(
        Key={
            'id': event['pathParameters']['id']
        }
    )

    #translate
    source_language = "auto"
    

    if event['pathParameters']['lg'] == 'en':
        target_language = 'en'
    elif event['pathParameters']['lg'] == 'fr':
        target_language = 'fr'
    else:
        target_language = 'auto'
        
    # The Lambda function calls the TranslateText operation and passes the 
    # review, the source language, and the target language to get the 
    # translated review. 
    test = translate.translate_text(Text= result['Item']['text'], SourceLanguageCode=source_language, TargetLanguageCode=target_language)
    #result['Item']["text"] = test.get('TranslatedText')
    #logging.info("Translation output: " + str(result['Item']["text"]))
    #logging.info("Translation test: " + str(test))
    logging.info("Translation getTranslated: " + str(test.get('TranslatedText')))

    
    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(test.get('TranslatedText'),
                           cls=decimalencoder.DecimalEncoder)
    }

    return response