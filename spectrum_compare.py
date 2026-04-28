import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt
import pandas as pd
import os

def load_and_plot_spectra():
    filepaths = filedialog.askopenfilenames(
        initialdir="C:/Users/username/path", #fill in the path to the folder where spectra are being written
        title="Choose spectra to read",
        filetypes=(("Spectra", "*.csv"))
    )

    if filepaths:
        plt.figure()
        
        for filepath in filepaths:
            df = pd.read_csv(filepath)
            x = df["Index"]
            y = df["Absorbance"]
            
            plt.scatter(x, y, label=os.path.basename(filepath))

        plt.xlabel("Step")
        plt.ylabel("Absorbance")
        plt.title("Combined Spectra")
        plt.legend()
        plt.show(block=False) 

root = tk.Tk()
root.title("Spectrum Viewer")

root.geometry("300x100") 

plot_button = tk.Button(root, text="Open and Plot Spectra", command=load_and_plot_spectra)
plot_button.pack(expand=True)

root.mainloop()
