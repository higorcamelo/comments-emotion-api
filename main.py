#from fastapi import FastAPI, Query
#from youtube_scraper import get_youtube_client, get_comments
#from sentiment_analyzer import analyze_comments
from collections import Counter
import os

app = FastAPI()

API_KEY = os.getenv("YOUTUBE_API_KEY")

@app.get("/analyze")
def analyze_video(video_id: str):
    youtube = get_youtube_client(API_KEY)
    comments = get_comments(youtube, video_id)
    if not comments:
        return {"error": "Nenhum comentário encontrado ou vídeo inválido."}

    analyzed = analyze_comments(comments)
    summary = Counter([c["sentiment"]["label"] for c in analyzed])

    return {
        "video_id": video_id,
        "total_comments": len(analyzed),
        "sentiment_summary": dict(summary),
        "comments": analyzed
    }