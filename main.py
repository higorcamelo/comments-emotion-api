from fastapi import FastAPI, HTTPException
from app.youtube_util import get_youtube_comments
from app.sentiments import analyze_sentiments
import pandas as pd
import logging

app = FastAPI(title="YouTube Comment Analysis API")

@app.get("/")
def read_root():
    return {"message": "API de análise de comentários do YouTube ativa!"}

@app.get("/analyze/youtube/{video_id}")
def analyze_youtube_video(video_id: str):
    try:
        # Coleta os comentários do vídeo
        comments_df = get_youtube_comments(video_id)
        if comments_df.empty:
            raise HTTPException(status_code=404, detail="Nenhum comentário encontrado para esse vídeo.")

        # Executa a análise com pysentimiento
        analyzed_df = analyze_sentiments(comments_df)

        # Adiciona a coluna com o texto original (se necessário)
        analyzed_df["text"] = comments_df["text_original"]

        # Gera um panorama geral (agregando os resultados)
        sentiment_summary = analyzed_df["sentiment"].value_counts().to_dict()
        emotion_summary = analyzed_df["emotion"].value_counts().to_dict()
        hate_series = analyzed_df["hate_speech"].fillna("Nenhum")
        hate_summary = hate_series.value_counts().to_dict()

        # Prepara os dados para retorno: converte o DataFrame em lista de dicionários
        comments_list = analyzed_df[[
            "text", "sentiment", "prob_positivo", "prob_neutro",
            "prob_negativo", "emotion", "hate_speech"
        ]].to_dict(orient="records")

        return {
            "video_id": video_id,
            "total_comments": len(analyzed_df),
            "panorama": {
                "sentiments": sentiment_summary,
                "emotions": emotion_summary,
                "hate_speech": hate_summary
            },
            "comentarios": comments_list
        }
    except Exception as e:
        logging.exception("Erro durante a análise do vídeo.")
        raise HTTPException(status_code=500, detail=str(e))
