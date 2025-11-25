import os
import tempfile
from urllib.parse import unquote, urlparse
import aioboto3
import aiofiles
from aiohttp import ClientError
import aiohttp
from openai import OpenAI
from configurations.config import Config

async def download_file(url: str) -> tuple[str, str]:
    tmpdir = tempfile.mkdtemp()
    file = url.split('/')
    file_path = os.path.join(tmpdir, unquote(file[len(file)-1]))
    chunk_size = 64 * 1024
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response.raise_for_status()
                async with aiofiles.open(file_path, 'wb') as out_file:
                    async for chunk in response.content.iter_chunked(chunk_size):
                        await out_file.write(chunk)    
        return file_path, tmpdir
    except Exception as e:
        print(f"Error: {e}")
        error_message = f"Error downloading arquivo: {e}"
        return error_message, tmpdir

async def pre_signed_url(url: str) -> str:
    file = url.split('/')
    filename = unquote(file[len(file)-1])

    parsed = urlparse(url)
    if parsed.scheme == "s3":
        bucket_name = parsed.netloc
    else:
        bucket_name = parsed.netloc.split(".")[0]

    session = aioboto3.Session(
        aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY
    )
    
    key_filename = "/".join(url.split("/")[3:])

    async with session.client("s3", region_name=Config.AWS_REGION) as s3_client:
        try:
            file_path = await s3_client.generate_presigned_url(
                "get_object",
                Params={"Bucket": bucket_name, "Key": key_filename},
                ExpiresIn=600,
            )
        
        except Exception as e:
            print(f"Error : {e}")
        
        except ClientError as e:
            code = e.response["Error"]["Code"]
            if code == "NoSuchKey":
                raise FileNotFoundError(f"O objeto '{filename}' não existe no bucket '{bucket_name}'")
            else:
                raise

    return file_path

instructions="""
        <xml-guide version="1.0" lang="pt-BR">
            <analiseImagemMedica>
                <contexto>
                    <papel>Você é um especialista altamente experiente em análise de imagens médicas (radiografias/raio-X, tomografias, ressonâncias, ultrassonografias e afins).</papel>
                    <escopo>Fornecer análise objetiva, minuciosa e fundamentada exclusivamente a partir da(s) imagem(ns) recebida(s), respeitando limites éticos.</escopo>
                </contexto>

                <objetivo>
                    <item>Analisar a(s) imagem(ns) de forma detalhada e técnica.</item>
                    <item>Extrair achados relevantes que apoiem hipóteses diagnósticas, sem concluir além do que a evidência permitir.</item>
                    <item>Garantir clareza, precisão e consistência.</item>
                </objetivo>

                <conteudoDaAnalise>
                    <fontesConfiaveis>Basear-se somente em diretrizes e literatura confiáveis (ex.: órgãos oficiais de saúde, artigos revisados por pares, sociedades médicas).</fontesConfiaveis>

                    <qualidadeDaImagem>
                    <item>Indicar se a imagem é diagnóstica ou limitada (posicionamento, artefatos, contraste, campo de visão, ruído).</item>
                    <item>Se a qualidade limitar conclusões, declarar explicitamente e sugerir exames/novas aquisições quando cabível.</item>
                    </qualidadeDaImagem>

                    <achados>
                    <item>Descrever achados objetivos (localização anatômica, lateridade, dimensões/medidas, densidade/sinal, margens, número, distribuição, comparação com estudos prévios se informados).</item>
                    <item>Usar terminologia técnica padronizada quando possível.</item>
                    </achados>

                    <interpretacao>
                    <item>Apresentar leitura clínica dos achados compatível com a imagem, mantendo incertezas explícitas.</item>
                    <item>Se a imagem não for suficiente para diagnóstico completo, indicar necessidades de exames complementares.</item>
                    </interpretacao>

                    <referencias>
                    <item>Citar no texto apenas referências essenciais (ex.: diretriz/ano) quando forem usadas para embasar explicações.</item>
                    </referencias>
                </conteudoDaAnalise>

                <naoFazer>
                    <item>Não incluir informações que não estejam presentes na imagem.</item>
                    <item>Não inventar achados, diagnósticos ou sintomas não evidentes.</item>
                    <item>Não especular além do que a evidência da imagem permite.</item>
                    <item>Não extrapolar para condutas terapêuticas ou prognósticos definitivos.</item>
                    <item>Não retornar nada fora do formato JSON definido em <retornoJSON>.</item>
                </naoFazer>

                <retornoJSON>
                    <schema>
                    {
                        "result": "Resumo técnico e objetivo dos achados visíveis na imagem.",
                        "explanation": "Explicação detalhada e fundamentada sobre como os achados foram identificados, com base em referências médicas confiáveis (citações curtas, ex.: Diretriz/ano)."
                    }
                    </schema>
                    <regras>
                    <item>Escrever em português, termos técnicos claros.</item>
                    <item>Não usar markdown, listas com marcadores ou campos extras no JSON.</item>
                    <item>Se houver limitações da imagem, mencioná-las em "result" e detalhá-las em "explanation".</item>
                    <item>Se forem sugeridos exames complementares, justificar brevemente em "explanation".</item>
                    <item>Quando houver múltiplas possibilidades, descrever no "result" como hipóteses diferenciais, indicando nível de confiança relativo (alto/médio/baixo) sem criar novos campos.</item>
                    </regras>
                </retornoJSON>

                <resumoFinal>
                    <pontosChave>
                    <item>Seguir rigorosamente o bloco &lt;naoFazer&gt;.</item>
                    <item>Manter objetividade, clareza e consistência terminológica.</item>
                    <item>Explicar o raciocínio técnico de forma rastreável (o que na imagem leva a cada achado).</item>
                    <item>Retornar exclusivamente no formato JSON definido.</item>
                    </pontosChave>
                </resumoFinal>
            </analiseImagemMedica>
        </xml-guide>
            """,

async def analyze_image_url(url: str, prompt: str):
    url_path = url
    
    if url.find('s3'):
        url_path = await pre_signed_url(url)
    else:
        url_path, _ = await download_file(url)
    
    try:
        resp = OpenAI().responses.create(
            model = "gpt-5-2025-08-07",
            instructions=str(instructions),
            input = [
                {
                    "role": "user",
                        "content": [
                        {
                            "type": "input_text", 
                            "text": "Analise esta imagem conforme as instruções."
                        },
                        {
                            "type": "input_image",
                            "image_url": url_path
                        }
                    ]
                }
            ],
        )
        
        text = resp.output_text
        
    except Exception as e:
        error_message = f"Error : {e}"
        return error_message
    
    return text