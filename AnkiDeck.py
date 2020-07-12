from typing import List
import ankiApi

# DEMO
# Creates a new deck called 'Birds of a Feather Flock Together' and adds
# a card with the front saying "Red" and the back saying "Robin" with the tags
# "bird" and "flying"
# deckName = 'Birds of a Feather Flock Together'
# myDeck = AnkiDeck(deckName)
# myDeck.create()
# myDeck.addBasicCard(front='Red', back='Robin', tags=['bird', 'flying'])

class AnkiDeck:
    def __init__(self, title: str):
        self.title = title

        if 'Front Back Extra' not in ankiApi.invoke('modelNames'):
            ankiApi.invoke('createModel',
                modelName='Front Back Extra',
                inOrderFields= ['Front', 'Back', 'Extra'],
                css= ".card {\n font-family: arial;\n font-size: 20px;\n text-align: left;\n color: black;\n background-color: white;\n}\n",
                cardTemplates= [
                    {
                        'Front': '{{Front}}',
                        'Back': """{{ FrontSide }}<hr id=answer>{{ Back }}<hr id=answer>{{ Extra }}""",
                    }
                ]
            )

        
    def create(self):
        ankiApi.invoke('createDeck', deck=self.title)
    
    def generateCardOutline(self, model: str, tags: List[str] = []):
        return {
            'deckName': self.title,
            'modelName': model,
            'options': {
                'allowDuplicate': False,
                'duplicateScope': 'deck'
            },
            'tags': tags,
        }

    def addBasicCard(self, front: str, back: str, tags: List[str] = []):
        basicCard = self.generateCardOutline(model='Basic', tags=tags)
        basicCard['fields'] = {
            'Front': front,
            'Back': back
        }

        ankiApi.invoke('addNote', note=basicCard)
