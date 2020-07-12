from bs4 import BeautifulSoup
import requests
import logincreds

import ankiApi
from AnkiDeck import AnkiDeck

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
    ankiApi.addCustomCardType(title='Prompt / Answer Choices / Answer / Extra',
                          fields=['Prompt', 'Answer Choices', 'Answer', 'Extra'],
                          css=".card {\n font-family: arial;\n font-size: 20px;\n text-align: left;\n color: black;\n background-color: white;\n}\n",
                          cardTemplates=[
                                {
                                    'Front': '{{Prompt}}<br><br>{{ Answer Choices }}',
                                    'Back': '{{ Prompt }}<hr id=answer>{{ Answer }}<hr id=answer>{{ Answer Choices }}<hr id=answer>{{ Extra }}',
                                }
                            ])
    
    myDeck = AnkiDeck('DENT 126 (Growth & Development)::Module Questions')
    myDeck.create()

    scraper = Scraper()
    scraper.login()
    modules = scraper.getModules()

    xml_url = "http://www.orthodonticinstruction.com/modules/modulefiles/dswmedia/studyphysgrowth/data.xml"
    normal = "http://www.orthodonticinstruction.com/modules/view/1/studyphysgrowth/section/4/page/1"

    for index, module in enumerate(modules):
        if index > 11 : break ## end of first "level"

        print('Starting ' + module.text)
        CARD_TAG = 'DENT126::' + module.text.replace(' ', '-').lower()
        module_abbreviation = module["href"].split("/")[-1]
        module_xml = scraper.getXml(module_abbreviation).content
        
        soup = BeautifulSoup(module_xml,'lxml')
        self_test_element = soup.find('title', string="Self-Test").parent
        
        questions = self_test_element.find_all("page")

        for page in questions:
            PROMPT = page.find("p").getText()
            
            choices = page.findAll("choice")
            if(len(choices)==0): break #Some modules have a residual question talking about textbook chapters
            OPTIONS = list(map(lambda x: x.getText(), choices))

            index_of_correct_choice = page.find("choices")["correctchoice"]
            ANSWER = choices[int(index_of_correct_choice)-1].getText()
            
            #EXTRA = page.find('correctResponse').getText() # because I couldnt get this to work
            EXTRA = page.find_all('p')[-2].getText() # enter super jank workaround
            if(EXTRA==None):
                EXTRA=""
            elif(EXTRA.startswith("That's right,") or EXTRA.startswith("That's correct,")):
                #good, we found it!
                EXTRA = EXTRA.replace("That's right, ", "")
                EXTRA = EXTRA.replace("That's correct, ", "")
            else:
                EXTRA = ""
                
            # Convert OPTIONS to something viewable on Anki
            letterOptions = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
            assembledOptions = ''

            for index, option in enumerate(OPTIONS):
                assembledOptions = assembledOptions + letterOptions[index] + '. ' + option + '<br>'

            # print((PROMPT,OPTIONS,ANSWER,EXTRA,CARD_TAG))
            myDeck.addCustomCard(model='Prompt / Answer Choices / Answer / Extra', fields={
                'Prompt': PROMPT,
                'Answer Choices': assembledOptions,
                'Answer': ANSWER,
                'Extra': EXTRA
            }, tags=[CARD_TAG])
    
    


#the last module in level 1 is module #12