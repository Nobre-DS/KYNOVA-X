# TP5 KYNOVA-X | Reforço de rubrica: qualidade dos insights e IA

Esta atualização é **incremental**. Preserva os TPs 1–4, os CSVs oficiais existentes, `api.py`, `rotas_llm.py` e `app.py`. Corrige a principal fragilidade detectada na rubrica: insights sem interpretação explícita e saída do LLM sem auditoria.

## O que foi alterado

1. `src/analise_tp5.py`: duas interpretações descritivas calculadas diretamente dos dados tabulares da amostra, indicadores de integridade do CSV, extração literal de fatos metodológicos da fonte textual, auditoria de eco de prompt e números ausentes do texto.
2. `pages/5_Dashboard_IA.py`: apresenta esses insights com fonte, limite, relação ESG/ODS e seção de auditoria visível após solicitar a síntese.
3. `llm_local.py`: prompt delimitado e, se houver eco, **segunda tentativa** com pergunta alternativa. Isso é aprimoramento de processo, **não demonstra precisão sem testes reais**. Mantém classes e API usadas no TP4.
4. `tests/test_reforco_rubrica_tp5.py`: onze testes novos; a versão de desenvolvimento verificou 25 testes combinados (sete do TP4, sete do TP5 e onze de reforço).
5. `docs/`: versão consolidada dos documentos TDSP, com metodologia, insights, evidências e limitações. Não apaga o histórico.

## Como integrar com segurança no Mac

**1.** Pare Streamlit e FastAPI com `Control + C` em cada terminal. Faça cópia local de `llm_local.py`, `pages/5_Dashboard_IA.py`, `src/analise_tp5.py` e dos dois arquivos Markdown em `docs/`.

**2.** Copie somente os seguintes arquivos deste pacote, preservando seus caminhos:

- `src/analise_tp5.py` → `projeto_cancer/src/` (substituir)
- `pages/5_Dashboard_IA.py` → `projeto_cancer/pages/` (substituir)
- `llm_local.py` → `projeto_cancer/` (substituir após backup)
- `tests/test_reforco_rubrica_tp5.py` → `projeto_cancer/tests/` (adicionar)
- `docs/project_charter.md`, `docs/data_summary_report.md` → `projeto_cancer/docs/` (substituir após backup)

**NÃO copiar:** `data/raw/` deste pacote (contém apenas fixtures iguais à amostra já existente), `rotas_llm.py` (cópia usada nos testes) e `tests/test_rotas_llm.py` (cópia de teste do TP4). Não substituir `app.py`, `api.py` nem `requirements.txt` já corrigido.

**3.** Com a pasta `projeto_cancer` aberta e `.venv_tp4` ativo:

```bash
python -m pytest tests/test_rotas_llm.py tests/test_analise_tp5.py tests/test_reforco_rubrica_tp5.py -q
```

**4.** Rode em dois terminais (cada qual com o ambiente virtual ativado):

```bash
python -m uvicorn api:app --reload
```

```bash
python -m streamlit run app.py
```

**5.** Abra `http://localhost:8501/Dashboard_IA` e registre **capturas reais**: (a) insights com fonte e limites, (b) auditoria de IA e texto resumido, (c) resultado de todos os testes. Compare a saída da IA com a fonte oficial: ela não pode apresentar informação sem suporte. Se a auditoria sinalizar problemas, registre-os e não declare a sumarização validada.

**6.** Verifique e publique apenas após o teste funcionar:

```bash
git status --short
git add src/analise_tp5.py pages/5_Dashboard_IA.py llm_local.py tests/test_reforco_rubrica_tp5.py docs/project_charter.md docs/data_summary_report.md
git diff --cached --stat
git commit -m "TP5 - Insights auditaveis e revisao da sumarizacao"
git push origin main
```

**7.** Revise o PDF `Francisca_Nobre_PB_TP5.PDF` para incluir capturas das funcionalidades aprimoradas e resultados efetivamente observados, mantendo a rubrica documentada. Não envie captura simulada de execução do modelo.

## Interpretação para defesa oral

Os valores de próstata (77.920 casos estimados) e mama feminina (78.610) são valores da amostra do INCA, cada um em seu recorte, e estão presentes na publicação oficial 2026–2028. **Não são previsão produzida pelo LLM** e não comprovam necessidade real de serviços. A aplicação usa Pandas para organizar dados, LLM local para sintetizar texto extraído e verificação explícita para evitar que uma resposta de IA seja tratada automaticamente como fato. ESG: dimensão social (informação em saúde, ODS 3) e governança informacional (proveniência, ODS 16); não são indicadores ESG corporativos mensurados.

## Uso de IA

ChatGPT (OpenAI) foi utilizado para apoiar implementação, revisão dos testes, redação técnica e auditoria do material. O texto de IA e a atualização deverão ser validados pela estudante no ambiente local antes de atribuir ganhos de qualidade.

**Fontes:** [INCA 2026-2028](https://www.gov.br/inca/pt-br/assuntos/cancer/numeros/estimativa/estado-capital/brasil) · [ODS 3/16](https://sdgs.un.org/goals) · [FLAN-T5](https://huggingface.co/google/flan-t5-small) · [GitHub KYNOVA-X](https://github.com/Nobre-DS/KYNOVA-X).
