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