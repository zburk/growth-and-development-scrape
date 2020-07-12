from typing import List
import ankiApi

class AnkiDeck:
    def __init__(self, title: str):
        self.title = title
        
    def create(self):
        ankiApi.invoke('createDeck', deck=self.title)
    
    def addCard(self, front: str, back: str, tags: List[str] = []):
        ankiApi.invoke('addNote', note={
            'deckName': self.title,
            'modelName': 'Basic',
            'fields': {
                'Front': front,
                'Back': back
            },
            'options': {
                'allowDuplicate': False,
                'duplicateScope': 'deck'
            },
            'tags': tags,
        })
