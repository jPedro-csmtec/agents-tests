from typing import Tuple
from agents import ModelSettings, Runner
from libs.utils.telegram_seed_info import send_message_telegram
from logs.logger import log_function_call
from services.agent_allergy.services.agent_allergy import agent_allergy

@log_function_call
async def allergy_info(payload:dict) -> Tuple[str, bool]:
    """
    Função para analisar o principil ativo da alergia encontrada.
    Args:
        model (str): model para a analise da alergia.
        text_allergy (str): texto para a analise de alergia.
    """
    try:
        model = payload.get("model")
        text = payload.get("text_allergy")

        if (model):
            agent_allergy.model = model
        else:
            agent_allergy.model_settings=ModelSettings(temperature=0.5)
            agent_allergy.model = "gpt-4o-2024-08-06"
        
        result = await Runner.run(agent_allergy, input=text)
        
    except Exception as e:
        error_message=f"Erro: {e}"
        send_message_telegram(error_message, "ALLERGY_AGENT")
        return error_message, False
    
    return result.final_output, True