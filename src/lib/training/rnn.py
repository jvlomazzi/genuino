import pickle
import pandas as pd 
import matplotlib.pyplot as plt 
import numpy as np 
import tensorflow as tf 
import re 
from tensorflow.keras.preprocessing.text import Tokenizer
import tensorflow as tf
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, precision_score, recall_score
import seaborn as sns 

plt.style.use('ggplot')

fake_df = pd.read_csv("src/lib/dataset/Fake.br/Fake.csv")
real_df = pd.read_csv("src/lib/dataset/Fake.br/True.csv")

fake_df.isnull().sum()
real_df.isnull().sum()
# fake_df.subject.unique()
# real_df.subject.unique()

fake_df.drop(['index', 'label'], axis=1, inplace=True)
real_df.drop(['index', 'label'], axis=1, inplace=True)

fake_df['class'] = 0 
real_df['class'] = 1


plt.figure(figsize=(10, 5))
plt.bar('Notícia Falsa', len(fake_df), color='red')
plt.bar('Notícia Real', len(real_df), color='blue')
plt.title('Arranjo de notícias Reais e Falsas', size=15)
plt.xlabel('Tipo', size=15)
plt.ylabel('Nº de artigos', size=15)


total_len = len(fake_df) + len(real_df)
plt.figure(figsize=(10, 5))
plt.bar('Notícia Falsa', len(fake_df) / total_len, color='red')
plt.bar('Notícia Real', len(real_df) / total_len, color='blue')
plt.title('Arranjo de notícias Reais e Falsas', size=15)
plt.xlabel('Tipo', size=15)
plt.ylabel('Proporção dos artigos', size=15)

print('Diferença entre os tipos:',  len(fake_df)-len(real_df))

news_df = pd.concat([fake_df, real_df], ignore_index=True, sort=False)

# news_df['text'] = news_df['title'] + news_df['text']
# news_df.drop('title', axis=1, inplace=True)

features = news_df['preprocessed_news']
targets = news_df['class']

X_train, X_test, y_train, y_test = train_test_split(features, targets, test_size=0.20, random_state=18)
stop_words = set(nltk.corpus.stopwords.words("portuguese"))
def normalize(data):
    normalized = []
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
        normalized.append(i)
    return normalized

X_train = normalize(X_train)
X_test = normalize(X_test)

max_vocab = 10000
tokenizer = Tokenizer(num_words=max_vocab)
tokenizer.fit_on_texts(X_train)

# tokenize the text into vectors 
X_train = tokenizer.texts_to_sequences(X_train)
X_test = tokenizer.texts_to_sequences(X_test)

X_train = tf.keras.preprocessing.sequence.pad_sequences(X_train, padding='post', maxlen=256)
X_test = tf.keras.preprocessing.sequence.pad_sequences(X_test, padding='post', maxlen=256)

# model = tf.keras.Sequential([
#     tf.keras.layers.Embedding(max_vocab, 32),
#     tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(64,  return_sequences=True)),
#     tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(16)),
#     tf.keras.layers.Dense(64, activation='relu'),
#     tf.keras.layers.Dropout(0.5),
#     tf.keras.layers.Dense(1)
# ])
model = tf.keras.Sequential()
model.add(tf.keras.layers.Embedding(input_dim=max_vocab, output_dim=64))
model.add(tf.keras.layers.GRU(256, return_sequences=True))
model.add(tf.keras.layers.SimpleRNN(128))
model.add(tf.keras.layers.Dense(64, activation='relu'))
model.add(tf.keras.layers.Dropout(0.5))
model.add(tf.keras.layers.Dense(1))
model.summary()

early_stop = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=2, restore_best_weights=True)
model.compile(loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
              optimizer=tf.keras.optimizers.Adam(1e-4),
              metrics=['accuracy'])

history = model.fit(X_train, y_train, epochs=10,validation_split=0.1, batch_size=30, shuffle=True, callbacks=[early_stop])
model.save('src/lib/model/rnn')
with open('src/lib/model/rnn/tokenizer.pickle', 'wb') as handle:
    pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)

history_dict = history.history

acc = history_dict['accuracy']
val_acc = history_dict['val_accuracy']
loss = history_dict['loss']
val_loss = history_dict['val_loss']
epochs = history.epoch

plt.figure(figsize=(12,9))
plt.plot(epochs, loss, 'r', label='Training loss')
plt.plot(epochs, val_loss, 'b', label='Validation loss')
plt.title('Training and validation loss', size=20)
plt.xlabel('Epochs', size=20)
plt.ylabel('Loss', size=20)
plt.legend(prop={'size': 20})
plt.show()

plt.figure(figsize=(12,9))
plt.plot(epochs, acc, 'g', label='Training acc')
plt.plot(epochs, val_acc, 'b', label='Validation acc')
plt.title('Training and validation accuracy', size=20)
plt.xlabel('Epochs', size=20)
plt.ylabel('Accuracy', size=20)
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

print('Accuracy on testing set:', accuracy_score(binary_predictions, y_test))
print('Precision on testing set:', precision_score(binary_predictions, y_test))
print('Recall on testing set:', recall_score(binary_predictions, y_test))

matrix = confusion_matrix(binary_predictions, y_test, normalize='all')
plt.figure(figsize=(16, 10))
ax= plt.subplot()
sns.heatmap(matrix, annot=True, ax = ax)

# labels, title and ticks
ax.set_xlabel('Indicadores previstos', size=20)
ax.set_ylabel('Indicadores reais', size=20)
ax.set_title('Matriz de Confusão', size=20) 
ax.xaxis.set_ticklabels(['Falso', 'Real'], size=15)
ax.yaxis.set_ticklabels(['Falso', 'Real'], size=15)
plt.show()

e = model.layers[0]
weights = e.get_weights()[0]
print(weights.shape) # shape: (vocab_size, embedding_dim)

word_index = list(tokenizer.word_index.keys())
word_index = word_index[:max_vocab-1]


# import io

# out_v = io.open('Fake.br/fakenews_vecs.tsv', 'w', encoding='utf-8')
# out_m = io.open('Fake.br/fakenews_meta.tsv', 'w', encoding='utf-8')

# for num, word in enumerate(word_index):
#   vec = weights[num+1] # skip 0, it's padding.
#   out_m.write(word + "\n")
#   out_v.write('\t'.join([str(x) for x in vec]) + "\n")
# out_v.close()
# out_m.close()