import cv2 as cv
from pathlib import Path
import os
import numpy as np



def find_edges(img):
    grayscale = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    blurred_img = cv.GaussianBlur(grayscale.copy(),(3,3),0)
    edged_img = cv.Canny(blurred_img,50,100)
    return edged_img

def create_mask(img):
    edged_img = find_edges(img)
    contours,_ = cv.findContours(edged_img.copy(),cv.RETR_LIST,cv.CHAIN_APPROX_NONE)
    filled_card = cv.fillPoly(edged_img.copy(), [max(contours, key = cv.contourArea)], color = (255, 255, 255))
    _, mask = cv.threshold(filled_card, thresh= 180, maxval = 255, type = cv.THRESH_BINARY)
    kernel = np.ones((5,5), np.uint8)
    eroded_mask = cv.erode(mask, kernel)
    return eroded_mask


def crop_image(img):
    img = cv.resize(img, (500, 600))
    mask = create_mask(img)
    img = cv.bitwise_and(img, img, mask = mask)
    x, y, w, h = cv.boundingRect(mask)    
    cropped_img = img[y-5:y+h+5, x-5:x+w+5]

    
    return cropped_img


def save_image(input_photo_path, output_folder, card):
    photo_name_without_extension = input_photo_path.split('/')[-1].split('.')[0]
    cv.imwrite(output_folder + '/' +  photo_name_without_extension + '.jpg', card)


def create_playing_card_dir(photo_DIR):
    PLAYING_CARDS_DIR = photo_DIR + '_processed'
    if not os.path.exists(PLAYING_CARDS_DIR):
        os.makedirs(PLAYING_CARDS_DIR)
    return PLAYING_CARDS_DIR


def process_photos(PHOTOS_DIR):
    PLAYING_CARDS_DIR = create_playing_card_dir(PHOTOS_DIR)
    photo_paths = [str(path) for path in Path(PHOTOS_DIR).glob('*')]

    for photo_path in photo_paths:
            photo = cv.imread(photo_path)
            card = crop_image(photo)
            save_image(photo_path, PLAYING_CARDS_DIR, card)

    print(f'Processed cards saved at: ' + PLAYING_CARDS_DIR)
    return PLAYING_CARDS_DIR



if __name__ == '__main__':
    # input parameters
    PHOTOS_DIR = '/home/moiki/Documents/Files/studies/4_Semester/ADL/ADL_W23/data/sg_card_photos'

    # do processing
    PLAYING_CARD_DIR = process_photos(PHOTOS_DIR)
    



    