from pysentimiento import create_analyzer
import pandas as pd
import logging

# Configura logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Carrega os modelos (usando "pt" para português)
sentiment_analyzer = create_analyzer(task="sentiment", lang="pt")
emotion_analyzer = create_analyzer(task="emotion", lang="pt")
hate_analyzer = create_analyzer(task="hate_speech", lang="pt")

def analyze_comment(text):
    try:
        sentiment = sentiment_analyzer.predict(text)
        emotion = emotion_analyzer.predict(text)

        # Garante que o output da emoção seja sempre uma string:
        if isinstance(emotion.output, list):
            emotion_str = ", ".join(emotion.output)
        else:
            emotion_str = emotion.output

        hate = None
        if sentiment.output == "NEG":
            hate_pred = hate_analyzer.predict(text)
            if isinstance(hate_pred.output, list):
                hate = ", ".join(hate_pred.output)
            else:
                hate = hate_pred.output

        return pd.Series([
            sentiment.output,
            sentiment.probas.get("POS", 0),
            sentiment.probas.get("NEU", 0),
            sentiment.probas.get("NEG", 0),
            emotion_str,
            hate
        ])
    except Exception as e:
        logging.warning(f"Erro ao analisar comentário: {text[:30]}... -> {e}")
        # Retorna valores default para evitar problemas
        return pd.Series(["Erro", 0, 0, 0, "Erro", None])

def analyze_sentiments(df: pd.DataFrame) -> pd.DataFrame:
    logging.info("Iniciando análise de sentimentos, emoções e discurso de ódio...")
    results = df["text_original"].apply(analyze_comment)
    results.columns = [
        "sentiment", "prob_positivo", "prob_neutro",
        "prob_negativo", "emotion", "hate_speech"
    ]
    result_df = pd.concat([df, results], axis=1)
    logging.info("Análises concluídas.")
    return result_df
