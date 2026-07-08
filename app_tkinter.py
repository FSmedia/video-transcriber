import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import yt_dlp
import whisper
import os
import threading

class VideoTranscriberApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Free Video Transcriber (Local Windows)")
        self.root.geometry("600x500")

        # URL Input
        self.url_frame = ttk.Frame(root, padding="10")
        self.url_frame.pack(fill=tk.X)

        ttk.Label(self.url_frame, text="Video URL:").pack(side=tk.LEFT)
        self.url_entry = ttk.Entry(self.url_frame, width=50)
        self.url_entry.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)

        # Model Selection
        self.model_frame = ttk.Frame(root, padding="10")
        self.model_frame.pack(fill=tk.X)

        ttk.Label(self.model_frame, text="Model Size:").pack(side=tk.LEFT)
        self.model_var = tk.StringVar(value="base")
        self.model_combo = ttk.Combobox(self.model_frame, textvariable=self.model_var, values=["tiny", "base", "small", "medium", "large"], state="readonly")
        self.model_combo.pack(side=tk.LEFT, padx=10)

        # Buttons
        self.button_frame = ttk.Frame(root, padding="10")
        self.button_frame.pack(fill=tk.X)

        self.transcribe_btn = ttk.Button(self.button_frame, text="Transcribe", command=self.start_transcription)
        self.transcribe_btn.pack(side=tk.LEFT)

        self.save_btn = ttk.Button(self.button_frame, text="Save to File", command=self.save_to_file, state=tk.DISABLED)
        self.save_btn.pack(side=tk.LEFT, padx=10)

        # Status
        self.status_var = tk.StringVar(value="Ready")
        self.status_label = ttk.Label(root, textvariable=self.status_var, padding="0 10")
        self.status_label.pack(fill=tk.X)

        # Text Area
        self.text_frame = ttk.Frame(root, padding="10")
        self.text_frame.pack(fill=tk.BOTH, expand=True)

        self.text_area = tk.Text(self.text_frame, wrap=tk.WORD)
        self.scrollbar = ttk.Scrollbar(self.text_frame, command=self.text_area.yview)
        self.text_area.configure(yscrollcommand=self.scrollbar.set)

        self.text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def download_audio(self, url):
        ydl_opts = {
            'format': 'm4a/bestaudio/best',
            'outtmpl': '%(id)s.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'm4a',
            }],
            'quiet': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            return f"{info['id']}.m4a"

    def start_transcription(self):
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showwarning("Warning", "Please enter a valid URL.")
            return

        self.transcribe_btn.config(state=tk.DISABLED)
        self.save_btn.config(state=tk.DISABLED)
        self.text_area.delete(1.0, tk.END)
        self.status_var.set("Downloading audio...")

        # Run in a separate thread to not block the GUI
        threading.Thread(target=self.transcribe_worker, args=(url, self.model_var.get()), daemon=True).start()

    def transcribe_worker(self, url, model_size):
        audio_file = None
        try:
            audio_file = self.download_audio(url)

            self.status_var.set("Loading model and transcribing (this may take a while)...")
            model = whisper.load_model(model_size)
            result = model.transcribe(audio_file)
            transcript = result["text"]

            # Update GUI safely from thread
            self.root.after(0, self.update_gui_success, transcript)

        except Exception as e:
            self.root.after(0, self.update_gui_error, str(e))

        finally:
            if audio_file and os.path.exists(audio_file):
                try:
                    os.remove(audio_file)
                except:
                    pass

    def update_gui_success(self, transcript):
        self.status_var.set("Transcription complete!")
        self.text_area.insert(tk.END, transcript)
        self.transcribe_btn.config(state=tk.NORMAL)
        self.save_btn.config(state=tk.NORMAL)

    def update_gui_error(self, error_msg):
        self.status_var.set("Error during transcription.")
        messagebox.showerror("Error", f"An error occurred:\n{error_msg}")
        self.transcribe_btn.config(state=tk.NORMAL)

    def save_to_file(self):
        transcript = self.text_area.get(1.0, tk.END).strip()
        if not transcript:
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
            title="Save Transcript"
        )

        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(transcript)
                messagebox.showinfo("Success", f"Saved to {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoTranscriberApp(root)
    root.mainloop()
