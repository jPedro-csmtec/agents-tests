from agents import Agent, ModelSettings

reports = Agent(
    name="reports",
    model="gpt-4o-2024-08-06",
    instructions="""
    Você é um agente especialista de análise de texto de laudos.
    Você deve levar consideração do texto que vai ser passado para você.
    Com isso deve procurar o laudo que contém os dados mais proximo com as informações passadas na mensagem.
    E retorna uma resposta em formato texto, focam apenas nos valores adicionado e o laudo.
    """,
    model_settings=ModelSettings( 
        temperature=0.2,
    ),
)