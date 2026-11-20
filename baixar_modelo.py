"""Executar UMA VEZ com internet; a API nao baixa modelos."""
from pathlib import Path
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

pasta = Path(__file__).resolve().parent / 'modelos' / 'flan-t5-small'
pasta.mkdir(parents=True, exist_ok=True)
nome = 'google/flan-t5-small'
print('Baixando tokenizer...')
AutoTokenizer.from_pretrained(nome).save_pretrained(str(pasta))
print('Baixando pesos do modelo...')
AutoModelForSeq2SeqLM.from_pretrained(nome).save_pretrained(str(pasta), safe_serialization=True)
print('Modelo salvo em', pasta)
