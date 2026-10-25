import streamlit as st
import pandas as pd
from pathlib import Path

@st.cache_data
def carregar_csv(caminho):
    return pd.read_csv(caminho)

st.set_page_config(
    page_title="KYNOVA-X",
    layout="wide"
)

st.title("KYNOVA-X")

st.subheader(
    "Plataforma de Inteligência de Dados para o Planejamento da Atenção Oncológica"
)

st.header("Problema de Negócio")

st.write(
    "As informações epidemiológicas e assistenciais estão "
    "distribuídas em diferentes bases oficiais, dificultando "
    "a consulta integrada para o planejamento e a gestão em saúde."
)

st.header("Objetivos do Projeto")

st.write(
    "A KYNOVA-X tem como objetivo reunir, organizar e apresentar "
    "informações de diferentes fontes oficiais para apoiar "
    "o planejamento e a gestão da atenção oncológica no Brasil."
)

st.write(
    "Nesta demonstração inicial, serão utilizadas amostras "
    "das Estimativas de Câncer 2026–2028 do INCA."
)

st.header("Links Úteis")

st.link_button(
    "Instituto Nacional de Câncer — INCA",
    "https://www.gov.br/inca/pt-br"
)

st.link_button(
    "ODS 3 - Saúde e Bem-Estar",
    "https://brasil.un.org/pt-br/sdgs/3"
)

st.header("Amostra de Dados — INCA")

arquivo = Path("data/raw/estimativas_inca_2026_amostra.csv")

if arquivo.exists():
    df = carregar_csv(arquivo)

    st.subheader("Consultar estimativas por sexo")

    if "sexo_selecionado" not in st.session_state:
        st.session_state.sexo_selecionado = "Todos"

    sexo_selecionado = st.selectbox(
        "Selecione o sexo:",
        ["Todos", "Homens", "Mulheres"],
        key="sexo_selecionado"
    )

    if sexo_selecionado == "Todos":
        df_filtrado = df
    else:
        df_filtrado = df[df["sexo"] == sexo_selecionado]

    st.dataframe(df_filtrado, width="stretch")

else:
    st.warning(
        "Arquivo CSV não encontrado na pasta data/raw."
    )

# Conteúdo extraído da página oficial do INCA
st.header("Informações da página do INCA")

arquivo_web = Path("data/raw/conteudo_inca_web.csv")

if arquivo_web.exists():
    df_web = carregar_csv(arquivo_web)

    st.dataframe(df_web, width="stretch")
else:
    st.warning("Arquivo com conteúdo da página do INCA não encontrado.")


# Upload e download de arquivos CSV
st.header("Upload e Download de Dados")

arquivo_enviado = st.file_uploader(
    "Envie um arquivo CSV para complementar os dados:",
    type=["csv"]
)

if arquivo_enviado is not None:
    dados_adicionais = pd.read_csv(arquivo_enviado)

    colunas_esperadas = ["sexo", "localizacao", "casos", "ano"]

    if all(coluna in dados_adicionais.columns for coluna in colunas_esperadas):
        dados_adicionais = dados_adicionais[colunas_esperadas]

        if arquivo.exists():
            dados_completos = pd.concat(
                [df, dados_adicionais],
                ignore_index=True
            )

            st.dataframe(dados_completos, width="stretch")

            st.download_button(
                "Baixar dados completos em CSV",
                data=dados_completos.to_csv(index=False).encode("utf-8-sig"),
                file_name="dados_completos_kynova.csv",
                mime="text/csv"
            )
    else:
        st.warning(
            "O CSV deve conter as colunas: sexo, localizacao, casos e ano."
        )