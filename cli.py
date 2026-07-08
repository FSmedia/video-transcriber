import argparse
import yt_dlp
import whisper
import os
import sys

def download_audio(url):
    print(f"Downloading audio from {url}...")
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

def main():
    parser = argparse.ArgumentParser(description="Free Video Transcriber CLI (YouTube/Facebook)")
    parser.add_argument("url", help="The URL of the video to transcribe")
    parser.add_argument("-m", "--model", choices=["tiny", "base", "small", "medium", "large"],
                        default="base", help="Whisper model size to use (default: base)")
    parser.add_argument("-o", "--output", default="transcript.txt",
                        help="Output file path (default: transcript.txt)")

    args = parser.parse_args()

    audio_file = None
    try:
        audio_file = download_audio(args.url)

        print(f"Loading Whisper model '{args.model}' and transcribing...")
        model = whisper.load_model(args.model)
        result = model.transcribe(audio_file)
        transcript = result["text"]

        with open(args.output, "w", encoding="utf-8") as f:
            f.write(transcript)

        print(f"\nTranscription complete! Saved to {args.output}")
        print("-" * 50)
        # Print a snippet
        snippet = transcript[:500] + "..." if len(transcript) > 500 else transcript
        print(snippet)
        print("-" * 50)

    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)
        sys.exit(1)

    finally:
        if audio_file and os.path.exists(audio_file):
            print("Cleaning up temporary audio file...")
            os.remove(audio_file)

if __name__ == "__main__":
    main()
