import requests
from bs4 import BeautifulSoup
import datetime
import traceback

# --- CONFIGURAÇÕES COM CAMINHOS 100% CORRIGIDOS ---
# O novo endereço base do nosso projeto
CAMINHO_BASE = r'C:\agente_noticias' 
# Construímos os caminhos completos a partir da base
CAMINHO_RELATORIO = CAMINHO_BASE + r'\relatorio.html'
CAMINHO_LOG_ERROS = CAMINHO_BASE + r'\log_erros_final.txt'
# ----------------------------------------------------

FONTES_RSS = {
    'G1 Tecnologia': 'https://g1.globo.com/dynamo/tecnologia/rss2.xml',
    'CERT.br': 'https://www.cert.br/rss/certbr-rss.xml',
    'Olhar Digital': 'https://olhardigital.com.br/seguranca/feed/'
}
PALAVRAS_CHAVE = ['ataque', 'cibernético', 'hacker', 'vazamento', 'dados', 'ransomware', 'phishing', 'golpe', 'invasão', 'falha', 'vulnerabilidade', 'ddos', 'malware']

try:
    print("Iniciando Agente Versão Final...")
    todas_as_noticias_relevantes = []

    for nome_fonte, url_rss in FONTES_RSS.items():
        print(f"Acessando fonte: {nome_fonte}...")
        response = requests.get(url_rss, timeout=15)
        response.raise_for_status()
        
        # (O resto do código continua exatamente igual)
        soup = BeautifulSoup(response.content, 'xml')
        noticias = soup.find_all('item')
        for noticia in noticias:
            titulo = noticia.find('title').text
            link = noticia.find('link').text
            descricao_tag = noticia.find('description')
            resumo = descricao_tag.text if descricao_tag else "Sem resumo disponível."
            texto_completo_para_analise = (titulo + " " + resumo).lower()
            if any(palavra in texto_completo_para_analise for palavra in PALAVRAS_CHAVE):
                noticia_organizada = {
                    'fonte': nome_fonte, 'titulo': titulo, 'link': link, 'resumo': resumo.strip()
                }
                if not any(n['link'] == noticia_organizada['link'] for n in todas_as_noticias_relevantes):
                    todas_as_noticias_relevantes.append(noticia_organizada)
    
    print(f"Análise concluída. Gerando relatório em: {CAMINHO_RELATORIO}")
    
    # Geração do HTML
    agora = datetime.datetime.now()
    timestamp = agora.strftime("%d/%m/%Y às %H:%M:%S")
    # (O código HTML completo vai aqui, exatamente como antes)
    html_content = f"""
    <!DOCTYPE html><html lang="pt-BR"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Relatório de Cibersegurança</title><style>body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; background-color: #f4f4f9; }}.container {{ max-width: 800px; margin: auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }}h1, h2 {{ color: #333; }}.report-header {{ text-align: center; border-bottom: 2px solid #eee; padding-bottom: 10px; margin-bottom: 20px; }}.news-item {{ border-bottom: 1px solid #eee; padding: 15px 0; }}.news-item:last-child {{ border-bottom: none; }}.news-item h3 {{ margin: 0 0 10px 0; }}.news-item a {{ color: #007BFF; text-decoration: none; }}.news-item a:hover {{ text-decoration: underline; }}.news-item p {{ margin: 5px 0 0 0; color: #555; }}.source-tag {{ background-color: #007BFF; color: white; padding: 3px 8px; font-size: 12px; border-radius: 4px; display: inline-block; margin-left: 10px; }}</style></head><body><div class="container"><div class="report-header"><h1>Relatório de Cibersegurança</h1><p>Gerado em: {timestamp}</p></div>
    """
    if todas_as_noticias_relevantes:
        for noticia in todas_as_noticias_relevantes:
            html_content += f"""<div class="news-item"><h3><a href="{noticia['link']}" target="_blank">{noticia['titulo']}</a> <span class="source-tag">{noticia['fonte']}</span></h3><p>{noticia['resumo']}</p></div>"""
    else:
        html_content += "<p>Nenhuma notícia relevante sobre segurança foi encontrada.</p>"
    html_content += """</div></body></html>"""

    with open(CAMINHO_RELATORIO, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print("Relatório criado com sucesso!")

except Exception as e:
    with open(CAMINHO_LOG_ERROS, 'w', encoding='utf-8') as f:
        f.write(f"Ocorreu um erro em: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
        f.write("="*40 + "\n")
        f.write(traceback.format_exc())
    print(f"ERRO! Detalhes salvos em '{CAMINHO_LOG_ERROS}'")