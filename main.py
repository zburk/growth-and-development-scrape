from bs4 import BeautifulSoup
import requests

import logincreds


login_URL = 'http://www.orthodonticinstruction.com'


session = requests.Session()
session.post(login_URL, 
data = {
    'submitCheck' : 1,
    'username': logincreds.username,
    'password' : logincreds.password,
    'submit' : 'Login'})


URL = 'http://www.orthodonticinstruction.com/modules/'
page = session.get(URL)
soup = BeautifulSoup(page.text)

print(soup)

from AnkiDeck import AnkiDeck
import ankiApi

# Creates a new deck called 'Birds of a Feather Flock Together' and adds
# a card with the front saying "Red" and the back saying "Robin" with the tags
# "bird" and "flying"
# deckName = 'Birds of a Feather Flock Together'
# myDeck = AnkiDeck(deckName)
# myDeck.create()
# myDeck.addBasicCard(front='Red', back='Robin', tags=['bird', 'flying'])