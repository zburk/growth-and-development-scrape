import json
import urllib.request
from typing import List, Dict

def request(action, **params):
    return {'action': action, 'params': params, 'version': 6}

# https://github.com/FooSoft/anki-connect
def invoke(action, **params):
    requestJson = json.dumps(request(action, **params)).encode('utf-8')
    response = json.load(urllib.request.urlopen(urllib.request.Request('http://localhost:8765', requestJson)))
    if len(response) != 2:
        raise Exception('response has an unexpected number of fields')
    if 'error' not in response:
        raise Exception('response is missing required error field')
    if 'result' not in response:
        raise Exception('response is missing required result field')
    if response['error'] is not None:
        raise Exception(response['error'])
    return response['result']

def addCustomCardType(title: str, fields: List[str], css: str = '', cardTemplates: List[Dict[str, str]] = []):
    if title not in invoke('modelNames'):
        if (len(cardTemplates) == 0):
            generateTemplateDict = {}
            for field in fields:
                generateTemplateDict[field] = '{{' + field + '}}'
            cardTemplates = [ generateTemplateDict ]

        invoke('createModel',
            modelName=title,
            inOrderFields=fields,
            css=css,
            cardTemplates=cardTemplates
        )