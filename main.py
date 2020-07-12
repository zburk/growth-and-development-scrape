from AnkiDeck import AnkiDeck
import ankiApi
from bs4 import BeautifulSoup
import requests

import logincreds




class Scraper:
    
    session = requests.Session()
    base_URL = 'http://www.orthodonticinstruction.com/modules/'

    def login(self):
        login_URL = 'http://www.orthodonticinstruction.com/index.php'
        response = self.session.post(login_URL, 
        data = {
        'submitCheck' : 1,
        'username': logincreds.username,
        'password' : logincreds.password,
        'submit' : 'Login'})

        return response.status_code

    def getModules(self):
        """must be called after login, returns a LIST of modules"""
        
        page = self.session.get(self.base_URL)
        soup = BeautifulSoup(page.text, "html.parser")
        modules = soup.findAll('a', attrs={'class': "module_link"})

        return modules

    
       

    
    
   



if __name__ == "__main__":
    scraper = Scraper()
    scraper.login()
    modules = scraper.getModules()
    for index, module in enumerate(modules):
        CARD_TAG = module[index].text
        
        break


#the last module in level 1 is module #12
