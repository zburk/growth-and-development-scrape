from typing import List
import ankiApi

class AnkiDeck:
    def __init__(self, title: str):
        self.title = title
        
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