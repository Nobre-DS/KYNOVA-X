
from fastapi import FastAPI
from pydantic import BaseModel, Field
from pathlib import Path
import csv

app = FastAPI(
    title="KYNOVA-X | API de Dados Oncológicos",
    description=(
        "API para consulta de uma amostra demonstrativa das estimativas "
        "de câncer do INCA e inclusão de registros adicionais. "
        "Os registros enviados são armazenados separadamente "
        "dos dados originais."
    ),
    version="1.0.0"
)

ARQUIVO_ORIGINAL = Path("data/raw/estimativas_inca_2026_amostra.csv")
ARQUIVO_ADICIONAL = Path("data/processed/registros_api.csv")

COLUNAS = ["sexo", "localizacao", "casos", "ano"]


class Registro(BaseModel):
    sexo: str
    localizacao: str
    casos: int = Field(ge=0)
    ano: int = Field(ge=2000)


def ler_csv(caminho):
    if not caminho.exists():
        return []

    with caminho.open("r", encoding="utf-8-sig", newline="") as arquivo:
        return list(csv.DictReader(arquivo))


@app.get("/estimativas")
def consultar_estimativas():
    registros = ler_csv(ARQUIVO_ORIGINAL)
    registros += ler_csv(ARQUIVO_ADICIONAL)
    return registros


@app.post("/estimativas", status_code=201)
def adicionar_estimativa(registro: Registro):
    ARQUIVO_ADICIONAL.parent.mkdir(parents=True, exist_ok=True)
    novo_registro = registro.model_dump()

    arquivo_novo = not ARQUIVO_ADICIONAL.exists()

    with ARQUIVO_ADICIONAL.open(
        "a", encoding="utf-8", newline=""
    ) as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=COLUNAS)

        if arquivo_novo:
            escritor.writeheader()

        escritor.writerow(novo_registro)

    return {
        "mensagem": "Registro adicionado com sucesso.",
        "registro": novo_registro
    }
