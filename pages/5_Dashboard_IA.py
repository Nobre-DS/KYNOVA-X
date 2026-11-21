"""TP5: dashboard com dados oficiais amostrais e sumarização local via FastAPI.

Execução: em terminais distintos, `python -m uvicorn api:app --reload`
e `python -m streamlit run app.py`. Não altera as páginas 1 a 4.
"""
from pathlib import Path
import pandas as pd
import requests
import streamlit as st

from src.validacao_resumo_tp5 import cobertura_fatos, resumo_referencia_da_fonte
from src.sintese_assistida_tp5 import sintetizar_com_rastreabilidade
from src.sintese_editorial_tp5 import referencia_editorial

from src.analise_tp5 import (
    FONTE_INCA, avaliar_saida, auditoria_resumo, carregar_estimativas, carregar_textos,
    fatos_comprovaveis_da_fonte, gerar_insights_amostra, indicadores_qualidade_amostra,
    palavras, textos_elegiveis,
)

RAIZ = Path(__file__).resolve().parents[1]
DADOS = RAIZ / 'data' / 'raw' / 'estimativas_inca_2026_amostra.csv'
TEXTOS = RAIZ / 'data' / 'raw' / 'conteudo_inca_web.csv'
API_URL = 'http://127.0.0.1:8000/processar_texto'

st.title('KYNOVA-X | Dashboard final de dados e IA')
st.caption('TP5 • Opção 2: sumarização de conteúdo web do INCA com PTT5-Summ local, ajustado para português')
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
    qualidade = indicadores_qualidade_amostra(DADOS)
    q1, q2, q3 = st.columns(3)
    q1.metric('Registros de origem (amostra)', qualidade['registros_origem'])
    q2.metric('Aptos para o gráfico', qualidade['registros_aptos'])
    q3.metric('Excluídos na validação', qualidade['registros_excluidos'])
    st.caption('Indicadores de controle do processamento local (G, governança da informação), '
               'não pontuação ESG ou certificação da base oficial.')

    st.subheader('Insights descritivos, calculados dos dados (não pelo LLM)')
    st.caption('Escopo: comparação apenas entre as categorias presentes na amostra de cada sexo. '
               'Não representa ranking nacional completo, taxa de incidência ou demanda por serviços.')
    for insight in gerar_insights_amostra(filtrados):
        st.markdown('**' + insight['titulo'] + '**')
        st.write(insight['descricao'])
        st.caption('Aplicação ESG/ODS: ' + insight['relevancia'])
        st.caption('Limite: ' + insight['limite'])
    st.info('Insight de governança (ODS 16): cada resultado conserva a fonte, o recorte, '
            'o ano e suas limitações. Antes de dimensionar serviços, seriam necessários '
            'dados de população, capacidade e acesso que não integram esta demonstração.')
    st.caption('Fonte numérica: https://www.gov.br/inca/pt-br/assuntos/cancer/numeros/estimativa/estado-capital/brasil')

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
            if texto.strip() != trecho.strip():
                st.caption('Aviso de proveniência: este texto foi editado. '
                           'Para comprovar uso do web scraping, teste também o trecho original do CSV.')
            editorial_preview = referencia_editorial(texto)
            if editorial_preview['disponivel']:
                st.caption('Texto editorial selecionado: 86 palavras por separação em espaços. '
                           'O contador lexical do dashboard mostra 88 unidades por dividir '
                           '“2026–2028” e “sub-registros” em dois termos cada. '
                           'O conteúdo do texto permanece idêntico.')
            enviar = st.form_submit_button('Gerar resumo local')
        if enviar:
            if not 30 <= len(texto.strip()) <= 1500:
                st.warning('Informe de 30 a 1.500 caracteres, conforme a validação do TP4.')
            else:
                try:
                    with st.spinner('Processando com FastAPI e PTT5-Summ local, ajustado para português...'):
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
            st.subheader('Resultado retornado pelo LLM — saída original, sem edição')
            st.write(saida.get('resultado', ''))
            st.caption(f"Modelo: {saida.get('modelo', '?')} | Execução: {saida.get('execucao', '?')} "
                       f"| Tempo de inferência: {saida.get('tempo_segundos', '?')} s")
            # O texto de referência NÃO substitui a geração, nem é apresentado como IA.
            st.subheader('Controle de qualidade da saída do modelo')
            resumo_llm = saida.get('resultado', '')
            cobertura = cobertura_fatos(texto, resumo_llm)
            fatores = []
            if not resumo_llm.rstrip().endswith(('.', '!', '?')):
                fatores.append('A saída do modelo termina sem pontuação final e pode estar truncada.')
            if palavras(texto) >= 55 and palavras(resumo_llm) < max(25, round(palavras(texto) * 0.28)):
                fatores.append('A síntese é excessivamente curta para a extensão do texto de origem.')
            if cobertura['total'] >= 3 and cobertura['proporcao'] < 0.5:
                fatores.append('Menos da metade dos marcadores factuais identificados foi preservada.')
            if fatores:
                st.error('A saída do LLM não passou nos controles mínimos de completude; '
                         'não deve ser usada como síntese validada.')
                for fator in fatores:
                    st.write('• ' + fator)
            else:
                st.warning('Sem falha formal evidente. A fidelidade factual e a qualidade '
                           'do português ainda exigem revisão humana.')
            if cobertura['total']:
                st.metric('Marcadores factuais preservados na resposta do LLM',
                          f"{cobertura['preservados']} de {cobertura['total']}")
                st.dataframe(pd.DataFrame([
                    {'Fato identificável no texto-fonte': item['fato'],
                     'Mencionado pela IA': 'Sim' if item['preservado'] else 'Não'}
                    for item in cobertura['itens']
                ]), use_container_width=True, hide_index=True)
            st.caption('Marcadores são conferência lexical, não validação semântica.')

            # Resultado de consulta supervisionada: NUNCA troca a saida do LLM.
            # Se o usuario colou exatamente o texto editorial previamente selecionado,
            # conserva-se esse texto sem modificar nenhuma palavra.
            editorial = referencia_editorial(texto)
            if editorial['disponivel']:
                st.subheader('Síntese editorial escolhida — NÃO gerada pelo LLM')
                st.write(editorial['texto'])
                st.caption(editorial['proveniencia'])
                st.metric('Palavras do texto editorial', editorial['palavras'])
                st.metric('Marcadores na referência editorial (conferência lexical)',
                          f"{editorial['cobertura']['preservados']} de {editorial['cobertura']['total']}")
                st.info('A referência editorial conserva o texto escolhido, mas NÃO altera '
                        'a cobertura factual nem o controle de qualidade da saída real do PTT5-Summ. '
                        'O texto fornecido aqui foi editado e não constitui nova coleta via web scraping.')
            else:
                assistida = sintetizar_com_rastreabilidade(texto, resumo_llm)
                if assistida['disponivel']:
                    st.subheader('Síntese factual por regras — NÃO gerada pelo LLM')
                    st.write(assistida['texto'])
                    st.caption(assistida['proveniencia'])
                    st.metric('Marcadores preservados na síntese factual por regras',
                              f"{assistida['cobertura']['preservados']} de {assistida['cobertura']['total']}")
                    st.info('Este resultado é uma reconstrução por regras, não uma saída do modelo. '
                            'Não corrige retroativamente a qualidade do LLM.')
                else:
                    st.caption('Síntese factual por regras indisponível para este recorte.')
                referencia = resumo_referencia_da_fonte(texto)
                st.subheader('Referência da fonte — NÃO gerada pelo LLM')
                st.write(referencia['texto'])
                st.caption(referencia['proveniencia'] + '. ' + referencia['metodo'] + '.')
                if not referencia['completo_para_fonte_inca']:
                    st.info('A referência é um extrato literal, não um resumo abstrativo validado.')

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

            st.subheader('Auditoria do texto produzido pela IA')
            verificacao = auditoria_resumo(texto, saida.get('resultado', ''))
            if verificacao['estado'] == 'REVISÃO PRIORITÁRIA':
                st.error('Resultado: REVISÃO PRIORITÁRIA — a saída possui sinais objetivos de problema.')
            else:
                st.warning('Resultado: REVISÃO HUMANA OBRIGATÓRIA — a ausência de alertas não comprova precisão.')
            for aviso in verificacao['alertas']:
                st.write('• ' + aviso)
            st.caption('Auditoria automática limitada: eco de instruções, semelhança, extensão e '
                       'números que não aparecem na origem. Não mede fidelidade semântica.')
            st.markdown('**Fatos explicitamente localizados no texto de origem (não produzidos pelo LLM):**')
            fatos = fatos_comprovaveis_da_fonte(texto)
            if fatos:
                for fato in fatos:
                    st.write('• ' + fato['fato'])
            else:
                st.caption('Nenhuma das expressões metodológicas pré-definidas foi encontrada no texto escolhido.')
            st.caption('Uso recomendado: confrontar a frase gerada com a fonte antes de incluí-la '
                       'em relatório ou decisão; a aplicação não fornece aconselhamento clínico.')

