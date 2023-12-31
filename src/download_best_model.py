'''
Script to download a trained YOLO model that is available on our Google Drive.
'''

import os
import gdown

def download_from_drive(BEST_MODEL_PATH):
    print('Downloading trained YOLO model...')
    gdown.download(id = '1py_SFvJWV5BLYJuIa6CYFhxhby12LCly', output = BEST_MODEL_PATH)

def get_model():
    MODELS_DIR = str(os.getcwd()) + '/models'
    BEST_MODEL_PATH = MODELS_DIR + '/best.pt'

    if not os.path.exists(MODELS_DIR):
        os.makedirs(MODELS_DIR)
        download_from_drive(BEST_MODEL_PATH)

    if not os.path.exists(BEST_MODEL_PATH):
        download_from_drive(BEST_MODEL_PATH)
    return BEST_MODEL_PATH
