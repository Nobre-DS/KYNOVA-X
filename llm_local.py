"""Modulo adicional da KYNOVA-X: sintese de texto em CPU, inteiramente local."""
from pathlib import Path
import threading
import time

MODEL_DIR = Path(__file__).resolve().parent / 'modelos' / 'flan-t5-small'
MODEL_NAME = 'google/flan-t5-small'

class ModeloIndisponivel(Exception):
    pass

class ModeloOcupado(Exception):
    pass

class ProcessadorLocal:
    def __init__(self):
        self._tokenizer = None
        self._model = None
        self._carregamento_lock = threading.Lock()
        self._inferencia_lock = threading.Lock()

    def carregar(self):
        if self._model is not None:
            return
        with self._carregamento_lock:
            if self._model is not None:
                return
            if not MODEL_DIR.is_dir():
                raise ModeloIndisponivel('Modelo local ausente. Execute python baixar_modelo.py.')
            try:
                from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
                tokenizer = AutoTokenizer.from_pretrained(str(MODEL_DIR), local_files_only=True)
                model = AutoModelForSeq2SeqLM.from_pretrained(str(MODEL_DIR), local_files_only=True)
                model.eval()
                self._tokenizer = tokenizer
                self._model = model
            except (OSError, ValueError, ImportError, RuntimeError) as exc:
                raise ModeloIndisponivel('Nao foi possivel carregar os arquivos do modelo local.') from exc

    def resumir(self, texto: str) -> tuple[str, float]:
        if not self._inferencia_lock.acquire(blocking=False):
            raise ModeloOcupado('O modelo esta processando outra solicitacao.')
        try:
            self.carregar()
            inicio = time.perf_counter()
            prompt = ('Resuma o texto a seguir em portugues, sem inventar dados: ' + texto)
            entradas = self._tokenizer(prompt, return_tensors='pt', truncation=True, max_length=384)
            import torch
            with torch.inference_mode():
                saida = self._model.generate(**entradas, max_new_tokens=110, do_sample=False)
            resumo = self._tokenizer.decode(saida[0], skip_special_tokens=True).strip()
            if not resumo:
                raise RuntimeError('O modelo retornou uma resposta vazia.')
            return resumo, round(time.perf_counter() - inicio, 3)
        finally:
            self._inferencia_lock.release()

processador = ProcessadorLocal()
