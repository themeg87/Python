import tkinter as tk
from tkinter import filedialog
from pytube import YouTube

def select_download_directory():
    download_dir = filedialog.askdirectory()
    if download_dir:
        download_dir_entry.delete(0, tk.END)
        download_dir_entry.insert(0, download_dir)

def download_video():
    url = url_entry.get()
    download_dir = download_dir_entry.get()
    try:
        yt = YouTube(url, on_progress_callback=show_progress)
        title = yt.title
        status_label.config(text="Downloading...")
        
        if download_dir:
            stream = yt.streams.filter(res="720p").first()
            stream.download(download_dir)
            status_label.config(text=f"{title} downloaded successfully to {download_dir}.")
        else:
            status_label.config(text="Please select a download directory.")
    except Exception as e:
        status_label.config(text="Error: Invalid URL or download failed.")

def show_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage_of_completion = (bytes_downloaded / total_size) * 100
    percentage_of_completion = round(percentage_of_completion, 2)
    progress_label.config(text=f"Progress: {percentage_of_completion}%")

# Create a GUI window
window = tk.Tk()
window.title("YouTube Video Downloader")

# Create a label for instructions
instructions_label = tk.Label(window, text="Enter the YouTube video URL:")
instructions_label.pack()

# Create an entry field for the URL
url_entry = tk.Entry(window, width=50)
url_entry.pack()

# Create a label and entry field for download directory
download_dir_label = tk.Label(window, text="Download Directory:")
download_dir_label.pack()
download_dir_entry = tk.Entry(window, width=50)
download_dir_entry.pack()

# Create a button to select download directory
select_dir_button = tk.Button(window, text="Select Download Directory", command=select_download_directory)
select_dir_button.pack()

# Create a button to initiate download
download_button = tk.Button(window, text="Download", command=download_video)
download_button.pack()

# Create a label to display download status
status_label = tk.Label(window, text="")
status_label.pack()

# Create a label to display download progress
progress_label = tk.Label(window, text="")
progress_label.pack()

# Start the GUI loop
window.mainloop()
