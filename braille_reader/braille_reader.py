import cv2
import numpy as np
#import pytesseract
from gtts import gTTS
import os
import img_to_braille_txt


def text_to_speech(english_text):
    # Text to be converted to speech
    text = english_text

    # Language in which you want to convert
    language = 'en'

    # Creating the gTTS object
    tts = gTTS(text=text, lang=language, slow=False)

    # Saving the converted audio to a file
    tts.save("../output/output.mp3")


def image_to_braille_text_conversion(image_path):
    encoding = img_to_braille_txt.process_image(image_path)
    # print("encoding of character:", encoding)
    text = img_to_braille_txt.braille_map[encoding]
    print("converted text:", img_to_braille_txt.braille_map[encoding])
    return text


# This one is the final method
def image_to_speech(english_text):
    text_to_speech(english_text)
    print("Audio file successfully save at ../output/output.mp3")


# Testing:
image_path = "../images/Braille_P.jpg"
english_text_from_img = image_to_braille_text_conversion(image_path)
english_text_ext = "Hello There!"
image_to_speech(english_text_from_img)
