"""Medicao simples no computador da estudante (tempo e RAM aproximada)."""
import os
import platform
import statistics
import time
import psutil
from llm_local import processador

amostras = [
    'O Instituto Nacional de Cancer divulga estimativas de incidencia para apoiar o planejamento em saude. As estimativas nao representam contagens individuais de pacientes e devem ser interpretadas com cuidado.',
    'A organizacao de informacoes epidemiologicas pode apoiar a consulta de indicadores. A aplicacao KYNOVA-X apresenta uma amostra reduzida de registros e nao substitui as bases oficiais completas.',
    'O planejamento da atencao oncologica depende de dados de qualidade, interpretacao adequada das fontes e analise dos limites dos indicadores. O texto sintetizado nao constitui recomendacao clinica.'
]
print('Sistema:', platform.platform(), '| CPU:', platform.processor(), '| RAM total GB:', round(psutil.virtual_memory().total/1024**3,2))
processo = psutil.Process(os.getpid())
inicio = time.perf_counter()
processador.carregar()
print('Carga inicial (s):', round(time.perf_counter()-inicio,3))
print('RAM do processo apos carga (MB):', round(processo.memory_info().rss/1024**2,1))
tempos=[]
for i, texto in enumerate(amostras,1):
    resultado, segundos = processador.resumir(texto)
    tempos.append(segundos)
    print(f'Teste {i}: {segundos}s | Resposta:', resultado)
print('Tempo medio de inferencia (s):', round(statistics.mean(tempos),3))
print('RAM do processo ao final (MB):', round(processo.memory_info().rss/1024**2,1))
print('A qualidade factual dos resumos deve ser avaliada manualmente; tempo nao indica precisao.')
