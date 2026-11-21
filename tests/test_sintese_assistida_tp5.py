from pathlib import Path
import csv

from src.sintese_assistida_tp5 import sintetizar_com_rastreabilidade

DADOS = Path(__file__).resolve().parents[1] / 'data/raw/conteudo_inca_web.csv'


def _original_inca():
    with DADOS.open(encoding='utf-8-sig', newline='') as f:
        return next(r['texto'] for r in csv.DictReader(f) if r['tipo'] == 'p')


def test_fonte_original_preserva_todos_marcadores_sem_atribuir_ao_llm():
    texto = _original_inca()
    resumo_ruim = 'O INCA publica estimativas desde 1995.'
    a = sintetizar_com_rastreabilidade(texto, resumo_ruim)
    assert a['disponivel']
    assert a['cobertura']['preservados'] == a['cobertura']['total'] == 7
    assert len(a['texto'].split()) < len(texto.split())
    assert 'não foi redigida pelo PTT5-Summ' in a['proveniencia']
    assert '2026–2028' in a['texto']


def test_anos_sao_dinamicos_e_extraidos_da_fonte():
    txt = (_original_inca().replace('desde 1995', 'desde 2005')
           .replace('de 2026 a 2028', 'de 2030 a 2032'))
    a = sintetizar_com_rastreabilidade(txt, '')
    assert a['disponivel']
    assert 'desde 2005' in a['texto']
    assert '2030–2032' in a['texto']
    assert '1995' not in a['texto']
    assert '2026' not in a['texto']


def test_textos_sem_fontes_necessarias_nao_geram_fatos_do_inca():
    texto = 'O relatório da prefeitura trata de custos de transporte para 2026.'
    a = sintetizar_com_rastreabilidade(texto, 'Custos de transporte')
    assert not a['disponivel']
    assert not a['texto']


def test_texto_parcial_nao_inventa_dados_ausentes():
    texto = 'O INCA publica estimativas de incidência desde 1995 com apoio da IARC.'
    a = sintetizar_com_rastreabilidade(texto, '')
    assert not a['disponivel']


def test_cobertura_llm_nao_e_alterada_por_saida_estruturada():
    texto = _original_inca()
    llm = 'O INCA publica estimativas de incidência desde 1995.'
    a = sintetizar_com_rastreabilidade(texto, llm)
    from src.validacao_resumo_tp5 import cobertura_fatos
    assert a['disponivel']
    assert cobertura_fatos(texto, llm)['preservados'] < 7
    assert a['cobertura']['preservados'] == 7
