from ui.main_window import BrailleReaderUI
import customtkinter
import warnings
warnings.filterwarnings('ignore')

if __name__ == '__main__':
    root = customtkinter.CTk()
    ui = BrailleReaderUI(root)
    root.mainloop()