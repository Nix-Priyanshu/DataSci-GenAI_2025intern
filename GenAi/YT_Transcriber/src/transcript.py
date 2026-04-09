import re
from youtube_transcript_api import YouTubeTranscriptApi
from pytube import YouTube
import yt_dlp
import requests
from functools import lru_cache

# ================================
# Clean Transcript Text
# ================================
def clean_transcript(text: str) -> str:
    """
    Cleans transcript:
    - Removes [Music], [Applause], <think> blocks
    - Removes extra whitespace and blank lines
    """
    text = re.sub(r"\[.*?\]", "", text)          # Remove [Music], [Applause]
    text = re.sub(r"<.*?>", "", text)            # Remove <think> or other tags
    text = re.sub(r"\n+", "\n", text)            # Collapse newlines
    text = re.sub(r"\s+", " ", text)             # Collapse spaces
    return text.strip()

# ================================
# Pytube Fallback
# ================================
def pytube_transcript(video_url: str) -> str | None:
    try:
        yt = YouTube(video_url)
        caption = yt.captions.get_by_language_code("en")
        if caption:
            srt_text = caption.generate_srt_captions()
            return clean_transcript(srt_text)
    except Exception:
        return None

# ================================
# yt-dlp Fallback
# ================================
def ytdlp_transcript(video_url: str) -> str | None:
    try:
        ydl_opts = {
            "skip_download": True,
            "writesubtitles": True,
            "writeautomaticsub": True,
            "quiet": True
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            subs = info.get("subtitles") or info.get("automatic_captions")
            if not subs:
                return None

            for lang in ["en", "en-US", "en-GB"]:
                if lang in subs:
                    link = subs[lang][0]["url"]
                    break
            else:
                first_lang = list(subs.keys())[0]
                link = subs[first_lang][0]["url"]

            response = requests.get(link, timeout=10)
            response.raise_for_status()

            if "application/json" in response.headers.get("Content-Type", ""):
                data = response.json()
                text = " ".join(
                    seg["utf8"]
                    for event in data.get("events", [])
                    if "segs" in event
                    for seg in event["segs"]
                )
            else:
                text = response.text

            return clean_transcript(text)
    except Exception:
        return None

# ================================
# Main Transcript Function
# ================================
@lru_cache(maxsize=20)
def get_transcript(video_id_or_url: str) -> str | None:
    """
    Attempts to fetch transcript via multiple methods:
    1. YouTubeTranscriptApi
    2. yt-dlp subtitles
    3. Pytube captions
    """
    # Determine if input is video ID or full URL
    video_url = f"https://www.youtube.com/watch?v={video_id_or_url}" if len(video_id_or_url) == 11 else video_id_or_url

    # --- 1. YouTubeTranscriptApi ---
    try:
        video_id = video_id_or_url if len(video_id_or_url) == 11 else None
        transcripts = YouTubeTranscriptApi.list_transcripts(video_id)
        try:
            transcript = transcripts.find_manually_created_transcript(["en"])
        except:
            transcript = transcripts.find_generated_transcript(["en"])
        data = transcript.fetch()
        text = " ".join([t["text"] for t in data])
        return clean_transcript(text)
    except Exception:
        pass

    # --- 2. yt-dlp fallback ---
    text = ytdlp_transcript(video_url)
    if text:
        return text

    # --- 3. pytube fallback ---
    text = pytube_transcript(video_url)
    if text:
        return text

    return None
