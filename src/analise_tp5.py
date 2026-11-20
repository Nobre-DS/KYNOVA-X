"""Regras verificáveis do dashboard TP5, separadas da interface Streamlit.

Nunca soma os dez valores selecionados como se fossem incidência nacional.
"""
from __future__ import annotations

import re
from pathlib import Path
from difflib import SequenceMatcher

import pandas as pd

COLUNAS_ESTIMATIVAS = ('sexo', 'localizacao', 'casos', 'ano')
COLUNAS_TEXTOS = ('tipo', 'texto')
FONTE_INCA = (
    'https://www.gov.br/inca/pt-br/assuntos/cancer/numeros/estimativa/'
    'estado-capital/por-estado-e-capital/brasil/brasil-consolidado'
)


def carregar_estimativas(caminho: Path) -> pd.DataFrame:
    """Valida esquema; distingue linhas inválidas sem fabricar estimativas."""
    df = pd.read_csv(caminho, encoding='utf-8-sig')
    faltantes = set(COLUNAS_ESTIMATIVAS) - set(df.columns)
    if faltantes:
        raise ValueError('Colunas ausentes nas estimativas: ' + ', '.join(sorted(faltantes)))
    df = df[list(COLUNAS_ESTIMATIVAS)].copy()
    df['casos'] = pd.to_numeric(df['casos'], errors='coerce')
    df['ano'] = pd.to_numeric(df['ano'], errors='coerce')
    df['sexo'] = df['sexo'].astype('string').str.strip()
    df['localizacao'] = df['localizacao'].astype('string').str.strip()
    df = df.dropna(subset=list(COLUNAS_ESTIMATIVAS))
    df = df[(df['casos'] >= 0) & (df['ano'] >= 2000)]
    df['casos'] = df['casos'].astype(int)
    df['ano'] = df['ano'].astype(int)
    return df.reset_index(drop=True)


def carregar_textos(caminho: Path) -> pd.DataFrame:
    """Lê conteúdo já coletado via web scraping nos TPs anteriores."""
    df = pd.read_csv(caminho, encoding='utf-8-sig')
    faltantes = set(COLUNAS_TEXTOS) - set(df.columns)
    if faltantes:
        raise ValueError('Colunas ausentes nos textos: ' + ', '.join(sorted(faltantes)))
    df = df[list(COLUNAS_TEXTOS)].fillna('').copy()
    df['tipo'] = df['tipo'].astype(str).str.strip()
    df['texto'] = df['texto'].astype(str).str.replace(r'\s+', ' ', regex=True).str.strip()
    return df[df['texto'] != ''].reset_index(drop=True)


def palavras(texto: str) -> int:
    return len(re.findall(r'\b\w+\b', texto or '', flags=re.UNICODE))


def textos_elegiveis(df: pd.DataFrame, minimo: int = 30, maximo: int = 1500) -> pd.DataFrame:
    elegiveis = df[df['texto'].str.len() >= minimo].copy()
    elegiveis['texto'] = elegiveis['texto'].str.slice(0, maximo)
    return elegiveis.reset_index(drop=True)


def avaliar_saida(original: str, resultado: str) -> tuple[list[str], int]:
    """Sinais heurísticos; NÃO mede acurácia, veracidade nem qualidade clínica."""
    alertas = []
    origem = re.sub(r'\s+', ' ', original).lower().strip()
    saida = re.sub(r'\s+', ' ', resultado).lower().strip()
    if not saida:
        return ['Resposta vazia: não é possível avaliar um resumo.'], 0
    if saida.startswith(('resuma o texto', 'resumo a seguir', 'tarefa:', 'resuma em')):
        alertas.append('A resposta parece reproduzir a instrução enviada ao modelo.')
    similaridade = SequenceMatcher(None, origem, saida).ratio()
    if similaridade > 0.85 or (len(origem) > 45 and origem in saida):
        alertas.append('A saída é muito semelhante ao texto original; pode não haver sumarização.')
    if palavras(saida) >= palavras(origem) and palavras(origem) > 20:
        alertas.append('O resultado não reduziu a quantidade de palavras.')
    if not alertas:
        alertas.append('Formato aparentemente sintetizado; fidelidade factual exige conferência humana.')
    return alertas, palavras(saida)
