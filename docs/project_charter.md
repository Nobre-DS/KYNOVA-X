# Project Charter - KYNOVA-X

## 1. Identificação do Projeto

**Nome do projeto:** KYNOVA-X

**Área de aplicação:** Ciência de Dados e Inteligência Artificial aplicada à saúde.

**Finalidade:** Apoio ao planejamento e à gestão da atenção oncológica.

**Fonte inicial de dados:** Estimativas de Câncer 2026–2028 do Instituto Nacional de Câncer (INCA).

## 2. Problema de Negócio

O problema central é a fragmentação de informações epidemiológicas e assistenciais em diferentes bases oficiais de dados, o que dificulta a consulta integrada e a utilização dessas informações no planejamento e na gestão em saúde.

## 3. Objetivo Geral

Desenvolver a KYNOVA-X como uma plataforma de inteligência de dados capaz de reunir, organizar e apresentar informações epidemiológicas e assistenciais provenientes de diferentes fontes oficiais, facilitando consultas e análises que apoiem o planejamento e a gestão da atenção oncológica no Brasil.

## 4. Escopo do Projeto

**Escopo inicial - TP1:**

Desenvolvimento de uma aplicação demonstrativa em Python com Streamlit, utilizando uma amostra das Estimativas de Câncer 2026–2028 do Instituto Nacional de Câncer (INCA).

**Evolução prevista do projeto:**

Integração gradual de informações provenientes do CNES, SIA/SUS, SIH/SUS, IBGE e Painel-Oncologia, permitindo consultas e análises epidemiológicas e assistenciais em um único ambiente.

**Limitação do projeto:**

A KYNOVA-X será uma ferramenta de apoio à análise e ao planejamento da atenção oncológica, não sendo apresentada como um sistema de previsão automática da demanda por tratamentos.

## 5. Stakeholders (Partes Interessadas)

**Stakeholders principais:**

Gestores de saúde pública, profissionais envolvidos no planejamento e na gestão dos serviços de saúde, pesquisadores e epidemiologistas.

**Stakeholders secundários:**

Profissionais da área oncológica, docentes e estudantes interessados em epidemiologia, pesquisa e saúde pública.

## 6. Evolução do Projeto - TP2

Nesta segunda etapa, a aplicação KYNOVA-X foi aprimorada com novas funcionalidades, mantendo o objetivo inicial de facilitar o acesso e a organização de informações relacionadas à atenção oncológica.

As melhorias desenvolvidas foram:

- **Controle de versão:** configuração do Git e criação do repositório KYNOVA-X no GitHub.
- **Interface interativa:** implementação de um filtro por sexo, permitindo consultar separadamente os registros masculinos e femininos das estimativas do INCA.
- **Extração de conteúdo da web:** utilização da biblioteca Beautiful Soup para coletar informações textuais de uma página oficial do INCA, com armazenamento em arquivo CSV.
- **Visualização dos dados extraídos:** apresentação das informações coletadas em uma tabela na aplicação Streamlit.
- **Cache:** implementação do `st.cache_data` para reutilizar os dados carregados dos arquivos CSV.
- **Estado de sessão:** utilização do `st.session_state` para manter a seleção do filtro durante as interações do usuário.
- **Upload e download:** implementação de recursos para enviar arquivos CSV, complementar temporariamente os registros apresentados e baixar os dados combinados.

As funcionalidades foram desenvolvidas utilizando Python e Streamlit, preservando os arquivos e a organização inicial do projeto.

Nesta etapa, a KYNOVA-X continua utilizando as estimativas do INCA como fonte principal. A integração das demais bases oficiais permanece prevista para as próximas fases do desenvolvimento.

**Repositório do projeto:** https://github.com/Nobre-DS/KYNOVA-X

## 7. Evolução do Projeto - TP3

A aplicação ganhou quatro páginas Streamlit (`pages/`) para consultar estimativas, texto extraído, recursos de upload/download e a API. O FastAPI implementou GET `/estimativas` e POST `/estimativas` para registros adicionais; estes são armazenados separadamente dos dados oficiais. Requests e Beautiful Soup permaneceram suficientes para coletar o texto da página institucional do INCA, sem Selenium. A utilização de LLMs foi planejada, mas não implementada nessa etapa.


## 8. Evolução do Projeto - TP4 (verificada em 20/11/2026)

- Modelo: `google/flan-t5-small`, baixado da Hugging Face e executado localmente em CPU com Transformers e PyTorch; ambiente macOS ARM64, Python 3.11.9.
- Backend: rota `POST /processar_texto`, incorporada ao `api.py` existente por `APIRouter`, com validação Pydantic e respostas estruturadas.
- Evidências do TP4: HTTP 200 com JSON contendo a saída, HTTP 422 para entrada curta, sete testes automatizados simulados aprovados, inferência média de 1,345 s e RAM ao final de 570,1 MB na medição documentada.
- Limitação real: o modelo repetiu a instrução e parte do texto; o sucesso HTTP não atesta boa sumarização. Cenários 503/504/500 foram avaliados em testes simulados.

## 9. Consolidação do TP5 (execução local verificada em 20/11/2026)

### 9.1. Proposta e justificativa de negócio

**Problema preservado:** informações epidemiológicas e textuais estão dispersas e podem demandar consultas separadas por gestores e pesquisadores. A KYNOVA-X organiza uma amostra rastreável de dados do INCA e permite visualizar o conteúdo textual coletado e solicitar uma síntese em interface única. Não se afirma que a aplicação substitui bases completas nem que produza decisões assistenciais automáticas.

