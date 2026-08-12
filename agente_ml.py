import requests
from bs4 import BeautifulSoup
import datetime
import traceback
from collections import Counter
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import base64

# --- CONFIGURAÇÕES DO AGENTE ---
CAMINHO_BASE = r'C:\agente_noticias'
CAMINHO_RELATORIO = CAMINHO_BASE + r'\relatorio_final.html'
CAMINHO_GRAFICO = CAMINHO_BASE + r'\grafico_categorias.png'
CAMINHO_LOG_ERROS = CAMINHO_BASE + r'\log_erros.txt'

FONTES_RSS = {
    'G1 Tecnologia': 'https://g1.globo.com/dynamo/tecnologia/rss2.xml',
    'CERT.br': 'https://www.cert.br/rss/certbr-rss.xml',
    'Olhar Digital': 'https://olhardigital.com.br/seguranca/feed/'
}
PALAVRAS_CHAVE = ['ataque', 'cibernético', 'hacker', 'vazamento', 'dados', 'ransomware', 'phishing', 'golpe', 'invasão', 'falha', 'vulnerabilidade', 'ddos', 'malware']

# --- MÓDULO DE IA ---
print("Treinando o modelo de IA...")
textos_treino = [ "empresa sofre com ataque de ransomware e dados são criptografados e sequestrados", "milhões de usuários têm senhas e emails expostos em vazamento de dados massivo", "novo golpe de phishing usa nome de banco para roubar informações de cartão de crédito", "site do governo fica fora do ar após intenso ataque ddos", "especialistas descobrem grave falha de segurança em aplicativo popular", "grupo hacker exige resgate em bitcoin após ataque de ransomware", "informações pessoais de clientes vazaram após invasão a servidor", "cuidado com email falso que tenta te enganar para clicar em link malicioso de phishing", ]
categorias_treino = [ "Ransomware", "Vazamento de Dados", "Phishing", "Ataque DDoS", "Falha de Segurança", "Ransomware", "Vazamento de Dados", "Phishing" ]
modelo_ia = Pipeline([('vectorizer', TfidfVectorizer()), ('classifier', MultinomialNB())])
modelo_ia.fit(textos_treino, categorias_treino)
print("Modelo de IA treinado.")

