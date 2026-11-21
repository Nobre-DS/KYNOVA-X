"""Testes para risco de truncamento e seleção do melhor resultado (sem modelo real)."""
from llm_local import _pontuar_resumo, construir_prompt


def test_saida_incompleta_detectada():
    fonte = ('O Instituto Nacional de Câncer (INCA) é uma instituição pública do '
             'Ministério da Saúde. Desde 1995, divulga estimativas da incidência. '
             'Os RCBP informam casos novos; o SIM informa óbitos e causas. '
             'No triênio 2026–2028, houve correções de sub-registros. ' * 2)
    cortado = ('O Instituto Nacional de Câncer (INCA) é uma pública do '
               'Ministério da Saúde. Desde 1995, elaborado')
    completo = ('O INCA publica estimativas desde 1995. As fontes incluem RCBP e SIM. '
                'No triênio 2026–2028, foram realizados ajustes de sub-registros.')
    assert _pontuar_resumo(fonte, cortado) < _pontuar_resumo(fonte, completo)


def test_prompt_nao_exige_apenas_uma_frase():
    p = construir_prompt('Este texto é a fonte.')
    assert '2 a 3 frases completas' in p
    assert 'UMA frase' not in p
    assert 'não invente' in p.lower()


def test_comparacao_nao_usa_resumo_programado_como_saida_do_modelo():
    # No processador, as respostas só vêm de self._model.generate.
    from pathlib import Path
    codigo = (Path(__file__).resolve().parents[1] / 'llm_local.py').read_text(encoding='utf-8')
    assert 'resumo_referencia_da_fonte' not in codigo
    assert "resumo = gerar(construir_prompt(texto))" in codigo
