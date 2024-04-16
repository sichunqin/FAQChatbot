import config
import secret
import requests
from bs4 import BeautifulSoup
import os
import pandas as pd
from urllib.parse import urlsplit
from urllib.parse import urljoin
import common
import copy

ROOT_URL = "https://confluence.amlogic.com"

BASE_DIR = os.path.join(os.path.dirname(__file__), '../database/')

HEADERS = {
    'Authorization': 'Bearer ' + secret.token,
    'Content-Type': 'application/json'
}

def generateFAQCategory(title_list,out_file_path,is_new_file=True):

    linked_title_list = []
    for title in title_list:
        linked_title_list.append(common.convertToLinkedText(title))
    title_list_row =  {'Question': ["FAQ Category"], 'Answer': ['\n'.join(linked_title_list)],'Class':["FAQCategory"]}
    df = pd.DataFrame(title_list_row)
    if(is_new_file):
        df.to_csv(out_file_path, sep='|',quotechar='\'',index=False)
    else:
        df.to_csv(out_file_path, sep='|',quotechar='\'',index=False,mode='a', header=False)
    print("Generate FAQ Category at : " + out_file_path)
    pass

def extract(urlPath, headers, output_file_path, question_tag,page_title, need_toc = True):
    response = requests.get(urlPath, headers=headers,verify=False)

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
                if url.get("href") is None:  # not href in the url, then ignore it.
                    continue
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

    linkedCleanQuestions = []
    for que in cleanQuesions:
        linkedCleanQuestions.append(common.convertToLinkedText(que))
        pass
    # Add question list to the data
    if need_toc:
        question_list_row =  {'Question': page_title, 'Answer': '\n'.join(linkedCleanQuestions),'Class':question_tag}
        df = df._append(question_list_row,ignore_index=True)

    df.to_csv(output_file_path, sep='|',quotechar='\'',index=False)
    print("Crawl data from the page: " + urlPath)

def extractH2FromPage(urlPath, headers, output_file_path, question_tag,page_title, need_toc = True):
    response = requests.get(urlPath, headers=headers, verify=False)

    soup = BeautifulSoup(response.text, 'html.parser')

    questions = soup.find_all('h2', {'id': lambda x: x and question_tag in x})
    cleanQuesions = []
    cleanAnswers = []
    answers = []
    q = ""

    for question in questions:
        cleanQuesions.append(question.text)
        answer_tag = soup.new_tag("div")
        n = question.next_sibling
        while (n != None):
            if(n.name == "h2"):
                break
            answer_tag.append(copy.copy(n))
            n = n.next_sibling

        answers.append(answer_tag)

    for answer in answers:
        if answer.find('a') != None:
            urls = answer.find_all('a')
            for url in urls:
                if url.get("href") is None:  # not href in the url, then ignore it.
                    continue
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

    linkedCleanQuestions = []
    for que in cleanQuesions:
        linkedCleanQuestions.append(common.convertToLinkedText(que))
        pass
    # Add question list to the data
    if need_toc:
        question_list_row =  {'Question': page_title, 'Answer': '\n'.join(linkedCleanQuestions),'Class':question_tag}
        df = df._append(question_list_row,ignore_index=True)

    df.to_csv(output_file_path, sep='|',quotechar='\'',index=False)
    print("Crawl data from the page: " + urlPath)


def extractAll():
    for url in config.urls:
        page_title = config.getH1PageTitle(url)
        question_tag = config.getCleanPageTitle(page_title)
        file_name = question_tag + ".csv"
        file_path = os.path.join(BASE_DIR, file_name)
        extract(url,HEADERS,file_path,question_tag,page_title)

def extractOne():

    url = config.urls[0]

    page_title = config.getH1PageTitle(url)
    question_tag = config.getCleanPageTitle(page_title)
    file_name = question_tag + ".csv"
    file_path = os.path.join(BASE_DIR, file_name)

    extract(url,HEADERS,file_path,question_tag,page_title)
    pass

def test_extractH2FromPage():

    url = config.urls[0]

    page_title = config.getH1PageTitle(url)
    question_tag = config.getCleanPageTitle(page_title)
    file_name = question_tag + ".csv"
    file_path = os.path.join(BASE_DIR, file_name)

    extractH2FromPage(url,HEADERS,file_path,question_tag,page_title)
    pass

def testGenerateCategory():
    file_path = os.path.join(BASE_DIR, "category.csv")
    title_list = ["a","b"]

    generateFAQCategory(title_list,file_path)
    pass

if __name__ == "__main__":
    test_extractH2FromPage()
    #extractAll()
    #extractOne()
    #testGenerateCategory()
    pass


