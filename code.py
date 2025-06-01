import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import requests
import threading

def start_download():
    url = url_entry.get()
    if not url:
        messagebox.showerror("Error", "Please enter a URL")
        return

    save_path = filedialog.asksaveasfilename()
    if not save_path:
        return

    progress_bar["value"] = 0
    status_label.config(text="Starting download...")
    threading.Thread(target=download_file, args=(url, save_path), daemon=True).start()

def download_file(url, path):
    try:
        response = requests.get(url, stream=True)
        total = int(response.headers.get("content-length", 0))
        downloaded = 0
        with open(path, "wb") as f:
            for data in response.iter_content(chunk_size=4096):
                f.write(data)
                downloaded += len(data)
                percent = (downloaded / total) * 100
                progress_bar["value"] = percent
                status_label.config(text=f"{int(percent)}% downloaded")
                window.update_idletasks()
        status_label.config(text="✅ Download complete!")
    except Exception as e:
        status_label.config(text="❌ Error during download")
        messagebox.showerror("Download Failed", str(e))

# ساخت پنجره اصلی
window = tk.Tk()
window.title("Dino Downloader")
window.geometry("500x250")
window.configure(bg="#1e1e2f")

# عنوان برنامه
title = tk.Label(window, text="🦖 Dino Downloader", font=("Helvetica", 18, "bold"), fg="white", bg="#1e1e2f")
title.pack(pady=10)

# ورودی لینک
url_entry = tk.Entry(window, width=50, font=("Helvetica", 12))
url_entry.pack(pady=10)

# دکمه دانلود
download_btn = tk.Button(window, text="Download", command=start_download, font=("Helvetica", 12), bg="#4CAF50", fg="white")
download_btn.pack(pady=10)

# نوار پیشرفت
progress_bar = ttk.Progressbar(window, length=400, mode="determinate")
progress_bar.pack(pady=10)

# وضعیت دانلود
status_label = tk.Label(window, text="", fg="white", bg="#1e1e2f", font=("Helvetica", 10))
status_label.pack()

window.mainloop()

