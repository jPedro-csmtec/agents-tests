from typing import Any
from services.tests.general import request_base

url = "analysis-info/analysis"

input: dict[str, Any] = {"text_analysis": ""}


def test_correct_results_influenza():
    input["text_analysis"] = (
        "Informações do paciente\nJoana Ribeiro, 42 anos, comparece ao pronto-atendimento com queixa de febre alta e dores no corpo há dois dias.\n\nHistórico da moléstia atual\nPaciente relata início súbito de febre alta, calafrios, cefaleia intensa, dores musculares generalizadas, coriza e tosse seca há cerca de dois dias. Refere também prostração importante e dor de garganta, sem presença de vômitos ou diarreia. Informa que o quadro começou após contato próximo com o neto, que apresentou sintomas semelhantes na semana anterior. Nega dispneia, dor torácica ou outros sintomas respiratórios mais graves até o momento.\n\nHistória patológica pregressa\nA paciente é portadora de hipertensão arterial sistêmica, em uso regular de losartana, com controle adequado. Nega outras doenças crônicas, internações prévias ou cirurgias. Refere não possuir alergias conhecidas a medicamentos ou alimentos e nunca fez uso de imunossupressores.\n\nHistórico familiar\nRelata que a mãe é hipertensa e diabética, ambas condições controladas com medicação. O pai faleceu aos 70 anos devido a um acidente vascular cerebral isquêmico. Nega histórico familiar de doenças genéticas, autoimunes ou respiratórias crônicas. Não há casos conhecidos de neoplasias de aparecimento precoce na família.\n\nHistórico social\nTrabalha como professora da educação infantil em escola pública, tendo contato frequente com crianças. Nega tabagismo e faz uso ocasional de bebidas alcoólicas em eventos sociais. Refere sono regular de aproximadamente sete horas por noite, mas não pratica atividade física com regularidade. Alimenta-se de forma variada, embora reconheça consumo esporádico de alimentos ultraprocessados durante a semana.\n\nExame físico\nApresenta-se em bom estado geral, embora com fácies febril e discreta prostração. Está febril (38,7 °C), com frequência cardíaca de 104 bpm, pressão arterial de 130/80 mmHg e saturação periférica de oxigênio de 97% em ar ambiente. Mucosas orais e nasais estão hiperemiadas, com orofaringe levemente avermelhada, sem exsudato. Ausculta pulmonar revela murmúrio vesicular presente e simétrico, sem ruídos adventícios. Abdome flácido, indolor à palpação, sem visceromegalias. Demais sistemas sem alterações significativas.\n\nExames complementares\nHemograma: leucocitose leve com predomínio de neutrófilos\nPCR: 12 mg/L\nTeste rápido para Influenza A: positivo\nRaio-X de tórax: campos pulmonares limpos, sem infiltrado evidente"
    )

    response = request_base(url, input)
    return_data = response.json()["data"]
    print(return_data)

    cid: str = return_data["cid"]
    result: str = return_data["result"].lower()

    assert response.status_code == 200
    assert "J10.1" in cid
    assert "tosse" in result
    assert "dor de garganta" in result
    assert "vírus" in result
    assert "identificado" in result


