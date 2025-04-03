import pandas as pd
import re
from datetime import datetime
import emoji
import time
from transformers import pipeline

# Inicializa o pipeline de análise de sentimento
sentiment_analyzer = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")

# Função para verificar se o texto contém um ponto de interrogação
def contains_question(text):
    return '?' in text

# Função para verificar se o texto contém links
def contains_links(text):
    return bool(re.search(r'http[s]?://', text))

# Função para extrair menções (ex.: @usuario)
def extract_mentions(text):
    return ','.join(re.findall(r'@\w+', text))

# Função para extrair a hora do comentário a partir do timestamp ISO
def get_posted_hour(timestamp):
    try:
        dt = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
        return dt.hour
    except Exception:
        return None

# Função para verificar se o texto contém emojis
def contains_emojis(text):
    return any(char in emoji.EMOJI_DATA for char in text)

# Função dummy para calcular um escore de toxicidade
def toxicity_score(text):
    keywords = ['ruim', 'horrível', 'péssimo', 'odiar']
    score = sum(text.lower().count(word) for word in keywords)
    return score

# Função dummy para calcular um escore de spam
def spam_score(text):
    score = 0
    if contains_links(text):
        score += 1
    if len(re.findall(r'(.)\1{5,}', text)) > 0:  # caracteres repetidos 6 vezes ou mais
        score += 1
    return score

# Função para obter o sentimento do texto (limitando o texto para 512 caracteres, se necessário)
def get_sentiment(text):
    try:
        result = sentiment_analyzer(text[:512])
        label = result[0]['label']
        score = result[0]['score']
        return label, score
    except Exception as e:
        return None, None

# Lê o CSV original
df = pd.read_csv('/scraping/youtube_comments.csv')

# Adiciona colunas básicas derivadas
df['comment_length'] = df['text'].astype(str).apply(len)
df['contains_question'] = df['text'].astype(str).apply(contains_question)
df['contains_links'] = df['text'].astype(str).apply(contains_links)
df['mentions'] = df['text'].astype(str).apply(extract_mentions)
df['posted_hour'] = df['updated_at'].astype(str).apply(get_posted_hour)
df['contains_emojis'] = df['text'].astype(str).apply(contains_emojis)
df['toxicity_score'] = df['text'].astype(str).apply(toxicity_score)
df['spam_score'] = df['text'].astype(str).apply(spam_score)

# Adiciona colunas de análise de sentimento
# Se o dataset for muito grande, pode ser necessário aplicar com pausa para evitar timeouts
sentiment_labels = []
sentiment_scores = []
for text in df['text'].astype(str):
    label, score = get_sentiment(text)
    sentiment_labels.append(label)
    sentiment_scores.append(score)
    # Pequena pausa para não sobrecarregar (opcional)
    time.sleep(0.1)

df['sentiment_label'] = sentiment_labels
df['sentiment_score'] = sentiment_scores

# Salva o CSV modificado
df.to_csv('/mnt/data/output_sentiment.csv', index=False)
print("Arquivo 'output_sentiment.csv' gerado com as novas colunas!")
