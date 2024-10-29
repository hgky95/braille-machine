import cv2
import numpy as np
import pytesseract
from gtts import gTTS
import os

def text_to_speech(english_text):
    //do something
    return audio;

def braille_to_text(braille_text):
    //do something    
    return english_text // this one can return english_text or english_text_path

def image_to_braille(image_path):
    //do something
    return braille_text // this one can return braille_text (string) or braille_text_path (.txt)

// This one is the final method
def image_to_speech(image_path):
    braille_text = image_to_braille(image_path)
    english_text = braille_to_text(braille_text)
    return text_to_speech(english_text)

// Testing:
image_path = "/home/scanned_image.png"
image_to_speech(image_path)

