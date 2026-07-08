# Video Transcriber

A completely free web application built with Streamlit that downloads and transcribes YouTube or Facebook videos. It uses [yt-dlp](https://github.com/yt-dlp/yt-dlp) to fetch the audio and [OpenAI's Whisper](https://github.com/openai/whisper) (running locally) to generate accurate transcripts without any limits on video or text length.

## Prerequisites

Before running the application, you need to have `ffmpeg` installed on your system.

* **Ubuntu/Debian:**
  ```bash
  sudo apt update && sudo apt install ffmpeg
  ```
* **macOS (using Homebrew):**
  ```bash
  brew install ffmpeg
  ```
* **Windows:**
  Download and install from the [official FFmpeg site](https://ffmpeg.org/download.html), and ensure it is added to your system's PATH.

## How to Run Locally

1. **Clone the repository** and navigate to the project folder.
2. **(Optional but recommended)** Create and activate a Python virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```
3. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Run the Streamlit application:**
   ```bash
   streamlit run app.py
   ```
5. **Open your browser** and go to the local URL provided in the terminal (usually `http://localhost:8501`).

## How to Use

1. Paste a valid YouTube or Facebook video URL into the input box.
2. Click the **Transcribe** button.
3. Wait for the audio to download and the transcription to finish. (The time it takes will depend on the length of the video and your computer's hardware).
4. Once completed, you can read and copy the transcript from the text area or click **Download Transcript** to save it as a `.txt` file.

## How to Deploy for Free

You can deploy this application for free using **Streamlit Community Cloud**.

1. **Push your code to a public GitHub repository.**
2. Go to [share.streamlit.io](https://share.streamlit.io/) and log in with your GitHub account.
3. Click on **New app**.
4. Select the GitHub repository, branch, and specify `app.py` as the Main file path.
5. **Important:** Streamlit Community Cloud needs `ffmpeg` installed via `packages.txt`. 
   Create a file named `packages.txt` in the root of your repository with the following content:
   ```
   ffmpeg
   ```
6. Click **Deploy!**

Your application will be live in a few minutes and accessible via a public URL provided by Streamlit.
