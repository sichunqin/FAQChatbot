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

def extract(urlPath, headers, output_file_path, question_tag,page_title):
    response = requests.get(urlPath, headers=headers)

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
    if len(cleanQuesions) !=len(cleanAnswers):
        print("Warning: question count doesn't match answer count for the page " + urlPath)
        print("Question count: " + str(len(cleanQuesions)) + "Answer count: " + str(len(cleanAnswers)))
    sz = min(len(cleanQuesions), len(cleanAnswers))

    df = pd.DataFrame({'Question': cleanQuesions[:sz], 'Answer': cleanAnswers[:sz],'Class': question_tag })

    # Add question list to the data
    question_list_row =  {'Question': page_title, 'Answer': '\n'.join(cleanQuesions),'Class':question_tag}
    df = df._append(question_list_row,ignore_index=True)

    #print(df)
    # output_file_path = os.path.join("src/data", output_file_name)

    df.to_csv(output_file_path, sep='|',quotechar='\'',index=False)
    print("Crawl data from the page: " + urlPath)

def extractAll():
    for url in config.urls:
        file_name = config.getCSVFileName(url)
        file_path = os.path.join(BASE_DIR, file_name)
        question_tag = config.getQuestionTag(url)
        page_title = config.getPageTitle(url)
        extract(url,HEADERS,file_path,question_tag,page_title)
def extractOne():
    url = config.urls[0]
    file_name = config.getCSVFileName(url)
    file_path = os.path.join(BASE_DIR, file_name)
    question_tag = config.getQuestionTag(url)
    page_title = config.getPageTitle(url)
    extract(url,HEADERS,file_path,question_tag)
    pass
if __name__ == "__main__":
    #extractAll()
    extractOne()
    pass


