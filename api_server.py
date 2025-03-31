from fastapi import FastAPI, BackgroundTasks, HTTPException
from pydantic import BaseModel, HttpUrl
from typing import Optional, Dict, Any
import asyncio
import requests
import os
import logging
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from browser_use import Agent, Browser, BrowserConfig
from dotenv import load_dotenv
from pydantic import SecretStr

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='api_server.log'
)
logger = logging.getLogger("browser-use-api")

# Carrega variáveis de ambiente
load_dotenv()

# Configuração de API keys
openai_api_key = os.getenv("OPENAI_API_KEY", "")
google_api_key = os.getenv("GOOGLE_API_KEY", "")
deepseek_api_key = os.getenv("DEEPSEEK_API_KEY", "")

app = FastAPI(title="Browser Use API", description="API para automação de navegador com IA")

class BrowserUseRequest(BaseModel):
    user_prompt: str
    system_message: str
    llm_model: str = "gpt-4o"
    temperature: float = 0.1
    callback_url: HttpUrl
    headless: bool = True
    use_vision: bool = True
    api_key: Optional[str] = None
    request_id: Optional[str] = None

async def run_browser_task(request: BrowserUseRequest):
    """Executa a tarefa do Browser Use em segundo plano e envia o resultado via webhook."""
    result = {
        "success": False,
        "result": None,
        "error": None,
        "request_id": request.request_id
    }
    
    browser = None
    
    try:
        # Configura o LLM
        logger.info(f"Configurando LLM: {request.llm_model} (Temperatura: {request.temperature})")
        
        if request.llm_model == "deepseek-v3" or request.llm_model == "deepseek-r1":
            # Usando DeepSeek API
            logger.info("Usando DeepSeek API")
            llm = ChatOpenAI(
                base_url='https://api.deepseek.com/v1',
                model='deepseek-chat' if request.llm_model == "deepseek-v3" else "deepseek-coder",
                api_key=request.api_key or deepseek_api_key,
                temperature=request.temperature,
            )
        elif request.llm_model == "gemini-2.0-flash-exp" or request.llm_model == "gemini-2.0-exp":
            # Usando Google Gemini API
            logger.info("Usando Google Gemini API")
            llm = ChatGoogleGenerativeAI(
                model=request.llm_model,
                temperature=request.temperature,
                api_key=SecretStr(request.api_key or google_api_key),
            )
        else:
            # Usando OpenAI API
            logger.info("Usando OpenAI API")
            llm = ChatOpenAI(
                model=request.llm_model,
                temperature=request.temperature,
                api_key=request.api_key or openai_api_key,
            )
        
        # Configura o navegador
        browser_config = BrowserConfig(
            headless=request.headless,
            disable_security=True,
            _force_keep_browser_alive=False  # Fecha o navegador automaticamente ao terminar
        )
        
        # Cria instância do navegador
        logger.info("Iniciando navegador")
        browser = Browser(config=browser_config)
        
        # Cria o agente
        logger.info("Criando agente")
        agent = Agent(
            task=request.user_prompt,
            llm=llm,
            browser=browser,
            use_vision=request.use_vision,
            save_conversation_path="logs/conversation",
            extend_system_message=request.system_message
        )
        
        # Cria diretório de logs se não existir
        os.makedirs("logs", exist_ok=True)
        
        # Executa o agente
        logger.info(f"Iniciando tarefa: {request.user_prompt[:100]}...")
        agent_result = await agent.run()
        
        # Prepara o resultado de sucesso
        logger.info("Tarefa concluída com sucesso")
        result["success"] = True
        result["result"] = agent_result
        
    except Exception as e:
        # Captura qualquer erro e o inclui no resultado
        logger.error(f"Erro ao executar tarefa: {str(e)}")
        result["error"] = str(e)
    
    finally:
        # Fecha o navegador se estiver aberto
        if browser:
            try:
                logger.info("Fechando navegador")
                await browser.close()
            except Exception as e:
                logger.error(f"Erro ao fechar navegador: {str(e)}")
        
        # Envia o resultado para o webhook, independentemente de sucesso ou falha
        try:
            logger.info(f"Enviando resultado para webhook: {request.callback_url}")
            response = requests.post(
                url=str(request.callback_url),
                json=result,
                headers={"Content-Type": "application/json"}
            )
            logger.info(f"Resposta do webhook: {response.status_code}")
        except Exception as webhook_error:
            logger.error(f"Erro ao enviar webhook: {str(webhook_error)}")

@app.post("/run_browser_task")
async def create_browser_task(request: BrowserUseRequest, background_tasks: BackgroundTasks):
    """
    Endpoint para executar uma tarefa do Browser Use.
    
    A tarefa é executada em segundo plano e o resultado é enviado para o URL de callback.
    """
    try:
        # Valida a requisição
        if not request.user_prompt:
            raise HTTPException(status_code=400, detail="O prompt do usuário não pode estar vazio")
        
        # Registra a requisição
        logger.info(f"Nova requisição recebida. ID: {request.request_id or 'não especificado'}")
        
        # Adiciona a tarefa para execução em segundo plano
        background_tasks.add_task(run_browser_task, request)
        
        # Retorna imediatamente com confirmação
        return {
            "status": "accepted",
            "message": "Tarefa iniciada em segundo plano. Os resultados serão enviados para o webhook quando concluídos.",
            "request_id": request.request_id
        }
    
    except Exception as e:
        logger.error(f"Erro ao processar requisição: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Endpoint para verificar se a API está funcionando."""
    return {"status": "ok", "version": "1.0.0"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
