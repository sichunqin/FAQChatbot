from flask import Flask
from flask import render_template, jsonify, request
from faqengine import *
import random
import os
from os import path

BASE_DIR = path.dirname(__file__)

FAQs_DATA_FOLDER = path.join(BASE_DIR, "data")
DATABASE_FOLDER = path.join(BASE_DIR, "database")

app = Flask(__name__)
app.secret_key = '12345'

faqs_list = [path.join(FAQs_DATA_FOLDER, "greetings.csv")]

for root, directories, filenames in os.walk(DATABASE_FOLDER):
    for filename in filenames:
        file_path = os.path.join(root, filename)
        if file_path.endswith('.csv'):
            faqs_list.append(file_path)

# ToDo: need to debug for 'gensim', 'bert' whereas 'spacy' (only pretrained), 'tfidf' seem ok.
faqs_engine = FaqEngine(faqs_list, "tfidf")


def get_response(user_message):
    return faqs_engine.query(user_message)


@app.route('/')
def hello_world():
    return render_template('home.html')


@app.route('/chat', methods=["POST"])
def chat():
    try:
        user_message = request.form["text"]
        response_text = get_response(user_message)
        return jsonify({"status": "success", "response": response_text})
    except Exception as e:
        print(e)
        return jsonify({"status": "success", "response": "Sorry I am not trained to do that yet..."})


if __name__ == "__main__":
    app.run(port=8080)
