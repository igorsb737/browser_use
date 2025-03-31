from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from browser_use import Agent, Browser, BrowserConfig
from dotenv import load_dotenv
from pydantic import SecretStr
import asyncio
import os

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

# Configuração de API keys
openai_api_key = "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"
google_api_key = "AIzaSyDziAVXeMco5Vez2GoCHBnciph4WOUVofU"  # Chave API do Google para Gemini

async def main():
    # Inicializa o modelo LLM
    print(f"\n=== Configurando LLM: gpt-4o (Temperatura: 0.1) ===")
    
    if "gpt-4o" == "deepseek-v3" or "gpt-4o" == "deepseek-r1":
        # Usando DeepSeek API
        print("Usando DeepSeek API")
        llm = ChatOpenAI(
            base_url='https://api.deepseek.com/v1',
            model='deepseek-chat',
            api_key="sk-e0fe9106c3c14888b4322d8bf9f1b62f",
            temperature=0.1,
        )
    elif "gpt-4o" == "gemini-2.0-flash-exp" or "gpt-4o" == "gemini-2.0-exp":
        # Usando Google Gemini API
        print("Usando Google Gemini API")
        llm = ChatGoogleGenerativeAI(
            model="gpt-4o",
            temperature=0.1,
            api_key=SecretStr(google_api_key),
        )
    else:
        # Usando OpenAI API
        print("Usando OpenAI API")
        llm = ChatOpenAI(
            model="gpt-4o",
            temperature=0.1,
            api_key=openai_api_key,
        )
    
    # Configura o navegador
    browser_config = BrowserConfig(
        headless=False,
        disable_security=True,
        _force_keep_browser_alive=True,  # Força manter o navegador aberto
    )
    
    # Cria instância do navegador
    browser = Browser(config=browser_config)
    
    # Cria o agente com o modelo
    agent = Agent(
        task="""Sua tarefa é fazer um pedido para o cliente koerich. \n\no Pedido é:\n200 peças do 0201 cor: preto tamanho: P\n\nEm observação: Camisetas koerich frente e logo manga""",
        llm=llm,
        browser=browser,
        use_vision=True,
        save_conversation_path="logs/conversation",
        extend_system_message="""
# Regras Gerais
- Analise a pagina toda sempre
- Se você não encontrar algo use o scroll caso necessário



# Acesso
1. Acessar bling.com.br 
2. Fazer acesso via email igor@suncamisetas.com.br, senha Ia123456789! 
# Iniciar Pedido
3. Entrar em vendas e pedido de vendas 
4. Clicar em Incluir pedido 
# Selecionar cliente
5- Selecionar o cliente: Você vai fazer isso pesquisando o nome dele. Ao colocar as 3 primeiras letras os clientes na lista, selecione o cliente na lista dropdown. Se a lista for ,muito grande você pode colocar a 4 ou 5 letras. **OBRIGATÓRIO** selecionar o cliente na lista 
# Adicionar Itens do pedido
- Como fazer pesquisa de itens: Em Descrição você vai pesquisar o item e aguardar a lista de dropdown aparecer na tela antes de selecionar o item correto. Você deve fazer esta pesquisa usando '&' entre as palavras. 
Por exemplo: a descrição do item é '0203 PREMIUM 30.1 PENTEADO INFANTIL COR:4895 PINK;TAMANHO:12', o usuario pode te entregar somente '0203 pink tamanho 16.  Pesquise em descrição da seguinte forma '0203 & pink', ou seja, sempre pesquise o item e a cor somente. No drowpdown você vai encontrar o tamanho e restante dos detalhes. 
**IMPORTANTE** redobre a atenção ao selecionar o item levando em consideração o tamanho o item com final TAMANHO:G é diferente de TAMANHO:GG e diferente de TAMANHO: XGG, ou seja, analise corretamente o tamanho antes de escolher.
**IMPORTANTE** ao colocar em descrição você está digitando uma referencia para aparecer os itens no dropdown. Então assim que você escrever na descrição, aguarde alguns segundos para o dropdown aparecer selecione o item correto e só depois adicione a quantidade de peças. Se mesmo assim você não encontrar o item você pode apagar o que escrever e somente colocar somente o codigo do item Ex. '0203' e procurar na lista dropdown se enconta o item. 
**IMPORTANTE** na lista de dropdown de itens verifique se você está escolhendo o item no tamanho correto
Lembrando que se você quer fazer uma nova tentantiva sempre apague o que escreveu anteriormente primeiro.
6 - Em 'Descrição' escreve o item (dentro das regras acima), depois adicione a quantidade ( na coluna 'quantidade') e depois clique em "adicionar outro item" e repita o processo se houver mais itens até acabar os itens.
# Pagamento
7 - Em 'condição de pagamento' escreva e selecione dinheiro no dropdown e depois clique 'gerar parcelas'
8 -  Se tiver observações escreva ela no campo 'observações'
9 - faça uma revisão se está tudo correto
9 -  Clique em 'salvar' para finalizar
"""
    )
    
    # Cria diretório de logs se não existir
    os.makedirs("logs", exist_ok=True)
    
    # Executa o agente
    print(f"""
Iniciando agente de Uso do Navegador com a tarefa: Sua tarefa é fazer um pedido para o cliente koerich. \n\no Pedido é:\n200 peças do 0201 cor: preto tamanho: P\n\nEm observação: Camisetas koerich frente e logo manga""")
    result = await agent.run()
    
    # Imprime o resultado
    print("\n=== RESULTADO DO AGENTE ===")
    print(result)
    print("===================")
    
    # Mantendo o navegador aberto com pausa explícita
    print("\nNavegador mantido aberto. Pressione Enter para encerrar o programa...")
    
    # Aguarda entrada do usuário para manter o programa rodando e o navegador aberto
    input()
    
    print("Programa encerrado. O navegador pode ser fechado manualmente.")

if __name__ == "__main__":
    asyncio.run(main())