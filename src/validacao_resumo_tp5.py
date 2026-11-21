"""TP5: comparação rastreável da resposta de IA com fatos EXPRESSOS no texto.

O resumo de referência é por regras e NÃO deve ser atribuído ao LLM.
Não se trata de validador de veracidade semântica automático.
"""
from __future__ import annotations

import re
from dataclasses import dataclass


def normalizar(texto: str) -> str:
    return re.sub(r'\s+', ' ', texto or '').strip()


def _contem(texto: str, padrao: str) -> bool:
    return bool(re.search(padrao, texto, flags=re.IGNORECASE))


def ancoras_verificaveis(texto: str) -> list[tuple[str, str]]:
    """Identifica fatos-chave textuais, sem inferir resultados clínicos."""
    t = normalizar(texto)
    regras = [
        ('INCA', r'\bINCA\b|Instituto Nacional de C[aâ]ncer'),
        ('Publicação desde 1995', r'\bdesde\s+1995\b'),
        ('Referência à IARC/OMS', r'\bIARC\b|International Agency for Research on Cancer'),
        ('Fonte RCBP', r'\bRCBP\b'),
        ('Fonte SIM', r'\bSIM\b|Sistema de Informa[cç][aã]o\s+sobre\s+Mortalidade'),
        ('Triênio 2026–2028', r'\b2026\b.{0,20}\b2028\b'),
        ('Correção de sub-registros', r'sub[- ]registros'),
    ]
    return [(nome, padrao) for nome, padrao in regras if _contem(t, padrao)]


def cobertura_fatos(texto_original: str, texto_resumo: str) -> dict:
    """Mede retenção de MARCADORES, não fidelidade semântica ou precisão."""
    fatos = ancoras_verificaveis(texto_original)
    itens = [
        {'fato': nome, 'preservado': _contem(texto_resumo, padrao)}
        for nome, padrao in fatos
    ]
    total = len(itens)
    preservados = sum(item['preservado'] for item in itens)
    return {'itens': itens, 'preservados': preservados, 'total': total,
            'proporcao': preservados / total if total else None}


def resumo_referencia_da_fonte(texto: str) -> dict:
    """Produz referência acadêmica restrita ao trecho INCA fornecido.

    As expressões e datas essenciais são conferidas antes de cada afirmação.
    Se a fonte for outra, devolve EXTRATO LITERAL, sem inventar síntese.
    """
    t = normalizar(texto)
    regras_minimas = (
        r'Instituto Nacional de C[aâ]ncer\s*\(INCA\)',
        r'Minist[eé]rio\s+da\s+Sa[uú]de',
        r'publica estimativas de incid[eê]ncia\s+desde\s+(\d{4})',
        r'International Agency for Research on Cancer',
        r'\bRCBP\b', r'\bSIM\b',
        r'tri[eê]nio\s+de\s+(\d{4})\s+a\s+(\d{4})',
        r'corre[cç][aã]o\s+de\s+sub[- ]registros\s+de\s+mortalidade\s+e\s+incid[eê]ncia',
    )
    encontrados = [re.search(x, t, flags=re.IGNORECASE) for x in regras_minimas]
    if all(encontrados):
        ano = encontrados[2].group(1)
        inicio, fim = encontrados[6].groups()
        resultado = (
            'O Instituto Nacional de Câncer (INCA), órgão técnico do Ministério da Saúde, '
            f'publica estimativas de incidência desde {ano}, com metodologia alinhada à IARC/OMS. '
            'Utiliza principalmente os Registros de Câncer de Base Populacional (RCBP) '
            'e o Sistema de Informação sobre Mortalidade (SIM). '
            f'Para o triênio {inicio}–{fim}, incorporou correções de sub-registros de '
            'mortalidade e incidência para aumentar a precisão e a representatividade das estimativas.'
        )
        return {
            'texto': resultado,
            'metodo': 'Síntese acadêmica estruturada, condicionada aos fatos do texto-fonte',
            'proveniencia': 'Regra local sobre texto coletado; NÃO é saída do LLM',
            'completo_para_fonte_inca': True,
        }
    # Em outros documentos, NÃO reutilizar o resumo do INCA nem inventar fatos.
    frases = [s.strip() for s in re.split(r'(?<=[.!?])\s+', t) if s.strip()]
    extrato = ' '.join(frases[:2])
    return {
        'texto': extrato,
        'metodo': 'Extrato literal das primeiras frases (não é resumo abstrativo)',
        'proveniencia': 'Extração local do texto-fonte; NÃO é saída do LLM',
        'completo_para_fonte_inca': False,
    }
