import json, sys
from load import Load
from newsfetch.news import newspaper
from tensorflow.keras.models import load_model
import tensorflow as tf

lstm = []

if not sys.stdin.isatty():
    def load():
        load = Load()
        return load.model('lstm')

    def chat_response():
        print("chat")

    def prediction():
        news = []
        text = newspaper(sys.argv[2])
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
        if line.rstrip() == 'initialize':
            lstm = load()
            print("O servidor carregou os modelos de predicao.")
        else:
            {
                'chat': chat_response,
                'url': prediction,
                'image': prediction,
                'feedback': mongodb
            }.get(line.rstrip(), default)()
else:
    print("Servidor finalizou o request.")

# import json, sys

# if not sys.stdin.isatty():

#     def chat_response():
#         print(variavel)

#     def default():
#         print("Nao foi possivel continuar a solicitacao")

#     # print(sys.stdin)
#     for line in sys.stdin:
#         data = json.loads(line)
#         print(data[:1])
#         if line.rstrip() == 'initialize':
#             variavel = "\nteste apenas vamos verificar"
#             print("O servidor carregou os modelos de predicao.")

#         else:
#             print("finalizou")
# else:
#     print("Servidor finalizou o request.")

