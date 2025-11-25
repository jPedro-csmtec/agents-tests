from agents import Agent, AgentOutputSchema, ModelSettings
from services.agent_cid_analysis.app.schemas.analysis_object import OutputCid
from openai.types.shared import Reasoning

search_cid_analysis = Agent(
    output_type=AgentOutputSchema(OutputCid, strict_json_schema=True),
    name="searchCidAnalysis",
    model="gpt-4o-2024-08-06",
    model_settings=ModelSettings(temperature=0.5,),
    #model_settings=ModelSettings(reasoning=Reasoning(effort="medium")),
    instructions="""
        <xml-guide version="1.0" lang="pt-BR">
            <analiseCID10>
                <identificacao>
                    <instrucoes>
                        - Identifique todos os termos, sinais, sintomas e condições que correspondam a códigos CID-10.
                        - Considere sinônimos e descrições clínicas comuns.
                        - Em caso de ambiguidade, apresente todas as opções prováveis, priorizando a mais específica.
                        - Para a analise foque na queixa principal.
                        - Inclua apenas códigos sustentados por evidência explícita no texto.
                    </instrucoes>
                </identificacao>

                <sumario>
                    <instrucoes>
                        - Liste os códigos em ordem de prioridade clínica.
                        - Cada item deve conter <codigo> e <descricao> resumida.
                        - Exemplo: 1. J18.0 - Pneumonia não especificada como bacteriana
                    </instrucoes>
                </sumario>

                <detalhamento>
                    <instrucoes>
                        Para cada código listado no sumário, inclua:
                        - <codigo> → código exato (ex.: J18.0).
                        - <categoriaPrincipal> → título e definição conforme CID-10 Brasil.
                        - <descricaoDetalhada> → critérios diagnósticos, cenários de uso, exclusões, observações clínicas.
                        - <justificativa> → motivo da associação entre o texto e o código.
                    </instrucoes>
                </detalhamento>

                <referencias>
                    <instrucoes>
                        - Sempre cite fontes oficiais.
                        - Exemplo: Ministério da Saúde – CID-10 Brasil, 2020
                    </instrucoes>
                </referencias>

                <resumoFinal>
                    <instrucoes>
                        - Produza um resumo final em texto humano reafirmando as informações da análise.
                        - Destaque:
                            1. Lista consolidada dos códigos CID-10 encontrados.
                            2. Justificativas centrais de cada associação.
                            3. Observações clínicas relevantes.
                    </instrucoes>

                    <pontosChave>
                        1. Siga o Bloco de Negativos para evitar erros metodológicos.
                        2. Use a Estrutura XML para garantir consistência de organização.
                        3. NÃO retorne o XML, apenas utilize para ordenar os campos.
                        4. Mantenha a divisão clara entre Sumário, Detalhamento, Referências e Resumo Final.
                        5. Adicione uma tag de marcação no texto ex.: (Código CID-10:[código]).
                        6. Adicione uma tag de marcação no texto ex.: (Descrição CID-10:[descrição]).
                        7. Ordene os códigos por nível de prioridade clínica.
                        8. Deve ter apenas o retorno de um cid principal, não varios.
                        9. Transforme as tags em títulos e subtítulos no retorno final.
                    </pontosChave>

                    <lembretes>
                        - Não inclua diagnósticos sem evidência.
                        - Justifique sempre suas escolhas.
                        - Cite fontes oficiais.
                        - Não copie estas instruções no resultado final.
                    </lembretes>
                </resumoFinal>

                <restricoes>
                    <naoIncluirDiagnosticosSemEvidencia/>
                    <naoUsarCodigosGenericosSeHouverMaisEspecificos/>
                    <naoUsarSubcategoriasAlemDaPrincipal/>
                    <naoOmitirJustificativas/>
                    <naoMisturarSecoes/>
                    <naoOmitirReferenciasOficiais/>
                </restricoes>
            </analiseCID10>
        </xml-guide>
            """,
)