import customtkinter
from tkinter import filedialog, messagebox


class TextToSpeech:
    def __init__(self, root):
        self.root = root

    def execute(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            messagebox.showinfo("Info", "Text to Speech feature executed successfully!")
        else:
            messagebox.showerror("Error", "No file selected")


class BrailleToText:
    def __init__(self, root):
        self.root = root

    def execute(self):
        # Placeholder for Braille to Text functionality
        messagebox.showinfo("Info", "Braille to Text feature coming soon!")


class ImageToBraille:
    def __init__(self, root):
        self.root = root

    def execute(self):
        # Placeholder for Image to Braille functionality
        messagebox.showinfo("Info", "Image to Braille feature coming soon!")


class SpeechToText:
    def __init__(self, root):
        self.root = root

    def execute(self):
        # Placeholder for Speech to Text functionality
        messagebox.showinfo("Info", "Speech to Text feature coming soon!")


class TextToBraille:
    def __init__(self, root):
        self.root = root

    def execute(self):
        # Placeholder for Text to Braille functionality
        messagebox.showinfo("Info", "Text to Braille feature coming soon!")


class BrailleReaderUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Braille Reader and Writer Interface")
        self.root.geometry("900x500")
        customtkinter.set_appearance_mode("light")  # Modes: "System", "Dark", "Light"
        customtkinter.set_default_color_theme(
            "blue"
        )  # Themes: "blue", "green", "dark-blue"

        # Main Frame
        self.main_frame = customtkinter.CTkFrame(master=root)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Left Frame for Buttons
        self.left_frame = customtkinter.CTkFrame(master=self.main_frame, width=300)
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
            font=("Helvetica", 18, "bold"),
        )
        self.title_label.pack(pady=20)

        # Frame for "To Braille" Functions
        self.to_braille_frame = customtkinter.CTkFrame(master=self.left_frame)
        self.to_braille_frame.pack(pady=10, padx=10, fill="x")

        # Title for "To Braille" Functions
        self.to_braille_title = customtkinter.CTkLabel(
            master=self.to_braille_frame,
            text="To Braille Functions",
            font=("Helvetica", 16, "bold"),
        )
        self.to_braille_title.pack(pady=5)
        self.to_braille_title.configure(text_color="orange")

        # Text to Braille Button
        self.text_to_braille = TextToBraille(root)
        self.text_to_braille_button = customtkinter.CTkButton(
            master=self.to_braille_frame,
            text="Text to Braille",
            command=lambda: [
                self.update_right_frame("text to braille"),
                self.dim_frames(self.to_braille_frame, self.text_to_braille_button),
            ],
        )
        self.text_to_braille_button.pack(pady=5, padx=10)

        # Image to Braille Button
        self.image_to_braille = ImageToBraille(root)
        self.image_to_braille_button = customtkinter.CTkButton(
            master=self.to_braille_frame,
            text="Image to Braille",
            command=lambda: [
                self.update_right_frame("image to braille"),
                self.dim_frames(self.to_braille_frame, self.image_to_braille_button),
            ],
        )
        self.image_to_braille_button.pack(pady=5, padx=10)

        # Frame for "To Text" Functions
        self.to_text_frame = customtkinter.CTkFrame(master=self.left_frame)
        self.to_text_frame.pack(pady=10, padx=10, fill="x")

        # Title for "To Text" Functions
        self.to_text_title = customtkinter.CTkLabel(
            master=self.to_text_frame,
            text="To Text Functions",
            font=("Helvetica", 16, "bold"),
        )
        self.to_text_title.pack(pady=5)
        self.to_text_title.configure(text_color="blue")

        # Braille to Text Button
        self.braille_to_text = BrailleToText(root)
        self.braille_to_text_button = customtkinter.CTkButton(
            master=self.to_text_frame,
            text="Braille to Text",
            command=lambda: [
                self.update_right_frame("braille to text"),
                self.dim_frames(self.to_text_frame, self.braille_to_text_button),
            ],
        )
        self.braille_to_text_button.pack(pady=5, padx=10)

        # Speech to Text Button
        self.speech_to_text = SpeechToText(root)
        self.speech_to_text_button = customtkinter.CTkButton(
            master=self.to_text_frame,
            text="Speech to Text",
            command=lambda: [
                self.update_right_frame("speech to text"),
                self.dim_frames(self.to_text_frame, self.speech_to_text_button),
            ],
        )
        self.speech_to_text_button.pack(pady=5, padx=10)

        # Text to Speech Button
        self.text_to_speech = TextToSpeech(root)
        self.text_to_speech_button = customtkinter.CTkButton(
            master=self.to_text_frame,
            text="Text to Speech",
            command=lambda: [
                self.update_right_frame("text to speech"),
                self.dim_frames(self.to_text_frame, self.text_to_speech_button),
            ],
        )
        self.text_to_speech_button.pack(pady=5, padx=10)

    def update_right_frame(self, function):
        # Clear the right frame
        for widget in self.right_frame.winfo_children():
            widget.destroy()

        # Update title based on selected function
        title_text = f"Please upload your {function.split(' ')[0]}"
        right_title = customtkinter.CTkLabel(
            master=self.right_frame, text=title_text, font=("Helvetica", 18, "bold")
        )
        right_title.pack(pady=20, anchor="center")  # Center horizontally with padding

        # Upload Button
        upload_button = customtkinter.CTkButton(
            master=self.right_frame,
            text="Upload",
            command=lambda: self.handle_upload(),
        )
        upload_button.pack(pady=10, anchor="center")  # Center horizontally

        # Convert Button
        convert_button = customtkinter.CTkButton(
            master=self.right_frame,
            text="Convert",
            command=lambda: self.handle_conversion(function),
        )
        convert_button.pack(pady=10, anchor="center")  # Center horizontally

    def handle_conversion(self, function_name):
        # Placeholder for handling the conversion functionality
        messagebox.showinfo("Info", f"Executing {function_name} conversion...")

    def handle_upload(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            messagebox.showinfo("Info", "Upload successfully!")
        else:
            messagebox.showerror("Error", "No file selected")

    def dim_frames(self, active_frame, active_button):
        frames = [self.to_braille_frame, self.to_text_frame]
        for frame in frames:
            if frame == active_frame:
                frame.configure(fg_color="white")  # Normal frame
                for child in frame.winfo_children():
                    if isinstance(child, customtkinter.CTkLabel):
                        # Preserve the original color for the active frame's label
                        if "To Braille" in child.cget("text"):
                            title_color = "orange"
                            child.configure(text_color=title_color)
                        elif "To Text" in child.cget("text"):
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
