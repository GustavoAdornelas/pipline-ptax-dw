import json
import requests
from pydantic import BaseModel, Field, ValidationError

# 1. Contrato de dados (nosso fiscal na alfândega)
class CotacaoDolar(BaseModel):
    cotacaoCompra: float = Field(gt=0)
    cotacaoVenda: float = Field(gt=0)
    dataHoraCotacao: str = Field(min_length=10)

url = (
    "https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/"
    "CotacaoDolarPeriodo(dataInicial=@dataInicial,dataFinalCotacao=@dataFinalCotacao)?"
    "@dataInicial='11-01-2026'&@dataFinalCotacao='11-23-2026'&$format=json"
)

# 2. Extração via HTTP
resposta = requests.get(url, timeout=10)
resposta.raise_for_status()

dados = resposta.json()
cotacoes_brutas = dados.get("value") or []
cotacoes_validadas = []

# 3. Validação linha a linha
for item in cotacoes_brutas:
    try:
        cotacao = CotacaoDolar(**item)
        cotacoes_validadas.append(cotacao.model_dump())
    except ValidationError as erro:
        print(f"Dado inválido descartado: {item} | Motivo: {erro}")

# 4. Salvando os dados aprovados em JSON
with open("cotacoes_validadas.json", "w", encoding="utf-8") as arquivo:
    json.dump(cotacoes_validadas, arquivo, indent=4, ensure_ascii=False)

print(f"sucesso! {len(cotacoes_validadas)} cotações validadas e salvas.")