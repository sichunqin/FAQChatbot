
import os
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import requests
import secret

def getCSVFileName(url):
    p = os.path.basename(urlparse(url).path)
    return p.replace("+", "") + ".csv"

def getQuestionTag(url):
    p = os.path.basename(urlparse(url).path)
    return p.replace("+", "")
def getPageTitle(url):
    if "display" in url:
        p = os.path.basename(urlparse(url).path)
        return p.replace("+", " ")
    else:
        p = getH1PageTitle(url,)
        return p

def getH1PageTitle(urlPath):

    HEADERS = {
    'Authorization': 'Bearer ' + secret.token,
    'Content-Type': 'application/json'
    }
    response = requests.get(urlPath, headers=HEADERS)

    soup = BeautifulSoup(response.text, 'html.parser')
    h1 = soup.find('h1', {'id': 'title-text'})
    return h1.text.strip()

def getCleanPageTitle(pageTitle):
    return pageTitle.replace(" ","").replace("#", "")
    pass
urls = [
    "https://confluence.amlogic.com/pages/viewpage.action?pageId=262496189",
    "https://confluence.amlogic.com/display/SW/Irdeto+SDK+Integration+User+Guide",
    "https://confluence.amlogic.com/display/SW/Irdeto+CAS+FAQ",
    "https://confluence.amlogic.com/display/SW/Chatbot+FAQ",
    "https://confluence.amlogic.com/display/SW/Security+FAQ",
    "https://confluence.amlogic.com/display/SW/TEE+FAQ",
    "https://confluence.amlogic.com/display/SW/DRM+FAQ",
    "https://confluence.amlogic.com/display/SW/VMX+CAS+FAQ",
    "https://confluence.amlogic.com/display/SW//Secure+Provision+FAQ",
    "https://confluence.amlogic.com/display/SW/001+TEE+Running+Enviroment",
    "https://confluence.amlogic.com/display/SW/002+TEE+Error+Code",
    "https://confluence.amlogic.com/display/SW/003+TEE+Debug",
    "https://confluence.amlogic.com/display/SW/004+TEE+Storage",
    "https://confluence.amlogic.com/display/SW/005+TA+Issue",
    "https://confluence.amlogic.com/display/SW/006+TDK+FAQ",

]
