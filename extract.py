import requests

url = (
    "https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/"
    "CotacaoDolarPeriodo(dataInicial=@dataInicial,dataFinalCotacao=@dataFinalCotacao)?"
    "@dataInicial='11-01-2026'&@dataFinalCotacao='11-23-2026'&$format=json"
)

resposta = requests.get(url, timeout=10)
resposta.raise_for_status()

print("URL final chamada:", resposta.url)
print("Resposta bruta:", resposta.json())