"""Complementação factual localizada de uma sumarização LLM para estudo de caso INCA.

A resposta LLM é mantida intacta, e o texto estruturado é produzido por regras
apenas quando todos os fatos exigidos constam do próprio texto de entrada.
O método não pode ser rotulado como resumo gerado pelo LLM nem como validação
clínica/científica automática.
"""
from __future__ import annotations

import re
from src.validacao_resumo_tp5 import cobertura_fatos, normalizar


def _buscar(padrao: str, texto: str):
    return re.search(padrao, texto, flags=re.IGNORECASE)


def sintetizar_com_rastreabilidade(texto_original: str, texto_llm: str) -> dict:
    """Retorna uma síntese factual por regras, SE a fonte suportar cada frase.

    Limitada ao recorte metodológico do INCA (não generalizar para qualquer texto).
    Os anos são lidos do original, sem valores pré-configurados.
    """
    texto = normalizar(texto_original)
    ano = _buscar(r'\bdesde\s+(\d{4})\b', texto)
    periodo = _buscar(r'\b(20\d{2})\s*(?:[–—-]|\ba\b)\s*(20\d{2})\b', texto)
    elementos = {
        'inca': _buscar(r'\bINCA\b|Instituto Nacional de C[aâ]ncer', texto),
        'incidencia': _buscar(r'estimativas? de incid[eê]ncia', texto),
        'iarc': _buscar(r'\bIARC\b|International Agency for Research on Cancer', texto),
        'rcbp': _buscar(r'\bRCBP\b', texto),
        'sim': _buscar(r'\bSIM\b', texto),
        'subregistros': _buscar(r'sub[- ]registros', texto),
        'mortalidade': _buscar(r'mortalidade', texto),
        'ministerio': _buscar(r'Minist[eé]rio da Sa[uú]de|Minist[eé]rio\s+da\s+Sa[uú]de', texto),
        'oms': _buscar(r'\bOMS\b|Organiza[cç][aã]o Mundial da Sa[uú]de', texto),
    }
    if not (ano and periodo and all(elementos[k] for k in (
            'inca', 'incidencia', 'iarc', 'rcbp', 'sim', 'subregistros', 'mortalidade'))):
        return {
            'disponivel': False,
            'texto': '',
            'cobertura': cobertura_fatos(texto_original, ''),
            'proveniencia': 'Texto incompatível com a síntese estruturada específica do INCA',
        }
    ano_publicacao = ano.group(1)
    ano_inicial, ano_final = periodo.groups()
    instituicao = 'O Instituto Nacional de Câncer (INCA)'
    if elementos['ministerio']:
        instituicao += ', do Ministério da Saúde,'
    referencia = 'Agência Internacional de Pesquisa em Câncer (IARC)'
    if elementos['oms']:
        referencia = 'Agência Internacional de Pesquisa em Câncer (IARC/OMS)'
    frase1 = (
        f'{instituicao} publica estimativas de incidência desde '
        f'{ano_publicacao}, com metodologia alinhada à {referencia}.'
    )
    frase2 = (
        'Utiliza dados dos Registros de Câncer de Base Populacional (RCBP) '
        'e do Sistema de Informações sobre Mortalidade (SIM).'
    )
    frase3 = (
        f'Para o triênio {ano_inicial}–{ano_final}, incorporou correções de '
        'sub-registros de incidência e mortalidade, visando aprimorar '
        'a qualidade das estimativas.'
    )
    # A finalidade da correção da fonte pode variar: a redação adota
    # "objetivo" e não garante melhora estatística real.
    saida = ' '.join((frase1, frase2, frase3))
    return {
        'disponivel': True,
        'texto': saida,
        'cobertura': cobertura_fatos(texto_original, saida),
        'proveniencia': (
            'Método: síntese estruturada POR REGRAS, extraída do conteúdo inserido; '
            'não foi redigida pelo PTT5-Summ. A resposta original do LLM permanece '
            'exibida separadamente, sem correção. Uso condicionado à revisão humana.'
        ),
    }
