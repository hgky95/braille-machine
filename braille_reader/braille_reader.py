from gtts import gTTS
import braille_maryna

braille_characters = ['⠴', '⠂', '⠆', '⠒', '⠲', '⠢', '⠖', '⠶', '⠦', '⠔',
                      '⠁', '⠃', '⠉', '⠙', '⠑', '⠋', '⠛', '⠓', '⠊', '⠚',
                      '⠅', '⠇', '⠍', '⠝', '⠕', '⠏', '⠟', '⠗', '⠎', '⠞',
                      '⠥', '⠧', '⠺', '⠭', '⠽', '⠵',
                      '⠱', '⠰', '⠣', '⠿', '⠀', '⠮', '⠐', '⠼', '⠫', '⠩',
                      '⠯', '⠄', '⠷', '⠾', '⠡', '⠬', '⠠', '⠤', '⠨', '⠌',
                      '⠜', '⠹', '⠈', '⠪', '⠳', '⠻', '⠘', '⠸']

english_characters = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                      'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
                      'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                      'u', 'v', 'w', 'x', 'y', 'z',
                      ':', ';', '<', '=', ' ', '!', '"', '#', '$', '%',
                      '&', '', '(', ')', '*', '+', ',', '-', '.', '/',
                      '>', '?', '@', '[', '\\', ']', '^', '_', ' ']

SPEECH_FILE_PATH = "output/english_to_speech.mp3"
BRAILLE_TO_ENGLISH_FILE_PATH = "output/braille_text_to_english.txt"
BRAILLE_IMAGE_TO_BRAILLE_TEXT_FILE_PATH = "output/braille_image_to_braille_text.txt"


def text_to_speech(english_text):
    """
        Convert english text to speech and save it to audio file (e.g: wav)
        :param
            english_text: english text
    """
    language = 'en'
    tts = gTTS(text=english_text, lang=language, slow=False)
    tts.save(SPEECH_FILE_PATH)
    print("Saved speech to ", SPEECH_FILE_PATH)
    return SPEECH_FILE_PATH


def braille_text_to_english(braille_text):
    """
        Convert the braille text to english text and save it to text file
        :param
            braille_text: braille text
        :return
             str: a .txt file with english text
    """
    english_text = ''.join(
        [english_characters[braille_characters.index(fi)] if fi in braille_characters else ' ' for fi in braille_text])
    try:
        with open(BRAILLE_TO_ENGLISH_FILE_PATH, 'w') as file:
            file.write(english_text)
        print(f"Content successfully written to {BRAILLE_TO_ENGLISH_FILE_PATH}")
    except IOError:
        print(f"An error occurred while writing to {BRAILLE_TO_ENGLISH_FILE_PATH}")
    return english_text


def braille_image_to_braille_text(image_path):
    """
        Convert Braille image to braille text and save it to text file
        :param
            image_path: a path of Braille image
        :return:
            str: braille text
    """
    braille_text = braille_maryna.braille_image_to_braille_text(image_path)
    try:
        with open(BRAILLE_IMAGE_TO_BRAILLE_TEXT_FILE_PATH, 'w') as file:
            file.write(braille_text)
        print(f"Content successfully written to {BRAILLE_IMAGE_TO_BRAILLE_TEXT_FILE_PATH}")
    except IOError:
        print(f"An error occurred while writing to {BRAILLE_IMAGE_TO_BRAILLE_TEXT_FILE_PATH}")
    return braille_text


def image_to_speech(image_path):
    """
        Convert Braille image to speech and save it to audio file
        :param
            image_path: a path of Braille image
        :return:
            str: audio (speech) path
    """
    braille_text = braille_image_to_braille_text(image_path)
    english_text = braille_text_to_english(braille_text)
    audio_path = text_to_speech(english_text)
    return audio_path
