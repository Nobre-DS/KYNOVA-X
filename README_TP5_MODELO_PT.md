# KYNOVA-X — Correção da sumarização em português (TP5)

## Motivo

O modelo FLAN-T5-small gerou resposta truncada e com problemas gramaticais: teste real com o texto de 86 palavras, resposta de 68 palavras, 5/7 marcadores, qualidade **reprovada**. Não se declara que passou.

A alternativa escolhida foi `recogna-nlp/ptt5-base-summ`, um modelo T5 de sumarização abstrativa **ajustado com dados em português brasileiro**, publicado sob licença MIT. É utilizado somente para a tarefa de sumarização; não altera os dados originais, análises, rotas nem a aplicação Streamlit. O checkpoint FLAN anterior permanece preservado em `modelos/flan-t5-small`.

## Instalação simples no Mac

1. Com FastAPI e Streamlit parados, faça backup do `llm_local.py` e de `pages/5_Dashboard_IA.py`.
2. Copie da pasta deste pacote `llm_local.py` para a **raiz** do `projeto_cancer` (**substituir**); copie `pages/5_Dashboard_IA.py` para `projeto_cancer/pages` (**substituir**).
3. Copie `baixar_modelo_pt_tp5.py` para a **raiz**, `tests/test_modelo_pt_tp5.py` para a pasta `tests/` e este README para a raiz (**adicionar**).
4. Ative o ambiente: `source .venv_tp4/bin/activate`.
5. Execute **uma vez com internet**: `python baixar_modelo_pt_tp5.py`. O modelo pode ocupar aproximadamente 900 MB no Mac. Não precisa reenviar esses pesos ao GitHub.
6. Execute os testes: `python -m pytest tests/test_rotas_llm.py tests/test_analise_tp5.py tests/test_reforco_rubrica_tp5.py tests/test_qualidade_resumo_tp5.py tests/test_truncamento_resumo_tp5.py tests/test_modelo_pt_tp5.py -q`.
7. Pare o servidor Uvicorn que já estiver rodando na porta 8000 e inicie novamente: `python -m uvicorn api:app --reload`. Em outro terminal, inicie o Streamlit: `python -m streamlit run app.py` (a porta poderá ser 8501 ou 8502).
8. Em `Dashboard IA > Resumo com IA local`, gere o resumo **do trecho original coletado**, não de um resumo manual. Observe a saída, os avisos e a cobertura dos marcadores.

### Como avaliar

- O novo modelo deve aparecer no dashboard como `recogna-nlp/ptt5-base-summ`.
- Verifique frases completas, correção gramatical, fatos da fonte e datas 1995 / 2026–2028.
- O controle automático é heurístico e não valida verdade factual. Se ainda houver problemas, mantenha o estado de reprovação; não substitua a saída do modelo pela síntese de referência.
- Os testes unitários usam simulações; **não demonstram qualidade real do modelo**.
- Não publique os pesos (`modelos/`) nem arquivos de ambiente (`.venv_tp4/`) no GitHub.
- Somente após a validação real, documente a mudança de modelo no relatório e no PDF.

**Modelo:** https://huggingface.co/recogna-nlp/ptt5-base-summ — autores e licença conforme model card.

**Observação:** modelos de sumarização especializados nem sempre utilizam um prompt instrucional. A engenharia de prompts foi explorada com FLAN-T5-small nos testes anteriores; este ajuste compara abordagens e utiliza os parâmetros de decodificação do modelo especializado.