with aba_ciclo:
    st.subheader('Ciclo de ciência de dados demonstrado')
    st.markdown('''
    **1. Coleta:** extração textual de página oficial do INCA com Requests e Beautiful Soup (TP2).  
    **2. Preparação:** armazenamento em CSV, verificação de colunas, normalização e seleção do trecho.  
    **3. Análise:** filtros, tabela e gráfico dos dez registros selecionados.  
    **4. Modelo e IA:** PTT5-Summ ajustado para sumarização em português, com parâmetros controlados de geração, executado localmente via Transformers e FastAPI; engenharia de prompts foi explorada nas versões anteriores.  
    **5. Comunicação:** resumo retornado no dashboard, métricas textuais e avisos de qualidade.
    ''')
    st.subheader('Evidências e indicadores replicáveis')
    st.write('Os dois insights quantitativos são ordenações e comparações dentro de recortes '
             'dos dez registros amostrais do INCA, calculadas com Pandas; o LLM não faz contas. '
             'As observações de metodologia são extraídas literalmente do CSV de texto. '
             'A auditoria de saída apenas aponta sinais; os fatos requerem checagem humana.')
    st.subheader('Conexão com sustentabilidade e governança')
    st.write(
        'ODS 3: apoio informacional ao planejamento da atenção oncológica; '
        'ODS 16: rastreabilidade das fontes e distinção entre dados oficiais e demonstrativos. '
        'Trata-se de alinhamento conceitual, não de impacto ou indicador ESG medido.'
    )
    st.caption('Bases como CNES, SIH/SUS, SIA/SUS, IBGE e Painel-Oncologia permanecem no escopo futuro.')
    st.link_button('Consultar a fonte oficial do INCA', FONTE_INCA)
