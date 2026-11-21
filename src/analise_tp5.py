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


def gerar_insights_amostra(df: pd.DataFrame) -> list[dict[str, str | int]]:
    """Comparações estritamente DESCRITIVAS; não estima demanda nem impacto ESG.

    Não calcula totais nacionais nem compara taxas entre os sexos.
    Cada observação é confrontada apenas com OUTROS itens do mesmo recorte
    amostral; o enunciado e a fonte original permanecem explicitados.
    """
    base = df.copy()
    colunas = set(COLUNAS_ESTIMATIVAS)
    if not colunas.issubset(base.columns):
        raise ValueError('Dados sem as colunas necessárias para gerar insights.')
    if base.empty:
        return []
    insights = []
    for sexo in ['Homens', 'Mulheres']:
        grupo = base[base['sexo'] == sexo].sort_values('casos', ascending=False)
        if grupo.empty:
            continue
        lider = grupo.iloc[0]
        segundo = grupo.iloc[1] if len(grupo) > 1 else None
        ano = int(lider['ano'])
        descricao = (
            f'No recorte de {len(grupo)} registros amostrais de {sexo.lower()} ({ano}), '
            f'{lider["localizacao"]} apresenta {int(lider["casos"]):,} casos novos estimados.'
            .replace(',', '.')
        )
        if segundo is not None:
            descricao += (
                f' O próximo valor na amostra é {segundo["localizacao"]}: '
                f'{int(segundo["casos"]):,}.'
            ).replace(',', '.')
        insights.append({
            'titulo': f'Maior valor na amostra — {sexo}',
            'descricao': descricao,
            'valor': int(lider['casos']),
            'fonte': 'data/raw/estimativas_inca_2026_amostra.csv (seleção da publicação INCA)',
            'relevancia': (
                'ODS 3 (dimensão social do ESG): orienta quais temas merecem exame '
                'posterior com dados de oferta de serviços e população, sem estabelecer '
                'prioridade de investimento apenas com esta amostra.'
            ),
            'limite': (
                'Não representa ranking nacional completo, taxa padronizada, '
                'demanda de consultas ou impacto assistencial observado.'
            ),
        })
    return insights


def fatos_comprovaveis_da_fonte(texto: str) -> list[dict[str, str]]:
    """Mostra somente afirmações que possuem expressão explícita no TEXTO recebido.

    Não produz interpretação clínica nem apresenta esta extração como resultado do LLM.
    """
    texto = re.sub(r'\s+', ' ', texto or '').lower()
    candidatos = [
        ('desde 1995', 'O texto menciona publicação de estimativas desde 1995.'),
        ('rcbp', 'O texto cita registros de câncer de base populacional (RCBP).'),
        ('sistema de informação sobre mortalidade', 'O texto cita o Sistema de Informação sobre Mortalidade.'),
        ('sub-registros', 'O texto menciona correção de sub-registros.'),
    ]
    return [{'termo_localizado': termo, 'fato': frase} for termo, frase in candidatos if termo in texto]


def auditoria_resumo(original: str, resposta: str) -> dict[str, object]:
    """Diagnóstico CONSERVADOR, sem alegar validação factual automática."""
    alertas, n = avaliar_saida(original, resposta)
    origem = re.sub(r'\s+', ' ', original or '').strip().lower()
    saida = re.sub(r'\s+', ' ', resposta or '').strip().lower()
    sinais_prompt = ('resuma o texto', 'resumo a seguir', 'sem inventar dados',
                     'tarefa:', 'resuma em', 'texto de origem:', 'resumo:')
    if any(sinal in saida[:180] for sinal in sinais_prompt) and not any(
        'instrução' in s for s in alertas
    ):
        alertas.insert(0, 'Possível eco da instrução de prompt; revise antes de usar.')
    # Verificação objetiva de números: cada número citado na saída deve
    # aparecer literalmente na origem. Não comprova que o contexto esteja correto.
    numeros_saida = set(re.findall(r'\b\d+(?:[.,]\d+)?\b', saida))
    numeros_origem = set(re.findall(r'\b\d+(?:[.,]\d+)?\b', origem))
    nao_encontrados = sorted(numeros_saida - numeros_origem)
    if nao_encontrados:
        alertas.append('Número(s) ausente(s) no texto-fonte: ' + ', '.join(nao_encontrados))
    flags = (bool(nao_encontrados) or any(
        termo in a.lower() for a in alertas for termo in
        ['eco', 'instrução', 'semelhante', 'vazia', 'não reduziu']
    ))
    return {
        'estado': 'REVISÃO PRIORITÁRIA' if flags else 'REVISÃO HUMANA OBRIGATÓRIA',
        'alertas': alertas,
        'palavras_origem': palavras(original),
        'palavras_saida': n,
        'numeros_sem_fonte': nao_encontrados,
        'validacao_factual_automatica': False,
    }


def indicadores_qualidade_amostra(caminho: Path) -> dict[str, int]:
    """Governança do CSV: linhas originais x linhas aptas ao dashboard.

    Não se trata de índice ESG institucional, nem certificação da fonte.
    """
    bruto = pd.read_csv(caminho, encoding='utf-8-sig')
    validos = carregar_estimativas(caminho)
    n = len(bruto)
    aproveitados = len(validos)
    return {
        'registros_origem': n,
        'registros_aptos': aproveitados,
        'registros_excluidos': n - aproveitados,
    }
