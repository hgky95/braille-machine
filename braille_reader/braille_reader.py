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

def braille_to_text(braille_string):
    # Translate each Braille character to English text
    return ''.join(braille_to_english.get(char, '?') for char in braille_string)


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



# Mapping of Braille characters to English alphabet (Grade 1 Braille)
braille_to_english = {
    "⠁": "a", "⠃": "b", "⠉": "c", "⠙": "d", "⠑": "e",
    "⠋": "f", "⠛": "g", "⠓": "h", "⠊": "i", "⠚": "j",
    "⠅": "k", "⠇": "l", "⠍": "m", "⠝": "n", "⠕": "o",
    "⠏": "p", "⠟": "q", "⠗": "r", "⠎": "s", "⠞": "t",
    "⠥": "u", "⠧": "v", "⠺": "w", "⠭": "x", "⠽": "y", "⠵": "z",
    "⠼": "#", # Number sign in Braille
    "⠴": " ", # Space in Braille
    # Add more Braille symbols as needed
}


# Testing:
# Specify the path to your text file to be converted into speech
file_path = "../input/a.txt"

# Read the file into a single string
with open(file_path, 'r', encoding='utf-8') as file:
    text = file.read()

print("Input Text for Speech conversion" + text)
text_to_speech(text)

image_path = "../images/Braille_P.jpg"
braille_text = "⠓⠑⠇⠇⠕"
print("Braille:", braille_text)
braille_to_eng_translated_text = braille_to_text(braille_text)
print("Braille text Translated to English:", braille_to_eng_translated_text)

# Specify the path to your text file
file_path = '../output/Braille_to_txt_output.txt'

# Write the text to the file
with open(file_path, 'w', encoding='utf-8') as file:
    file.write(braille_to_eng_translated_text)

print("Text has been saved to", file_path)

english_text_from_img = image_to_braille_text_conversion(image_path)
print("Braille image to English converted Text: " + english_text_from_img)






