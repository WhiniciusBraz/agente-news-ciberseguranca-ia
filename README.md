# 🛡️ Agente Autônomo de Inteligência em Cibersegurança

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Scikit-Learn](https://img.shields.io/badge/scikit--learn-%23F7931E.svg?style=for-the-badge&logo=scikit-learn&logoColor=white)
![Status](https://img.shields.io/badge/Status-Concluído-success?style=for-the-badge)

Este projeto foi desenvolvido como meu **Trabalho de Conclusão de Curso (TCC) em Sistemas de Informação**. Trata-se de um pipeline automatizado que coleta, analisa e classifica notícias de incidentes de cibersegurança em tempo real utilizando Machine Learning.

## 📌 O Problema que este Sistema Resolve
Analistas de segurança da informação perdem horas diárias monitorando portais de notícias para identificar novas ameaças. Este agente automatiza a varredura de feeds RSS, filtra o ruído e utiliza Inteligência Artificial para classificar o tipo de ataque (DDoS, Ransomware, Phishing, etc.), gerando um relatório gerencial em HTML de forma 100% autônoma.

## 🚀 Principais Funcionalidades
* **Web Scraping Automatizado:** Extração de dados de fontes confiáveis (G1 Tecnologia, CERT.br, Olhar Digital) via RSS.
* **Filtro Inteligente de Relevância:** Varredura contextual baseada em palavras-chave do nicho de segurança.
* **Classificação com IA (NLP):** Modelo treinado com algoritmo `Multinomial Naive Bayes` (via Scikit-Learn) que lê os textos e prevê a categoria do incidente reportado.
* **Geração Automática de Relatórios:** Criação de um dashboard portátil em formato `.html`, com gráficos estatísticos gerados via Matplotlib e convertidos em Base64 para visualização offline.

## 🧠 Arquitetura e Tecnologias Utilizadas
A solução foi construída inteiramente em Python, com foco em automação e análise de dados:
* **Linguagem:** Python 3.x
* **Extração de Dados:** `requests`, `BeautifulSoup` (bs4)
* **Machine Learning / NLP:** `scikit-learn` (TfidfVectorizer, MultinomialNB)
* **Visualização de Dados:** `matplotlib`
* **Automação:** Scripts de lote (Batch `.bat`) para execução programada e rotinas de log.

## 🛠️ Como Executar o Projeto na sua Máquina

1. Clone este repositório:
   ```bash
   git clone [https://github.com/SeuUsuario/seu-repositorio.git](https://github.com/SeuUsuario/seu-repositorio.git)