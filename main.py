from fastapi import FastAPI, HTTPException
from app.youtube_util import get_youtube_comments
from app.sentiments import analyze_sentiments
from pydantic import BaseModel
import pandas as pd

# Criação do app FastAPI
app = FastAPI()

# Modelo da resposta de análise
class CommentAnalysisResult(BaseModel):
    text: str
    sentimento: str
    prob_positivo: float
    prob_neutro: float
    prob_negativo: float
    emocao: str
    discurso_odio: bool

@app.get("/")
def read_root():
    return {"message": "API de análise de comentários do YouTube ativa!"}

@app.get("/analyze/youtube/{video_id}", response_model=list[CommentAnalysisResult])
def analyze_youtube_video(video_id: str):
    try:
        # Coleta os comentários do vídeo
        comments_df = get_youtube_comments(video_id)

        # Verifica se encontrou algum comentário
        if comments_df.empty:
            raise HTTPException(status_code=404, detail="Nenhum comentário encontrado.")

        # Executa a análise de sentimentos, emoções e discurso de ódio
        result_df = analyze_sentiments(comments_df)

        # Adiciona a coluna com os textos originais
        result_df["text"] = comments_df["text_original"]

        # Seleciona as colunas para retorno
        selected_columns = [
            "text", "sentimento", "prob_positivo", "prob_neutro",
            "prob_negativo", "emocao", "discurso_odio"
        ]

        # Converte para dicionário e retorna como JSON
        return result_df[selected_columns].to_dict(orient="records")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
