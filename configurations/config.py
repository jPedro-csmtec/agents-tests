import os
import sys
from dotenv import load_dotenv

if getattr(sys, 'frozen', False):
    BASE_DIR = sys._MEIPASS
else:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ENV_PATH = os.path.join(BASE_DIR, ".env")

load_dotenv(ENV_PATH)

class Config:
    
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
    AWS_REGION = os.getenv("AWS_DEFAULT_REGION")
    AWS_BUCKET_NAME = os.getenv("AWS_BUCKET_NAME")
    CUDA_CONFIG = os.getenv("CUDA_CONFIG")
    PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
    PINECONE_CLOUD = os.getenv("PINECONE_CLOUD")
    PINECONE_REGION = os.getenv("PINECONE_REGION")
    PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")
    SECRET_KEY = os.getenv("SECRET_KEY")
    ALGORITHM = os.getenv("ALGORITHM")
    RATE_LIMIT = os.getenv("RATE_LIMIT")
    WINDOW = os.getenv("WINDOW")
    ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
    USERNAME = os.getenv("USERNAME")
    PASSWORD = os.getenv("PASSWORD")
    TELEGRAM_URL_MESSAGE = os.getenv("TELEGRAM_URL_MESSAGE")
    
    TRY_CALL_AGENTS = os.getenv("TRY_CALL_AGENTS")
    TIME_TO_WAIT = os.getenv("TIME_TO_WAIT")
    
    SERVICE_NAME = os.getenv("SERVICE_NAME")
    UPSTREAM_BASE_URL = os.getenv("UPSTREAM_BASE_URL")
    FORWARD_CLIENT_BEARER = os.getenv("FORWARD_CLIENT_BEARER")
    UPSTREAM_STATIC_BEARER = os.getenv("UPSTREAM_STATIC_BEARER")
    HTTP_TIMEOUT = os.getenv("HTTP_TIMEOUT")
