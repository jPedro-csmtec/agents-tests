from services.tests.general import request_base, url_base

url = f"{url_base}/diagnostic-info/diagnostics"


def test_correct_results():
    data = {
        "text_diagnostic": """
        Informações do paciente
        Joana Ribeiro, 42 anos, comparece ao pronto-atendimento com queixa de febre alta e dores no corpo há dois dias.

        Histórico da moléstia atual 
        Paciente relata início súbito de febre alta, calafrios, cefaleia intensa, dores musculares generalizadas, coriza e tosse seca há cerca de dois dias. Refere também prostração importante e dor de garganta, sem presença de vômitos ou diarreia. Informa que o quadro começou após contato próximo com o neto, que apresentou sintomas semelhantes na semana anterior. Nega dispneia, dor torácica ou outros sintomas respiratórios mais graves até o momento.


        História patológica pregressa 
        A paciente é portadora de hipertensão arterial sistêmica, em uso regular de losartana, com controle adequado. Nega outras doenças crônicas, internações prévias ou cirurgias. Refere não possuir alergias conhecidas a medicamentos ou alimentos e nunca fez uso de imunossupressores.


        Histórico familiar 
        Relata que a mãe é hipertensa e diabética, ambas condições controladas com medicação. O pai faleceu aos 70 anos devido a um acidente vascular cerebral isquêmico. Nega histórico familiar de doenças genéticas, autoimunes ou respiratórias crônicas. Não há casos conhecidos de neoplasias de aparecimento precoce na família.


        Histórico social 
        Trabalha como professora da educação infantil em escola pública, tendo contato frequente com crianças. Nega tabagismo e faz uso ocasional de bebidas alcoólicas em eventos sociais. Refere sono regular de aproximadamente sete horas por noite, mas não pratica atividade física com regularidade. Alimenta-se de forma variada, embora reconheça consumo esporádico de alimentos ultraprocessados durante a semana.


        Exame físico
        Apresenta-se em bom estado geral, embora com fácies febril e discreta prostração. Está febril (38,7 °C), com frequência cardíaca de 104 bpm, pressão arterial de 130/80 mmHg e saturação periférica de oxigênio de 97% em ar ambiente. Mucosas orais e nasais estão hiperemiadas, com orofaringe levemente avermelhada, sem exsudato. Ausculta pulmonar revela murmúrio vesicular presente e simétrico, sem ruídos adventícios. Abdome flácido, indolor à palpação, sem visceromegalias. Demais sistemas sem alterações significativas.


        Exames complementares
        Hemograma: leucocitose leve com predomínio de neutrófilos
        PCR: 12 mg/L
        Teste rápido para Influenza A: positivo
        Raio-X de tórax: campos pulmonares limpos, sem infiltrado evidente

        ## Código CID

        ### Sumário de códigos encontrados

        1. **J10.1 – Influenza [gripe] devida a vírus influenza identificado, com outras manifestações respiratórias**  
        2. **I10 – Hipertensão essencial (primária)**  
        3. **R50.9 – Febre, não especificada**  
        4. **R51 – Cefaleia**  
        5. **M79.1 – Mialgia**  
        6. **R05 – Tosse**  
        7. **R07.0 – Dor de garganta**  
        8. **R53 – Mal-estar e fadiga**  
        9. **D72.8 – Outros transtornos especificados dos leucócitos (leucocitose)**  
        10. **R79.8 – Outros achados anormais especificados de exames químicos do sangue (PCR elevada)**  

        > Observação: em prática de codificação, geralmente o diagnóstico principal (influenza) e comorbidades relevantes (hipertensão) são prioritários; os sintomas costumam ser codificados apenas se houver necessidade específica. Aqui, todos os códigos possíveis a partir dos dados fornecidos estão listados.

        ---

        ### Detalhes por código

        #### 1. Código CID
        **J10.1**

        - **Descrição:** Influenza [gripe] devida a vírus influenza identificado, com outras manifestações respiratórias  
        - **Categoria Principal:** Capítulo X – Doenças do aparelho respiratório (J00–J99)  
        - **Nome:** Influenza por vírus identificado, com outras manifestações respiratórias  
        - **Definição:**  
        Influenza aguda causada por vírus influenza comprovado por exame laboratorial ou outro método de identificação, caracterizada por início súbito de febre, sintomas respiratórios altos (coriza, tosse, dor de garganta) e sintomas sistêmicos (mialgia, cefaleia, mal-estar), **sem pneumonia**.  
        - **Descrição Detalhada (critérios, cenários de uso, observações):**  
        - Usar J10.* quando há identificação do vírus influenza (por exemplo, teste rápido positivo, PCR, cultura).  
        - Subcategoria **J10.1** específica para casos em que:
            - há manifestações respiratórias (tosse, coriza, dor de garganta, irritação de vias aéreas superiores);  
            - não há evidência de pneumonia clínica ou radiológica.  
        - Excluir J10.0 (com pneumonia) quando o RX de tórax é normal e não há sinais clínicos de pneumonia.  
        - Pode coexistir com sintomas sistêmicos intensos (mialgia, cefaleia, prostração), sem necessidade de subcategoria adicional, pois estes estão incluídos na síndrome gripal.  
        - **Justificativa de associação:**  
        - Teste rápido para **Influenza A: positivo** → vírus influenza identificado.  
        - Quadro agudo de 2 dias com:
            - febre alta, calafrios;  
            - tosse seca, coriza, dor de garganta;  
            - cefaleia intensa, dores musculares generalizadas, prostração;  
        - Ausência de infiltrado pulmonar em RX de tórax e ausculta pulmonar sem ruídos adventícios → **sem pneumonia**, logo J10.0 é excluído.  
        → Portanto, o código mais adequado é **J10.1** (influenza por vírus identificado com outras manifestações respiratórias).

        ---

        #### 2. Código CID
        **I10**

        - **Descrição:** Hipertensão essencial (primária)  
        - **Categoria Principal:** Capítulo IX – Doenças do aparelho circulatório (I00–I99)  
        - **Nome:** Hipertensão arterial essencial (primária)  
        - **Definição:**  
        Elevação crônica da pressão arterial sem causa secundária identificável (não atribuída a doença renal, endócrina, etc.), frequentemente tratada de forma contínua com anti-hipertensivos.  
        - **Descrição Detalhada (critérios, cenários de uso, observações):**  
        - Utilizado para pacientes com diagnóstico estabelecido de hipertensão arterial sistêmica, controlada ou não, sem etiologia secundária descrita no prontuário.  
        - Abrange a hipertensão tratada com monoterapia ou combinação de fármacos.  
        - Importante como comorbidade em qualquer atendimento agudo, pois pode influenciar conduta e risco cardiovascular.  
        - **Justificativa de associação:**  
        - História patológica pregressa: “**portadora de hipertensão arterial sistêmica, em uso regular de losartana, com controle adequado**.”  
        - Não há menção de causa secundária (doença renal, endócrina etc.).  
        → Configura **hipertensão essencial**, código **I10**.

        ---

        #### 3. Código CID
        **R50.9**

        - **Descrição:** Febre, não especificada  
        - **Categoria Principal:** Capítulo XVIII – Sintomas, sinais e achados anormais de exames clínicos e de laboratório, não classificados em outra parte (R00–R99)  
        - **Nome:** Febre, não especificada  
        - **Definição:**  
        Elevação da temperatura corporal acima dos valores considerados normais, sem especificação da causa no próprio código.  
        - **Descrição Detalhada (critérios, cenários de uso, observações):**  
        - Usado quando se deseja registrar o sintoma febre como dado clínico relevante.  
        - Em presença de diagnóstico etiológico (influenza), muitas vezes o sintoma não é codificado separadamente, mas é perfeitamente aceitável listá-lo se o foco for documentar o quadro clínico completo.  
        - **Justificativa de associação:**  
        - Queixa principal de “**febre alta**” há dois dias.  
        - Exame físico: temperatura de **38,7 °C**.  
        → Sintoma febre presente e documentado, compatível com **R50.9**.

        ---

        #### 4. Código CID
        **R51**

        - **Descrição:** Cefaleia  
        - **Categoria Principal:** Capítulo XVIII – Sintomas, sinais e achados anormais de exames clínicos e de laboratório (R00–R99)  
        - **Nome:** Cefaleia  
        - **Definição:**  
        Dor localizada na região da cabeça, sem especificação de tipo (tensional, enxaqueca, etc.) quando codificada em R51.  
        - **Descrição Detalhada (critérios, cenários de uso, observações):**  
        - Utilizado para dor de cabeça como sintoma em diversos contextos.  
        - Em quadros infecciosos agudos, a cefaleia é frequentemente secundária à doença de base (aqui, influenza), mas pode ser registrada.  
        - **Justificativa de associação:**  
        - HMA: “**cefaleia intensa**” associada ao quadro febril.  
        - Não há descrição de enxaqueca ou outro tipo específico → cefaleia inespecífica.  
        → Código sintomático adequado: **R51**.

        ---

        #### 5. Código CID
        **M79.1**

        - **Descrição:** Mialgia  
        - **Categoria Principal:** Capítulo XIII – Doenças do sistema osteomuscular e do tecido conjuntivo (M00–M99)  
        - **Nome:** Mialgia  
        - **Definição:**  
        Dor muscular localizada ou generalizada, de origem não especificada, podendo estar associada a infecções virais, esforço físico, doenças reumáticas etc.  
        - **Descrição Detalhada (critérios, cenários de uso, observações):**  
        - Usado para dor muscular sem diagnóstico etiológico distinto no próprio código.  
        - Em síndromes gripais, mialgia difusa é um achado típico e pode ser registrada como tal.  
        - **Justificativa de associação:**  
        - HMA: “**dores musculares generalizadas**”.  
        - Não há descrição de trauma, doenças musculares específicas ou outra etiologia.  
        → Sintoma de mialgia codificável como **M79.1**.

        ---

        #### 6. Código CID
        **R05**

        - **Descrição:** Tosse  
        - **Categoria Principal:** Capítulo XVIII – Sintomas, sinais e achados anormais de exames clínicos e de laboratório (R00–R99)  
        - **Nome:** Tosse  
        - **Definição:**  
        Expulsão súbita e ruidosa de ar dos pulmões, voluntária ou reflexa, acompanhando diversas doenças respiratórias.  
        - **Descrição Detalhada (critérios, cenários de uso, observações):**  
        - Sintoma respiratório muito comum, usado quando se quer explicitar a presença de tosse.  
        - Em casos de influenza, a tosse faz parte do quadro síndrome gripal, mas ainda assim pode ser codificada como sintoma.  
        - **Justificativa de associação:**  
        - HMA: “**tosse seca**” há cerca de dois dias.  
        - Não há especificação adicional (expectorante, hemoptise etc.), logo código genérico de tosse é adequado.  
        → **R05** devidamente aplicável.

        ---

        #### 7. Código CID
        **R07.0**

        - **Descrição:** Dor de garganta  
        - **Categoria Principal:** Capítulo XVIII – Sintomas, sinais e achados anormais de exames clínicos e de laboratório (R00–R99)  
        - **Nome:** Dor de garganta  
        - **Definição:**  
        Dor localizada na região da orofaringe/hipofaringe, seja por processo infeccioso, inflamatório, irritativo ou outro, sem especificação etiológica.  
        - **Descrição Detalhada (critérios, cenários de uso, observações):**  
        - Usado quando a dor de garganta é descrita como sintoma, sem diagnóstico específico de faringite ou amigdalite (J02, J03 etc.).  
        - Quando se opta por manter o diagnóstico global de influenza (sem faringite específica), a dor de garganta pode ser codificada como sintoma.  
        - **Justificativa de associação:**  
        - HMA: “**dor de garganta**”.  
        - Exame físico: “**orofaringe levemente avermelhada, sem exsudato**”, mas o diagnóstico principal adotado foi influenza, não faringite isolada.  
        → Sintoma compatível com **R07.0**.

        ---

        #### 8. Código CID
        **R53**

        - **Descrição:** Mal-estar e fadiga  
        - **Categoria Principal:** Capítulo XVIII – Sintomas, sinais e achados anormais de exames clínicos e de laboratório (R00–R99)  
        - **Nome:** Mal-estar e fadiga  
        - **Definição:**  
        Sensação de fraqueza, cansaço, prostração ou indisposição geral, não atribuída a uma condição específica no próprio código.  
        - **Descrição Detalhada (critérios, cenários de uso, observações):**  
        - Comum em quadros infecciosos agudos como influenza.  
        - Pode ser usado para documentar a intensidade do comprometimento geral do paciente.  
        - **Justificativa de associação:**  
        - HMA: “**prostração importante**”.  
        - Exame físico: discreta prostração, apesar de bom estado geral.  
        → Sintoma de mal-estar/prostração enquadra-se em **R53**.

        ---

        #### 9. Código CID
        **D72.8**

        - **Descrição:** Outros transtornos especificados dos leucócitos  
        - **Categoria Principal:** Capítulo III – Doenças do sangue e dos órgãos hematopoéticos e alguns transtornos imunitários (D50–D89)  
        - **Nome:** Outros transtornos especificados dos leucócitos  
        - **Definição:**  
        Alterações quantitativas ou qualitativas dos leucócitos não classificadas em categorias mais específicas, incluindo leucocitose.  
        - **Descrição Detalhada (critérios, cenários de uso, observações):**  
        - Abrange **leucocitose** não atribuída a doenças hematológicas específicas.  
        - Frequentemente secundária a processos infecciosos agudos, inflamações etc.  
        - Em muitas situações, este código não é usado isoladamente quando a leucocitose é claramente reacional à infecção de base; contudo, é um código válido para registrar o achado laboratorial.  
        - **Justificativa de associação:**  
        - Hemograma: “**leucocitose leve com predomínio de neutrófilos**.”  
        - Não há evidência de doença hematológica primária, sendo compatível com leucocitose reacional ao quadro infeccioso.  
        → Achado laboratorial compatível com **D72.8**.

        ---

        #### 10. Código CID
        **R79.8**

        - **Descrição:** Outros achados anormais especificados de exames químicos do sangue  
        - **Categoria Principal:** Capítulo XVIII – Sintomas, sinais e achados anormais de exames clínicos e de laboratório (R00–R99)  
        - **Nome:** Outros achados anormais especificados de exames químicos do sangue  
        - **Definição:**  
        Alterações em parâmetros de exames bioquímicos sanguíneos que não possuem código específico em outras categorias.  
        - **Descrição Detalhada (critérios, cenários de uso, observações):**  
        - Inclui resultados alterados de marcadores inflamatórios (como proteína C reativa) quando não codificados de outra forma.  
        - Em geral é código secundário, usado quando se deseja registrar explicitamente o achado laboratorial.  
        - **Justificativa de associação:**  
        - Exames complementares: **PCR: 12 mg/L**, valor descrito como elevado para o contexto.  
        - Não há outro código mais específico para PCR elevada.  
        → Achado enquadrável em **R79.8**.

        ---

        Ministério da Saúde - CID-10 Brasil, 10ª Revisão, 2020.
        """,
        "model": "gpt-4o-mini"
    }

    response = request_base(url, data)
    return_data = response.json()['data']['result']

    assert response.status_code == 200
    assert "Influenza" in return_data
    assert "J10" in return_data
    assert "teste rápido positivo" in return_data
    assert "febre" in return_data
