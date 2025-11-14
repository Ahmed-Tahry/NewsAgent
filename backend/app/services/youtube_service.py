import os
import time
import random
import json
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import re
import yt_dlp
import whisper
import torch
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from langchain_google_genai import ChatGoogleGenerativeAI
from ..config import YOUTUBE_API_KEY, GEMINI_API_KEY

def summarize_text(text: str) -> str:
    """Summarize the given text using Gemini."""
    if not GEMINI_API_KEY:
        return "Error: GEMINI_API_KEY not set."
    
    try:
        if len(text.strip()) < 100:
            return "Text is too short to generate a meaningful summary."
        
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            temperature=0,
            google_api_key=GEMINI_API_KEY
        )
        
        prompt = f"""
Summarize the following text in concise, factual bullet points.
Text to summarize:
{text}

Summary in bullet points:
"""
        
        response = llm.invoke(prompt)
        summary = response.content.strip()
        return summary
        
    except Exception as e:
        return f"Error during summary generation: {str(e)}"

class AudioTranscriber:
    def __init__(self):
        self.whisper_model = None
        self.model_loaded = False
        
    def load_whisper_model(self):
        print("Attempting to load Whisper model...")
        try:
            self.whisper_model = whisper.load_model("base")
            self.model_loaded = True
            print("Whisper model loaded successfully.")
        except Exception as e:
            print(f"Failed to load Whisper model: {e}")
            self.model_loaded = False
    
    def transcribe_audio(self, audio_path: str) -> Optional[Dict]:
        print("Attempting to transcribe audio...")
        try:
            if not self.model_loaded:
                self.load_whisper_model()
                if not self.model_loaded:
                    print("Transcription failed because Whisper model is not loaded.")
                    return None
            
            print(f"Transcribing audio file at: {audio_path}")
            result = self.whisper_model.transcribe(
                audio_path,
                fp16=torch.cuda.is_available(),
            )
            print("Transcription successful.")
            return result
            
        except Exception as e:
            print(f"An error occurred during transcription: {e}")
            return None

class YouTubeService:
    def __init__(self):
        if not YOUTUBE_API_KEY:
            raise ValueError("YOUTUBE_API_KEY is not set in the configuration.")
        self.youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
        self.transcriber = AudioTranscriber()

    def fetch_videos_by_interests(self, interests: List[str], max_results: int = 5) -> List[Dict]:
        all_videos = []
        for interest in interests:
            try:
                search_response = self.youtube.search().list(
                    q=interest,
                    part="snippet",
                    type="video",
                    maxResults=max_results,
                    order="date",
                    publishedAfter=(datetime.utcnow() - timedelta(days=7)).isoformat() + "Z",
                ).execute()

                for item in search_response.get("items", []):
                    video_id = item["id"]["videoId"]
                    snippet = item["snippet"]
                    all_videos.append({
                        "video_id": video_id,
                        "title": snippet.get("title", ""),
                        "channel": snippet.get("channelTitle", ""),
                        "published_at": snippet.get("publishedAt", ""),
                        "thumbnail": snippet.get("thumbnails", {}).get("high", {}).get("url", ""),
                        "url": f"https://www.youtube.com/watch?v={video_id}",
                    })
                time.sleep(random.uniform(0.5, 1.5))
            except HttpError as e:
                print(f"An HTTP error {e.resp.status} occurred: {e.content}")
            except Exception as e:
                print(f"An error occurred while fetching videos for interest '{interest}': {e}")

        # Remove duplicates
        seen_ids = set()
        unique_videos = []
        for video in all_videos:
            if video["video_id"] not in seen_ids:
                unique_videos.append(video)
                seen_ids.add(video["video_id"])
        
        return unique_videos

    def extract_video_id(self, url: str) -> Optional[str]:
        patterns = [
            r'(?:youtube\.com\/watch\?v=|youtu\.be\/)([^&?\n]+)',
            r'youtube\.com\/embed\/([^&?\n]+)',
            r'youtube\.com\/v\/([^&?\n]+)'
        ]
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        return None

    def transcribe_video(self, video_url: str) -> Dict:
        video_id = self.extract_video_id(video_url)
        if not video_id:
            return {"status": "error", "message": "Invalid YouTube URL"}

        audio_dir = "backend/audio"
        os.makedirs(audio_dir, exist_ok=True)
        audio_path = os.path.join(audio_dir, f"{video_id}")

        if not os.path.exists(f"{audio_path}.mp3"):
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': audio_path,
                'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3'}],
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_url])

        transcription = self.transcriber.transcribe_audio(f"{audio_path}.mp3")
        if transcription:
            return {"status": "success", "transcript": transcription["text"]}
        else:
            return {"status": "error", "message": "Failed to transcribe audio"}

    def summarize_video(self, video_url: str) -> Dict:
        transcription_result = self.transcribe_video(video_url)
        if transcription_result["status"] != "success":
            return transcription_result
        
        summary = summarize_text(transcription_result["transcript"])
        return {"status": "success", "summary": summary}
