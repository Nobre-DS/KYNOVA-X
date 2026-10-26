import streamlit as st
import pandas as pd
from pathlib import Path

st.title("Consulta de Estimativas do INCA")

st.write(
    "Nesta página, é possível consultar uma amostra das "
    "estimativas de câncer do INCA para 2026."
)

arquivo = Path("data/raw/estimativas_inca_2026_amostra.csv")

if arquivo.exists():
    df = pd.read_csv(arquivo)

    sexo = st.selectbox(
        "Selecione o sexo:",
        ["Todos", "Homens", "Mulheres"]
    )

    if sexo == "Todos":
        df_filtrado = df
    else:
        df_filtrado = df[df["sexo"] == sexo]

    st.dataframe(df_filtrado, use_container_width=True)

else:
    st.warning("Arquivo CSV não encontrado.")