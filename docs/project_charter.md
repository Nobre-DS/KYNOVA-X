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