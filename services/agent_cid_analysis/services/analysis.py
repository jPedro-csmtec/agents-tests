import time
from typing import Tuple
from libs.utils.telegram_seed_info import send_message_telegram
from logs.logger import log_function_call
from services.agent_cid_analysis.services.agents_cid_analysis import search_cid_analysis
from agents import Runner

@log_function_call
async def analysis_info(payload: str) -> Tuple[str, bool]:
    """
    Função para analisar o código CID-10 baseado em uma queixa dada pelo paciente.
    Args:
        text_analysis (str): Queixa principal dada pelo paciente.
    """    

    try:
        result = await Runner.run(search_cid_analysis, input=payload)
    
    except Exception as e:
        error_message = f"ERRO: {e}"
        send_message_telegram(error_message, "CID_AGENT")
        return error_message, False
        
    return result.final_output, True