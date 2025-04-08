import googleapiclient.discovery
import pandas as pd
from dotenv import load_dotenv
import os
import logging

# Configuração de logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Carrega variáveis do .env
load_dotenv()
DEVELOPER_KEY = os.getenv("YOUTUBE_API_KEY")

if not DEVELOPER_KEY:
    raise ValueError("Erro: YOUTUBE_API_KEY não encontrada no .env.")

def get_youtube_comments(video_id, max_comments=500):
    api_service_name = "youtube"
    api_version = "v3"

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=DEVELOPER_KEY
    )

    comments = []
    next_page_token = None
    total_collected = 0

    while total_collected < max_comments:
        request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=100,
            pageToken=next_page_token
        )
        response = request.execute()

        for item in response['items']:
            top_comment = item['snippet']['topLevelComment']['snippet']
            comment_id = item['snippet']['topLevelComment']['id']
            comments.append({
                'author': top_comment['authorDisplayName'],
                'published_at': top_comment['publishedAt'],
                'updated_at': top_comment['updatedAt'],
                'like_count': top_comment['likeCount'],
                'text_original': top_comment['textOriginal'],
                'is_reply': False,
                'parent_author': None,
                'parent_comment': None
            })
            total_collected += 1

            if item['snippet']['totalReplyCount'] > 0:
                replies_request = youtube.comments().list(
                    part="snippet",
                    parentId=comment_id,
                    maxResults=100
                )
                replies_response = replies_request.execute()

                for reply in replies_response.get('items', []):
                    reply_snippet = reply['snippet']
                    comments.append({
                        'author': reply_snippet['authorDisplayName'],
                        'published_at': reply_snippet['publishedAt'],
                        'updated_at': reply_snippet['updatedAt'],
                        'like_count': reply_snippet['likeCount'],
                        'text_original': reply_snippet['textOriginal'],
                        'is_reply': True,
                        'parent_author': top_comment['authorDisplayName'],
                        'parent_comment': top_comment['textOriginal']
                    })
                    total_collected += 1

        next_page_token = response.get("nextPageToken")
        if not next_page_token:
            break

    logging.info(f"Todas as operações realizadas com sucesso para o vídeo com ID: {video_id}")
    print(comments)
    return pd.DataFrame(comments)
