from services.tests.general import request_base, url_base

url = f"{url_base}/anamnesis-info/anamnesis-strunction-data"


def test_returns_correct_cid():
    data = {
        "PatientEntity": {
            "birth_date": "1999-09-01T00:00:00-03:00",
            "genre": "M",
            "address": "Avenida Octávio Mangabeira",
            "number": "123",
            "complement": "Casa",
            "neighborhood": "Boca do Rio",
            "neighborhood_type": 0,
            "state_address": "BA",
            "zip_code": "41706690",
            "city": "Salvador",
            "nationalities": "Indígena",
        },
        "HistoricoAtendimentoEntity": [],
        "AnamnesisEntity": {
            "careUnitDescription": "2",
            "professionalName": "Thiago",
            "modifiedDateTime": "2025-11-18T18:24:12.548966Z",
            "lastAnamnesis": {
                "vitalSigns": {
                    "cardioFrequency": 72,
                    "bodyTemperature": 36.5,
                    "weight": 77,
                    "height": 171,
                    "pas": 120,
                    "pad": 80,
                }
            },
            "historicoClinicoPep2": "true",
            "hasRecordRestriction": "true",
            "ia_anamnesis_entity": "Síntese Clínica:\nQueixa Principal (QP): Dor de cabeça e enjoo após treino intenso.\nHistória da Doença Atual (HDA): Início dos sintomas ontem, surgiram de repente após treino pesado. Dor localizada na parte de cima da cabeça, sem irradiação. Dor contínua desde o início, com piora progressiva. Esforço físico piora a dor, repouso alivia.\nNão fez uso de medicações até o momento. \nAntecedentes Pessoais: Não informado. \nAntecedentes Familiares: Não informado. \nHábitos de Vida: Treinamento físico intenso. Outros hábitos não informados. \nHistória Psicossocial: Não informado. \nRevisão de Sistemas: Sem outros sintomas relatados além da dor de cabeça e enjoo. \nConclusão/Hipótese inicial: Cefaleia induzida por esforço físico e possivelmente desidratação ou fadiga muscular associada.",
        },
        "Interview": "string",
        "files": [],
    }

    response = request_base(url, data)

    data = response.json()["data"]

    assert response.status_code == 200
    assert "G44" in data["cid"]
