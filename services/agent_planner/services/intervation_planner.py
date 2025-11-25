import time
from typing import Tuple
from agents import Runner
from libs.utils.telegram_seed_info import send_message_telegram
from logs.logger import log_function_call
from services.agent_planner.services.agent_planner import agents_planner

@log_function_call
async def planner_call(text_info: str) -> Tuple[str, bool]:
    """
    Função para criar planejamento do tratamento, baseado nas informações passadas para o agente.
    Args:
        text_info (str): Informação passada para a construção do planejamento.
    """  
    try:
        result = await Runner.run(agents_planner, input=text_info)
    
    except Exception as e:
        error_message = f"ERRO: {e}"
        send_message_telegram(error_message, "INTERVATION_PLANNER_AGENT")
        return error_message, False
        
    return result.final_output, True