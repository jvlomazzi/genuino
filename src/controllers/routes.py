import json, sys
# from load import Load
from newsfetch.news import newspaper
# from tensorflow.keras.models import load_model
# import tensorflow as tf

if not sys.stdin.isatty():
    # def load():
    #     load = Load()
    #     return load.model('lstm')

    def chat_response():
        sys.stdout.write(variavel)

    # def prediction():
    #     news = []
    #     text = newspaper(sys.argv[2])
    #     news.append(text.article)
    #     news = lstm['tokenizer'].texts_to_sequences(news)
    #     news = tf.keras.preprocessing.sequence.pad_sequences(news, padding='post', maxlen=256)
    #     pred = lstm['model'].predict(news)
    #     sys.stdout.write('fake' if pred < 1 else 'true')

    def mongodb():
        sys.stdout.write("mongodb")

    def default():
        sys.stdout.write("Nao foi possivel continuar a solicitacao")

    for line in sys.stdin:
        if line.rstrip() == 'initialize':
            print('Iniciando o carregamento dos arquivos')
            variavel = "teste apenas vamos verificar"
            # lstm = load()
            sys.stdout.write("O servidor carregou os modelos de predicao.")
        else:
            {
                'chat': chat_response,
                # 'url': prediction,
                # 'image': prediction,
                'feedback': mongodb
            }.get(line.rstrip(), default)()
else:
    sys.stdout.write("Servidor finalizou o request.")

