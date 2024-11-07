import sys
import os

# Add the project's root directory to the Python path at runtime
# so that Python can locate the modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pygame
import customtkinter
from tkinter import filedialog, messagebox
from tkinter import Text

from braille_writer.braille_writer import speech_to_braille
from braille_reader.braille_reader import image_to_speech


class BrailleToSpeech:
    def __init__(self, root):
        self.root = root

    def handle_play(self, file_path):
        # image_to_speech(file_path)
        # Handle playing the audio file
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init()  # Reinitialize if not initialized
            pygame.mixer.music.load(file_path)  # Load the audio file
            pygame.mixer.music.play()  # Play the audio
            messagebox.showinfo("Info", "Playing audio...")
        except pygame.error as e:
            messagebox.showerror(
                "Error", f"An error occurred while playing the audio: {str(e)}"
            )


class SpeechToBraille:
    def __init__(self, root):
        self.root = root

    def handle_conversion(self, file_path, text_display):
        # Call the speech_to_braille function and update the text display
        speech_to_braille(file_path)
        output_braille = "output/english_to_braille_text.txt"
        output_english = "output/speech_to_english.txt"

        try:
            # Read braille text
            with open(output_braille, "r", encoding="utf-8") as file:
                braille_text = file.read()

            # Read English text
            with open(output_english, "r", encoding="utf-8") as file:
                english_text = file.read()

            # Update the text display widget
            text_display.config(state="normal")
            text_display.delete("1.0", "end")
            text_display.insert("1.0", f"Braille Text:\n{braille_text}\n\n")
            text_display.insert("end", f"English Text:\n{english_text}")
            text_display.config(state="disabled")  # Make text widget read-only

        except FileNotFoundError:
            messagebox.showerror(
                "Error", "One or more output files could not be found."
            )
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")


class BrailleReaderUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Braille Reader and Writer Interface")
        self.root.geometry("1200x700")
        customtkinter.set_appearance_mode("light")  # Modes: "System", "Dark", "Light"
        customtkinter.set_default_color_theme(
            "blue"
        )  # Themes: "blue", "green", "dark-blue"

        # Initialize file_content attribute
        self.file_content = None
        self.file_path = None

        # Main Frame
        self.main_frame = customtkinter.CTkFrame(master=root)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Left Frame for Buttons
        self.left_frame = customtkinter.CTkFrame(master=self.main_frame, width=350)
        self.left_frame.pack(side="left", fill="y", padx=10, pady=10)
        self.left_frame.pack_propagate(
            False
        )  # Prevent the frame from shrinking to fit content

        # Right Frame for Upload Area
        self.right_frame = customtkinter.CTkFrame(master=self.main_frame)
        self.right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # Title Label
        self.title_label = customtkinter.CTkLabel(
            master=self.left_frame,
            text="Braille Reader & Writer",
            font=("Helvetica", 22, "bold"),
        )
        self.title_label.pack(pady=20)

        # Frame for "Braille to Speech" Functions
        self.braille_to_speech_frame = customtkinter.CTkFrame(master=self.left_frame)
        self.braille_to_speech_frame.pack(pady=10, padx=10, fill="x")

        # Title for "Braille to Speech" Functions
        self.braille_to_speech_title = customtkinter.CTkLabel(
            master=self.braille_to_speech_frame,
            text="Braille to Speech",
            font=("Helvetica", 20, "bold"),
        )
        self.braille_to_speech_title.pack(pady=5)
        self.braille_to_speech_title.configure(text_color="orange")

        # Braille to Speech Button
        self.braille_to_speech = BrailleToSpeech(root)
        self.braille_to_speech_button = customtkinter.CTkButton(
            master=self.braille_to_speech_frame,
            text="Braille to Speech",
            font=("Helvetica", 18),
            command=lambda: [
                self.update_right_frame("Braille Text"),
                self.dim_frames(
                    self.braille_to_speech_frame, self.braille_to_speech_button
                ),
            ],
        )
        self.braille_to_speech_button.pack(pady=5, padx=10)

        # Frame for "Speech to Braille" Functions
        self.speech_to_braille_frame = customtkinter.CTkFrame(master=self.left_frame)
        self.speech_to_braille_frame.pack(pady=10, padx=10, fill="x")

        # Title for "Speech to Braille" Functions
        self.speech_to_braille_title = customtkinter.CTkLabel(
            master=self.speech_to_braille_frame,
            text="Speech To Braille",
            font=("Helvetica", 20, "bold"),
        )
        self.speech_to_braille_title.pack(pady=5)
        self.speech_to_braille_title.configure(text_color="blue")

        # Speech to Braille Button
        self.speech_to_braille = SpeechToBraille(root)
        self.speech_to_braille_button = customtkinter.CTkButton(
            master=self.speech_to_braille_frame,
            text="Speech to Braille",
            font=("Helvetica", 18),
            command=lambda: [
                self.update_right_frame("Speech File"),
                self.dim_frames(
                    self.speech_to_braille_frame, self.speech_to_braille_button
                ),
            ],
        )
        self.speech_to_braille_button.pack(pady=5, padx=10)

    def update_right_frame(self, function):
        # Clear the right frame
        for widget in self.right_frame.winfo_children():
            widget.destroy()

        # Update title based on selected function
        title_text = f"Please upload your {function}"
        right_title = customtkinter.CTkLabel(
            master=self.right_frame, text=title_text, font=("Helvetica", 22, "bold")
        )
        right_title.pack(pady=20, anchor="center")  # Center horizontally with padding

        # Upload Button
        upload_button = customtkinter.CTkButton(
            master=self.right_frame,
            text="Upload",
            font=("Helvetica", 18),
            command=lambda: self.handle_upload(),
        )
        upload_button.pack(pady=5, anchor="center")  # Center horizontally

        # Show uploaded file name
        self.uploaded_file_label = customtkinter.CTkLabel(
            master=self.right_frame,
            text="No file uploaded",
            font=("Helvetica", 16),
        )
        self.uploaded_file_label.pack(pady=5, anchor="center")

        # Convert Button (only for Speech to Braille)
        if function == "Speech File":
            convert_button = customtkinter.CTkButton(
                master=self.right_frame,
                text="Convert",
                font=("Helvetica", 18),
                command=lambda: self.speech_to_braille.handle_conversion(
                    self.file_path, self.text_display
                ),
            )
            convert_button.pack(pady=5, anchor="center")  # Center horizontally

            # Text Widget to Display the Converted Content (Initially Empty)
            self.text_display = Text(
                self.right_frame,
                wrap="word",
                width=80,
                height=25,
                font=("Helvetica", 24),
            )
            self.text_display.pack(pady=20, anchor="center")
        else:
            play_button = customtkinter.CTkButton(
                master=self.right_frame,
                text="Convert and Play",
                font=("Helvetica", 18),
                command=lambda: self.braille_to_speech.handle_play(self.file_path),
            )
            play_button.pack(pady=5, anchor="center")  # Center horizontally

    def handle_upload(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Audio files", "*.wav;*.mp3;*.jpeg")]
        )
        if file_path:
            # Store the file path
            self.file_path = file_path
            self.uploaded_file_label.configure(
                text=f"Uploaded File: {file_path.split('/')[-1]}"
            )
            messagebox.showinfo("Info", "File uploaded successfully!")
        else:
            messagebox.showerror("Error", "No file selected")

    def dim_frames(self, active_frame, active_button):
        frames = [self.braille_to_speech_frame, self.speech_to_braille_frame]
        for frame in frames:
            title_color = "transparent"  # Initialize title_color
            if frame == active_frame:
                frame.configure(fg_color="white")  # Normal frame
                for child in frame.winfo_children():
                    if isinstance(child, customtkinter.CTkLabel):
                        # Preserve the original color for the active frame's label
                        if "Braille to Speech" in child.cget("text"):
                            title_color = "orange"
                            child.configure(text_color=title_color)
                        elif "Speech To Braille" in child.cget("text"):
                            title_color = "blue"
                            child.configure(text_color=title_color)
                    if isinstance(child, customtkinter.CTkButton):
                        if child == active_button:
                            # Set the active button color to match the title color
                            child.configure(text_color="white", fg_color=title_color)
                        else:
                            # Dim the unselected buttons in the active frame
                            child.configure(text_color="gray", fg_color="lightgray")
            else:
                frame.configure(fg_color="transparent")  # Dimmed frame
                for child in frame.winfo_children():
                    if isinstance(child, customtkinter.CTkLabel):
                        child.configure(text_color="gray")  # Dimmed text color
                    if isinstance(child, customtkinter.CTkButton):
                        child.configure(
                            text_color="white", fg_color="gray"
                        )  # Further dimmed button color


if __name__ == "__main__":
    root = customtkinter.CTk()
    ui = BrailleReaderUI(root)
    root.mainloop()
