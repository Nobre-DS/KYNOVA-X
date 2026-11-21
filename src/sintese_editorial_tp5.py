"""Referencia editorial escolhida para o TP5; NUNCA a atribuir ao LLM.

A referencia exata so e apresentada para o texto especifico selecionado
pela usuaria, impedindo associar texto preescrito a outra fonte arbitraria.
"""
from __future__ import annotations

import re
from src.validacao_resumo_tp5 import cobertura_fatos

SINTese_APROVADA = (
    'O Instituto Nacional de Câncer (INCA), vinculado ao Ministério da Saúde, '
    'é referência nacional na produção de informações para a prevenção e o '
    'controle do câncer. Desde 1995, publica estimativas de incidência com '
    'metodologia alinhada à da Agência Internacional de Pesquisa em Câncer '
    '(IARC), da Organização Mundial da Saúde (OMS). Baseadas nos Registros de '
    'Câncer de Base Populacional (RCBP) e no Sistema de Informações sobre '
    'Mortalidade (SIM), as estimativas de 2026–2028 incorporam correções de '
    'sub-registros, buscando aprimorar a precisão e subsidiar decisões '
    'fundamentadas em saúde pública.'
)


def _uniformizar(s: str) -> str:
    return re.sub(r'\s+', ' ', (s or '').strip())


def referencia_editorial(texto_entrada: str) -> dict:
    """Mostra a referencia APENAS se o usuario inseriu esse texto escolhido.

    Retorna cobertura lexica separada; nao altera a saida nem a nota do LLM.
    """
    identico = _uniformizar(texto_entrada) == _uniformizar(SINTese_APROVADA)
    if not identico:
        return {
            'disponivel': False, 'texto': '', 'palavras': 0,
            'cobertura': cobertura_fatos(texto_entrada, ''),
            'proveniencia': 'A referencia editorial nao corresponde ao trecho selecionado.',
        }
    return {
        'disponivel': True,
        'texto': SINTese_APROVADA,
        'palavras': len(SINTese_APROVADA.split()),
        'cobertura': cobertura_fatos(texto_entrada, SINTese_APROVADA),
        'proveniencia': (
            'Texto editorial selecionado e revisado na conversa, com auxilio de IA; '
            'NAO foi produzido pelo PTT5-Summ neste teste, NAO substitui a saida '
            'original do modelo nem valida semanticamente fatos.'
        ),
    }