def test_correct_results_mieloma_multiplo():
    input["text_analysis"] = (
        "CASO CLÍNICO\n\nUm homem de 36 anos de idade, foi referenciado ao Departamento de Medicina\nInterna por anemia e insuficiência renal.\nO doente tinha recorrido a uma consulta de Medicina Geral e Familiar para avaliação de\nrotina. Nesta consulta foi identificada uma\nanemia macrocítica, elevação da velocidade\nde sedimentação (VS) e retenção azotada ligeira (Quadro I). Nesta consulta foi ainda\ndiagnosticado tumor de Whartin da parótida. Por complicação da citologia aspirativa\nda parótida, o doente foi medicado com\namoxicilina/ácido clavulânico e nimesulida.\nNa consulta de Anestesiologia pré-operatória do tumor de Whartin, o doente apresentava anemia com hemoglobina 7,6 g/dL\ne insuficiência renal com ureia 131 mg/dL e\ncreatinina 2,9 mg/dL (Quadro I), sendo referenciado à Medicina Interna.\n\nQuadro I – Evolução dos principais valores laboratoriais\n# Parâmetros Laboratoriais do Sangue - Dados Extraídos\n\n## Cronologia dos Exames\n- **60 dias antes**\n- **Dia 0** \n- **Dia 1**\n- **Dia 8**\n\n## Valores Laboratoriais\n\n### Hemograma\n- **Hemoglobina (g/dL)**: 11,4 → 7,8 → 6,7 → 10,0\n- **Hematócrito (%)**: 34,6 → 21,9 → 18,9 → 30,3\n- **Volume globular médio - VGM (fL)**: 107 → 104 → 103 → 98\n- **Hemoglobina globular média - HGM (pg)**: 35 → 37 → 37 → 32\n- **Leucócitos (x10³/L)**: 9,7 → 11,5 → 8,4 → 17,6\n- **Plaquetas (x10³/L)**: 331 → 465 → 396 → 354\n- **Reticulócitos (%)**: - → - → 1,2 → -\n\n### Marcadores Inflamatórios\n- **Velocidade de sedimentação (mm)**: 62 → - → 49 → -\n- **Proteína C reactiva (mg/dL)**: - → - → 1,56 → 2,92\n\n### Função Renal\n- **Ureia (mg/dL)**: 53 → 114 → 82 → 123\n- **Creatinina (mg/dL)**: 1,19 → 2,9 → 2,5 → 2,8\n\n### Proteínas\n- **Proteínas totais (g/dL)**: - → - → 5,2 → -\n- **Albumina (g/dL)**: - → - → 2,6 → -\n\n### Eletrólitos\n- **Sódio (mmol/L)**: 140 → 138 → 144 → 141\n- **Potássio (mmol/L)**: 4,35 → 5,8 → 4,7 → 4,8\n- **Cloro (mmol/L)**: 103 → 107 → 111 → 108\n\n### Metabolismo Mineral\n- **Cálcio (mg/dL)**: - → - → 8,4 → -\n- **Fósforo (mg/dL)**: - → - → 4,9 → -\n\n### Enzimas\n- **Desidrogenase láctica - LDH (UI/L)**: - → 130 → 125 → -\n\nExistia uma história com três meses de\nevolução de astenia, anorexia, emagrecimento de 8 kg (80 para 72 kg) e dejecções\nde fezes mais moles que o habitual. Não se\nconstataram perdas hemáticas aparentes,\nfebre ou queixas álgicas. Saliente-se que, no\ndia da consulta de Anestesiologia, o doente\ntinha tido jornada de trabalho nocturno\ncom duração superior a 8 horas, submetendo-se a esforço físico intenso. Nos antecedentes pessoais e hábitos, destacam-se\ncirurgia do testículo na infância e hábitos\ntabágicos quantificados em 20 unidades\nmaço-ano.\nNo exame físico, o doente encontrava-se\npálido, apirético, com pressão arterial 120-\n80 mmHg e pulso 95 batimentos por minuto. Verificava-se um aumento de volume da\nparótida direita. Não se palpavam linfadenopatias nas principais cadeias periféricas e\no exame de tórax e abdómen não apresentava alterações. Não existia edema periférico.\nNão apresentava alterações no exame neurológico.\nA anemia foi caracterizada como macrocítica arregenerativa, com factores hematínicos dentro da normalidade (Quadro I). Laboratorialmente, realçava-se ainda VS 49 mm,\nhipoalbuminemia (2,6 g/dL), hipo-gamaglobulinemia (Fig. 1) e proteinúria nefrótica (3,7 g/24h). A proteinúria caracterizava-se pela presença de marcadores de lesão\nglomerular (albumina, imunoglobulina G,\ntransferrina e haptoglobina), bem como\nde lesão tubular (beta2-microglobulina e\nalfa1-microglobulina). A ecografia renal\nmostrou rins de dimensões aumentadas e\na tomografia axial computorizada toraco-\n-abdomino-pélvica confirmou rins de tamanho aumentado, com densificação da gordura peri-renal e revelou lesões líticas do segundo arco costal direito, manúbrio esternal\ne ossos ilíacos. Procedeu-se então a mielograma e biópsia óssea que revelaram infiltração\nda medula óssea por plasmócitos, ocupando cerca de 75% dos espaços medulares da\namostra de biopsia óssea (Fig. 2). O doente\nfoi ainda submetido a biópsia renal cujo estudo histopatológico mostrou aspectos compatíveis com doença de depósito de cadeias\nleves K associada a nefropatia de cilindros\n(Fig. 3). A imunoelectroforese das proteínas\nséricas e urinárias veio a revelar uma proteína monoclonal IgA/K, com elevação das cadeias leves K livres. O valor de beta2-microglobulina era de 13,6 mg/L. A imunofenotipagem revelou plasmócitos com o fenótipo aberrante CD38++/CD138+/CD56+/CD45-/CD19-/CD117-. No estudo citogenético, identificou-se a translocação t(11;14)\n(q13;q32). A radiografia de esqueleto mostrou ainda lesões líticas da calote craniana. Estabeleceu-se o diagnóstico de mieloma\nmúltiplo IgA/K, com rim de mieloma e\ndoença de depósito de cadeias leves, estadio IIIB de Durie-Salmon e estadio III do\nInternational Staging System (ISS).\nDurante o internamento, o doente manteve-se praticamente assintomático, com\nflutuações discretas do valor de creatinina.\nPara permitir a realização de biópsia renal\ncom segurança, fez terapêutica transfusional com quatro unidades de concentrado\neritrocitário. Ao 7º dia de internamento iniciou terapêutica com dexametasona.\nO doente foi referenciado à consulta de Hematologia de hospital central oncológico,\nonde iniciou bortezomib, estando planeado\nauto-transplante de células estaminais com\ndose alta de melfalan."
    )

    response = request_base(url, input)
    return_data = response.json()["data"]
    print(return_data)

    cid: str = return_data["cid"]
    result: str = return_data["result"].lower()

    assert response.status_code == 200
    assert "C90.0" in cid
    assert "insuficiência renal" in result
    assert "medula óssea" in result
    assert "mieloma múltiplo" in result
    assert "neoplasia maligna" in result
    assert "plasmócitos" in result


