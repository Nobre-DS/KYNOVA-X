from src.sintese_editorial_tp5 import SINTese_APROVADA, referencia_editorial
from src.validacao_resumo_tp5 import cobertura_fatos


def test_texto_escolhido_e_conservado_sem_edicao():
    dado = referencia_editorial(SINTese_APROVADA)
    assert dado['disponivel']
    assert dado['texto'] == SINTese_APROVADA
    assert dado['palavras'] == 86


def test_sete_marcadores_na_referencia_sem_alterar_llm():
    d = referencia_editorial(SINTese_APROVADA)
    assert d['cobertura']['preservados'] == d['cobertura']['total'] == 7
    texto_modelo_incompleto = 'O INCA publica estimativas desde 1995.'
    dado = cobertura_fatos(SINTese_APROVADA, texto_modelo_incompleto)
    assert dado['preservados'] < d['cobertura']['preservados']


def test_texto_diferente_nao_recebe_resumo_fixo():
    d = referencia_editorial('O relatório de transporte indica fluxo urbano de veículos.')
    assert not d['disponivel']
    assert d['texto'] == ''


def test_espacos_nao_alteram_identidade_do_editorial():
    versao = SINTese_APROVADA.replace(' Ministério', '\nMinistério')
    assert referencia_editorial(versao)['disponivel']
