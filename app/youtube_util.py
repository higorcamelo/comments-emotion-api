import googleapiclient.discovery
import pandas as pd
from dotenv import load_dotenv
import os
import time

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

DEVELOPER_KEY = os.getenv("YOUTUBE_API_KEY")
if DEVELOPER_KEY is None:
    raise ValueError("Erro: YOUTUBE_API_KEY não foi encontrado no arquivo .env.")
else:
    print("YOUTUBE_API_KEY carregado com sucesso.")

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
                'text_display': top_comment['textDisplay'],
                'text_original': top_comment['textOriginal'],
                'is_reply': False,
                'parent_author': None,
                'parent_comment': None
            })
            total_collected += 1

            # Se houver respostas, buscar também
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
                        'text_display': reply_snippet['textDisplay'],
                        'text_original': reply_snippet['textOriginal'],
                        'is_reply': True,
                        'parent_author': top_comment['authorDisplayName'],
                        'parent_comment': top_comment['textOriginal']
                    })
                    total_collected += 1

        next_page_token = response.get("nextPageToken")
        if not next_page_token:
            break

    df = pd.DataFrame(comments)
    print(f"Total de comentários coletados (incluindo respostas): {len(df)}")
    return df


# Execução direta do script
if __name__ == "__main__":
    video_id = "ulGEcgH0eIU"  # Substitua pelo ID desejado
    comments_df = get_youtube_comments(video_id)
    print(comments_df.head())
    print(f"Total de comentários coletados: {len(comments_df)}")
    # Salvar em CSV
    comments_df.to_csv(f"comments_{video_id}.csv", index=False)
    print(f"Comentários salvos em comments_{video_id}.csv")
