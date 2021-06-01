import os
import pickle
from tensorflow.keras.models import load_model
import tensorflow as tf

class Load:
    path = './lib/model/' #'genuino/src/lib/model/'
    neural_networks = []

    def __init__(self):
        self.set_networks()
        self.set_tokenizers(0)
        self.set_models(0)
    
    def create_pickle(self, model):
        with open(self.pickle_path + 'prediction_model.pickle', 'wb') as handle:
            pickle.dump(model, handle, protocol=pickle.HIGHEST_PROTOCOL)

    def set_networks(self):
        for x in os.walk(self.path):
            folder = x[0].replace(self.path+"\\", "")
            name = x[0].replace(self.path, "")
            obj = {
                'name': name,
                'folder': folder,
                'model': '',
                'tokenizer': ''
            }
            if folder.find("\\") == -1 and folder != self.path: self.neural_networks.append(obj)
    
    def set_tokenizers(self, index):
        if(index < len(self.neural_networks)):
            with open(self.neural_networks[index]['folder'] +'/tokenizer.pickle', 'rb') as handle:
                self.neural_networks[index]['tokenizer'] = pickle.load(handle)
            return self.set_tokenizers(index+1)
        else:
            return 1

    def set_models(self, index):
        if(index < len(self.neural_networks)):
            self.neural_networks[index]['model'] = load_model(self.neural_networks[index]['folder'])
            return self.set_models(index+1)
        else:
            return 1
    
    def model(self, model):
        for x in self.neural_networks:
            if(x['name'] == model):
                return x

load = Load()
