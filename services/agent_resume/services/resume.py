import time
from typing import Tuple
from agents import Runner
from libs.utils.telegram_seed_info import send_message_telegram
from logs.logger import log_function_call
from services.agent_resume.services.agent_resume import agents_resume

@log_function_call
async def resume_call(text_resume: str) -> Tuple[str, bool]:
    """
    Função responsavel para a criação do resumo das informações, levando em consideração os ponto.
    Args:
        text_resume (str): Informação passadas para construção do resumo.
    """
    try:
        result = await Runner.run(agents_resume, input=text_resume)
    
    except Exception as e:
        error_message = f"ERRO: {e}"
        send_message_telegram(error_message, "RESUME_AGENT")
        return error_message, False
        
    return result.final_output, True