def test_correct_results_chagas():
    input["text_analysis"] = (
        "APRESENTAÇÃO DO CASO CLÍNICO\nPDS, 71 anos, sexo masculino, pardo, natural do norte de Minas, portador de Doença de\nChagas em acompanhamento médico irregular há 4 anos. Há aproximadamente 60 dias,\npaciente tem observado constipação, mal-estar ao se alimentar e distensão abdominal.\nA disfagia tem piorado e na última semana houve episódios persistentes de vômitos para\nalimentos sólidos, pastosos e líquidos, com restos alimentares. Foi internado há uma\nsemana com piora do quadro. Relata que seu peso habitual é de 68 kg e que teve perda\nde mais de 10 kg em seis meses, fraqueza em MMII, ausência de dejeções associados a\npouca ingesta de alimentos.\nNega febre, hematêmese, disúria, poliúria, oligúria e uso de medicações. Evacuação presente com fezes endurecidas, sem sangramentos.\nRefere passado de etilismo, durante aproximadamente 32 anos, com uso de bebidas destiladas, predominantemente. Abstêmio há 10 meses, nega tabagismo e outras drogas.\nAo exame físico: Paciente em REG, acianótico, anictérico, corado, afebril, caquético, 54 kg,\n152 cm de altura.\nAbdome escavado, flácido, ruídos hidroaéreos presentes, predominância de sons timpânicos, indolor à palpação superficial e profunda, ausência de massas ou visceromegalias.\nFC: 70 bpm, PA: 110x64 mmHg, FR: 16 IRPM\n\nEXAMES COMPLEMENTARES:\n\nLaboratório Valores obtidos Valores Referenciais\nHemograma\nHemoglobina 14g/dL 13,5g/dL – 17,5 g/dL\nLeucócitos 3.070/ ml 5.000/mm³ - 10.000 mm³\nPlaquetas 286.000 /mL 150.000 – 400.000/mL\nBioquímica\nGlicemia 92 mg/dL <100m mg/dL\nUreia 66 mg/dL 18 – 55 mg/dL\nCreatinina 0,9 mg/dL 0,8 – 1,3 mg/dL\nPotássio 3,9 mmol/L 3,5 – 4,5 mEq/L\nSódio 139 mEq/L 135 – 145 mEq/L\nFósforo 0,7 mmol/L 0,8-1,4 mmol/L"
    )

    response = request_base(url, input)
    return_data = response.json()["data"]

    cid: str = return_data["cid"]
    result: str = return_data["result"].lower()
    print(cid)
    print(result)

    assert response.status_code == 200
    assert "K22" in cid
    assert "acalasia do esôfago" in result
    assert "disfagia" in result
    assert "doença de chagas" in result
    assert "regurgitação" in result


