# Data Summary Report - KYNOVA-X

## 1. Identificação do Projeto

**Nome do projeto:** KYNOVA-X

**Finalidade:** Centralizar informações epidemiológicas e assistenciais de fontes oficiais para apoiar o planejamento e a gestão da atenção oncológica no Brasil.

**Fonte inicial:** Estimativas de Câncer 2026–2028 do Instituto Nacional de Câncer (INCA).

**Situação do documento:** Consolidado até TP5; execução da interface e sumarização local verificadas em 20/11/2026. Não corresponde à implantação em produção.

## 2. Fonte Principal de Dados

**Fonte:** Instituto Nacional de Câncer (INCA).

**Publicação:** Estimativas de Câncer 2026–2028.

**Tipo de dados:** Estimativas de casos novos de câncer, segundo localização e recortes disponíveis na publicação oficial.

**Objetivo de uso:** Apresentar informações epidemiológicas sobre a incidência de câncer no Brasil, permitindo consultas, visualizações e comparações que possam apoiar a identificação de prioridades e o planejamento da atenção oncológica.

**Situação:** Fonte principal selecionada para a aplicação demonstrativa do TP1.

## 3. Fontes Complementares Previstas

As seguintes fontes oficiais estão previstas para avaliação e possível integração futura à KYNOVA-X:

- **CNES:** estabelecimentos de saúde, serviços especializados e equipamentos cadastrados.
- **SIA/SUS:** procedimentos ambulatoriais registrados no Sistema Único de Saúde.
- **SIH/SUS:** internações e procedimentos hospitalares registrados no SUS.
- **IBGE:** informações populacionais e territoriais.
- **Painel-Oncologia:** indicadores relacionados ao diagnóstico e ao início do tratamento oncológico.

A incorporação dessas fontes será realizada progressivamente, conforme a disponibilidade, a compatibilidade e as necessidades de análise do projeto.

## 4. Tipos de Dados e Objetivos de Utilização

| Fonte | Dados de interesse | Aplicação na KYNOVA-X | Prioridade |
|---|---|---|---|
| INCA — Estimativas 2026–2028 | Estimativas de casos novos de câncer, segundo localização e recortes disponíveis | Contextualização epidemiológica e identificação de prioridades | 1 — Principal |
| CNES | Estabelecimentos, serviços especializados e equipamentos cadastrados | Mapeamento da oferta assistencial | 2 — Complementar |
| SIA/SUS | Procedimentos ambulatoriais registrados no SUS | Análise da produção ambulatorial oncológica | 3 — Complementar |
| SIH/SUS | Internações e procedimentos hospitalares registrados | Análise da produção hospitalar | 3 — Complementar |
| IBGE | População e informações territoriais | Indicadores populacionais e análises territoriais | 4 — A avaliar |
| Painel-Oncologia | Indicadores relacionados ao diagnóstico e ao início do tratamento | Análise de aspectos da trajetória assistencial | 4 — Complementar |

## 5. Atualização das Fontes e dos Dados - TP2

Nesta segunda etapa, foram mantidas as Estimativas de Câncer 2026–2028 do Instituto Nacional de Câncer (INCA) como fonte principal de informações epidemiológicas da KYNOVA-X.

Além da utilização da amostra de dados já existente no TP1, foi realizada a extração de conteúdo textual de uma página oficial do INCA, utilizando Python e a biblioteca Beautiful Soup.

### 5.1. Arquivos de dados utilizados

| Arquivo | Origem | Tipo de dados | Finalidade |
|---|---|---|---|
| `estimativas_inca_2026_amostra.csv` | Amostra de estimativas do INCA utilizada no TP1 | Dados tabulares: sexo, localização do câncer, casos estimados e ano | Permitir consultas e filtragem por sexo na aplicação |
| `conteudo_inca_web.csv` | Conteúdo extraído de uma página oficial do INCA com Beautiful Soup | Dados textuais: tipo de elemento HTML e texto extraído | Apresentar informações da página do INCA na aplicação |
| CSV enviado pelo usuário | Arquivo selecionado por meio do recurso de upload | Dados tabulares com as colunas sexo, localizacao, casos e ano | Complementar temporariamente os registros apresentados e permitir o download dos dados combinados |

