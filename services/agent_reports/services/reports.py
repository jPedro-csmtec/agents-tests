from typing import Tuple
from libs.utils.telegram_seed_info import send_message_telegram
from logs.logger import log_function_call
from services.agent_reports.services.agents_reports import reports
from agents import Runner

@log_function_call
async def reports_info(payload: str) -> Tuple[str, bool]:
    
    try:
        result = await Runner.run(reports, input=payload)
    except Exception as e:
        error_message=f"Erro: {e}"
        send_message_telegram(error_message, "REPORT_AGENT")
        return error_message, False
    
    return result.final_output, True