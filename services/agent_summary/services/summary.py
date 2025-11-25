import time
from typing import Tuple
from agents import Runner
from libs.utils.telegram_seed_info import send_message_telegram
from logs.logger import log_function_call
from services.agent_summary.app.schemas.summary_object import RequestSummary
from services.agent_summary.services.agent_summary import agent_summary
from services.agent_summary.services.agent_summary_resume import agent_summary_resume

@log_function_call
async def summary_call(payload: RequestSummary) -> Tuple[str, bool]:
    """
    Função responsavel para a criação do sumario.
    Args:
        text_summary (str): Conjunto de informações, enviadas para construção do sumario.
        agent_resume (bool): Campo para seleção de formato completo ou resumido do sumario.
    """
    try:
        if (payload.agent_resume):
            result = await Runner.run(agent_summary_resume, input=payload.text_summary)
        else:
            result = await Runner.run(agent_summary, input=payload.text_summary)
    
    except Exception as e:
        error_message = f"ERRO: {e}"
        send_message_telegram(error_message, "SUMMARY_AGENT")
        return error_message, False
        
    return result.final_output, True