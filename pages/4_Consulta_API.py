
import streamlit as st
import pandas as pd
import requests

st.title("Consulta de Dados pela API")

st.write(
    "Nesta página, é possível consultar os registros "
    "disponibilizados pela API da KYNOVA-X, desenvolvida com FastAPI."
)

URL_API = "http://127.0.0.1:8000/estimativas"

if st.button("Consultar dados da API"):
    try:
        resposta = requests.get(URL_API, timeout=10)
        resposta.raise_for_status()

        dados = resposta.json()
        df = pd.DataFrame(dados)

        st.success("Consulta realizada com sucesso.")
        st.dataframe(df, width="stretch")

    except requests.exceptions.RequestException:
        st.error(
            "Não foi possível acessar a API. "
            "Verifique se o servidor FastAPI está em execução."
        )
