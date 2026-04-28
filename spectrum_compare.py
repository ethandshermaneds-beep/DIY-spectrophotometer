import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt
import pandas as pd
import os

def load_and_plot_spectra():
    filepaths = filedialog.askopenfilenames(
        initialdir="C:/Users/Hanna/OneDrive - Asbury University/2026 Spring/CHE 322 CHE 422/from spectrophotometer",
        title="Choose spectra to read",
        filetypes=(("Spectra", "*.csv"), ("Nitrates", "*.nit"), ("Quasicrystals", "*.qsc"), ("Fluorescent probes", "*.flp"))
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
root.title("Spectra Viewer")

root.geometry("300x100") 

plot_button = tk.Button(root, text="Open and Plot Spectra", command=load_and_plot_spectra)
plot_button.pack(expand=True) # Centers the button in the window

root.mainloop()
