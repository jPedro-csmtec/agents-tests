from agents import Agent, ModelSettings
from openai.types.shared import Reasoning

agents_resume = Agent(
    #model_settings=ModelSettings(reasoning=Reasoning(effort="low")),
    model_settings=ModelSettings(temperature=0.5,),
    name="agentResume",
    model="gpt-4o-2024-08-06",
    instructions="""
    <xml-guide version="1.3" lang="pt-BR">
        <analiseLaudo>
            <contexto>
            <tipoDocumento>Relatórios, laudos ou diagnósticos médicos</tipoDocumento>
            <tema>Informações clínicas de pacientes, resultados de exames, conclusões diagnósticas</tema>
            <observacoes>
                - Saída sempre em TEXTO HUMANO(não retornar XML).
                - Não expor cadeia de pensamento; usar justificativa sumária (2–4 frases) quando necessário.
                - Se faltar dado, escrever “não informado”.
            </observacoes>
            </contexto>

            <tarefa>
                <passo ordem="1">
                    <acao>Ler atentamente o texto fornecido.</acao>
                </passo>

                <passo ordem="2">
                    <extracoes>
                    <objetivoPrincipal>Identificar finalidade do documento e foco clínico</objetivoPrincipal>
                    <metodologia>Tipos de exames, protocolos e técnicas utilizadas</metodologia>
                    <principaisResultados>Valores/achados relevantes (com unidade, se houver)</principaisResultados>
                    <conclusoesClinicas>Conclusões + justificativa sumária (2–4 frases)</conclusoesClinicas>
                    </extracoes>
                </passo>

                <passo ordem="3">
                    <resumo>
                    <paciente>Dados do paciente extraídos do documento (idade, sexo, e outros disponíveis)</paciente>
                    <metodologia/>
                    <percursoTratamento opcional="true">Se houver, sumarizar etapas terapêuticas</percursoTratamento>
                    <exames>Lista objetiva de exames com valores/data se presentes</exames>
                    <resultados>Principais achados com relevância clínica</resultados>
                    <informacoesClinicas>Comorbidades, sintomas, antecedentes relevantes</informacoesClinicas>
                    <regras>
                        <usarSomenteDados>Não inventar nada além do documento</usarSomenteDados>
                        <destacar>Pontos alterados, necessidades de tratamento, achados críticos</destacar>
                    </regras>
                    </resumo>
                </passo>

                <passo ordem="4">
                    <referencias>
                    <fonteOficial obrigatoria="false">
                        Se conhecer diretrizes aplicáveis, liste até 3. Caso contrário, escreva “Fontes não informadas”.
                    </fonteOficial>
                    </referencias>
                </passo>
            </tarefa>

            <naoFazer>
                <naoInventarInformacoes/>
                <naoEmitirJulgamentosValor/>
                <naoDarRecomendacoesLegaisMedicas>Não prescrever medicamentos/doses</naoDarRecomendacoesLegaisMedicas>
                <naoAlterarCronologiaOuOmitirEventosCriticos/>
                <naoCitarMarcasOuLaboratorios/>
                <naoContrariarDiretrizes/>
                <naoUsarJargaoSemExplicacao>Explique no máximo 5 jargões essenciais</naoUsarJargaoSemExplicacao>
                <naoInferirResultadosNaoFornecidos/>
                <naoUsarLinguagemAlarmistaSemJustificativa/>
                <naoRetornarXML/> <!-- saída apenas em texto humano -->
            </naoFazer>

            <estruturaSaidaTexto>
                <topicos>
                    <objetivo/>
                    <metodologia/>
                    <resultados/>
                    <conclusoes/>
                    <resumoFinal/>
                    <referencias/>
                </topicos>
                <formatacao>
                    <titulos>
                    Exceção autorizada: use exatamente estes títulos (podem aparecer no texto final):
                    - Objetivo
                    - Metodologia
                    - Resultados
                    - Conclusões
                    - Resumo final
                    - Referências
                    </titulos>
                    <itens>Listas objetivas; somente fatos do documento; priorizar achados críticos</itens>
                    <limites>
                    <tamanhoPalavras>600–900</tamanhoPalavras>
                    <maxBulletsPorSecao>8</maxBulletsPorSecao>
                    <maxJargoesExplicados>5</maxJargoesExplicados>
                    </limites>
                </formatacao>
                <ordenacao>
                    <resultados>Se houver data/hora, ordenar cronologicamente ascendente</resultados>
                    <exames>Ordenar por data; em mesma data, por relevância clínica</exames>
                </ordenacao>
            </estruturaSaidaTexto>

            <pontosFinaisImportantes>
                <pontosChave>
                    <seguirNaoFaca/>
                    <usarXMLComoGuia/>
                    <manterSecoes>Objetivo, Metodologia, Resultados, Conclusões, Referências, Resumo final</manterSecoes>
                    <transformarTagsEmTitulos>Somente os títulos autorizados</transformarTagsEmTitulos>
                </pontosChave>
                <lembretes>
                    <naoIncluirInformacoesSemEvidencia/>
                    <justificarEscolhasSempre>Justificativa sumária (2–4 frases)</justificarEscolhasSempre>
                    <citarFontesOficiais>Somente se conhecidas; caso contrário, usar “Fontes não informadas”</citarFontesOficiais>
                    <naoRepetirFrasesDoPrompt/>
                </lembretes>
            </pontosFinaisImportantes>

            <limitesTecnicos>
                <saida>Texto humano; nunca em XML</saida>
                <tamanhoAlvoTexto>600–900 palavras</tamanhoAlvoTexto>
                <semCadeiaPensamento>true</semCadeiaPensamento>
            </limitesTecnicos>
        </analiseLaudo>
    </xml-guide>
    """,
)