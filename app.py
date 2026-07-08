import streamlit as st
import yt_dlp
import whisper
import os

def download_audio(url):
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

st.title("Video Transcriber")
st.write("Paste a YouTube or Facebook video link below to get the transcript.")

url = st.text_input("Video URL:")

if st.button("Transcribe"):
    if url:
        with st.spinner("Downloading audio..."):
            try:
                audio_file = download_audio(url)
            except Exception as e:
                st.error(f"Error downloading audio: {e}")
                st.stop()
        
        with st.spinner("Transcribing... (This may take a while depending on the video length)"):
            try:
                # Load the Whisper model (using "base" for faster processing, change as needed)
                model = whisper.load_model("base")
                result = model.transcribe(audio_file)
                transcript = result["text"]
                
                st.success("Transcription complete!")
                st.text_area("Transcript:", transcript, height=300)
                
                # Provide a download button
                st.download_button(
                    label="Download Transcript",
                    data=transcript,
                    file_name="transcript.txt",
                    mime="text/plain"
                )
            except Exception as e:
                st.error(f"Error during transcription: {e}")
            finally:
                # Cleanup audio file
                if os.path.exists(audio_file):
                    os.remove(audio_file)
    else:
        st.warning("Please enter a valid URL.")
