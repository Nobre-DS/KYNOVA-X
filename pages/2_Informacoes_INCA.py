import streamlit as st
import pandas as pd
from pathlib import Path

st.title("Informações da página do INCA")

st.write(
    "Nesta página, são apresentadas informações "
    "extraídas do site oficial do INCA utilizando Beautiful Soup."
)

arquivo = Path("data/raw/conteudo_inca_web.csv")

if arquivo.exists():
    df_web = pd.read_csv(arquivo)
    st.dataframe(df_web, width="stretch")
else:
    st.warning("Arquivo com conteúdo do INCA não encontrado.")