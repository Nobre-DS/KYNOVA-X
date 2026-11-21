"""Testes estáticos de integração; NÃO comprovam qualidade da inferência real."""
from llm_local import MODEL_DIR, MODEL_NAME, ProcessadorLocal


def test_modelo_portugues_e_diretorio_separado_do_legacy():
    assert MODEL_NAME == 'recogna-nlp/ptt5-base-summ'
    assert MODEL_DIR.name == 'ptt5-base-summ'
    assert 'flan-t5-small' not in str(MODEL_DIR)

def test_modo_pt_usa_texto_direto_sem_prompt():
    class Tokenizador:
        def __init__(self):
            self.entrada = None
        def __call__(self, entrada, **kwargs):
            self.entrada = entrada
            return {'input_ids': [entrada]}
        def decode(self, saida, **kwargs):
            return saida
    class Modelo:
        def __init__(self):
            self.cont = 0
        def generate(self, **kwargs):
            self.cont += 1
            return ['O INCA utiliza os RCBP e o SIM para estimativas.']
    p=ProcessadorLocal()
    p._tokenizer=Tokenizador()
    p._model=Modelo()
    p._modelo_portugues=True
    origem='O INCA elabora estimativas de câncer considerando RCBP e SIM.'
    resumo, tempo=p.resumir(origem)
    assert p._tokenizer.entrada == origem
    assert p._model.cont == 1
    assert resumo.startswith('O INCA')
    assert tempo >= 0

def test_modo_pt_nao_sintetiza_sem_geracao():
    class Tokenizador:
        def __call__(self, entrada, **kwargs):
            return {'input_ids': [entrada]}
        def decode(self, saida, **kwargs):
            return saida
    class Modelo:
        def generate(self, **kwargs):
            return ['']
    p=ProcessadorLocal()
    p._tokenizer=Tokenizador()
    p._model=Modelo()
    p._modelo_portugues=True
    try:
        p.resumir('Texto de origem longo o suficiente para sumarização.')
    except RuntimeError as exc:
        assert 'resposta vazia' in str(exc)
    else:
        raise AssertionError('Aceitou geração vazia')
