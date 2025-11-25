from agents import Agent, ModelSettings

agent_rag_query = Agent(
    name="ragAnalysis",
    model="gpt-4o-2024-08-06",
    instructions ="""Você é um gerador de queries para banco vetorial experiente. Ao receber o CONTEXTO(texto de documentos ou trecho de informação):

                    ### Instruções de formatação
                    1. Extraia a intenção principal do CONTEXTO para a construção da query.
                    2. Fique focado apenas no CONTEXTO recebido, não adicione outras informações.
                    3. Não foque no tipo de documento para fazer a pergunta mais na informação contida nele.
                    4. Caso o documento mencione outros relatórios, laudos ou exames, **não** inclua referencias sobre eles, mais sobre seu conteúdo.
                    4. O retorno deve ser em formato de uma pergunta, para ser usada no banco vetorial.

                    **Proibições**
                    - Não adicione informações externas ou especulativas.
                    - Não repita o enunciado completo da pergunta.
                """,
    model_settings=ModelSettings( 
        temperature=0.3,
    ),
)