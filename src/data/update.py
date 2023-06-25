import secret
import requests
from bs4 import BeautifulSoup
import os
import re
import pandas as pd
from urllib.parse import urlsplit
from urllib.parse import urljoin
import extract

BASE_DIR = os.path.join(os.path.dirname(__file__), '../database/')
BASE_URL = 'https://confluence.amlogic.com'
HEADERS = {
    'Authorization': 'Bearer ' + secret.token,
    'Content-Type': 'application/json'
}

def get_pages(tag="security-chatbot"):
    # Define the tag to search for
    #tag = 'security-chatbot'

    # Search for pages with the tag
    url = f'{BASE_URL}/rest/api/content/search?cql=label="{tag}"&limit=100'

    response = requests.get(url, headers=HEADERS)
    data = response.json()

    # Extract the page IDs and titles
    pages = []
    for result in data['results']:
        page_id = result['id']
        page_title = result['title']
        webui = result['_links']['webui']
        page_url = BASE_URL + webui
        pages.append((page_id, page_title,page_url))

    return pages

def get_no_toc_title_list():
    title_list = []
    pages = get_pages("security-chatbot-no-toc")
    for page_id, page_title,page_url in pages:
        title_list.append(page_title)

    return title_list

def update():

    print('=== Updating START ===')
    pages = get_pages()

    no_toc_list = get_no_toc_title_list()
    title_list = []
    print('GET ' + str(len(pages)) + ' FAQs with TAG "security-chatbot"!')
    for page_id, page_title,page_url in pages:

        file_name = page_title.replace(" ", '') + ".csv"
        file_path = os.path.join(BASE_DIR, file_name)
        question_tag = page_title.replace(' ', '').replace("#", '')

        print(file_name)
        print(file_path)
        print(page_url)
        if page_title not in no_toc_list:
            title_list.append(page_title)
            extract.extract(page_url, HEADERS, file_path, question_tag, page_title)

    catagory_file_path = os.path.join(BASE_DIR, "category.csv")

    extract.generateFAQCategory(title_list,catagory_file_path)
    print('=== Updated ' + str(len(pages)) + ' FAQs ===')
    print('=== Updating DONE ===')


if __name__ == "__main__":
    update()
    pass
