"""Verifica cobertura, transparência e lógica de reprompt; NÃO testa modelo real."""
from pathlib import Path
import csv

from llm_local import ProcessadorLocal, construir_prompt, _pontuar_resumo
from src.validacao_resumo_tp5 import (
    ancoras_verificaveis, cobertura_fatos, resumo_referencia_da_fonte,
)

RAIZ = Path(__file__).resolve().parents[1]


def _fonte_inca():
    with (RAIZ / 'data/raw/conteudo_inca_web.csv').open(encoding='utf-8-sig', newline='') as f:
        return next(r['texto'] for r in csv.DictReader(f) if r['tipo'] == 'p')


def test_sintese_referencia_fiel_e_mais_curta():
    fonte = _fonte_inca()
    resumo = resumo_referencia_da_fonte(fonte)
    assert resumo['completo_para_fonte_inca']
    assert 'NÃO é saída do LLM' in resumo['proveniencia']
    assert len(resumo['texto'].split()) < len(fonte.split())
    assert cobertura_fatos(fonte, resumo['texto'])['preservados'] == 7
    assert 'órgão técnico do Ministério da Saúde' in resumo['texto']


def test_texto_alheio_nao_recebe_fatos_do_inca():
    fonte = 'Um relatório municipal registra custos operacionais para 2025. O estudo descreve a organização das despesas. Outra conclusão será divulgada.'
    resumo = resumo_referencia_da_fonte(fonte)
    assert not resumo['completo_para_fonte_inca']
    assert '1995' not in resumo['texto']
    assert 'INCA' not in resumo['texto']
    assert resumo['texto'] in fonte


def test_ano_diferente_da_fonte_e_capturado_dinamicamente():
    fonte = _fonte_inca().replace('desde 1995', 'desde 2005').replace('de 2026 a 2028', 'de 2030 a 2032')
    resumo = resumo_referencia_da_fonte(fonte)['texto']
    assert 'desde 2005' in resumo
    assert '2030–2032' in resumo
    assert '1995' not in resumo
    assert '2026' not in resumo


def test_marcadores_ausentes_nunca_sao_pontuados():
    original = _fonte_inca()
    incompleto = 'As principais fontes são RCBP e SIM.'
    cobertura = cobertura_fatos(original, incompleto)
    assert cobertura['total'] == 7
    assert cobertura['preservados'] == 2
    assert cobertura['proporcao'] < 0.5
    assert _pontuar_resumo(original, incompleto) < 6.0


def test_prompt_revisado_solicita_resumo_informativo():
    prompt = construir_prompt(_fonte_inca())
    assert '2 a 3 frases' in prompt
    assert 'fontes de informação' in prompt
    assert '=== TEXTO FONTE ===' in prompt


def test_se_primeiro_resumo_for_incompleto_reprompta():
    fonte = _fonte_inca()
    referencia = resumo_referencia_da_fonte(fonte)['texto']

    class TokenizerFalso:
        def __call__(self, prompt, **kwargs):
            return {'input_ids': [prompt]}
        def decode(self, tokens, **kwargs):
            return tokens if isinstance(tokens, str) else tokens[0]

    class ModeloFalso:
        def __init__(self):
            self.chamadas = 0
        def generate(self, **kwargs):
            self.chamadas += 1
            if self.chamadas == 1:
                return ['As principais fontes são RCBP e SIM.']
            return [referencia]

    proc = ProcessadorLocal()
    proc._tokenizer = TokenizerFalso()
    proc._model = ModeloFalso()
    resumo, segundos = proc.resumir(fonte)
    assert resumo == referencia
    assert segundos >= 0
    assert proc._model.chamadas == 2


def test_rejeita_numero_estranho_na_pontuacao():
    fonte = _fonte_inca()
    ref = resumo_referencia_da_fonte(fonte)['texto']
    assert _pontuar_resumo(fonte, ref + ' No ano 2099.') < _pontuar_resumo(fonte, ref)
