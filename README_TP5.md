# KYNOVA-X — TP5 (Projeto de Bloco: IA Aplicada)

**Opção 2:** automação da sumarização de textos oficiais coletados via web scraping, com LLM local (FLAN-T5-small). Reaproveita os TPs 1–4 sem mudar o problema de negócio.

## O que foi acrescentado

- `pages/5_Dashboard_IA.py`: página Streamlit interativa com amostra tabular do INCA, gráfico, seleção do texto coletado, chamada local à API de sumarização, resultado, comparação de extensão e alertas de baixa qualidade.
- `src/analise_tp5.py`: leitura e validação dos CSVs, contagem de palavras e heurísticas de qualidade (não substituem avaliação humana).
- `llm_local.py`: variante do TP4 com instruções de prompt mais restritas, preservando a classe, a rota e o processamento local. **É necessário validar o resultado no Mac; não se presume melhora.**
- `docs/project_charter.md` e `docs/data_summary_report.md`: documentos TDSP consolidados e alinhamento aos ODS/ESG, com limites explícitos.
- `tests/test_analise_tp5.py`: testes do tratamento de dados e alertas. Testes do TP4 continuam disponíveis.
- `requirements_tp5.txt`: reutilização do ambiente TP4 e dependências dos TPs anteriores.

## Integração no projeto existente

1. Faça cópia de segurança de `projeto_cancer`.
2. Copie `pages/5_Dashboard_IA.py`, `src/analise_tp5.py`, `tests/test_analise_tp5.py`, `README_TP5.md` e `requirements_tp5.txt` para as pastas correspondentes.
3. Confira os dois arquivos Markdown de `docs/` antes de substituir os existentes (as versões deste pacote consolidam o TP3 e acrescentam TP4–TP5).
4. **Opcional, para usar o prompt TP5:** faça backup do `llm_local.py` existente e substitua pelo novo `llm_local.py`. A rota e a API permanecem com os mesmos nomes. Ao executar, valide a fidelidade da saída.
5. **Não substitua** `api.py`, `app.py`, os CSVs em `data/raw` ou as quatro páginas anteriores.

No terminal do VS Code aberto em `projeto_cancer`:

```bash
source .venv_tp4/bin/activate
python -m pip install -r requirements_tp5.txt
python -m pytest tests/test_analise_tp5.py tests/test_rotas_llm.py -q
```

Abra **dois terminais** (com o ambiente TP4 ativo em ambos):

**Terminal FastAPI**

```bash
python -m uvicorn api:app --reload
```

**Terminal Streamlit**

```bash
python -m streamlit run app.py
```

Acesse o endereço local apresentado pelo Streamlit (geralmente `http://localhost:8501`) e, no menu lateral, selecione **5 Dashboard IA**. Selecione o trecho do CSV extraído e clique em **Gerar resumo local**. A API deve estar disponível em `http://127.0.0.1:8000/docs`.

## Conferência de entrega (execução real no Mac)

- Registrar print da tela com os **10 registros amostrais**, filtro e gráfico.
- Registrar print da aba **Resumo com IA local**, com fonte selecionada, texto e resposta real.
- Registrar print do gráfico **Texto de origem × Saída do LLM** e avisos de qualidade.
- Registrar print dos testes automatizados do TP5 (mais testes antigos do TP4).
- Executar `git status --short` e conferir se `.venv_tp4/`, `modelos/` e `.pytest_cache/` estão ignorados.
- Após validar, publicar alterações com `git add ...`, `git commit ...` e `git push origin main`.
- Atualizar o relatório PDF com **as capturas e resultados reais do TP5**. Não apresentar testes locais não executados como concluídos.

## Fonte, integridade e limitações

- Texto selecionado de `data/raw/conteudo_inca_web.csv`, obtido com Requests e Beautiful Soup de uma página do INCA. Há **2 registros de texto**, dos quais apenas **1** tem comprimento suficiente para entrada na API do TP4.
- A tabela numérica utiliza `data/raw/estimativas_inca_2026_amostra.csv` (**10 registros selecionados**). O gráfico não é ranking nacional, e seus valores não devem ser somados como total único de câncer.
- `data/processed/registros_api.csv` pode conter registros de teste **não oficiais**; a página TP5 **não** utiliza esse arquivo para exibir dados oficiais.
- O modelo FLAN-T5-small foi executado no TP4, mas repetiu parcialmente a instrução no exemplo documentado. O TP5 modifica o prompt, mas **sua qualidade deve ser reavaliada no Mac**.
- As heurísticas de texto são sinais de possível problema, não provas de acurácia factual.
- Não há medições de impacto causal, desempenho ESG, capacidade assistencial, previsão de demanda ou aconselhamento clínico.

## Alinhamento

**ODS 3:** saúde e bem-estar — acesso a informações para apoiar planejamento oncológico. **ODS 16:** transparência/rastreabilidade da informação. O tema é *sustentabilidade social e governança da informação*, não um dataset corporativo de indicadores ESG.

## Referências e uso de IA

- INCA: https://www.gov.br/inca/pt-br/assuntos/cancer/numeros/estimativa/estado-capital/por-estado-e-capital/brasil/brasil-consolidado
- ONU/ODS: https://sdgs.un.org/goals
- FLAN-T5-small: https://huggingface.co/google/flan-t5-small
- Streamlit: https://docs.streamlit.io/
- Código e histórico: https://github.com/Nobre-DS/KYNOVA-X
- ChatGPT (OpenAI) foi utilizado para auxiliar na organização, redação, desenvolvimento e revisão do código e documentação; as saídas precisam ser validadas pela estudante em execução local.
