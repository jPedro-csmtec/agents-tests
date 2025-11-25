import time
from typing import Tuple
from agents import ModelSettings, Runner
from openai.types.shared import Reasoning
from libs.utils.telegram_seed_info import send_message_telegram
from services.agent_diagnostic.services.agent_diagnostic import agent_diagnostic

async def diagnostic_info(payload:dict) -> Tuple[str, bool]:
    """
    Função para analisar diagnostico baseado das informações encaminhadas.
    Args:
        model (str): model utilizado pelo agente.
        text_diagnostic (str): Informação passada para a construção do diagnostico.
    """   
    
    try:
        model = payload.get("model")
        text = payload.get("text_diagnostic")
        if (model):
            agent_diagnostic.model = model
        if ("gpt-5" in model):
            agent_diagnostic.model_settings=ModelSettings(reasoning=Reasoning(effort="medium"))
        else:
            agent_diagnostic.model_settings=ModelSettings(temperature=0.3,)
        
        result = await Runner.run(agent_diagnostic, input=text)
        
    except Exception as e:
        error_message=f"Erro: {e}"
        send_message_telegram(error_message, "DIAGNOSTIC_AGENT")
        return error_message, False
        
    return result.final_output, True