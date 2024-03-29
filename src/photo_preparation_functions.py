"""
This file contains functions that are used to process the input photos.
The cards need to be cropped so they can then be placed on a background
in the second step.
This is done be detecting the outer edges of a card, filling the inner area,
which leaves us with a mask we can use to distinguish card and background.
The images are saved in a separate folder for further use.
"""

import cv2 as cv
from pathlib import Path
import os
import numpy as np
from tqdm import tqdm


def find_edges(img):
    """
    Return image containing the detected edges of the input image.
    """
    grayscale = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    blurred_img = cv.GaussianBlur(grayscale.copy(), (3, 3), 0)
    edged_img = cv.Canny(blurred_img, 50, 100)
    return edged_img


def create_mask(img):
    """
    Return mask for detected playing card on photo.
    """
    edged_img = find_edges(img)
    contours, _ = cv.findContours(edged_img.copy(), cv.RETR_LIST, cv.CHAIN_APPROX_NONE)
    filled_card = cv.fillPoly(
        edged_img.copy(), [max(contours, key=cv.contourArea)], color=(255, 255, 255)
    )
    _, mask = cv.threshold(filled_card, thresh=180, maxval=255, type=cv.THRESH_BINARY)
    kernel = np.ones((5, 5), np.uint8)
    eroded_mask = cv.erode(
        mask, kernel
    )  # erode mask to remove single white pixels in background
    return eroded_mask


def crop_image(img):
    """
    Return cropped playing card.
    """
    height, width, _ = img.shape
    img = cv.resize(img, (int(width / 4), int(height / 4)))
    mask = create_mask(img)
    img = cv.bitwise_and(img, img, mask=mask)  # keep card, make background black
    x, y, w, h = cv.boundingRect(mask)
    cropped_img = img[
        y - 5 : y + h + 5, x - 5 : x + w + 5
    ]  # add 5 pixels to each edge, to ensure the whole card is still in the image
    return cropped_img


def save_image(input_photo_path: str, output_folder: str, card) -> None:
    """
    Saves the processed photo to the output folder.
    """
    photo_name_without_extension = input_photo_path.split("/")[-1].split(".")[0]
    cv.imwrite(output_folder + "/" + photo_name_without_extension + ".jpg", card)


def create_playing_card_dir(photo_DIR: str) -> str:
    """
    Creates the folder to save images if it does not exist yet. Returns the directory it created.
    """
    PLAYING_CARDS_DIR = photo_DIR + "_processed"
    if not os.path.exists(PLAYING_CARDS_DIR):
        os.makedirs(PLAYING_CARDS_DIR)
    return PLAYING_CARDS_DIR


def process_photos(PHOTOS_DIR: str) -> str:
    """
    Processes input photos for the train-image generation. Returns the directory of the saved processed images.
    """
    PLAYING_CARDS_DIR = create_playing_card_dir(PHOTOS_DIR)
    photo_paths = [str(path) for path in Path(PHOTOS_DIR).glob("*")]
    print(f"Processing {len(photo_paths)} input photos...")
    for photo_path in tqdm(photo_paths):
        photo = cv.imread(photo_path)
        card = crop_image(photo)
        save_image(photo_path, PLAYING_CARDS_DIR, card)
    print(f'Finished processing. Playing cards saved at: "{PLAYING_CARDS_DIR}"!')
    return PLAYING_CARDS_DIR
