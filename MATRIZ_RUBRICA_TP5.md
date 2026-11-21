# TP5 — matriz de evidências para os oito critérios binários

| Critério oficial (síntese fiel) | Evidência no projeto | Status da revisão |
|---|---|---|
| 1. Integração de funcionalidade LLM ao dashboard | Aba "2. Resumo com IA local" → FastAPI → FLAN-T5 | Comprovada no TP5 original |
| 2. Dados coletados geram insights ESG/ODS | Insights numéricos calculados do CSV (por sexo) e fatos metodológicos extraídos do texto; fonte e limites | Implementado no reforço; captura no Mac pendente |
| 3. Coleta, processamento, análise, apresentação | `data/raw`, `src`, gráficos Streamlit, FastAPI e IA | Documentado; reforçado |
| 4. Solução do problema e impacto ESG/ODS | Problema de fragmentação; ODS 3 e ODS 16; limites explícitos | Demonstrado conceitualmente; impacto não mensurado |
| 5. LLM eficiente e alinhado | Modelo local + prompt revisado + segunda tentativa condicional + auditoria | Código testado com simulações; fidelidade do LLM real pendente |
| 6. Visualizações claras | Gráficos, indicadores, tabela, insights e auditoria | Visualização antiga demonstrada; nova captura pendente |
| 7. Project Charter e Data Summary Report atualizados | `docs/` com histórico + método e evidências | Atualizado; publicação da revisão pendente |
| 8. Simplicidade e fluidez | Mesma navegação Streamlit em abas, botão de resumo e avisos explícitos | Fluxo antigo demonstrado; nova versão pendente de inspeção |

**Regra de integridade:** "implementado" não é sinônimo de "comprovado no Mac" nem de "aprovado pelo professor". Não há garantia de pontuação antes da avaliação docente. Nunca inferir efeito assistencial ou nível ESG corporativo apenas a partir de uma amostra de dez linhas.
