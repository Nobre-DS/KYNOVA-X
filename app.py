import streamlit as st
import pandas as pd
from pathlib import Path

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
    df = pd.read_csv(arquivo)
    st.dataframe(df, use_container_width=True)
else:
    st.warning(
        "Arquivo CSV não encontrado na pasta data/raw."
    )