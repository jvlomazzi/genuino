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
        print('fake' if pred < 1 else 'true')

    def mongodb():
        print("mongodb")

    def default():
        print("Nao foi possivel continuar a solicitacao")

    for line in sys.stdin:
        data = json.loads(line)
        if data["type"] == 'start':
            lstm = load()
            print("Modelo carregado")
        else:
            {
                'chat': chat_response,
                'url': prediction,
                'image': prediction,
                'feedback': mongodb
            }.get(data["type"], default)()
else:
    print("Servidor finalizou o request.")
