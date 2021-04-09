import tkinter as tk
class ExtEntry(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, borderwidth=1, relief="sunken", background="white")

        dot = tk.Label(self, text=".", background="white")
        dot.pack(side="left")

        self.entry = tk.Entry(self, borderwidth=0, justify="left", highlightthickness=0, background="white")
        self.entry.pack(side="left")
    
    def get(self):
        return self.entry.get()