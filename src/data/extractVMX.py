headers = {
    'Authorization': 'Bearer NjIzMzg1ODk0NTIzOobFjkSTjwAQe4vM388UZqE9sPS2',
    'Content-Type': 'application/json'
}

import requests
url = 'https://confluence.amlogic.com/display/SW/VMX+CAS+FAQ'
response = requests.get(url, headers=headers)

from bs4 import BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

questions = soup.find_all('h2', {'id': lambda x: x and 'VMXCASFAQ' in x})
cleanQuesions = []
cleanAnswers = []
for question in questions:
    cleanQuesions.append(question.text)
    # print(question.text)

answers = soup.find_all('div', {'class': lambda x: x and 'panelContent' == x})

for answer in answers:
    cleanAnswers.append(answer.encode_contents().strip().decode('utf-8'))
    # cleanAnswers.append(answer.text.strip())

import pandas as pd

df = pd.DataFrame({'Question': cleanQuesions, 'Answer': cleanAnswers,'Class': "vmx" })
print(df)
df.to_csv('src/data/vcas.csv', sep='|',quotechar='\'',index=False)





