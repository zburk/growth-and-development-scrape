from typing import List, Dict
import ankiApi

# DEMO
# Creates a new deck called 'Birds of a Feather Flock Together' and adds
# a card with the front saying "Red" and the back saying "Robin" with the tags
# "bird" and "flying"
# deckName = 'Birds of a Feather Flock Together'
# myDeck = AnkiDeck(deckName)
# myDeck.create()
# myDeck.addBasicCard(front='Red', back='Robin', tags=['bird', 'flying'])
# myDeck.addCustomCard(model='Front Back Extra', fields={
#     'Front': 'asdfsdfsd',
#     'Back': '2342323k',
#     'Extra': 'sdfkjs dlfks dflksdj fs',
# }, tags=['bird'])

class AnkiDeck:
    def __init__(self, title: str):
        self.title = title

    def create(self):
        ankiApi.invoke('createDeck', deck=self.title)

    def generateCardOutline(self, model: str, tags: List[str] = []):
        if model not in ankiApi.invoke('modelNames'):
            raise Exception('card type does not yet exist')

        return {
            'deckName': self.title,
            'modelName': model,
            'options': {
                'allowDuplicate': False,
                'duplicateScope': 'deck'
            },
            'fields': {},
            'tags': tags,
        }

    def addBasicCard(self, front: str, back: str, tags: List[str] = []):
        basicCard = self.generateCardOutline(model='Basic', tags=tags)
        basicCard['fields'] = {
            'Front': front,
            'Back': back
        }

        ankiApi.invoke('addNote', note=basicCard)
    
    def addCustomCard(self, model: str, fields: Dict[str, str], tags: List[str] = []):
        customCard = self.generateCardOutline(model=model, tags=tags)
        for fieldName, fieldContent in fields.items():
            customCard['fields'][fieldName] = fieldContent
        
        ankiApi.invoke('addNote', note=customCard)