**Opção selecionada:** Opção 2 - automação de sumarização de textos usando LLM local; as opções de memória conversacional e agentes inteligentes não foram implementadas porque o enunciado exige somente uma.

**Como o prompt engineering agrega valor:** entrada baseada em conteúdo previamente extraído da fonte; instruções em português delimitam escopo, formato e vedam acréscimo de números e recomendações clínicas. A resposta é apresentada com a origem, a duração e avisos quando o texto reproduz a instrução ou não diminui de extensão. A fidelidade factual continua exigindo revisão humana.

### 9.2. Entregas e responsabilidades

| Entrega | Evidência e localização | Situação |
|---|---|---|
| Dados tabulares | `data/raw/estimativas_inca_2026_amostra.csv` (10 linhas) | Existente TP1 |
| Extração textual | `data/raw/conteudo_inca_web.csv` (2 linhas), `src/extrair_inca.py` | Existente TP2 |
| API com estimativas | `api.py`, GET e POST `/estimativas` | Existente TP3 |
| LLM local | `llm_local.py`, `rotas_llm.py`, POST `/processar_texto` | Testado TP4 |
| Dashboard com IA | `pages/5_Dashboard_IA.py`, `src/analise_tp5.py` | Executado localmente no Streamlit: tabela, gráfico e sumarização via FastAPI |
| Testes/documentação | `tests/test_analise_tp5.py`, `tests/test_rotas_llm.py` e artefatos TDSP | 14 testes automatizados aprovados, com 1 aviso de depreciação; evidências registradas em capturas locais |

**Responsável pelo projeto:** estudante autora da KYNOVA-X. **Usuários de interesse:** gestores, pesquisadores, docentes e estudantes, em cenário demonstrativo.

### 9.3. Ciclo TDSP e correspondência com Ciência de Dados

1. **Entendimento do negócio:** melhorar organização e consulta de informações relacionadas ao planejamento oncológico.
2. **Aquisição e entendimento:** amostra tabular selecionada da publicação oficial do INCA e coleta textual via Requests/Beautiful Soup; registrar proveniência e limitações.
3. **Preparação:** CSVs com esquema explícito, leitura via Pandas, verificação de colunas, tipos numéricos e remoção de entradas inválidas para visualização.
4. **Modelagem:** geração de texto com FLAN-T5-small local e prompt restritivo, sem fornecer ao LLM a tarefa de calcular casos ou inferir decisões clínicas.
5. **Avaliação:** testes de esquema, execução local, avaliação humana da fidelidade, avisos sobre ecos do prompt, gráficos e rotas com HTTP apropriado.
6. **Operacionalização/comunicação:** painel Streamlit, FastAPI, README, versionamento Git e relatório acadêmico. Não há hospedagem pública ou operação em produção.

### 9.4. Indicadores de acompanhamento (sem metas de impacto inventadas)

- Quantidade de registros amostrais exibidos e quantidade de textos coletados.
- Tempo de inferência da API e sucesso/falha das requisições.
- Contagem de palavras antes/depois da síntese, exclusivamente como métrica de extensão.
- Frequência de alertas heurísticos de eco/reprodução (não corresponde a índice de acurácia).
- Comprovação da rastreabilidade dos dados e separação de registros não oficiais.

### 9.5. ESG e ODS - alinhamento sem extrapolações

**E (ambiental):** a versão atual não mede emissões, recursos nem impactos ambientais. **S (social):** organização de informações relacionadas à saúde pública; alinhamento conceitual ao ODS 3 (Saúde e Bem-Estar). **G (governança):** transparência sobre proveniência, limitações, respostas de IA e distinção entre registros oficiais e testes; relação conceitual com o ODS 16 (instituições eficazes e responsáveis). A aplicação não foi testada para impacto causal em saúde ou pontuação ESG institucional.

### 9.6. Riscos, premissas e limites

- Fonte tabular reduzida (10 linhas), texto web reduzido (2 linhas, somente 1 elegível para resumo no limite atual); não atende ainda a processamento real de grandes volumes.
- Uma saída de LLM não deve ser interpretada como resumo correto sem confrontação com a fonte.
- Requisição ocorre em `localhost`, após download do modelo. O processamento não envia o conteúdo para API online, mas a validação offline requer teste específico se for alegada.
- Não combinar registros enviados pelos usuários com estatísticas oficiais sem identificar sua procedência.
- A página TP5 foi aberta e testada no Mac em 20/11/2026: exibiu dez registros tabulares, dois registros textuais, gráficos e o resultado do LLM local. Na captura, o texto de origem tinha 86 palavras e a saída 46; o resultado ainda reproduziu instruções de sumarização, portanto **não** se atestou qualidade semântica satisfatória. A redução de palavras não demonstra precisão.
- Após ajuste local de compatibilidade das bibliotecas (NumPy 2.2.6 e Pandas 2.2.3), a interface carregou sem o erro anterior do PyArrow. A correção deverá ser registrada no arquivo de dependências.
- A execução offline, a escala em grandes volumes e impacto assistencial/ESG não foram avaliados; não devem ser alegados.

**Referências:** INCA (Estimativas 2026-2028); Nações Unidas (ODS 3 e 16); Hugging Face (modelo FLAN-T5-small); código em https://github.com/Nobre-DS/KYNOVA-X; uso do ChatGPT (OpenAI) como ferramenta de apoio ao desenvolvimento, mediante validação do usuário.
