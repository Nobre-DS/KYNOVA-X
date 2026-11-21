# TP5 KYNOVA-X — preservar síntese de referência escolhida

## Escopo
Para aplicar esta revisão sem depender de ter copiado o pacote híbrido anterior:

- **Substituir** `pages/5_Dashboard_IA.py` (dashboard atualizado, com as duas saídas separadas).
- **Adicionar** `src/sintese_editorial_tp5.py` (síntese escolhida; 86 palavras).
- **Adicionar, caso ainda não exista** `src/sintese_assistida_tp5.py` (síntese por regras para o CSV original; mesmo conteúdo do pacote anterior).
- **Adicionar** `tests/test_sintese_editorial_tp5.py` (novos testes de preservação).
- **Adicionar, caso ainda não exista** `tests/test_sintese_assistida_tp5.py` (testes da síntese por regras).
- **Adicionar** `README_TP5_REFERENCIA_ESCOLHIDA.md` à raiz do projeto.

Faça backup de `pages/5_Dashboard_IA.py` antes de substituir. Não altere `llm_local.py`, `api.py`, os dados CSV, os modelos nem os READMEs anteriores.

## Como funciona

A saída do modelo PTT5-Summ continua visível, intocada e avaliada com seus indicadores reais. Quando o campo de entrada contém **exatamente** a síntese editorial escolhida, a interface também exibe, em seção separada, o mesmo texto de 86 palavras, com 7/7 marcadores lexicais, declarando que **não foi gerado pelo PTT5-Summ**. Os resultados editoriais e do LLM não são confundidos.

Para o texto original do CSV coletado por web scraping, a síntese estruturada por regras do pacote anterior continua disponível como etapa distinta, quando se aplicam os critérios da fonte. Esta não é apresentada como saída do LLM. Não use a referência de 86 palavras como comprovação do desempenho isolado do modelo.

**Validação do código:**

```bash
source .venv_tp4/bin/activate
python -m pytest tests/test_rotas_llm.py tests/test_analise_tp5.py tests/test_reforco_rubrica_tp5.py tests/test_qualidade_resumo_tp5.py tests/test_truncamento_resumo_tp5.py tests/test_modelo_pt_tp5.py tests/test_sintese_assistida_tp5.py tests/test_sintese_editorial_tp5.py -q
```

**Teste no dashboard:** reinicie somente o Streamlit, selecione a aba `Resumo com IA local`, insira o texto exato escolhido de 86 palavras e acione `Gerar resumo local`. Confira a seção **Síntese editorial escolhida — NÃO gerada pelo LLM**, além da seção original do LLM. Não substitua evidências de scraping pelo texto editado.

A contagem de palavras usa `str.split()` e pode variar entre aplicações que consideram pontuação composta diferentemente. O método usado deve ser declarado no relatório.

## Por que aparecem 86 e 88?
O texto editorial tem **86 palavras** quando contadas por separação em espaços (`split`). O contador lexical preexistente da aplicação (`src.analise_tp5.palavras`) separa também termos compostos unidos por hífen ou travessão, resultando em **88 unidades lexicais** para o mesmo texto. Não houve alteração no conteúdo e não é necessário modificar os testes antigos.

## Controle de qualidade
**Não é correto transformar a saída de 41 palavras e 3/7 do PTT5-Summ em 86 palavras e 7/7, pois esses últimos indicadores pertencem à referência editorial escolhida, e não ao modelo.** A aplicação apresenta as duas métricas com origem identificada. A referência foi escolhida e revisada fora do modelo local com auxílio de IA, portanto o uso de IA deve continuar citado na entrega acadêmica.
