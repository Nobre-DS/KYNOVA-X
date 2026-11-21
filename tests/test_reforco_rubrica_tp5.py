"""Testes adicionais para critérios 2 (insights), 5 (LLM) e 6 (dashboard)."""
from pathlib import Path

import pandas as pd

from src.analise_tp5 import (
    auditoria_resumo, carregar_estimativas, carregar_textos,
    fatos_comprovaveis_da_fonte, gerar_insights_amostra, indicadores_qualidade_amostra,
)
from llm_local import construir_prompt, construir_prompt_alternativo, saida_com_eco

RAIZ = Path(__file__).resolve().parents[1]


def test_insights_reais_do_recorte_amostral():
    df = carregar_estimativas(RAIZ / 'data/raw/estimativas_inca_2026_amostra.csv')
    insights = gerar_insights_amostra(df)
    assert len(insights) == 2
    assert insights[0]['valor'] == 77920
    assert insights[1]['valor'] == 78610
    assert 'Próstata' in insights[0]['descricao']
    assert 'Mama feminina' in insights[1]['descricao']
    assert all('amostr' in x['descricao'] for x in insights)
    assert all('ODS 3' in x['relevancia'] for x in insights)
    assert not any('ranking nacional completo' in x['descricao'] for x in insights)


def test_insights_respeitam_filtro():
    df = carregar_estimativas(RAIZ / 'data/raw/estimativas_inca_2026_amostra.csv')
    assert len(gerar_insights_amostra(df[df.sexo == 'Mulheres'])) == 1
    assert gerar_insights_amostra(df.iloc[0:0]) == []


def test_nao_cria_insights_sem_colunas():
    try:
        gerar_insights_amostra(pd.DataFrame({'sexo': ['Homens']}))
    except ValueError:
        pass
    else:
        raise AssertionError('Esquema inválido foi aceito')


def test_fatos_metodologicos_apenas_presentes_na_fonte():
    textos = carregar_textos(RAIZ / 'data/raw/conteudo_inca_web.csv')
    texto = textos.loc[textos.tipo == 'p', 'texto'].iloc[0]
    fatos = fatos_comprovaveis_da_fonte(texto)
    termos = {x['termo_localizado'] for x in fatos}
    assert 'desde 1995' in termos
    assert 'rcbp' in termos
    assert 'sub-registros' in termos
    assert fatos_comprovaveis_da_fonte('Fonte não informada.') == []


def test_auditoria_detecta_eco_de_prompt_em_qualquer_posicao_inicial():
    texto = 'O INCA publica estimativas para planejamento de atenção oncológica.'
    resposta = 'Resultado: Resuma o texto a seguir em português, sem inventar dados. O INCA...'
    analise = auditoria_resumo(texto, resposta)
    assert analise['estado'] == 'REVISÃO PRIORITÁRIA'
    assert any('instrução' in item for item in analise['alertas'])
    assert not analise['validacao_factual_automatica']


def test_auditoria_detecta_numero_inventado():
    resultado = auditoria_resumo('O estudo apresentou 1995 como referência.',
                                'O estudo apresentou 1995 e 9999 como referências.')
    assert resultado['numeros_sem_fonte'] == ['9999']
    assert resultado['estado'] == 'REVISÃO PRIORITÁRIA'


def test_sem_alertas_nao_significa_validacao_factual():
    resultado = auditoria_resumo('O INCA apresenta dados sobre incidência e métodos.',
                                'Foram descritos métodos e dados.')
    assert resultado['validacao_factual_automatica'] is False


def test_prompt_local_e_restrito():
    prompt = construir_prompt('A fonte menciona incidência.')
    assert 'A fonte menciona incidência.' in prompt
    assert 'fatos' in prompt
    assert '=== TEXTO FONTE ===' in prompt
    assert 'não' in prompt.lower()


def test_tentativa_2_nao_repete_instrucoes_originais():
    entrada = 'O INCA registra estimativas para o planejamento da atenção oncológica.'
    assert 'principal informação' in construir_prompt_alternativo(entrada)
    assert entrada in construir_prompt_alternativo(entrada)
    assert saida_com_eco('Resuma o texto a seguir em português, sem inventar dados:', entrada)
    assert not saida_com_eco('O INCA fornece informações para planejamento.', entrada)


def test_reprompt_automatico_se_primeira_saida_tiver_eco():
    """Simula saída do modelo: testa estratégia, NÃO qualidade do modelo real."""
    from llm_local import ProcessadorLocal

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
                return ['Resuma o texto a seguir em português, sem inventar dados.']
            return ['O INCA utiliza informações para publicar estimativas.']

    processador = ProcessadorLocal()
    processador._tokenizer = TokenizerFalso()
    processador._model = ModeloFalso()
    saida, segundos = processador.resumir('O INCA divulga estimativas para apoio ao planejamento da atenção oncológica.')
    assert saida == 'O INCA utiliza informações para publicar estimativas.'
    assert processador._model.chamadas == 2
    assert segundos >= 0


def test_qualidade_do_csv_e_rastreabilidade_da_amostra(tmp_path):
    real = indicadores_qualidade_amostra(RAIZ / 'data/raw/estimativas_inca_2026_amostra.csv')
    assert real == {'registros_origem': 10, 'registros_aptos': 10, 'registros_excluidos': 0}
    arquivo = tmp_path / 'teste.csv'
    arquivo.write_text('sexo,localizacao,casos,ano\nHomens,Próstata,100,2026\nHomens,Estômago,,2026\n', encoding='utf-8')
    resultado = indicadores_qualidade_amostra(arquivo)
    assert resultado == {'registros_origem': 2, 'registros_aptos': 1, 'registros_excluidos': 1}
