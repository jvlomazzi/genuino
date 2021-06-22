import pickle
import pandas as pd 
import matplotlib.pyplot as plt
import tensorflow as tf 
import re 
from tensorflow.keras.preprocessing.text import Tokenizer
import tensorflow as tf
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, precision_score, recall_score
import seaborn as sns 

plt.style.use('ggplot')

noticias_falsas = pd.read_csv("src/lib/dataset/Fake.br/Fake.csv")
noticias_reais = pd.read_csv("src/lib/dataset/Fake.br/True.csv")

noticias_falsas.drop(['index', 'label'], axis=1, inplace=True)
noticias_reais.drop(['index', 'label'], axis=1, inplace=True)

noticias_falsas['class'] = 0 
noticias_reais['class'] = 1


plt.figure(figsize=(10, 5))
plt.bar('Notícia Falsa', len(noticias_falsas), color='red')
plt.bar('Notícia Real', len(noticias_reais), color='blue')
plt.title('Arranjo de notícias Reais e Falsas', size=15)
plt.xlabel('Tipo', size=15)
plt.ylabel('Nº de artigos', size=15)


total_len = len(noticias_falsas) + len(noticias_reais)
plt.figure(figsize=(10, 5))
plt.bar('Notícia Falsa', len(noticias_falsas) / total_len, color='red')
plt.bar('Notícia Real', len(noticias_reais) / total_len, color='blue')
plt.title('Arranjo de notícias Reais e Falsas', size=15)
plt.xlabel('Tipo', size=15)
plt.ylabel('Proporção dos artigos', size=15)

print('Diferença entre os tipos:',  len(noticias_falsas)-len(noticias_reais))

news_df = pd.concat([noticias_falsas, noticias_reais], ignore_index=True, sort=False)


conteudo = news_df['preprocessed_news']
classe_alvo = news_df['class']

X_train, X_test, y_train, y_test = train_test_split(conteudo, classe_alvo, test_size=0.20, random_state=18)

def normalizar(data):
    normalizada = []
    for i in data:
        i = i.lower()
        # get rid of urls
        i = re.sub('https?://\S+|www\.\S+', '', i)
        # get rid of non words and extra spaces
        i = re.sub('\\W', ' ', i)
        i = re.sub('\n', '', i)
        i = re.sub(' +', ' ', i)
        i = re.sub('^ ', '', i)
        i = re.sub(' $', '', i)
        normalizada.append(i)
    return normalizada

X_train = normalizar(X_train)
X_test = normalizar(X_test)

max_vocab = 10000
tokenizer = Tokenizer(num_words=max_vocab)
tokenizer.fit_on_texts(X_train)

X_train = tokenizer.texts_to_sequences(X_train)
X_test = tokenizer.texts_to_sequences(X_test)
X_train = tf.keras.preprocessing.sequence.pad_sequences(X_train, padding='post', maxlen=256)
X_test = tf.keras.preprocessing.sequence.pad_sequences(X_test, padding='post', maxlen=256)

model = tf.keras.Sequential([
    tf.keras.layers.Embedding(max_vocab, 32),
    tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(64,  return_sequences=True)),
    tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(32)),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dropout(0.5),
    tf.keras.layers.Dense(1)
])

model.summary()

early_stop = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=2, restore_best_weights=True)
model.compile(loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
              optimizer=tf.keras.optimizers.Adam(1e-4),
              metrics=['accuracy'])


history = model.fit(X_train, y_train, epochs=10,validation_split=0.1, batch_size=30, shuffle=True, callbacks=[early_stop])

model.save('src/lib/model/lstm')
with open('src/lib/model/lstm/tokenizer.pickle', 'wb') as handle:
    pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)

history_dict = history.history

acc = history_dict['accuracy']
val_acc = history_dict['val_accuracy']
loss = history_dict['loss']
val_loss = history_dict['val_loss']
epochs = history.epoch

plt.figure(figsize=(12,9))
plt.plot(epochs, loss, 'r', label='Loss no treinamento')
plt.plot(epochs, val_loss, 'b', label='Loss na validação')
plt.title('Loss de validação e treinamento', size=20)
plt.xlabel('Épocas', size=20)
plt.ylabel('Loss', size=20)
plt.legend(prop={'size': 20})
plt.show()

plt.figure(figsize=(12,9))
plt.plot(epochs, acc, 'g', label='Acurácia de Treinamento')
plt.plot(epochs, val_acc, 'b', label='Acurácia de validação')
plt.title('Acurácia do modelo', size=20)
plt.xlabel('Épocas', size=20)
plt.ylabel('Acurácia', size=20)
plt.legend(prop={'size': 20})
plt.ylim((0.5,1))
plt.show()

model.evaluate(X_test, y_test)
pred = model.predict(X_test)
binary_predictions = []

for i in pred:
    if i >= 0.5:
        binary_predictions.append(1)
    else:
        binary_predictions.append(0)

print(len(X_test))
print(len(y_test))
print('Acurácia (testes):', accuracy_score(binary_predictions, y_test))
print('Precisão (testes):', precision_score(binary_predictions, y_test))

matrix = confusion_matrix(binary_predictions, y_test, normalizar='all')
plt.figure(figsize=(16, 10))
ax = plt.subplot()
sns.heatmap(matrix, annot=True, ax = ax)

ax.set_xlabel('Indicadores previstos', size=20)
ax.set_ylabel('Indicadores reais', size=20)
ax.set_title('Matriz de Confusão', size=20) 
ax.xaxis.set_ticklabels(['Falso', 'Real'], size=15)
ax.yaxis.set_ticklabels(['Falso', 'Real'], size=15)
plt.show()

e = model.layers[0]
weights = e.get_weights()[0]
word_index = list(tokenizer.word_index.keys())
word_index = word_index[:max_vocab-1]