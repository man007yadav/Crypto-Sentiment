import json
from tqdm import tqdm

import pandas as pd
import datetime

import string
import re

import spacy
from spacy.language import Language
from spacy_langdetect import LanguageDetector
from spacytextblob.spacytextblob import SpacyTextBlob

import plotly.express as px


def get_lang_detector(nlp, name):
    return LanguageDetector()

nlp_sentiment = spacy.load('en_core_web_sm')
nlp_sentiment.add_pipe('spacytextblob')

nlp = spacy.load("en_core_web_sm")
Language.factory("language_detector", func=get_lang_detector)
nlp.add_pipe('language_detector', last=True)


def contains_word(sentence, word):
    return f' {word} ' in f' {sentence} '

def filter(text):
    if len(text) > 0 \
        and (contains_word(text.upper(), 'SHIB') or contains_word(text.upper(), 'DOGE')):
        return True
    return False

def get_filtered_msgs(data):

    filtered_msg = []
    for msg in tqdm(data['messages']):
        try:
            if type(msg['text']) is list:
                for i in range(len(msg['text'])):
                    if type(msg['text'][i]) is str:
                        if filter(msg['text'][i]):
                            msg['text'] = msg['text'][i]
                            filtered_msg.append(msg)
                        break
            elif type(msg['text']) is str:
                if filter(msg['text']):
                    filtered_msg.append(msg)
        except:
            print(msg['text'])

    return filtered_msg

def detect_english_text(text):
    doc = nlp(text)
    return doc._.language['language'] == 'en'

def preprocess_text(text):
    try:
        punctuationfree = "".join([i for i in text if i not in string.punctuation])
        punctuationfree = text
        punctuationfree = punctuationfree.lower()
        tokens = re.split('\W+',punctuationfree)
        return " ".join(tokens)
    except:
        print(text)

def get_text_polarity(text):
    doc = nlp_sentiment(text)
    return doc._.polarity


if __name__ == "__main__":

    with open("result.json") as f:
        data = json.load(f)
        print('Total messages : ' + str(len(data['messages'])))

    filtered_msgs = get_filtered_msgs(data)

    ids = []
    dates = []
    texts = []
    sentiment_polarity = []

    print('Preprocessing text...')
    for msg in tqdm(filtered_msgs):
        text = preprocess_text(msg['text'])
        if len(text) > 0 \
            and detect_english_text(text):
            ids.append(msg['id'])
            dates.append(datetime.datetime
                        .strptime(msg['date'], "%Y-%m-%dT%H:%M:%S")
                        .strftime("%Y-%m-%d"))
            texts.append(text)
            sentiment_polarity.append(get_text_polarity(text))

    print("Total count of preprocessed text : " + str(len(texts)))

    data_dict = {'id' : ids, 'date' : dates, 'text' : texts, 'sentiment' : sentiment_polarity}
    text_df = pd.DataFrame(data_dict)

    date_sentiment_df = text_df.groupby('date')['sentiment'].mean()
    date_sentiment_df = date_sentiment_df.reset_index()

    date_num_msg_df = text_df.groupby('date')['id'].count()
    date_num_msg_df = date_num_msg_df.reset_index()
    date_num_msg_df = date_num_msg_df.rename(columns = {'id' : 'num_msgs'})

    fig = px.line(date_num_msg_df, x='date', y='num_msgs', markers=True)
    fig.write_image("num_msgs.jpeg")

    fig = px.line(date_sentiment_df, x='date', y='sentiment', markers=True)
    fig.write_image("sentiment.jpeg")