### 5.2. Organização e armazenamento

Os arquivos de dados utilizados pela aplicação estão organizados no diretório `data/raw/` do projeto.

O arquivo `estimativas_inca_2026_amostra.csv` contém 10 registros utilizados na demonstração inicial da KYNOVA-X.

O arquivo `conteudo_inca_web.csv` contém informações textuais obtidas por meio da extração de conteúdo de uma página oficial do INCA.

O conteúdo extraído foi armazenado em formato CSV para posterior leitura e apresentação na aplicação Streamlit.

### 5.3. Tratamento e utilização dos dados

Os arquivos CSV são carregados utilizando a biblioteca Pandas.

A aplicação permite filtrar os registros de estimativas por sexo e visualizar os dados em tabelas.

O carregamento dos arquivos utiliza `st.cache_data`, enquanto `st.session_state` mantém a seleção do filtro durante as interações do usuário.

Também foi implementado o envio de arquivos CSV pelo usuário, com verificação das colunas esperadas, combinação temporária dos registros e disponibilização de um novo arquivo CSV para download.

### 5.4. Limitações e continuidade

Os registros utilizados nesta etapa constituem uma amostra demonstrativa, não representando a totalidade das informações disponíveis nas publicações oficiais do INCA.

O conteúdo textual extraído da página do INCA é apresentado para consulta e não constitui uma nova base de estimativas epidemiológicas.

As fontes complementares CNES, SIA/SUS, SIH/SUS, IBGE e Painel-Oncologia permanecem previstas para avaliação e possível integração nas próximas etapas do projeto.

## 6. Atualização do Data Summary Report - TP3

O TP3 manteve os dois arquivos principais (`data/raw/estimativas_inca_2026_amostra.csv` e `data/raw/conteudo_inca_web.csv`) e implementou a API FastAPI GET `/estimativas` e POST `/estimativas`. Registros enviados ao POST são gravados separadamente em `data/processed/registros_api.csv`, que pode conter casos fictícios de teste e não é parte da base oficial. A página Streamlit `4_Consulta_API.py` consome o GET. Não houve integração de novas bases nem uso de Selenium; o texto já vinha da extração via Requests/Beautiful Soup.

## 7. Integração técnica TP4 e TP5 - linhagem dos dados

| Camada | Entrada | Operação | Saída e utilização |
|---|---|---|---|
| Aquisição numérica (TP1) | Página de estimativas do INCA, amostra selecionada | Organização tabular | `data/raw/estimativas_inca_2026_amostra.csv` |
| Aquisição textual (TP2) | Página oficial do INCA | Requests + Beautiful Soup, extração `h1`/`p` | `data/raw/conteudo_inca_web.csv` |
| Preparação de dados (TP5) | Os dois CSVs originais | Pandas; conferência de colunas, normalização de espaços e tipos | Tabelas e trechos aptos à sumarização |
| Modelagem LLM (TP4/5) | Texto previamente extraído e selecionado no painel | Prompt delimitado + FLAN-T5-small local via FastAPI | JSON de sucesso com resumo, modelo e tempo |
| Avaliação/comunicação (TP5) | Dados tabulares + JSON do modelo | Gráficos de estimativas selecionadas, comparação de palavras e alertas heurísticos | Página `pages/5_Dashboard_IA.py` |

### 7.1. Dicionário de dados observado

**Estimativas (10 linhas selecionadas):** `sexo` (categoria), `localizacao` (categoria descritiva), `casos` (inteiro de casos estimados, não contagem de pacientes do projeto) e `ano` (2026 na amostra). O gráfico se baseia estritamente nessas dez linhas e não representa ranking nacional, taxas padronizadas ou prevalência.

