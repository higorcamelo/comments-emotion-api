from pysentimiento import create_analyzer
import pandas as pd
from tqdm import tqdm

# Carregar modelos
sentiment_analyzer = create_analyzer(task="sentiment", lang="en")
emotion_analyzer = create_analyzer(task="emotion", lang="en")
hate_analyzer = create_analyzer(task="hate_speech", lang="en")

# Ativar barra de progresso para o pandas
tqdm.pandas()

def analyze_comment(text):
    sentiment = sentiment_analyzer.predict(text)
    emotion = emotion_analyzer.predict(text)

    if sentiment.output == "NEG":
        hate = hate_analyzer.predict(text)
        return pd.Series([
            sentiment.output,
            sentiment.probas["POS"],
            sentiment.probas["NEU"],
            sentiment.probas["NEG"],
            emotion.output,
            hate.output
        ])
    else:
        return pd.Series([
            sentiment.output,
            sentiment.probas["POS"],
            sentiment.probas["NEU"],
            sentiment.probas["NEG"],
            emotion.output,
            None
        ])

# Aplicar no DataFrame
comments_df[[
    "sentiment", "prob_pos", "prob_neu", "prob_neg",
    "emotion", "hate_speech"
]] = comments_df["text_original"].progress_apply(analyze_comment)
