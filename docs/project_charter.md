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

Nesta terceira etapa, a KYNOVA-X foi aprimorada para facilitar a navegação entre as funcionalidades e permitir a consulta de dados por meio de uma API, mantendo sua proposta inicial de apoiar o planejamento e a gestão da atenção oncológica.

### 7.1. Funcionalidades desenvolvidas

- **Aplicação com múltiplas páginas:** organização da interface Streamlit em páginas destinadas à consulta das estimativas do INCA, apresentação das informações extraídas da página oficial, upload e download de arquivos CSV e consulta de dados por meio de uma API.
- **Menu de navegação:** implementação de um menu lateral para acessar as diferentes funcionalidades.
- **Integração com FastAPI:** desenvolvimento de uma API para consultar e adicionar registros.
- **Rota GET `/estimativas`:** consulta aos registros disponíveis na aplicação.
- **Rota POST `/estimativas`:** inclusão de registros adicionais, armazenados separadamente do arquivo original.
- **Integração entre Streamlit e FastAPI:** criação de uma página que permite consultar os dados da API diretamente na interface da KYNOVA-X.

As funcionalidades foram verificadas em ambiente local, incluindo testes das rotas GET e POST e da comunicação entre Streamlit e FastAPI.

### 7.2. Atualização do escopo

O problema de negócio permanece relacionado à fragmentação das informações epidemiológicas e assistenciais utilizadas no planejamento da atenção oncológica.

A implementação de múltiplas páginas e de uma API amplia as possibilidades de organização, consulta e disponibilização dos dados, sem alterar a finalidade inicial da KYNOVA-X.

Nesta etapa, foram mantidas as amostras demonstrativas das estimativas do INCA e os conteúdos textuais coletados anteriormente com Beautiful Soup.

Não foi necessário utilizar Selenium, pois a coleta realizada não exigiu interação com elementos dinâmicos da página consultada.

### 7.3. Preparação para integração futura com LLMs

Os dados disponíveis na KYNOVA-X poderão apoiar futuras funcionalidades baseadas em modelos de linguagem de grande porte (LLMs).

Uma possibilidade é desenvolver um recurso de perguntas e respostas sobre os dados epidemiológicos e os conteúdos oficiais utilizados na aplicação. Outra possibilidade é a geração de resumos de textos e informações que possam auxiliar a compreensão dos dados.

Essas funcionalidades representam possibilidades de evolução e não foram implementadas no TP3.

### 7.4. Limitações e continuidade

A KYNOVA-X continua utilizando uma amostra demonstrativa das estimativas do INCA, sem representar a totalidade das informações epidemiológicas disponíveis.

Os registros adicionais enviados à API são armazenados separadamente dos dados originais. Os registros utilizados nos testes não representam estimativas oficiais.

A integração de outras bases oficiais, como CNES, SIA/SUS, SIH/SUS, IBGE e Painel-Oncologia, permanece prevista para etapas futuras.

A aplicação e a API foram desenvolvidas e testadas localmente, sem publicação em ambiente público nesta etapa.