import time
from typing import Tuple
from agents import Runner
from libs.utils.telegram_seed_info import send_message_telegram
from logs.logger import log_function_call
from services.agent_treatment.services.agent_treatment import agent_treatment

@log_function_call
async def treatment_call(payload: str) -> Tuple[str, bool]:
    """
    Função responsavel para a criação do tratamentto a ser seguido.
    Args:
        text_treatment (str): Conjunto de informações, enviadas para construção do tratamento.
    """
    try:
        result = await Runner.run(agent_treatment, input=payload)
    
    except Exception as e:
        error_message = f"ERRO: {e}"
        send_message_telegram(error_message, "TREATMENT_AGENT")
        return error_message, False
        
    return result.final_output, True