import gradio as gr
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

def transcribe_video(url, model_size="base"):
    if not url:
        return "Please enter a valid URL.", None

    audio_file = None
    try:
        # Download
        audio_file = download_audio(url)

        # Transcribe
        model = whisper.load_model(model_size)
        result = model.transcribe(audio_file)
        transcript = result["text"]

        # Save transcript to file for download
        transcript_file = "transcript.txt"
        with open(transcript_file, "w", encoding="utf-8") as f:
            f.write(transcript)

        return transcript, transcript_file

    except Exception as e:
        return f"Error: {str(e)}", None

    finally:
        # Cleanup audio file
        if audio_file and os.path.exists(audio_file):
            os.remove(audio_file)

with gr.Blocks(title="Free Video Transcriber") as demo:
    gr.Markdown("# Free Video Transcriber")
    gr.Markdown("Paste a YouTube or Facebook video link below to get the transcript with no limits.")

    with gr.Row():
        url_input = gr.Textbox(label="Video URL", placeholder="https://www.youtube.com/watch?v=...")
        model_dropdown = gr.Dropdown(
            choices=["tiny", "base", "small", "medium", "large"],
            value="base",
            label="Whisper Model Size (Larger = more accurate but slower)"
        )

    submit_btn = gr.Button("Transcribe", variant="primary")

    with gr.Row():
        transcript_output = gr.Textbox(label="Transcript", lines=15, show_copy_button=True)
        file_output = gr.File(label="Download Transcript File")

    submit_btn.click(
        fn=transcribe_video,
        inputs=[url_input, model_dropdown],
        outputs=[transcript_output, file_output]
    )

if __name__ == "__main__":
    demo.launch()