try:
    print("Iniciando Agente Final...")
    todas_as_noticias_relevantes = []

    for nome_fonte, url_rss in FONTES_RSS.items():
        print(f"Acessando fonte: {nome_fonte}...")
        response = requests.get(url_rss, timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'xml')
        noticias = soup.find_all('item')
        
        for noticia in noticias:
            titulo = noticia.find('title').text; link = noticia.find('link').text; descricao_tag = noticia.find('description')
            resumo = descricao_tag.text if descricao_tag else "Sem resumo."; texto_para_analise = (titulo + " " + resumo).lower()
            if any(palavra in texto_para_analise for palavra in PALAVRAS_CHAVE):
                categoria_prevista = modelo_ia.predict([texto_para_analise])[0]
                noticia_organizada = {'fonte': nome_fonte, 'titulo': titulo, 'link': link, 'resumo': resumo.strip(), 'categoria': categoria_prevista}
                if not any(n['link'] == noticia_organizada['link'] for n in todas_as_noticias_relevantes):
                    todas_as_noticias_relevantes.append(noticia_organizada)
    
    # --- MÓDULO DE VISUALIZAÇÃO E ANÁLISE ---
    grafico_html = ""
    resumo_grafico_html = ""
    if todas_as_noticias_relevantes:
        print("Agregando dados e gerando gráfico...")
        categorias_encontradas = [noticia['categoria'] for noticia in todas_as_noticias_relevantes]
        contagem_categorias = Counter(categorias_encontradas)
        total_noticias = len(categorias_encontradas)
        if total_noticias > 0:
            categoria_principal, contagem_principal = contagem_categorias.most_common(1)[0]; percentual = (contagem_principal / total_noticias) * 100
            resumo_grafico_html = f"""<div class="chart-summary"><p>Analisando um total de <strong>{total_noticias}</strong> incidentes reportados, a categoria predominante foi <strong>"{categoria_principal}"</strong>, representando <strong>{percentual:.1f}%</strong> do total de notícias classificadas.</p></div>"""
        
        fig, ax = plt.subplots(figsize=(10, 7), subplot_kw=dict(aspect="equal")); wedges, texts, autotexts = ax.pie(contagem_categorias.values(), autopct='%1.1f%%', startangle=90); ax.legend(wedges, contagem_categorias.keys(), title="Categorias", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1)); plt.setp(autotexts, size=10, weight="bold", color="white"); ax.set_title("Distribuição de Tipos de Incidentes Reportados", fontsize=16, pad=20); plt.savefig(CAMINHO_GRAFICO, bbox_inches='tight')
        
        print("Codificando o gráfico para embutir no HTML...")
        with open(CAMINHO_GRAFICO, "rb") as image_file:
            imagem_base64 = base64.b64encode(image_file.read()).decode('utf-8')
        data_uri = f"data:image/png;base64,{imagem_base64}"
        grafico_html = f'<h2>Resumo Visual</h2><img class="report-graphic" src="{data_uri}" alt="Gráfico de Categorias">'

    # --- GERAÇÃO DO RELATÓRIO HTML FINAL ---
    print("Gerando relatório final portátil...")
    agora = datetime.datetime.now()
    timestamp = agora.strftime("%d/%m/%Y às %H:%M:%S")
    html_content = f"""
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Relatório de Cibersegurança</title>
        <style>
            body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; margin: 0; padding: 20px; background-color: #f4f4f9; }}
            .container {{ max-width: 800px; margin: auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 0 15px rgba(0,0,0,0.1); }}
            h1, h2 {{ color: #333; border-bottom: 1px solid #eee; padding-bottom: 10px; }}
            .report-header {{ text-align: center; border-bottom: 2px solid #ddd; padding-bottom: 10px; margin-bottom: 20px; }}
            .report-graphic {{ max-width: 700px; width: 100%; height: auto; display: block; margin: 20px auto; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }}
            .chart-summary {{ text-align: center; padding: 10px; margin: -10px auto 20px auto; background-color: #e9f5ff; border-left: 5px solid #007BFF; max-width: 90%; font-size: 1.1em; }}
            .news-item {{ border-bottom: 1px solid #eee; padding: 20px 0; }}
            .news-item:last-child {{ border-bottom: none; }}
            .news-item h3 {{ margin: 0 0 10px 0; font-size: 18px; }}
            .news-item a {{ color: #0056b3; text-decoration: none; }}
            .news-item a:hover {{ text-decoration: underline; }}
            .news-item p {{ margin: 5px 0 0 0; color: #555; line-height: 1.7; text-align: justify; }}
            .tag {{ color: white; padding: 4px 9px; font-size: 12px; font-weight: bold; border-radius: 4px; display: inline-block; margin-left: 8px; vertical-align: middle; }}
            .source-tag {{ background-color: #007BFF; }}
            .category-tag {{ background-color: #28a745; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="report-header">
                <h1>Relatório de Cibersegurança</h1>
                <p>Gerado em: {timestamp}</p>
            </div>
            {grafico_html}
            {resumo_grafico_html}
            <h2>Notícias Detalhadas</h2>
    """
    if todas_as_noticias_relevantes:
        for noticia in todas_as_noticias_relevantes:
            html_content += f"""<div class="news-item"><h3><a href="{noticia['link']}" target="_blank">{noticia['titulo']}</a><span class="tag source-tag">{noticia['fonte']}</span><span class="tag category-tag">{noticia['categoria']}</span></h3><p>{noticia['resumo']}</p></div>"""
    else:
        html_content += "<p>Nenhuma notícia relevante sobre segurança foi encontrada.</p>"
    html_content += """</div></body></html>"""

    with open(CAMINHO_RELATORIO, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print("Relatório final foi criado com sucesso!")

except Exception as e:
    with open(CAMINHO_LOG_ERROS, 'w', encoding='utf-8') as f:
        f.write(f"Ocorreu um erro em: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
        f.write("="*40 + "\n")
        f.write(traceback.format_exc())
    print(f"ERRO! Detalhes salvos em '{CAMINHO_LOG_ERROS}'")