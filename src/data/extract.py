import config
import requests
from bs4 import BeautifulSoup
import os
import pandas as pd


def extract(url, headers, output_file_path, question_tag):
    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.text, 'html.parser')

    questions = soup.find_all('h2', {'id': lambda x: x and question_tag in x})
    cleanQuesions = []
    cleanAnswers = []
    for question in questions:
        cleanQuesions.append(question.text)
        # print(question.text)

    answers = soup.find_all('div', {'class': lambda x: x and 'panelContent' == x})

    for answer in answers:
        cleanAnswers.append(answer.encode_contents().strip().decode('utf-8'))
        # cleanAnswers.append(answer.text.strip())

    sz = min(len(cleanQuesions), len(cleanAnswers))

    df = pd.DataFrame({'Question': cleanQuesions[:sz], 'Answer': cleanAnswers[:sz],'Class': question_tag })
    print(df)
    # output_file_path = os.path.join("src/data", output_file_name)

    df.to_csv(output_file_path, sep='|',quotechar='\'',index=False)


if __name__ == "__main__":
    for file in config.urls:
        file_path = os.path.join("src/data", file["file_name"])
        extract(file["url"],config.headers,file_path,file["question_tag"])
        pass
    pass


