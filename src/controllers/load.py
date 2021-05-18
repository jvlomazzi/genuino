import os
import pickle
from tensorflow.keras.models import load_model

class Load:
    path = 'src/lib/model'
    neural_networks = []

    def __init__(self):
        self.get_networks()
        self.tokenizers(0)
        self.models(0)

    # 
    def get_networks(self):
        for x in os.walk(self.path):
            folder = x[0].replace(self.path+"\\", "")
            obj = {
                'name': folder,
                'model': '',
                'tokenizer': ''
            }
            if folder.find("\\")  == -1 and folder != self.path: self.neural_networks.append(obj)
    
    def tokenizers(self, index):
        if(index < len(self.neural_networks)):
            with open(self.path + self.neural_networks[index]['name'] +'/tokenizer.pickle', 'rb') as handle:
                self.neural_networks[index]['tokenizer'] = pickle.load(handle)
        else:
            return 1;

    def models(self, index):
        if(index < len(self.neural_networks)):
            self.neural_networks[index]['model'] = load_model(self.path + self.neural_networks[index]['name'])
            return self.models(index+1)
        else:
            return 1;