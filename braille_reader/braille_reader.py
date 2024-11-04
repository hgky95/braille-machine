import cv2
import numpy as np
import pytesseract
from gtts import gTTS
import os

def text_to_speech(english_text):
    # Text to be converted to speech
    text = english_text
    
    # Language in which you want to convert
    language = 'en'
    
    # Creating the gTTS object
    tts = gTTS(text=text, lang=language, slow=False)
    
    # Saving the converted audio to a file
    tts.save("output/output.mp3")

def image_to_braille_text_conversion(image_path):
    ## image_path = r'C:\Users\neelr\Desktop\Parita Study Work\HCI\A2\download.jpeg'
    
    image = cv2.imread(image_path,1)
    # Convert to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply thresholding
    _, thresh_image = cv2.threshold(gray_image, 150, 255, cv2.THRESH_BINARY_INV)

    # Read the path of pytesseract.pytesseract.tesseract_cmd from local
    import shutil
    # Use shutil to automatically find the Tesseract executable path
    tesseract_path = shutil.which("tesseract")
    if tesseract_path is None:
        print("pytesseract.pytesseract.tesseract_cmd path is not readable, Hence provide the local path manually.")
        pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
        
    custom_config = r'--oem 3 --psm 6'
    text = pytesseract.image_to_string(thresh_image, config=custom_config)

    print("Extracted Text:", text)
    
    content = text
    # Specify the file name
    file_name = r'output/braille_reader_output.txt'
    
    with open(file_name, 'w') as file:
        file.write(content)
    
    print(f"Content saved to {file_name}")
    return text

## This one is the final method
def image_to_speech(image_path):
    english_text = image_to_braille_text_conversion(image_path)
    # english_text = braille_to_text(braille_text)
    return text_to_speech(english_text)

## Testing:
image_path = "/images/braille input image.jpeg"
image_to_speech(image_path)

