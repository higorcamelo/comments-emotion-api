import pandas as pd
import re
from datetime import datetime
import emoji

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

# Função para calcular um escore de spam
def spam_score(text):
    score = 0
    if contains_links(text):
        score += 1
    if len(re.findall(r'(.)\1{5,}', text)) > 0:  # caracteres repetidos 6 vezes ou mais
        score += 1
    return score

# Nova métrica: Número de palavras no comentário
def word_count(text):
    return len(text.split())

# Nova métrica: Número de caracteres especiais (!, ?, *, etc.)
def special_char_count(text):
    return len(re.findall(r'[!@#$%^&*()_+=\[\]{};:"\',.<>?/\\|]', text))

# Nova métrica: Proporção de letras maiúsculas
def uppercase_ratio(text):
    if len(text) == 0:
        return 0
    return sum(1 for c in text if c.isupper()) / len(text)

# Lendo o CSV original
df = pd.read_csv('./scraping/youtube_comments.csv')

# Adicionando colunas adicionais
df['comment_length'] = df['text'].astype(str).apply(len)
df['word_count'] = df['text'].astype(str).apply(word_count)
df['contains_question'] = df['text'].astype(str).apply(contains_question)
df['contains_links'] = df['text'].astype(str).apply(contains_links)
df['mentions'] = df['text'].astype(str).apply(extract_mentions)
df['posted_hour'] = df['published_at'].astype(str).apply(get_posted_hour)
df['contains_emojis'] = df['text'].astype(str).apply(contains_emojis)
df['spam_score'] = df['text'].astype(str).apply(spam_score)
df['special_char_count'] = df['text'].astype(str).apply(special_char_count)
df['uppercase_ratio'] = df['text'].astype(str).apply(uppercase_ratio)

# Salvando o CSV modificado
df.to_csv('youtube_comments_2.csv', index=False)
print("Arquivo 'youtube_comments_2.csv' gerado com as novas colunas.")
