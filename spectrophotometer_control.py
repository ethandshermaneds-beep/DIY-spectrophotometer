import socket
import tkinter as tk
from tkinter import messagebox
import time
import os
import pandas as pd
import matplotlib.pyplot as plt
import threading

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


WATCH_FOLDER = r"C:\Users\username\path" #fill in with the path to the folder where new spectra are being written


class CSVHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return

        if event.src_path.endswith(".csv"):
            print(f"New spectrum detected: {event.src_path}")

            time.sleep(1)

            try:
                process_csv(event.src_path)
            except Exception as e:
                print(f"Error processing file: {e}")


def process_csv(filepath):
    df = pd.read_csv(filepath)

    x = df["Index"]
    y = df["Absorbance"]

    plt.figure()
    plt.scatter(x, y)

    plt.xlabel("Index")
    plt.ylabel("Absorbance")
    plt.title(os.path.basename(filepath))

    plt.show()


def start_watcher():
    event_handler = CSVHandler()
    observer = Observer()
    observer.schedule(event_handler, WATCH_FOLDER, recursive=False)
    observer.start()

    print("Watching for new spectra...")

    try:
        while True:
            time.sleep(1)
    except Exception:
        observer.stop()

    observer.join()


def blank():
    HOST = 'hostname' #fill in the hostname of the RPi you'll be using
    PORT = 5000

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((HOST, PORT))
            s.sendall("blank".encode())
            s.recv(1024)
        except ConnectionRefusedError:
            messagebox.showerror("Connection Error", "Cannot connect to Pi.")

def sample():
    HOST = 'hostname' #fill in the hostname of the RPi you'll be using
    PORT = 5000

    name = entry.get()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((HOST, PORT))
            s.sendall(str(name).encode())
            s.recv(1024)
        except ConnectionRefusedError:
            messagebox.showerror("Connection Error", "Cannot connect to Pi.")


root = tk.Tk()
root.title("Spectrophotometer Control")

tk.Label(root, text="On startup you must run a blank before a sample").pack(padx=10, pady=5)

button = tk.Button(root, text="Blank", command=blank)
button.pack(padx=10, pady=10)

tk.Label(root, text="What is the name of the sample?").pack(padx=10, pady=5)

entry = tk.Entry(root)
entry.pack(padx=10, pady=5)

button = tk.Button(root, text="Sample", command=sample)
button.pack(padx=10, pady=10)


watcher_thread = threading.Thread(target=start_watcher, daemon=True)
watcher_thread.start()


root.mainloop()
