
import csv
from pathlib import Path

import requests
from bs4 import BeautifulSoup

# Página oficial do INCA utilizada no projeto
url = "https://www.gov.br/inca/pt-br/assuntos/cancer/numeros/estimativa"

# Obter o conteúdo da página
resposta = requests.get(url, timeout=30)
resposta.raise_for_status()

# Extrair o conteúdo HTML com Beautiful Soup
soup = BeautifulSoup(resposta.text, "html.parser")

# Selecionar o conteúdo principal da página
conteudo = soup.find("main") or soup

dados = []

for elemento in conteudo.find_all(["h1", "h2", "h3", "p"]):
    texto = elemento.get_text(" ", strip=True)

    if texto:
        dados.append({
            "tipo": elemento.name,
            "texto": texto
        })

# Salvar os dados extraídos na pasta data/raw
pasta_dados = Path(__file__).resolve().parent.parent / "data" / "raw"
pasta_dados.mkdir(parents=True, exist_ok=True)

arquivo_saida = pasta_dados / "conteudo_inca_web.csv"

with open(arquivo_saida, "w", newline="", encoding="utf-8-sig") as arquivo:
    escritor = csv.DictWriter(arquivo, fieldnames=["tipo", "texto"])
    escritor.writeheader()
    escritor.writerows(dados)

print(f"Extração concluída: {len(dados)} registros.")
print(f"Arquivo salvo em: {arquivo_saida}")
