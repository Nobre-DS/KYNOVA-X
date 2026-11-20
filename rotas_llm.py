"""Router para incluir no api.py existente, sem alterar as rotas do TP3."""
import asyncio
import logging
from typing import Literal
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field, field_validator
from llm_local import MODEL_NAME, processador, ModeloIndisponivel, ModeloOcupado

logger = logging.getLogger(__name__)
TEMPO_LIMITE_S = 60.0
router = APIRouter(tags=['LLM local'])

class TextoEntrada(BaseModel):
    texto: str = Field(min_length=30, max_length=1500, description='Texto a resumir; sem dados pessoais.')

    @field_validator('texto')
    @classmethod
    def nao_apenas_espacos(cls, valor: str) -> str:
        valor = valor.strip()
        if len(valor) < 30:
            raise ValueError('Informe um texto com pelo menos 30 caracteres nao vazios.')
        return valor

class TextoSaida(BaseModel):
    texto_original: str
    tipo_analise: Literal['resumo']
    resultado: str = Field(min_length=1)
    modelo: str
    execucao: Literal['local']
    tempo_segundos: float = Field(ge=0)

@router.post('/processar_texto', response_model=TextoSaida)
async def processar_texto(dados: TextoEntrada):
    try:
        # Thread evita bloquear o loop da API; wait_for limita a espera HTTP.
        resultado, segundos = await asyncio.wait_for(
            asyncio.to_thread(processador.resumir, dados.texto), timeout=TEMPO_LIMITE_S
        )
        return TextoSaida(texto_original=dados.texto, tipo_analise='resumo',
                          resultado=resultado, modelo=MODEL_NAME,
                          execucao='local', tempo_segundos=segundos)
    except ModeloIndisponivel as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except ModeloOcupado as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except TimeoutError as exc:
        # O trabalho em thread pode continuar ate terminar mesmo apos o timeout HTTP.
        raise HTTPException(status_code=504, detail='O processamento excedeu 60 segundos.') from exc
    except Exception as exc:
        logger.exception('Erro interno no processamento local')
        raise HTTPException(status_code=500, detail='Falha interna ao processar texto.') from exc
