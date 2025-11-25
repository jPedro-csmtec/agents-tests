from services.agent_analysis_vision.app.schemas.vision_object import ModelVisionData
from services.agent_analysis_vision.service.agent_vision import *
from logs.logger import log_function_call

@log_function_call
async def vision_info(url: str, prompt: str) -> tuple[str, bool]:
    """
    Função responsavel pela analise da imagem passada pela url, mais prompt para direcionamento do agente.
    Args:
        url (str): model para a analise da imagem.
        prompt (str): texto de direcinamento da analise do arquivo enviado.
    """
    try:
        response =  await analyze_image_url(url, prompt)
        
        text = ModelVisionData.model_validate_json(response)
    except Exception as e:
        error_message = f"Error applying Vision: {e}"
        return error_message, False
    
    return text, True