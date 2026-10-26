# KYNOVA-X

**Plataforma de Inteligência de Dados para o Planejamento da Atenção Oncológica**

A KYNOVA-X é um projeto acadêmico desenvolvido em Python e Streamlit, no curso de Ciência de Dados. A proposta é facilitar a consulta e a organização de informações que possam contribuir para o planejamento da atenção oncológica no Brasil.

## O que foi desenvolvido no TP2

Nesta etapa, a aplicação utiliza uma amostra de 10 registros das estimativas de câncer do INCA para 2026, no contexto da publicação *Estimativas de Câncer 2026–2028*. Essa amostra é usada apenas para demonstração e não representa todos os dados disponíveis no INCA.

A aplicação permite:

- Consultar os registros e filtrar os dados por sexo.
- Visualizar informações de uma página oficial do INCA, coletadas com Requests e Beautiful Soup.
- Carregar arquivos CSV com o auxílio da biblioteca Pandas.
- Utilizar `st.cache_data` no carregamento dos arquivos e `st.session_state` para manter a seleção do filtro.
- Enviar um arquivo CSV para acrescentar registros à tabela apresentada.
- Baixar um CSV com os dados combinados.

## Organização do projeto

```
projeto_cancer/
├── .venv/
├── .venv_tp2/
├── data/
│   ├── processed/
│   └── raw/
│       ├── conteudo_inca_web.csv
│       └── estimativas_inca_2026_amostra.csv
├── docs/
│   ├── data_summary_report.md
│   └── project_charter.md
├── notebooks/
├── src/
│   └── extrair_inca.py
├── .gitignore
├── app.py
├── README.md
└── requirements.txt
```

As pastas `.venv` e `.venv_tp2` correspondem aos ambientes virtuais criados no computador para o desenvolvimento do projeto. Esses diretórios são utilizados localmente e não precisam ser enviados ao GitHub.

## Como executar a aplicação

Para executar o projeto no computador, é necessário ter Python instalado. O ambiente utilizado no TP2 foi criado com Python 3.9.

Abra o Terminal na pasta `projeto_cancer` e execute os comandos abaixo, na ordem apresentada:

```
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
streamlit run app.py
```

Depois, abra no navegador o endereço local informado pelo Streamlit.

O arquivo `conteudo_inca_web.csv` já está salvo na pasta `data/raw/`. Caso seja necessário executar novamente a coleta de texto da página do INCA, utilize:

```
python src/extrair_inca.py
```

Essa coleta depende de conexão com a internet e da disponibilidade da página consultada.

## Upload e download de dados

Na seção **Upload e Download de Dados**, é possível enviar um arquivo CSV que contenha as colunas `sexo`, `localizacao`, `casos` e `ano`.

Os registros enviados são acrescentados temporariamente aos dados exibidos na aplicação. O arquivo original não é alterado. O resultado pode ser baixado com o nome `dados_completos_kynova.csv`.

Para testar essa função, foi enviado o próprio arquivo da amostra inicial. Assim, o resultado apresentou 20 registros, sendo 10 repetidos somente para confirmar que o upload e o download estavam funcionando.

## Preparação para publicação

Os arquivos do projeto, as dependências e os documentos estão organizados para facilitar uma possível publicação da aplicação. O código também está armazenado no GitHub.

No TP2, a aplicação foi executada e testada localmente. **Ela ainda não foi publicada em um endereço público.**

## Fontes e documentação

A fonte principal é o Instituto Nacional de Câncer (INCA):

