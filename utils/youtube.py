from __future__ import unicode_literals
import youtube_dl
import os
import assemblyai as aai
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
aai.settings.api_key = os.getenv("AAI_TOKEN")

def get_audio_file(url: str) -> None:

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    audio_file = [f for f in os.listdir(".") if f.endswith(".mp3")][0]
    os.rename(os.path.join(".", audio_file),
              os.path.join(".", "audio.mp3"))


def extract_text_from_mp3(audio_file) -> str:
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(audio_file)
    os.remove(audio_file)
    return transcript.text


if __name__ == "__main__":

    get_audio_file("https://www.youtube.com/shorts/kupAyqfiPxU")
    text = extract_text_from_mp3("audio.mp3")
    print(text)
