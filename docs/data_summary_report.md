# Data Summary Report - KYNOVA-X

## 1. Identificação do Projeto

**Nome do projeto:** KYNOVA-X

**Finalidade:** Centralizar informações epidemiológicas e assistenciais de fontes oficiais para apoiar o planejamento e a gestão da atenção oncológica no Brasil.

**Fonte inicial:** Estimativas de Câncer 2026–2028 do Instituto Nacional de Câncer (INCA).

**Situação do documento:** Primeiro esboço do Data Summary Report, elaborado na etapa de planejamento do projeto.

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

## 6. Atualização das Fontes e dos Dados - TP3

Nesta terceira etapa, a KYNOVA-X manteve as fontes de dados utilizadas anteriormente e passou a disponibilizar informações por meio de uma API desenvolvida com FastAPI.

### 6.1. Dados utilizados

A aplicação continua utilizando dois arquivos principais:

- **`data/raw/estimativas_inca_2026_amostra.csv`:** contém uma amostra demonstrativa de 10 registros das estimativas de câncer do INCA para 2026, organizados pelas colunas `sexo`, `localizacao`, `casos` e `ano`.
- **`data/raw/conteudo_inca_web.csv`:** contém informações textuais coletadas de uma página oficial do INCA utilizando Requests e Beautiful Soup, organizadas pelas colunas `tipo` e `texto`.

Esses arquivos foram mantidos para alimentar as páginas de consulta da aplicação Streamlit.

### 6.2. Dados adicionais recebidos pela API

No TP3, foi desenvolvida uma API com FastAPI, utilizando duas rotas:

- **GET `/estimativas`:** permite consultar os registros disponíveis.
- **POST `/estimativas`:** permite adicionar registros com os campos `sexo`, `localizacao`, `casos` e `ano`.

Os registros enviados pela rota POST são armazenados no arquivo `data/processed/registros_api.csv`, sem modificar o CSV original das estimativas do INCA.

Durante os testes, foi incluído um registro demonstrativo para verificar o funcionamento da rota POST. Esse registro não corresponde a uma estimativa epidemiológica oficial.

### 6.3. Integração dos dados com Streamlit

A aplicação foi organizada em múltiplas páginas, permitindo consultar separadamente:

- A amostra das estimativas do INCA.
- As informações textuais extraídas da página oficial.
- Os registros combinados por meio de upload e download de arquivos CSV.
- Os registros disponibilizados pela API FastAPI.

A integração com a API foi testada por meio de uma requisição GET realizada pela aplicação Streamlit.

### 6.4. Coleta de dados de páginas web

A coleta de conteúdo textual permanece baseada em Requests e Beautiful Soup.

Não foi necessário utilizar Selenium nesta etapa, pois a fonte consultada não exigiu interação com elementos dinâmicos para a extração realizada.

Também não foram incorporadas novas fontes de dados oficiais durante o TP3.

### 6.5. Preparação dos dados para uso futuro com LLMs

Os dados estruturados das estimativas e os conteúdos textuais coletados poderão ser utilizados futuramente em funcionalidades baseadas em modelos de linguagem de grande porte (LLMs).

Uma possibilidade é desenvolver um sistema de perguntas e respostas que utilize os dados disponíveis para apoiar consultas sobre informações epidemiológicas.

Outra possibilidade é utilizar os textos oficiais coletados para gerar resumos que facilitem a compreensão das informações.

Essas funcionalidades não foram implementadas nesta etapa.

### 6.6. Limitações dos dados

A amostra utilizada não representa a totalidade das estimativas oficiais do INCA.

Os registros adicionais recebidos pela API devem ser diferenciados dos dados originais, especialmente quando utilizados apenas para testes.

As demais fontes previstas, como CNES, SIA/SUS, SIH/SUS, IBGE e Painel-Oncologia, continuam previstas para avaliação e possível integração nas próximas etapas do projeto.


### Referência da fonte oficial dos dados

Instituto Nacional de Câncer (INCA).
Brasil — estimativa dos casos novos.
Estimativas para o ano de 2026.

Fonte: https://www.gov.br/inca/pt-br/assuntos/cancer/numeros/estimativa/estado-capital/por-estado-e-capital/brasil/brasil-consolidado