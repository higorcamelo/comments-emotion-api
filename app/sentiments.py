from pysentimiento import create_analyzer
import pandas as pd
import logging

# Configura logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Carrega os modelos
sentiment_analyzer = create_analyzer(task="sentiment", lang="pt")
emotion_analyzer = create_analyzer(task="emotion", lang="pt")
hate_analyzer = create_analyzer(task="hate_speech", lang="pt")

# Traduções
SENTIMENT_TRANSLATION = {
    "POS": "Positivo",
    "NEU": "Neutro",
    "NEG": "Negativo"
}

EMOTION_TRANSLATION = {
    "admiration": "Admiração",
    "amusement": "Diversão",
    "anger": "Raiva",
    "annoyance": "Irritação",
    "approval": "Aprovação",
    "caring": "Cuidado",
    "confusion": "Confusão",
    "curiosity": "Curiosidade",
    "desire": "Desejo",
    "disappointment": "Decepção",
    "disapproval": "Desaprovação",
    "disgust": "Nojo",
    "embarrassment": "Constrangimento",
    "excitement": "Empolgação",
    "fear": "Medo",
    "gratitude": "Gratidão",
    "grief": "Luto",
    "joy": "Alegria",
    "love": "Amor",
    "nervousness": "Nervosismo",
    "optimism": "Otimismo",
    "pride": "Orgulho",
    "realization": "Percepção",
    "relief": "Alívio",
    "remorse": "Remorso",
    "sadness": "Tristeza",
    "surprise": "Surpresa",
    "neutral": "Neutro"
}

HATE_TRANSLATION = {
    "sexism": "Sexismo",
    "body": "Ataque ao corpo",
    "racism": "Racismo",
    "ideology": "Ideologia",
    "homophobia": "Homofobia"
}

def analyze_comment(text):
    try:
        sentiment = sentiment_analyzer.predict(text)
        emotion = emotion_analyzer.predict(text)

        sentimento = SENTIMENT_TRANSLATION.get(sentiment.output, "Desconhecido")
        emocao = EMOTION_TRANSLATION.get(emotion.output, "Outro")

        odio = None
        if sentiment.output == "NEG":
            hate = hate_analyzer.predict(text)

            if isinstance(hate.output, list):
                odio = ", ".join([HATE_TRANSLATION.get(x, "Desconhecido") for x in hate.output])
            else:
                odio = HATE_TRANSLATION.get(hate.output, "Desconhecido")

        return pd.Series([sentimento, emocao, odio])

    except Exception as e:
        logging.error(f"Erro ao analisar comentário: {e}")
        return pd.Series(["Erro", "Erro", "Erro"])
