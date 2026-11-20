"""TP5: dashboard com dados oficiais amostrais e sumarização local via FastAPI.

Execução: em terminais distintos, `python -m uvicorn api:app --reload`
e `python -m streamlit run app.py`. Não altera as páginas 1 a 4.
"""
from pathlib import Path
import pandas as pd
import requests
import streamlit as st

from src.analise_tp5 import (
    FONTE_INCA, avaliar_saida, carregar_estimativas, carregar_textos,
    palavras, textos_elegiveis,
)

RAIZ = Path(__file__).resolve().parents[1]
DADOS = RAIZ / 'data' / 'raw' / 'estimativas_inca_2026_amostra.csv'
TEXTOS = RAIZ / 'data' / 'raw' / 'conteudo_inca_web.csv'
API_URL = 'http://127.0.0.1:8000/processar_texto'

st.title('KYNOVA-X | Dashboard final de dados e IA')
st.caption('TP5 • Opção 2: sumarização de conteúdo web do INCA com FLAN-T5-small local')
st.info(
    'Os números apresentados provêm de uma amostra acadêmica de 10 linhas, '
    'não da base epidemiológica completa do Brasil. A IA não estima casos nem recomenda tratamentos.'
)

try:
    df = carregar_estimativas(DADOS)
    coletados = carregar_textos(TEXTOS)
except (FileNotFoundError, pd.errors.ParserError, ValueError) as erro:
    st.error(f'Não foi possível carregar os arquivos esperados: {erro}')
    st.stop()

c1, c2, c3 = st.columns(3)
c1.metric('Registros na amostra', len(df))
c2.metric('Registros textuais coletados', len(coletados))
c3.metric('Ano de referência', ', '.join(map(str, sorted(df['ano'].unique()))))

aba_dados, aba_ia, aba_ciclo = st.tabs(
    ['1. Dados e gráficos', '2. Resumo com IA local', '3. Ciclo TDSP e ODS']
)

with aba_dados:
    st.subheader('Estimativas selecionadas do INCA')
    sexo = st.selectbox('Recorte da amostra por sexo', ['Todos', 'Homens', 'Mulheres'])
    filtrados = df if sexo == 'Todos' else df[df['sexo'] == sexo]
    st.dataframe(filtrados, use_container_width=True, hide_index=True)
    st.caption(
        'Gráfico dos registros selecionados; não representa ranking nacional nem soma de casos '
        'independentes. Os recortes e categorias são os da amostra.'
    )
    legenda = filtrados.copy()
    legenda['categoria'] = legenda['sexo'] + ' | ' + legenda['localizacao']
    st.bar_chart(legenda.set_index('categoria')[['casos']])
    st.subheader('Textos obtidos via web scraping')
    st.dataframe(coletados, use_container_width=True, hide_index=True)
    st.caption(f'Origem declarada: {FONTE_INCA}')

with aba_ia:
    st.subheader('Sumarização com o modelo instalado no Mac')
    st.write(
        'O texto parte do CSV `conteudo_inca_web.csv`, coletado com Requests e Beautiful Soup. '
        'A aplicação envia o trecho selecionado para a rota local `POST /processar_texto`.'
    )
    validos = textos_elegiveis(coletados)
    if validos.empty:
        st.warning('Não há texto coletado com pelo menos 30 caracteres.')
    else:
        opcoes = [f'Registro {i+1} | <{row.tipo}> | {palavras(row.texto)} palavras'
                  for i, row in validos.iterrows()]
        selecao = st.selectbox('Escolha um trecho coletado do INCA', range(len(opcoes)),
                              format_func=lambda i: opcoes[i])
        trecho = validos.iloc[selecao]['texto']
        with st.form('gerar_resumo_tp5'):
            texto = st.text_area('Texto de entrada (editável para avaliação)', value=trecho,
                                 height=210, max_chars=1500, key=f'fonte_{selecao}')
            enviar = st.form_submit_button('Gerar resumo local')
        if enviar:
            if not 30 <= len(texto.strip()) <= 1500:
                st.warning('Informe de 30 a 1.500 caracteres, conforme a validação do TP4.')
            else:
                try:
                    with st.spinner('Processando com FastAPI e FLAN-T5-small local...'):
                        resposta = requests.post(API_URL, json={'texto': texto.strip()}, timeout=75)
                    resposta.raise_for_status()
                    saida = resposta.json()
                    st.session_state['resultado_tp5'] = saida
                except requests.exceptions.Timeout:
                    st.error('O servidor excedeu o tempo de espera. Confira o FastAPI no terminal.')
                except requests.exceptions.ConnectionError:
                    st.error('FastAPI indisponível. Execute `python -m uvicorn api:app --reload` em outro terminal.')
                except requests.exceptions.HTTPError as erro:
                    codigo = erro.response.status_code if erro.response is not None else '?'
                    st.error(f'A API retornou HTTP {codigo}: {erro}')
                except (ValueError, KeyError) as erro:
                    st.error(f'A resposta recebida não pôde ser interpretada: {erro}')
        saida = st.session_state.get('resultado_tp5')
        if saida and saida.get('texto_original') == texto.strip():
            st.subheader('Resultado retornado pelo LLM')
            st.write(saida.get('resultado', ''))
            st.caption(f"Modelo: {saida.get('modelo', '?')} | Execução: {saida.get('execucao', '?')} "
                       f"| Tempo de inferência: {saida.get('tempo_segundos', '?')} s")
            alertas, num_saida = avaliar_saida(texto, saida.get('resultado', ''))
            if any('não' in a.lower() or 'reproduzir' in a.lower() or 'semelhante' in a.lower()
                   for a in alertas):
                for alerta in alertas:
                    st.warning(alerta)
            else:
                for alerta in alertas:
                    st.info(alerta)
            comparacao = pd.DataFrame({'etapa': ['Texto de origem', 'Saída do LLM'],
                                      'palavras': [palavras(texto), num_saida]})
            st.subheader('Comparação de extensão textual (não mede qualidade)')
            st.bar_chart(comparacao.set_index('etapa')[['palavras']])
            st.dataframe(comparacao, hide_index=True, use_container_width=True)
            st.caption('A correção de informações epidemiológicas deve ser feita na fonte original. '
                       'Redução de palavras não comprova fidelidade nem utilidade do resumo.')

with aba_ciclo:
    st.subheader('Ciclo de ciência de dados demonstrado')
    st.markdown('''
    **1. Coleta:** extração textual de página oficial do INCA com Requests e Beautiful Soup (TP2).  
    **2. Preparação:** armazenamento em CSV, verificação de colunas, normalização e seleção do trecho.  
    **3. Análise:** filtros, tabela e gráfico dos dez registros selecionados.  
    **4. Modelo e prompt:** FLAN-T5-small executado localmente via Transformers e FastAPI.  
    **5. Comunicação:** resumo retornado no dashboard, métricas textuais e avisos de qualidade.
    ''')
    st.subheader('Conexão com sustentabilidade e governança')
    st.write(
        'ODS 3: apoio informacional ao planejamento da atenção oncológica; '
        'ODS 16: rastreabilidade das fontes e distinção entre dados oficiais e demonstrativos. '
        'Trata-se de alinhamento conceitual, não de impacto ou indicador ESG medido.'
    )
    st.caption('Bases como CNES, SIH/SUS, SIA/SUS, IBGE e Painel-Oncologia permanecem no escopo futuro.')
    st.link_button('Consultar a fonte oficial do INCA', FONTE_INCA)