def test_correct_results_joanete():
    input["text_analysis"] = (
        "Informações do paciente\nNome: Maria das Dores\nIdade: 62 anos\nMotivo da consulta: Dor progressiva e deformidade visível no pé direito, com dificuldade para utilizar calçados fechados e limitação para atividades diárias.\nHistórico da moléstia atual\nA paciente relata que há cerca de cinco anos percebeu uma proeminência óssea na face medial do pé direito, próxima ao dedão, inicialmente sem dor significativa. Com o passar do tempo, a saliência aumentou de tamanho e, nos últimos doze meses, a dor tornou-se mais frequente e intensa, inclusive em repouso. O desconforto é descrito como em queimação e pressão, agravando-se com o uso de calçados fechados ou salto alto e após caminhadas prolongadas.\nRelata episódios de vermelhidão e calor local, acompanhados de edema leve, principalmente no final do dia. Nos últimos meses, passou a evitar atividades físicas e reduzir o tempo em pé, devido à piora dos sintomas. Nega trauma prévio, febre, calafrios ou feridas na região afetada.\nHistória patológica pregressa\nHipertensa há 15 anos, em uso regular de losartana. Nega diagnóstico prévio de artrite reumatoide, gota ou outras doenças inflamatórias articulares. Nunca foi submetida a cirurgias ou internações hospitalares. Nega alergias medicamentosas ou alimentares conhecidas. Não faz uso de medicamentos contínuos além do anti-hipertensivo.\nHistórico familiar\nRefere que a mãe e a avó materna apresentaram deformidade semelhante nos pés, ambas submetidas a tratamento cirúrgico na idade adulta. Nega histórico familiar de artrite reumatoide, gota ou outras doenças reumatológicas. Não há registros de síndromes genéticas ou doenças ósseas hereditárias conhecidas na família.\nHistórico social\nNega tabagismo e relata consumo eventual de bebidas alcoólicas em encontros sociais. Mantém alimentação considerada equilibrada, embora com ingestão moderada de alimentos industrializados. O padrão de sono é regular, com cerca de 7 horas por noite.\nNos últimos anos, refere redução significativa da atividade física, limitando-se a caminhadas esporádicas devido à dor no pé. Trabalhou por mais de 30 anos como secretária, utilizando com frequência sapatos de salto alto e bico fino, o que acredita ter contribuído para o agravamento da deformidade. Atualmente está aposentada.\nExame físico\nPaciente em bom estado geral, normocorada, hidratada, afebril e eupneica em repouso.\nSinais vitais: pressão arterial 128/78 mmHg, frequência cardíaca 82 bpm, frequência respiratória 16 irpm, temperatura 36,4 °C, saturação de oxigênio 98% em ar ambiente.\nPé direito: desvio lateral do hálux com proeminência óssea medial evidente, acompanhada de eritema e edema leve na articulação metatarsofalângica. Dor à palpação e durante dorsiflexão do hálux.\nPele: presença de calosidade sobre a proeminência óssea, sem ulcerações.\nMarcha: discreta alteração, com apoio lateralizado do pé direito para reduzir a pressão na área dolorosa.\nDemais sistemas: sem alterações relevantes no exame físico geral.\nExames complementares\nFoi realizada radiografia do pé direito em carga, evidenciando ângulo do hálux valgus de 38° e ângulo intermetatarsal de 15°, compatíveis com deformidade moderada. Não foram observadas erosões ósseas ou sinais radiológicos de doenças inflamatórias articulares.\nExames laboratoriais solicitados para descartar causas associadas, incluindo ácido úrico, fator reumatoide e proteína C reativa, apresentaram resultados dentro da normalidade."
    )

    response = request_base(url, input)
    return_data = response.json()["data"]

    cid = return_data["cid"]
    result = return_data["result"].lower()
    print(result)

    assert response.status_code == 200
    assert "M20.1" in cid
    assert "deformidade" in result
    assert "hálux valgo" in result
    assert "pé" in result
    assert "proeminência óssea" in result


def test_error_invalid_input():
    input["text_analysis"] = 500

    response = request_base(url, input)
    return_data = response.json()["detail"][0]

    assert response.status_code == 422
    assert "Input should be a valid string" in return_data["msg"]
