#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Script gerado automaticamente pela Interface AI de Uso do Navegador
# Este arquivo é auto-executável - basta clicar duas vezes nele para executar

import os
import sys
import subprocess
import logging
import platform

# Configurando logs
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Função para criar um arquivo de log
def setup_file_logger():
    log_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "browser_agent_log.txt")
    file_handler = logging.FileHandler(log_file, mode='w')
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    logger.addHandler(file_handler)
    return log_file

# Configurar logger de arquivo
log_file = setup_file_logger()
logger.info("Iniciando script de automação do navegador")
logger.info(f"Sistema operacional: {platform.system()} {platform.release()}")

# Código principal do script
from langchain_openai import ChatOpenAI
from browser_use import Agent, Browser, BrowserConfig
from dotenv import load_dotenv
import asyncio
import os

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

# Configuração de API keys
openai_api_key = "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"

async def main():
    # Inicializa o modelo LLM
    if "gpt-4o" == "deepseek-v3" or "gpt-4o" == "deepseek-r1":
        # Usando DeepSeek API
        llm = ChatOpenAI(
            base_url='https://api.deepseek.com/v1',
            model='deepseek-chat',
            api_key="sk-e0fe9106c3c14888b4322d8bf9f1b62f",
            temperature=0.0,
        )
    else:
        # Usando OpenAI API
        llm = ChatOpenAI(
            model="gpt-4o",
            temperature=0.0,
            api_key=openai_api_key,
        )
    
    # Configura o navegador
    browser_config = BrowserConfig(
        headless=False,
        disable_security=True,
        # Usando caminho personalizado do navegador
        browser_instance_path='C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
    )
    
    # Cria instância do navegador
    browser = Browser(config=browser_config)
    
    # Cria o agente com o modelo
    agent = Agent(
        task="quero que você abra o n8n https://n8n.apoioservidoria.top/home/credentials. E reconect todas as contas credenciais google shets, docs, drive, grave os nomes pois elas mudam de posicionamento. após abrir elas. você precisa fazer o reconnect fazendo o sign in with google",
        llm=llm,
        browser=browser,
        use_vision=True,
        save_conversation_path="logs/conversation",
    )
    
    # Cria diretório de logs se não existir
    os.makedirs("logs", exist_ok=True)
    
    # Executa o agente
    print(f"\nIniciando agente de Uso do Navegador com a tarefa: quero que você abra o n8n https://n8n.apoioservidoria.top/home/credentials. E reconect todas as contas credenciais google shets, docs, drive, grave os nomes pois elas mudam de posicionamento. após abrir elas. você precisa fazer o reconnect fazendo o sign in with google")
    result = await agent.run()
    
    # Imprime o resultado
    print("\n=== RESULTADO DO AGENTE ===")
    print(result)
    print("===================")
    
    # Mantendo o navegador aberto conforme solicitado
    print("\nNavegador mantido aberto conforme solicitado.")

if __name__ == "__main__":
    asyncio.run(main())

# Código para manter a janela aberta no Windows após a execução
if platform.system() == "Windows":
    logger.info("Script concluído. Pressione Enter para sair...")
    input("Script concluído. Pressione Enter para sair...")
