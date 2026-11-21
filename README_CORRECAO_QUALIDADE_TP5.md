# KYNOVA-X — Correção dirigida da sumarização no TP5

## Diagnóstico da execução de 20/11/2026

No teste real do Mac, um texto editado com 178 palavras produziu uma resposta de apenas 32 palavras, com expressão incorreta ("é uma pública") e final incompleto ("Desde 1995, elaborado"). O código enviado continha instrução de apenas UMA frase e `max_new_tokens=96`. O modelo FLAN-T5-small, por ser pequeno, pode continuar produzindo resultados inadequados mesmo com o prompt melhorado.

## Arquivos — copiar mantendo exatamente estas pastas

- **SUBSTITUIR** `projeto_cancer/llm_local.py`.
- **SUBSTITUIR** `projeto_cancer/pages/5_Dashboard_IA.py`.
- **INCLUIR** `projeto_cancer/src/validacao_resumo_tp5.py` (se já existir, substituir somente após backup).
- **INCLUIR** `projeto_cancer/tests/test_qualidade_resumo_tp5.py` (se já existir, substituir somente após backup).
- **INCLUIR** `projeto_cancer/tests/test_truncamento_resumo_tp5.py`.

Não alterar `api.py`, `app.py`, `rotas_llm.py`, dados CSV ou READMEs originais. Fazer backup dos arquivos substituídos.

## O que muda

1. Prompt de **duas a três frases completas**, em vez de uma frase curta.
2. `max_new_tokens=168`, `num_beams=3`, `length_penalty=1.15`.
3. Segunda tentativa do FLAN-T5-small quando a primeira tem pontuação heurística baixa, inclusive truncamento.
4. Dashboard diferencia a **saída real, não editada, do LLM** da **síntese de referência por regras** sobre o texto extraído. O modelo **nunca** recebe uma síntese pronta como resposta.
5. Indicadores de marcadores preservados e avisos de saída demasiado curta ou cortada. Marcadores não medem fidelidade semântica.

## Testes, em terminal com ambiente .venv_tp4

```bash
python -m pytest tests/test_rotas_llm.py tests/test_analise_tp5.py tests/test_reforco_rubrica_tp5.py tests/test_qualidade_resumo_tp5.py tests/test_truncamento_resumo_tp5.py -q
```

## Teste real do Mac

1. Reinicie o FastAPI (Ctrl+C no terminal onde já está rodando; em seguida `python -m uvicorn api:app --reload`). Evite executar um segundo servidor na porta 8000.
2. Execute `python -m streamlit run app.py` no outro terminal, se ainda não estiver aberto.
3. Na página **IA do Painel de Controle** selecione o registro textual coletado do INCA (`conteudo_inca_web.csv`) e clique em **Gerar resumo local**.
4. Anote quantidade de palavras, marcadores preservados, conclusão das frases e tempo de inferência. Compare com a síntese de referência, sem confundir as origens.
5. Faça também uma execução com texto editado, identificando-a como **entrada manual de teste**, não como scraping.
6. Guarde capturas de tela. Não declare que a qualidade da IA está aprovada se o novo texto continuar truncado ou incorreto.

## Limitações técnicas e integridade acadêmica

A extensão ou os marcadores são indicadores de forma e cobertura lexical, não prova de veracidade. A saída do LLM pode continuar incompleta e exigir revisão humana. Uma melhoria de qualidade mais substancial pode exigir modelo especializado em português ou serviço de IA externo, com avaliação e referência de modelo.

O professor avalia o uso efetivo da IA e a aplicação dos dados coletados; o PDF final deve ser atualizado com **evidências de execução**, e citar os assistentes de IA utilizados na elaboração do código e da documentação.
