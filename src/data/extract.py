import config
import secret
import requests
from bs4 import BeautifulSoup
import os
import pandas as pd
from urllib.parse import urlsplit
from urllib.parse import urljoin

ROOT_URL = "https://confluence.amlogic.com"

BASE_DIR = os.path.join(os.path.dirname(__file__), '../database/')

HEADERS = {
    'Authorization': 'Bearer ' + secret.token,
    'Content-Type': 'application/json'
}

def extract(url, headers, output_file_path, question_tag):
    response = requests.get(url, headers=headers, verify=False)

    soup = BeautifulSoup(response.text, 'html.parser')

    questions = soup.find_all('h2', {'id': lambda x: x and question_tag in x})
    cleanQuesions = []
    cleanAnswers = []
    for question in questions:
        cleanQuesions.append(question.text)
        # print(question.text)

    #answers = soup.find_all('div', {'class': lambda x: x and 'panelContent' == x})
    answers = soup.select("[class=panelContent]")
    for answer in answers:
        if answer.find('a') != None:
            urls = answer.find_all('a')
            for url in urls:
                if urlsplit(url["href"]).netloc == "":  # relative path
                    url["href"] = urljoin(ROOT_URL,  url["href"])
                    pass

        if answer.find('img') != None:
            urls = answer.find_all('img')
            for url in urls:
                if urlsplit(url["src"]).netloc == "":  # relative path
                    url["src"] = urljoin(ROOT_URL,  url["src"])
                    pass
        cleanAnswers.append(answer.encode_contents().strip().decode('utf-8'))
        #cleanAnswers.append(answer.text.strip())
    sz = min(len(cleanQuesions), len(cleanAnswers))

    df = pd.DataFrame({'Question': cleanQuesions[:sz], 'Answer': cleanAnswers[:sz],'Class': question_tag })
    print(df)
    # output_file_path = os.path.join("src/data", output_file_name)

    df.to_csv(output_file_path, sep='|',quotechar='\'',index=False)

def extractAll():
    for url in config.urls:
        file_name = config.getCSVFileName(url)
        file_path = os.path.join(BASE_DIR, file_name)
        question_tag = config.getQuestionTag(url)
        extract(url,HEADERS,file_path,question_tag)
def extractOne():
    url = config.urls[0]
    file_name = config.getCSVFileName(url)
    file_path = os.path.join(BASE_DIR, file_name)
    question_tag = config.getQuestionTag(url)

    extract(url,HEADERS,file_path,question_tag)
    pass
if __name__ == "__main__":
    #extractAll()
    extractOne()
    pass


