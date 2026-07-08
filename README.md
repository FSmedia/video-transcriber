# Free Video Transcriber

A completely free, multi-platform tool that downloads and transcribes YouTube or Facebook videos. It uses [yt-dlp](https://github.com/yt-dlp/yt-dlp) to fetch the audio and [OpenAI's Whisper](https://github.com/openai/whisper) to generate highly accurate transcripts with **no limits** on video length or text output.

Because users have different preferences and run on different systems, this project offers **multiple ways** to run the transcriber!

---

## Prerequisites (For all local options)

Before running the application locally, you must have `ffmpeg` installed on your system. Whisper needs it to process audio files.

* **Windows:**
  Download and install from the [official FFmpeg site](https://ffmpeg.org/download.html), and ensure it is added to your system's PATH. Alternatively, you can use `winget install ffmpeg`.
* **Ubuntu/Debian:**
  ```bash
  sudo apt update && sudo apt install ffmpeg
  ```
* **macOS (using Homebrew):**
  ```bash
  brew install ffmpeg
  ```

---

## How to Run: Choose Your Option

### Option 1: The Easiest Way for Windows (Local GUI)
If you are on Windows and want a native Desktop app experience without using the command line:

1. Double-click the `start_windows.bat` file in this folder.
2. The script will automatically create a virtual environment, install all the required dependencies, and launch a menu.
3. Choose **Option 1 (Local Desktop App - Tkinter)**.
4. Paste the video URL, select your model size, and click Transcribe!

*(You can also use this batch file to launch the Gradio Web App, the Streamlit App, or the CLI).*

### Option 2: The Best Online Free GPU Way (Google Colab)
If you don't want to install anything on your computer, or if your computer is slow, use Google Colab to borrow a free GPU from Google:

1. Open `transcriber_colab.ipynb` in [Google Colab](https://colab.research.google.com/).
2. Change the Runtime to a **T4 GPU** (Runtime > Change runtime type > Hardware accelerator).
3. Run the cells, paste your link, and get a super-fast transcription right in your browser!

### Option 3: Python Web App (Gradio)
Gradio provides a very clean, robust web interface. This is highly recommended over Streamlit if you want to deploy to free platforms like Hugging Face Spaces.

**To run locally:**
```bash
pip install -r requirements.txt
python app_gradio.py
```
Then open `http://localhost:7860` in your browser.

### Option 4: Python Web App (Streamlit)
The original Streamlit interface is still available.

**To run locally:**
```bash
pip install -r requirements.txt
streamlit run app.py
```
Then open `http://localhost:8501` in your browser.

### Option 5: Command Line Interface (CLI)
For developers or users who prefer the terminal:

```bash
pip install -r requirements.txt
python cli.py "https://www.youtube.com/watch?v=..." --model base --output my_transcript.txt
```

### Option 6: Docker Container
If you have Docker installed, you can run the Gradio app without worrying about Python or `ffmpeg` installations:

```bash
docker build -t video-transcriber .
docker run -p 7860:7860 video-transcriber
```
Then open `http://localhost:7860` in your browser.

---

## Important Note on Whisper Models

When running locally or via CLI, you can choose the Whisper model size (`tiny`, `base`, `small`, `medium`, `large`).
* **Tiny/Base:** Fastest, uses very little RAM, but less accurate.
* **Large:** Very accurate, but requires significant RAM/VRAM and takes much longer to process on a standard CPU. (Highly recommended to use the **Colab** option if you want to use the `large` model).
