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

    def getXml(self, module_abreviation):
        return self.session.get(f"http://www.orthodonticinstruction.com/modules/modulefiles/dswmedia/{module_abreviation}/data.xml")

if __name__ == "__main__":
    scraper = Scraper()
    scraper.login()
    modules = scraper.getModules()

    xml_url = "http://www.orthodonticinstruction.com/modules/modulefiles/dswmedia/studyphysgrowth/data.xml"
    normal = "http://www.orthodonticinstruction.com/modules/view/1/studyphysgrowth/section/4/page/1"

    for index, module in enumerate(modules):
        CARD_TAG = module.text
        module_abbreviation = module["href"].split("/")[-1]
        module_xml = scraper.getXml(module_abbreviation)

        
        if index >=11 : break ## end of first "level"
    
    


#the last module in level 1 is module #12