**Textos web (2 linhas):** `tipo` (elemento HTML; por exemplo `h1` e `p`) e `texto` (conteúdo textual extraído do site oficial). Somente o registro `p` tem 30 ou mais caracteres e pode ser encaminhado à rota de TP4; `h1` isolado é insuficiente. O campo de texto enviado pela API tem limite de 30 a 1.500 caracteres.

### 7.2. Preparação e qualidade dos dados

- Confirmar presença de colunas obrigatórias antes do processamento.
- Converter `casos` e `ano` em tipos numéricos e eliminar linhas inválidas para os gráficos, sem corrigir números manualmente.
- Remover espaços redundantes dos trechos coletados; selecionar apenas conteúdo textual utilizável.
- Conservar os dados brutos originais, separados dos registros de teste enviados pela API.
- Evitar soma de categorias epidemiológicas diferentes como total nacional; os registros são apenas uma seleção de valores publicados.
- Transparência: a comparação de palavras antes/depois é medida **linguística de comprimento**, não índice de fidelidade ou precisão.

### 7.3. Prompt Engineering e inferência local

O TP4 comprovou integração via POST `/processar_texto` com FLAN-T5-small e JSON `texto_original`, `tipo_analise`, `resultado`, `modelo`, `execucao` e `tempo_segundos`. A versão de prompt disponibilizada para o TP5 restringe a resposta a até duas frases e instrui que não se acrescentem números nem recomendações clínicas. A saída original do TP4 teve eco parcial da instrução. No teste efetivo da página TP5, a saída ainda incluiu expressão instrucional; não há evidência de melhoria factual. A fidelidade e a utilidade dos resumos exigem revisão humana.

### 7.4. Dados coletados versus dados adicionais

`data/processed/registros_api.csv` não alimenta a visualização de amostra oficial no dashboard TP5. Qualquer registro enviado pelo usuário permanece distinto da base `data/raw`. As demais fontes (CNES, SIA/SUS, SIH/SUS, IBGE e Painel-Oncologia) **não foram integradas** e não podem ser mencionadas como resultados presentes.

### 7.5. Estado de verificação e limitações

**Comprovado nos testes do TP4 (20/11/2026):** CPU local ARM64/Python 3.11.9; média de inferência 1,345 s; memória final do processo 570,1 MB; HTTP 200/422 reais; 7 testes automatizados com simulações aprovados; código do TP4 publicado no GitHub.

**Comprovado nos testes do TP5 (20/11/2026):** dashboard Streamlit carregado no Mac após correção de compatibilidade das bibliotecas; 10 linhas da amostra numérica e 2 registros de coleta textual exibidos; gráfico de estimativas gerado; sumarização requisitada à API local com saída apresentada e gráfico de palavras (86 palavras na origem e 46 na saída, conforme captura); execução de `pytest` com **14 testes aprovados e 1 aviso de depreciação**. A resposta observada reproduziu texto instrucional, limitando a utilidade da sumarização. A publicação dos códigos do TP5 no GitHub ainda depende de `git commit` e `git push`; não está declarada como concluída.

**Limites:** apenas uma pequena amostra e um parágrafo elegível para resumo; não há evidência de sumarização de grandes volumes, de ganho de produtividade medido ou de efetividade clínica. A geração do LLM pode omitir/alterar fatos.

### 7.6. Fontes e IA utilizada

- INCA. Estimativas de Câncer 2026–2028. https://www.gov.br/inca/pt-br/assuntos/cancer/numeros/estimativa/estado-capital/por-estado-e-capital/brasil/brasil-consolidado
- Nações Unidas. Objetivos de Desenvolvimento Sustentável. https://sdgs.un.org/goals
- Hugging Face. `google/flan-t5-small`. https://huggingface.co/google/flan-t5-small
- Repositório: https://github.com/Nobre-DS/KYNOVA-X
- ChatGPT (OpenAI) como apoio à redação, documentação e geração/revisão de código, sujeito a teste e validação humana.
