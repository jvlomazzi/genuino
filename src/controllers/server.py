import json, sys
from load import Load
from newsfetch.news import newspaper
from tensorflow.keras.models import load_model
import tensorflow as tf
import asyncio
import time

if not sys.stdin.isatty():
    def load():
        load = Load()
        return load.model('lstm')

    def chat_response():
        print('chat')

    def prediction():
        news = []
        text = newspaper(data["data"])
        news.append(text.article)
        news = lstm['tokenizer'].texts_to_sequences(news)
        news = tf.keras.preprocessing.sequence.pad_sequences(news, padding='post', maxlen=256)
        pred = lstm['model'].predict(news)
        print('fake' if pred < 0 else 'true')

    def image_prediction():
        print("imagem")

    def default():
        print("Nao foi possivel continuar a solicitacao")

    for line in sys.stdin:
        data = json.loads(line)
        if data["type"] == 'start':
            lstm = load()
            print("started")
        else:
            {
                'chat': chat_response,
                'url': prediction,
                'image': image_prediction
            }.get(data["type"], default)()
else:
    print("Servidor finalizou o request.")
