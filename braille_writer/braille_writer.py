import braille
import speech_recognition as sr

BRAILLE_TEXT_OUTPUT_PATH = "output/english_to_braille_text.txt"
ENGLISH_TEXT_OUTPUT_PATH = "output/speech_to_english.txt"


def speech_to_braille(audio_path):
    """
        Convert the audio (speech) to braille text and store in the .txt file
        :param
            audio_path: audio file path (e.g: mp3 file)
    """
    text_file = speech_to_text(audio_path)
    text_to_braille(text_file)


def speech_to_text(audio_path):
    """
        Converting speech to English text
        :param
            audio_path: audio file path (e.g: wav)
        :return
            str: a .txt file path with English text
    """
    recognizer = sr.Recognizer()
    output_path = ENGLISH_TEXT_OUTPUT_PATH

    # Handle the audio recording and convert it into text.
    with sr.AudioFile(audio_path) as source:
        audio = recognizer.record(source)
        try:
            text_output = recognizer.recognize_google(audio)
            write_to_file(text_output, output_path)
        # Error Handling - 1
        except sr.UnknownValueError:
            print("Not able to identify audio.")
        # Error Handling - 2
        except sr.RequestError:
            print("Speech recognition service error")

    return output_path


def text_to_braille(file_path: str):
    """
        Convert English texts from a .txt file to braille text and store it in .txt file
        :param
            file_path: a .txt file with English texts
        :return:
            str: a .txt file path with braille text
    """
    content = read_text_file(file_path)
    braille_text = braille.textToBraille(content)
    write_to_file(braille_text, BRAILLE_TEXT_OUTPUT_PATH)
    return BRAILLE_TEXT_OUTPUT_PATH


def read_text_file(file_path):
    """
        Read text from file path
        :param
            file_path: text file path
        :return
            str: a content from this file
    """
    try:
        with open(file_path, 'r', encoding="utf-8") as file:
            content = file.read()
            return content
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return None
    except IOError:
        print(f"Error: Facing error when read file at {file_path}")
        return None


def write_to_file(content, filename=BRAILLE_TEXT_OUTPUT_PATH):
    """
        Write content to file
        :param
            content: text content
            filename: output file name
    """
    try:
        with open(filename, 'w', encoding="utf-8") as file:
            file.write(content)
        print(f"Content successfully written to {filename}")
    except IOError:
        print(f"An error occurred while writing to {filename}")
