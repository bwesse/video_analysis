import tkinter as tk
from tkinter import filedialog

def browse_files():
    filename = filedialog.askopenfilename()
    label_file_explorer.configure(text="File Opened: " + filename)

window = tk.Tk()
window.title('Video Search System')
window.geometry("700x500")

label_file_explorer = tk.Label(window, text="File Explorer", width=100, height=4, fg="blue")
button_explore = tk.Button(window, text="Browse Files", command=browse_files)
button_exit = tk.Button(window, text="Exit", command=exit)

label_file_explorer.grid(column=1, row=1)
button_explore.grid(column=1, row=2)
button_exit.grid(column=1, row=3)

window.mainloop()
