from PIL import Image
# from answers import POSITIVE, NEGATIVE
import pytesseract
class News:
    def __init__(self, news):
        self.data_processing(news)
    
    def data_processing(news):
        