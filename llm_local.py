"""KYNOVA-X: sumarização com PTT5-Summ treinado para português do Brasil.

Preserva as funções de prompt e a estratégia FLAN anterior para testes legados.
Na produção, o PTT5-Summ recebe somente o texto original, como recomenda a
documentação do modelo. Toda saída exibida é gerada pelo modelo, sem edição.
A checagem lexical não comprova fidelidade semântica.
"""
from pathlib import Path
import re
import threading
import time

MODEL_DIR = Path(__file__).resolve().parent / 'modelos' / 'ptt5-base-summ'
MODEL_NAME = 'recogna-nlp/ptt5-base-summ'


def construir_prompt(texto: str) -> str:
    """Instrução de resumo informativo, preservando os dados da fonte."""
    return (
        'Faça um RESUMO INFORMATIVO em português claro, com 2 a 3 frases completas. '
        'Preserve fatos essenciais presentes no texto, incluindo instituições, datas, '
        'fontes de informação e mudanças metodológicas, quando citadas. '
        'Use apenas fatos da fonte; não invente números, não faça recomendações clínicas '
        'e não repita estas instruções. Termine o resumo com ponto final.\n'
        '=== TEXTO FONTE ===\n' + texto.strip() +
        '\n=== FIM DA FONTE ===\nRESUMO:'
    )


def construir_prompt_alternativo(texto: str) -> str:
    """Segunda instrução, curta, quando a primeira geração é insuficiente."""
    return (
        'Qual é a principal informação expressa no texto abaixo? '
        'Responda em português, em um parágrafo de 2 ou 3 frases completas. '
        'Inclua as instituições, as fontes de dados e os períodos mencionados, '
        'sem adicionar fatos externos.\nTexto: ' + texto.strip() +
        '\nResposta:'
    )


def saida_com_eco(resumo: str, texto: str) -> bool:
    """Detecção de eco das instruções e de cópia integral da origem."""
    s = re.sub(r'\s+', ' ', resumo or '').lower().strip()
    origem = re.sub(r'\s+', ' ', texto or '').lower().strip()
    indicadores = (
        'resuma o texto', 'sem inventar dados', 'resuma em',
        'resumo a seguir', 'qual é a principal informação',
        'texto de origem:', '=== texto fonte ===',
        'faça um resumo informativo', 'resumo informativo em português',
    )
    return (not s or any(i in s[:180] for i in indicadores)
            or (len(origem) >= 60 and (s == origem or origem in s)))


def _pontuar_resumo(texto: str, resumo: str) -> float:
    """Heurística para escolher entre DUAS saídas reais do LLM.

    Não detecta alucinações semânticas nem valida a correção científica.
    """
    if saida_com_eco(resumo, texto):
        return -100.0
    from src.validacao_resumo_tp5 import cobertura_fatos

    n_origem = len(texto.split())
    n_saida = len((resumo or '').split())
    if not n_saida:
        return -100.0
    nota = 2.0
    if n_origem >= 55:
        minimo = max(25, min(50, round(n_origem * 0.28)))
        if n_saida < minimo:
            nota -= 6.0
        elif n_saida < n_origem * 0.85:
            nota += 2.0
        else:
            nota -= 3.0
    if not (resumo or '').rstrip().endswith(('.', '!', '?')):
        nota -= 8.0  # penaliza respostas cortadas no meio da frase
    elif n_origem >= 60 and len(re.findall(r'[.!?](?:\s|$)', resumo)) >= 2:
        nota += 2.0
    if re.search(r'\b(de|do|da|dos|das|para|com|que|desde|sobre|em|por|e)\s*[.!?]?$',
                 resumo.strip(), flags=re.I):
        nota -= 6.0
    cobertura = cobertura_fatos(texto, resumo)
    if cobertura['proporcao'] is not None:
        nota += cobertura['proporcao'] * 9.0
    numeros_saida = set(re.findall(r'\b\d+(?:[.,]\d+)?\b', resumo))
    numeros_fonte = set(re.findall(r'\b\d+(?:[.,]\d+)?\b', texto))
    if numeros_saida - numeros_fonte:
        nota -= 15.0
    if re.search(r'\bmedica[cç][aã]o sobre mortalidade\b|\bé uma pública\b',
                 resumo, flags=re.I):
        nota -= 12.0
    return nota


class ModeloIndisponivel(Exception):
    pass


class ModeloOcupado(Exception):
    pass


class ProcessadorLocal:
    def __init__(self):
        self._tokenizer = None
        self._model = None
        self._modelo_portugues = False
        self._carregamento_lock = threading.Lock()
        self._inferencia_lock = threading.Lock()

    def carregar(self):
        if self._model is not None:
            return
        with self._carregamento_lock:
            if self._model is not None:
                return
            if not MODEL_DIR.is_dir():
                raise ModeloIndisponivel(
                    'Modelo PTT5-Summ não instalado. Execute: python baixar_modelo_pt_tp5.py'
                )
            try:
                from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
                tokenizer = AutoTokenizer.from_pretrained(
                    str(MODEL_DIR), local_files_only=True
                )
                model = AutoModelForSeq2SeqLM.from_pretrained(
                    str(MODEL_DIR), local_files_only=True
                )
                model.eval()
                self._tokenizer = tokenizer
                self._model = model
                self._modelo_portugues = True
            except (OSError, ValueError, ImportError, RuntimeError) as exc:
                raise ModeloIndisponivel(
                    'Não foi possível carregar os arquivos do modelo local.'
                ) from exc

    def resumir(self, texto: str) -> tuple[str, float]:
        if not self._inferencia_lock.acquire(blocking=False):
            raise ModeloOcupado('O modelo está processando outra solicitação.')
        try:
            self.carregar()
            inicio = time.perf_counter()
            import torch

            def gerar(entrada_texto: str) -> str:
                entradas = self._tokenizer(
                    entrada_texto, return_tensors='pt', truncation=True, max_length=512
                )
                # PTT5-Summ foi treinado diretamente na tarefa de sumarização PT-BR.
                # A fase anterior usava FLAN-T5-small com instruções em prompt.
                parametros = (
                    dict(max_new_tokens=132, min_new_tokens=28, num_beams=4,
                         no_repeat_ngram_size=3, do_sample=False, early_stopping=True)
                    if self._modelo_portugues else
                    dict(max_new_tokens=168, num_beams=3, length_penalty=1.15,
                         do_sample=False, no_repeat_ngram_size=3, early_stopping=True)
                )
                with torch.inference_mode():
                    saida = self._model.generate(**entradas, **parametros)
                return self._tokenizer.decode(
                    saida[0], skip_special_tokens=True
                ).strip()

            if self._modelo_portugues:
                # Sem prompt instrucional: esse checkpoint espera texto puro.
                resumo = gerar(texto.strip())
            else:
                # Compatibilidade com o modo anterior e testes que usam dublês.
                resumo = gerar(construir_prompt(texto))
                nota = _pontuar_resumo(texto, resumo)
                if nota < 10.0:
                    alternativa = gerar(construir_prompt_alternativo(texto))
                    if alternativa and _pontuar_resumo(texto, alternativa) > nota:
                        resumo = alternativa
            if not resumo:
                raise RuntimeError('O modelo retornou uma resposta vazia.')
            return resumo, round(time.perf_counter() - inicio, 3)
        finally:
            self._inferencia_lock.release()


processador = ProcessadorLocal()
