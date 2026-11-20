# KYNOVA-X - extensao TP4

**Nao substitua `api.py` do TP3**. Copie `rotas_llm.py`, `llm_local.py`, `baixar_modelo.py`, `medir_modelo.py`, a pasta `tests` e `requirements_tp4.txt` para a raiz do repositorio existente.

Adicione ao `api.py` existente, **apos a declaracao da variavel `app = FastAPI(...)`**:

```python
from rotas_llm import router as router_llm
app.include_router(router_llm)
```

## Execucao no Mac (terminal VS Code)

```bash
python3 -m venv .venv_tp4
source .venv_tp4/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements_tp4.txt
python baixar_modelo.py
python medir_modelo.py
python -m pytest tests/test_rotas_llm.py -q
uvicorn api:app --reload
```

Confira `http://127.0.0.1:8000/docs`; `POST /processar_texto`; clicar Try it out. Exemplo:

```json
{"texto":"O Instituto Nacional de Cancer divulga estimativas de incidencia para apoiar o planejamento em saude. Essas estimativas exigem interpretacao cuidadosa e consulta a fonte original."}
```

O primeiro download usa internet; a API carrega **apenas a pasta local**, sem servicos remotos. Para comprovar falta de rede, desligue a internet DEPOIS de baixar e repita o teste. Usar `--reload` pode reimportar arquivos se eles mudarem.

## Erros

422: entrada curta/incorreta; 503: modelo ausente ou ocupado; 504: tempo de espera HTTP excedido; 500: falha interna. Em 504, a thread de inferencia **pode continuar executando**; e um limite de espera da requisicao, nao interrupcao forcada do calculo.

## Git

Acrescente `modelos/` ao `.gitignore` existente, sem apagar as regras do TP3. Nao inclua modelos nem ambientes virtuais no repositório. Atualize README existente com esta secao. Confirme que `api.py` original e as rotas GET/POST de `/estimativas` permanecem intactos.

## Limites

O FLAN-T5-small e modelo instrucional seq2seq, nao um chatbot autoregressivo de varios bilhoes de parametros. Seu desempenho em portugues e em texto epidemiologico precisa ser medido; respostas podem omitir ou alterar fatos. Nao o utilize para aconselhamento clinico ou inferencia quantitativa automatizada. Os testes pytest sao simulacoes do caminho de erros, e nao substituem o teste real do modelo.

## Resultados dos testes locais - TP4

Ambiente: macOS ARM64, Python 3.11.9.

Modelo: google/flan-t5-small.
Execução: local, utilizando Transformers e PyTorch.

Resultados:
- Tempo médio de inferência: 1,345 segundo.
- Memória do processo ao final: 570,1 MB.
- Requisição FastAPI: HTTP 200.
- Tempo da requisição registrada: 7,114 segundos.
- Validação de texto inválido: HTTP 422.
- Testes automatizados: 7 aprovados.

Limitação identificada:
O modelo executou localmente, mas apresentou reprodução
parcial da instrução e do texto original, sem produzir
uma síntese satisfatória. Sua qualidade factual ainda
necessita de aprimoramento e avaliação adicional.
