import requests
from bs4 import BeautifulSoup

# O endereço do "serviço de entrega" RSS do G1 Tecnologia
url_rss_g1 = 'https://g1.globo.com/dynamo/tecnologia/rss2.xml'

print(f"Acessando o Feed RSS do G1 Tecnologia...")

try:
    # Usamos o requests, nossa ferramenta mais simples e rápida
    response = requests.get(url_rss_g1)
    response.raise_for_status() # Isso vai gerar um erro se o site estiver fora do ar

    print("Feed acessado com sucesso! Lendo as notícias...")

    # Usamos o BeautifulSoup para ler o conteúdo, especificando que é um arquivo 'xml'
    soup = BeautifulSoup(response.content, 'xml')

    # Em um RSS, cada notícia fica dentro de uma tag chamada <item>
    noticias = soup.find_all('item')

    print("\n--- ÚLTIMAS NOTÍCIAS DE TECNOLOGIA (G1) ---")

    # Agora, para cada notícia, pegamos o título, o link e a descrição
    for noticia in noticias:
        titulo = noticia.find('title').text
        link = noticia.find('link').text
        descricao = noticia.find('description').text
        
        print(f"\n■ TÍTULO: {titulo}")
        # A descrição já vem pronta no RSS!
        print(f"  DESCRIÇÃO: {descricao}")
        print(f"  LINK: {link}")

except requests.exceptions.RequestException as e:
    print(f"Ocorreu um erro ao acessar o feed: {e}")