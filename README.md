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