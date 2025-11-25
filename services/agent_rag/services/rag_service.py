from typing import Tuple
from agents import Runner
import openai
from configurations.config import Config
from libs.utils.telegram_seed_info import send_message_telegram
from logs.logger import log_function_call
from services.agent_rag.app.schemas.rag_object import PostQuery
from services.agent_rag.services.agents_rag import agent_rag, chunck_put
from services.agent_rag.services.agent_rag_analysis import agent_rag_query 
from pinecone import Pinecone

@log_function_call
def embed_text_ada(text: str) -> list[float]:
    response = openai.embeddings.create(
        input=text,
        model="text-embedding-ada-002"
    )
    return response.data[0].embedding

@log_function_call
def retrieve_messages(
    id_descriptions: list[dict],
    user_message: str,
    top_k: int = 300
) -> list[str]:

    embedding = embed_text_ada(user_message)
    
    pc = Pinecone(api_key=Config.PINECONE_API_KEY)
    index = pc.Index(Config.PINECONE_INDEX_NAME,
                    pool_threads=50,
                    connection_pool_maxsize=50)

    rag_texts: list[str] = []
    
    namespaces= [item['id'] for item in id_descriptions if item['id'] != '']
    group_ids = [item['group_id'] for item in id_descriptions if item['group_id'] != '']
    
    filtro = {"group_id": {"$in": group_ids}} if group_ids else None
    
    if len(namespaces) == 1:
        query_fn = index.query
        query_args = {
            "vector": embedding,
            "top_k": top_k,
            "include_metadata": True,
            "namespace": namespaces[0]
        }
    else:
        if not namespaces:
            stats = index.describe_index_stats().get('namespaces', {})
            namespaces = list(stats.keys())
        query_fn = index.query_namespaces
        query_args = {
            "vector": embedding,
            "namespaces": namespaces,
            "top_k": top_k,
            "metric": "cosine",
            "include_metadata": True
        }

    if filtro:
        query_args["filter"] = filtro

    results = query_fn(**query_args)

    for match in results.matches:
        text = match.metadata.get('text', '')
        if text:
            rag_texts.append(text)

    return rag_texts

@log_function_call
async def rag_info(payload: PostQuery) -> Tuple[str, bool]:
    
    rag_texts = retrieve_messages(
        id_descriptions=[item.model_dump() for item in payload.id_descriptions],
        user_message=payload.message
    )
                    
    agent_rag.instructions = chunck_put(rag_texts)
    
    try:
        result = await Runner.run(agent_rag, input=payload.message)
    except Exception as e:
        error_message=f"Erro: {e}"
        send_message_telegram(error_message, "RAG_INFO_AGENT")
        return error_message, False
    
    return result.final_output, True

@log_function_call
async def rag_query(payload: str) -> Tuple[str, bool]:
    
    try:
        result = await Runner.run(agent_rag_query, input=payload)
    except Exception as e:
        error_message=f"Erro: {e}"
        send_message_telegram(error_message, "RAG_QUERY_AGENT")
        return error_message, False
    
    return result.final_output, True