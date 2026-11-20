from pathlib import Path
import pandas as pd
import pytest
from src.analise_tp5 import (
    avaliar_saida, carregar_estimativas, carregar_textos, palavras, textos_elegiveis,
)

RAIZ = Path(__file__).resolve().parents[1]


def test_arquivo_estimativas_e_esquema():
    df = carregar_estimativas(RAIZ / 'data/raw/estimativas_inca_2026_amostra.csv')
    assert len(df) == 10
    assert set(df.columns) == {'sexo', 'localizacao', 'casos', 'ano'}
    assert (df['casos'] >= 0).all()


def test_texto_coletado_pode_ser_enviado_ao_modelo():
    df = carregar_textos(RAIZ / 'data/raw/conteudo_inca_web.csv')
    assert len(df) == 2
    elegiveis = textos_elegiveis(df)
    assert len(elegiveis) == 1
    assert len(elegiveis.loc[0, 'texto']) >= 30


def test_textos_nao_sao_casos_numericos():
    df = carregar_textos(RAIZ / 'data/raw/conteudo_inca_web.csv')
    assert 'tipo' in df.columns and 'texto' in df.columns
    assert 'casos' not in df.columns


def test_resposta_repetida_deve_gerar_alerta():
    texto = 'O Instituto Nacional de Câncer divulga estimativas para o planejamento da saúde.'
    mensagens, _ = avaliar_saida(texto, texto)
    assert any('semelhante' in m for m in mensagens)


def test_repeticao_da_instrucao_deve_gerar_alerta():
    mensagens, _ = avaliar_saida('O Instituto Nacional de Câncer divulga estimativas de incidência.',
                                  'Resuma o texto a seguir em portugues, sem inventar dados: ...')
    assert any('instrução' in m for m in mensagens)


def test_validacao_detecta_falta_de_coluna(tmp_path):
    csv = tmp_path / 'amostra.csv'
    csv.write_text('sexo,casos\nHomens,42\n', encoding='utf-8')
    with pytest.raises(ValueError, match='Colunas ausentes'):
        carregar_estimativas(csv)


def test_contagem_de_palavras():
    assert palavras('Saúde e bem-estar.') == 4
