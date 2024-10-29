import braille
import speech_recognition as sr

def speech_to_braille(audio_path):
    """
        Convert the audio to braille format
        :param
            audio_path: audio file path (e.g: mp3 file)
        :return
             str: a .txt file with braille text
    """
    text_file = speech_to_text(audio_path)
    text_to_braille(text_file)
    return


def speech_to_text(audio_path):
    """
        Converting speech to English text
        :param
            audio_path: audio file path (e.g: mp3)
        :return
            str: a .txt file with English text
    """
    recognizer = sr.Recognizer()
    text_file = "speech.txt"
    # Handle the audio recording and convert it into text.
    with sr.AudioFile(audio_path) as source:
        audio = recognizer.record(source)
        try:
            text_output = recognizer.recognize_google(audio)
            with open(text_file, "w") as file:
                # Save the transcribed text to a .txt file
                file.write(text_output)
            print("Transcription successful. Check speech.txt for the text.")
        # Error Handling - 1
        except sr.UnknownValueError:
            print("Not able to identify audio.")
        # Error Handling - 2
        except sr.RequestError:
            print("Speech recognition service error")

    return text_file


def read_text_file(file_path):
    """
        Read text from file path
        :param
            file_path: text file path
        :return
            str: a content from this file
    """
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            return content
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return None
    except IOError:
        print(f"Error: Facing error when read file at {file_path}")
        return None


def write_to_file(content, filename="output/output.txt"):
    """
        Write content to file
        :param
            content: text content
            filename: output file name
    """
    try:
        with open(filename, 'w') as file:
            file.write(content)
        print(f"Content successfully written to {filename}")
    except IOError:
        print(f"An error occurred while writing to {filename}")


def text_to_braille(file_path: str):
    """
        Convert English texts to braille format
        :param
            file_path: a .txt file with English texts
        :return:
            str: a .txt file with braille text
    """
    content = read_text_file(file_path)
    braille_text = braille.textToBraille(content)
    print(braille_text)
    write_to_file(braille_text, "../output/output.txt")
    return braille_text


if __name__ == '__main__':
    file_path = "../test.txt"
    text_to_braille(file_path)
    input_audio = "../test_speech.wav"
    speech_to_text(input_audio)