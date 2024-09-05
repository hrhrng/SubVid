import argparse
import whisper
from moviepy.editor import VideoFileClip
import os

def extract_audio(video_path):
    video = VideoFileClip(video_path)
    audio = video.audio
    audio.write_audiofile("temp_audio.wav")
    return "temp_audio.wav"

def transcribe_audio(audio_path):
    model = whisper.load_model("base")
    result = model.transcribe(audio_path)
    return result["segments"]

def format_time(seconds):
    hours = int(seconds / 3600)
    minutes = int((seconds % 3600) / 60)
    seconds = seconds % 60
    milliseconds = int((seconds - int(seconds)) * 1000)
    return f"{hours:02d}:{minutes:02d}:{int(seconds):02d},{milliseconds:03d}"

def create_srt(segments, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        for i, segment in enumerate(segments, start=1):
            start_time = format_time(segment['start'])
            end_time = format_time(segment['end'])
            text = segment['text'].strip()
            f.write(f"{i}\n{start_time} --> {end_time}\n{text}\n\n")

def main():
    parser = argparse.ArgumentParser(description="Extract SRT subtitles from a video using Whisper")
    parser.add_argument("video_path", help="Path to the input video file")
    parser.add_argument("output_path", help="Path to save the output SRT subtitle file")
    args = parser.parse_args()

    print("Extracting audio from video...")
    audio_path = extract_audio(args.video_path)

    print("Transcribing audio...")
    segments = transcribe_audio(audio_path)

    print("Creating SRT file...")
    create_srt(segments, args.output_path)

    print(f"SRT subtitles extracted and saved to {args.output_path}")

    # Clean up temporary audio file
    os.remove(audio_path)

if __name__ == "__main__":
    main()