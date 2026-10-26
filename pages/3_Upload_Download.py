import streamlit as st
import pandas as pd
from pathlib import Path

st.title("Upload e Download de Dados")

st.write(
    "Nesta página, é possível enviar um arquivo CSV "
    "para complementar os registros apresentados na KYNOVA-X."
)

arquivo = Path("data/raw/estimativas_inca_2026_amostra.csv")

if arquivo.exists():
    df = pd.read_csv(arquivo)

    arquivo_enviado = st.file_uploader(
        "Envie um arquivo CSV:",
        type=["csv"]
    )

    if arquivo_enviado is not None:
        dados_adicionais = pd.read_csv(arquivo_enviado)

        colunas_esperadas = ["sexo", "localizacao", "casos", "ano"]

        if all(coluna in dados_adicionais.columns for coluna in colunas_esperadas):
            dados_adicionais = dados_adicionais[colunas_esperadas]

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
else:
    st.warning("Arquivo CSV original não encontrado.")