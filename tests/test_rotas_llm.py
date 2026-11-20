from fastapi import FastAPI
from fastapi.testclient import TestClient
from unittest.mock import patch
import time
from rotas_llm import router
from llm_local import ModeloIndisponivel, ModeloOcupado

app = FastAPI()
app.include_router(router)
client = TestClient(app)
TEXTO = 'O Instituto Nacional de Cancer divulga estimativas para planejamento da atencao oncologica.'

def test_sucesso_simulado():
    with patch('rotas_llm.processador.resumir', return_value=('Sintese demonstrativa.', 0.05)):
        resp=client.post('/processar_texto', json={'texto': TEXTO})
    assert resp.status_code == 200
    assert resp.json()['tipo_analise']=='resumo'
    assert resp.json()['execucao']=='local'

def test_entrada_invalida():
    resp=client.post('/processar_texto', json={'texto':'curto'})
    assert resp.status_code==422

def test_modelo_indisponivel():
    with patch('rotas_llm.processador.resumir', side_effect=ModeloIndisponivel('Modelo ausente')):
        resp=client.post('/processar_texto', json={'texto': TEXTO})
    assert resp.status_code==503

def test_modelo_ocupado():
    with patch('rotas_llm.processador.resumir', side_effect=ModeloOcupado('Ocupado')):
        resp=client.post('/processar_texto', json={'texto': TEXTO})
    assert resp.status_code==503

def test_erro_interno():
    with patch('rotas_llm.processador.resumir', side_effect=RuntimeError('Interno')):
        resp=client.post('/processar_texto', json={'texto': TEXTO})
    assert resp.status_code==500


def test_texto_excessivo_422():
    resp = client.post('/processar_texto', json={'texto': 'x' * 1501})
    assert resp.status_code == 422


def test_timeout_504():
    def inferencia_lenta(texto):
        time.sleep(0.08)
        return 'Resposta gerada tarde.', 0.08

    with patch('rotas_llm.TEMPO_LIMITE_S', 0.005):
        with patch('rotas_llm.processador.resumir', side_effect=inferencia_lenta):
            resp = client.post('/processar_texto', json={'texto': TEXTO})
    assert resp.status_code == 504
    assert 'excedeu' in resp.json()['detail']
