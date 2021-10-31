from tkinter import ttk

class Style(ttk.Style):
    def __init__(self, master) -> None:
        super().__init__(master)
        self.configure("Accent.TButton", font=("Bahnschrift Condensed", 12, "bold"))