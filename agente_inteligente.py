import requests
from bs4 import BeautifulSoup

# --- O CÉREBRO DO NOSSO AGENTE ---
# Esta é a lista de palavras que definem o que é "relevante" para nós.
PALAVRAS_CHAVE = [
    'ataque cibernético', 'hacker', 'vazamento dados', 
    'ransomware', 'phishing', 'invasão de dados', 'falha de segurança', 
    'vulnerabilidade', 'ddos', 'malware', 'dados'
]
# ---------------------------------

url_rss_g1 = 'https://g1.globo.com/dynamo/tecnologia/rss2.xml'

print("Iniciando Agente Inteligente...")
print(f"Buscando notícias no Feed RSS: {url_rss_g1}")

try:
    response = requests.get(url_rss_g1)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, 'xml')
    noticias = soup.find_all('item')
    
    print(f"{len(noticias)} notícias encontradas. Analisando relevância...")

    # Uma lista para guardar apenas as notícias que nos interessam
    noticias_relevantes = []

    for noticia in noticias:
        titulo = noticia.find('title').text
        link = noticia.find('link').text
        descricao = noticia.find('description').text
        
        # Combinamos título e descrição para fazer uma busca completa
        texto_completo_para_analise = (titulo + " " + descricao).lower()
        
        # O agente verifica se alguma palavra-chave está no texto
        if any(palavra in texto_completo_para_analise for palavra in PALAVRAS_CHAVE):
            # Se encontrou, guardamos a notícia como um "dicionário" organizado
            noticia_organizada = {
                'titulo': titulo,
                'link': link,
                'resumo': descricao
            }
            noticias_relevantes.append(noticia_organizada)

    print("\n--- ANÁLISE CONCLUÍDA ---")

    if noticias_relevantes:
        print(f"Encontradas {len(noticias_relevantes)} notícias relevantes sobre segurança:\n")
        # Imprimimos de forma mais bonita
        for i, noticia_filtrada in enumerate(noticias_relevantes, start=1):
            print(f"--- Notícia Relevante #{i} ---")
            print(f"Título: {noticia_filtrada['titulo']}")
            print(f"Resumo: {noticia_filtrada['resumo']}")
            print(f"Link: {noticia_filtrada['link']}\n")
    else:
        print("Nenhuma notícia relevante sobre segurança encontrada nas últimas postagens.")

except requests.exceptions.RequestException as e:
    print(f"Ocorreu um erro ao acessar o feed: {e}")