[https://www.gov.br/inca/pt-br/assuntos/cancer/numeros/estimativa](https://www.gov.br/inca/pt-br/assuntos/cancer/numeros/estimativa)

Os documentos do projeto estão na pasta `docs/`:

- `project_charter.md`: apresenta o problema de negócio, os objetivos, o escopo e o público interessado.
- `data_summary_report.md`: descreve as fontes de dados utilizadas e as limitações desta etapa.

Outras fontes, como CNES, SIA/SUS, SIH/SUS, IBGE e Painel-Oncologia, poderão ser avaliadas nas próximas etapas. Elas ainda não foram integradas à aplicação.

**Repositório no GitHub:** [https://github.com/Nobre-DS/KYNOVA-X](https://github.com/Nobre-DS/KYNOVA-X)

## Ferramentas utilizadas

Foram utilizados Python, Streamlit, Pandas, Requests, Beautiful Soup, Git e GitHub. O ChatGPT (OpenAI) foi utilizado como ferramenta de apoio e revisão da documentação do TP2. As funcionalidades foram verificadas por meio de testes na aplicação local.

## Evolução do projeto no TP3

No TP3, a aplicação KYNOVA-X foi ampliada com novas funcionalidades de navegação e consulta de dados, mantendo as informações e os recursos desenvolvidos nas etapas anteriores.

### Aplicação com múltiplas páginas

A interface foi organizada em páginas, com menu lateral de navegação:

- **Consulta INCA:** apresenta uma amostra das estimativas de câncer do INCA para 2026, com filtro por sexo.
- **Informações INCA:** apresenta o conteúdo textual extraído de uma página oficial do INCA com Beautiful Soup.
- **Upload e Download:** permite enviar arquivos CSV e baixar os dados combinados.
- **Consulta API:** permite consultar informações disponibilizadas pela API desenvolvida com FastAPI.

A aplicação continua sendo executada pelo arquivo `app.py`.

### Integração com FastAPI

Foi criado o arquivo `api.py`, responsável pela disponibilização de duas rotas:

- **GET `/estimativas`:** consulta os registros disponíveis.
- **POST `/estimativas`:** recebe novos registros com os campos `sexo`, `localizacao`, `casos` e `ano`.

Os registros adicionados pela API são armazenados separadamente em `data/processed/registros_api.csv`, preservando o arquivo original das estimativas do INCA.

As duas rotas foram testadas por meio da documentação interativa do FastAPI, disponível em `http://127.0.0.1:8000/docs`.

A consulta GET também foi testada na interface Streamlit, por meio da página Consulta API.

### Como executar o projeto no TP3

O ambiente utilizado nesta etapa foi identificado como `.venv_tp3`.

Para preparar o ambiente, abra o Terminal na pasta principal `projeto_cancer` e execute:

```bash
python3-m venv .venv_tp3
source.venv_tp3/bin/activate
python-m pip install -r requirements.txt
```

Para iniciar a API, execute:

```bash
python -m uvicorn api:app --reload --port 8000
```

A documentação interativa da API poderá ser acessada em:

`http://127.0.0.1:8000/docs`

Em outro Terminal, com o mesmo ambiente virtual ativado, execute:

```bash
python-m streamlit run app.py
```

A aplicação Streamlit poderá ser acessada pelo endereço local informado no Terminal, normalmente `http://localhost:8501`.

A página Consulta API depende de o servidor FastAPI estar em execução.

### Coleta de dados

Nesta etapa, foram mantidos os dados coletados anteriormente com Requests e Beautiful Soup. Não foi necessário utilizar Selenium, pois a extração realizada não dependeu de interações com elementos dinâmicos.

### Preparação para uso futuro com LLMs

Os dados estruturados e o conteúdo textual disponíveis na KYNOVA-X poderão ser utilizados, nas próximas etapas, para desenvolver funcionalidades de perguntas e respostas e geração de resumos.

Esses recursos de inteligência artificial ainda não foram implementados no TP3.

### Limitações

A aplicação utiliza uma amostra demonstrativa de 10 registros das estimativas do INCA. Os registros adicionais utilizados para testar a API não representam estimativas epidemiológicas oficiais.

No TP3, a aplicação e a API foram desenvolvidas e testadas localmente, sem publicação em endereço público.

### Documentação

Os documentos `project_charter.md` e `data_summary_report.md`, disponíveis na pasta `docs/`, foram atualizados para registrar as funcionalidades e as decisões tomadas no TP3.

### Ferramentas utilizadas no TP3

Foram utilizados Python, Streamlit, Pandas, Requests, Beautiful Soup, FastAPI, Uvicorn, Git e GitHub. O ChatGPT (OpenAI) foi utilizado como ferramenta de apoio no desenvolvimento e na revisão da documentação do TP3. As funcionalidades foram verificadas por meio de testes realizados na aplicação local.