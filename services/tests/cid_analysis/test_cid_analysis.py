from services.tests.general import request_base, url_base

url = f"{url_base}/analysis-info/analysis"


def test_returns_correct_information():
    data = {
        "text_analysis": """Informações do paciente\nJoana Ribeiro, 42 anos, comparece ao pronto-atendimento com queixa de febre alta e dores no corpo há dois dias.\n\nHistórico da moléstia atual\nPaciente relata início súbito de febre alta, calafrios, cefaleia intensa, dores musculares generalizadas, coriza e tosse seca há cerca de dois dias. Refere também prostração importante e dor de garganta, sem presença de vômitos ou diarreia. Informa que o quadro começou após contato próximo com o neto, que apresentou sintomas semelhantes na semana anterior. Nega dispneia, dor torácica ou outros sintomas respiratórios mais graves até o momento.\n\nHistória patológica pregressa\nA paciente é portadora de hipertensão arterial sistêmica, em uso regular de losartana, com controle adequado. Nega outras doenças crônicas, internações prévias ou cirurgias. Refere não possuir alergias conhecidas a medicamentos ou alimentos e nunca fez uso de imunossupressores.\n\nHistórico familiar\nRelata que a mãe é hipertensa e diabética, ambas condições controladas com medicação. O pai faleceu aos 70 anos devido a um acidente vascular cerebral isquêmico. Nega histórico familiar de doenças genéticas, autoimunes ou respiratórias crônicas. Não há casos conhecidos de neoplasias de aparecimento precoce na família.\n\nHistórico social\nTrabalha como professora da educação infantil em escola pública, tendo contato frequente com crianças. Nega tabagismo e faz uso ocasional de bebidas alcoólicas em eventos sociais. Refere sono regular de aproximadamente sete horas por noite, mas não pratica atividade física com regularidade. Alimenta-se de forma variada, embora reconheça consumo esporádico de alimentos ultraprocessados durante a semana.\n\nExame físico\nApresenta-se em bom estado geral, embora com fácies febril e discreta prostração. Está febril (38,7 °C), com frequência cardíaca de 104 bpm, pressão arterial de 130/80 mmHg e saturação periférica de oxigênio de 97% em ar ambiente. Mucosas orais e nasais estão hiperemiadas, com orofaringe levemente avermelhada, sem exsudato. Ausculta pulmonar revela murmúrio vesicular presente e simétrico, sem ruídos adventícios. Abdome flácido, indolor à palpação, sem visceromegalias. Demais sistemas sem alterações significativas.\n\nExames complementares\nHemograma: leucocitose leve com predomínio de neutrófilos\nPCR: 12 mg/L\nTeste rápido para Influenza A: positivo\nRaio-X de tórax: campos pulmonares limpos, sem infiltrado evidente"""
    }

    response = request_base(url, data)
    data = response.json()["data"]
    print(data)
    assert response.status_code == 200
    assert "J10.1" in data["cid"]
    assert "tosse" in data["result"]
    assert "dor de garganta" in data["result"]
    assert "vírus" in data["result"]
    assert "identificado" in data["result"]

def test_error_invalid_input():
    data = {
        "text_analysis": 500
        }

    response = request_base(url, data)
    result_data = response.json()["detail"][0]

    assert response.status_code == 422
    assert "Input should be a valid string" in result_data["msg"]
