# YouTube Comments Emotion Analysis API

Esse projeto foi um experimento para explorar algumas ideias que eu queria testar:  
coletar comentários do YouTube, analisar sentimentos, emoções e discurso de ódio usando a biblioteca `pysentimiento`, e expor tudo isso numa API simples com FastAPI.

A ideia inicial era criar algo que pudesse crescer para outras redes (Instagram, TikTok), mas a dificuldade com APIs e o tempo curto limitaram o foco só no YouTube.

Não foi um produto acabado, nem algo que eu pretendia lançar de imediato — era mais uma prova de conceito, um aprendizado prático com dados, APIs e modelos de linguagem.

O código está meio parado, sem interface visual ou armazenamento de dados, mas cumpre bem o papel de coletar e analisar comentários “na hora”.

Quem sabe um dia retomo para transformar em algo maior, com dashboard, histórico, suporte a mais fontes… ou talvez só fique aqui como registro do que já fiz (vai que meu SaaS de milhões está aqui).

---

## O que tem aqui

- Coleta de comentários e respostas do YouTube via API oficial  
- Análise de sentimento, emoção e discurso de ódio com `pysentimiento` (em português)  
- API REST básica com FastAPI para consultar as análises por vídeo  
- Logs simples para acompanhar o processo  

---

## Tecnologias e bibliotecas usadas

- Python 3.x  
- FastAPI  
- google-api-python-client (YouTube Data API v3)  
- pysentimiento  
- pandas  

## Ideias para o futuro

- Adicionar suporte a mais plataformas além do YouTube (talvez? Tiktok?).  
- Criar um dashboard visual — talvez em Streamlit, Dash, ou até mesmo desenvolvimento web tradicional — para que o usuário possa visualizar as análises de forma mais agradável.  
- Implementar armazenamento de dados: banco SQL ou NoSQL para manter histórico, consultar tendências ao longo do tempo e gerar relatórios.  
- Melhorar os modelos: talvez testar modelos próprios treinados em português, ou usar alternativas mais robustas para análise de sentimentos e emoções (preciso de um dataset enorme em português).  
- Explorar análise temporal dos sentimentos: como a percepção sobre um vídeo muda com o tempo? Dá pra fazer algo interessante?
- Realizar scrapings automáticos de novos vídeos e atualizar o dashboard (ou raspar todos os vídeos de todo mundo num único horário, tipo 1 da manhã)
- Criar alertas ou notificações automáticas, caso um vídeo comece a ter muitos comentários negativos ou discurso de ódio.  
- Pensar num modelo de SaaS, se um dia fizer sentido: planos, limites, autenticação, pagamentos e acesso a dashboards personalizados (provavelmente um plano com o dashboard normal e outro que dá acesso a API?).  
