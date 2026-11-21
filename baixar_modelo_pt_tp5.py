"""Baixe uma vez o PTT5-Summ para a pasta modelos, sem apagar o FLAN anterior.

Execute na raiz do projeto com .venv_tp4 ativado:
python baixar_modelo_pt_tp5.py
"""
from pathlib import Path
from huggingface_hub import snapshot_download

NOME = 'recogna-nlp/ptt5-base-summ'
DESTINO = Path(__file__).resolve().parent / 'modelos' / 'ptt5-base-summ'
DESTINO.mkdir(parents=True, exist_ok=True)
print('Baixando modelo específico para português (aprox. 900 MB).')
snapshot_download(
    repo_id=NOME,
    local_dir=str(DESTINO),
    allow_patterns=[
        'config.json', 'generation_config.json', 'model.safetensors',
        'spiece.model', 'tokenizer_config.json', 'special_tokens_map.json',
        'tokenizer.json',
    ],
)
print('Modelo salvo em:', DESTINO)
# Verificação efetiva do carregamento, antes de iniciar FastAPI.
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
AutoTokenizer.from_pretrained(str(DESTINO), local_files_only=True)
AutoModelForSeq2SeqLM.from_pretrained(str(DESTINO), local_files_only=True)
print('OK: tokenizer e modelo carregados localmente.')
