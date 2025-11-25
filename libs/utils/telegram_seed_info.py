from shlex import quote
import requests
from configurations.config import Config
from logs.logger import log_function_call
from urllib.parse import quote

@log_function_call
def send_message_telegram(text: str, module_name: str):
    
    log_text = f"AI_AGENTS DEV - {module_name} #{text.upper()}"
    base_url = f"{Config.TELEGRAM_URL_MESSAGE}{quote(log_text)}"

    res = requests.get(base_url)

    if res.status_code == 200:
        print("Mensagem enviada com sucesso!")
        print(res.json())
    else:
        print("Erro ao enviar:", res.status_code, res.text)
