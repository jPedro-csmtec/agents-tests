import asyncio
import base64
from enum import Enum
import os
from mistralai import Mistral
from configurations.config import Config

class MistralAgentRunType(Enum):
    OCR = 1
    DOCUMENT_UNDERSTANDING = 2

class MistralAgent:
    def __init__(self, agent_name: str, system_prompt: str):
        """
        Initialize the MistralAgent with the given parameters.

        :param agent_name: Name of the agent
        :param system_prompt: System prompt describing the agent's behavior
        """
        self.client = Mistral(api_key=Config.MISTRAL_API_KEY)
        self.name = agent_name
        self.agent_name = agent_name
        self.system_prompt = system_prompt

    async def run_concurrent(self, message: str, image_path: str, type: MistralAgentRunType, model_name: str = "mistral-ocr-2505") -> str:
        """
        Run the MistralAgent with the given run type.

        :param type: Type of run to execute
        :return: Output of the agent
        """
        if type == MistralAgentRunType.OCR:
            return await self.ocr_reader(image_path)
        elif type == MistralAgentRunType.DOCUMENT_UNDERSTANDING:
            return await self.document_understanding(self.system_prompt + '\n' + message, image_path, model_name)
        else:
            raise ValueError("Invalid MistralAgentRunType")
        
    async def document_understanding(self, message: str, image_path: str, model_name: str) -> str:
        
        document = await self.prepare_document(image_path)
        chat_response = await self.client.chat.complete_async(
            model=model_name,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": message
                        },
                        document
                    ]
                }
            ]
        )

        return chat_response.choices[0].message.content

    async def ocr_reader(self, image_path: str):
        
        document = await self.prepare_document(image_path)
        ocr_response = await self.client.ocr.process_async(
            model="mistral-ocr-2505",
            document=document,
        )

        ocr_data = ocr_response.model_dump()
        joined_pages = ""
        for page in ocr_data["pages"]:
            joined_pages += page["markdown"] + '\n'

        return joined_pages

    async def prepare_document(self, image_path: str):
        document = None

        if self.is_pdf_by_extension(image_path):
            uploaded_pdf = await self.client.files.upload_async(
                file={
                    "file_name": os.path.basename(image_path),
                    "content": open(image_path, "rb"),
                },
                purpose="ocr"
            )
            self.client.files.retrieve(file_id=uploaded_pdf.id)
            signed_url = self.client.files.get_signed_url(file_id=uploaded_pdf.id)
            document={
                "type": "document_url",
                "document_url": signed_url.url,
            }
        else:
            base64_image = self.encode_image(image_path)
            document={
                "type": "image_url",
                "image_url": f"data:image/jpeg;base64,{base64_image}" 
            }

        return document

    def is_pdf_by_extension(self, file_path: str) -> bool:
        return os.path.splitext(file_path)[1].lower() == ".pdf"
    
    def build_image_url_format(self, image_path: str) -> str:
        _, extension = os.path.splitext(image_path)
        extension = extension.lower().lstrip(".")
        mime_types = {
            "jpg": "jpeg",
            "jpeg": "jpeg",
            "png": "png",
            "gif": "gif",
            "bmp": "bmp",
            "webp": "webp",
        }

        if extension not in mime_types:
            raise ValueError("Unsupported image extension")

        with open(image_path, "rb") as image_file:
            image_data = image_file.read()
            base64_image = base64.b64encode(image_data).decode("utf-8")

        return f"data:image/{mime_types[extension]};base64,{base64_image}"

    def encode_image(self, image_path):
        try:
            with open(image_path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode('utf-8')
        except FileNotFoundError:
            print(f"Error: The file {image_path} was not found.")
            return None
        except Exception as e:
            print(f"Error: {e}")
            return None

