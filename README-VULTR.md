# Implantação do Browser Use API no Vultr

Este guia descreve como implantar a API do Browser Use em um servidor Vultr.

## Pré-requisitos

1. Uma conta na Vultr
2. Acesso SSH ao servidor
3. Chaves de API para os modelos de LLM que você pretende usar

## Passos para implantação

### 1. Criar uma instância no Vultr

1. Faça login na sua conta Vultr
2. Clique em "Products" > "Cloud Compute"
3. Clique em "+ Deploy Server"
4. Selecione as seguintes opções:
   - Choose Server: Cloud Compute
   - CPU & Storage Technology: Regular Performance
   - Server Location: Escolha o mais próximo de você
   - Server Image: Ubuntu 22.04 LTS x64
   - Server Size: Recomendado 2GB RAM, 1 vCPU ($12/mês)
   - Adicione sua chave SSH ou defina uma senha
   - Dê um nome ao servidor (ex: browser-use-api)
   - Clique em "Deploy Now"

### 2. Conectar ao servidor

Após a criação do servidor (pode levar alguns minutos), conecte-se via SSH:

```bash
ssh root@IP_DO_SERVIDOR
```

### 3. Preparar os arquivos

1. Faça upload dos arquivos necessários para o servidor:

```bash
# No seu computador local
scp api_server.py setup_vultr.sh browser-use-api.service root@IP_DO_SERVIDOR:/root/
```

2. Ou clone o repositório diretamente no servidor:

```bash
# No servidor
git clone https://github.com/seu-usuario/browser-use.git
cd browser-use
```

### 4. Configurar o servidor

1. Torne o script de configuração executável:

```bash
chmod +x setup_vultr.sh
```

2. Edite o script para adicionar suas chaves de API:

```bash
nano setup_vultr.sh
```

Substitua `seu_openai_api_key`, `seu_google_api_key` e `seu_deepseek_api_key` pelas suas chaves reais.

3. Execute o script de configuração:

```bash
./setup_vultr.sh
```

O script irá:
- Atualizar o sistema
- Instalar o Chrome e dependências
- Configurar o Python e ambiente virtual
- Instalar o Browser Use e dependências
- Configurar o serviço systemd
- Configurar o Nginx como proxy reverso
- Configurar o firewall

### 5. Verificar a instalação

1. Verifique se o serviço está rodando:

```bash
systemctl status browser-use-api
```

2. Verifique os logs:

```bash
journalctl -u browser-use-api -f
```

3. Teste a API:

```bash
curl http://localhost:8000/health
```

Você deve receber: `{"status":"ok","version":"1.0.0"}`

## Uso da API

A API estará disponível em `http://IP_DO_SERVIDOR/run_browser_task` e aceita requisições POST com o seguinte formato:

```json
{
  "user_prompt": "Sua tarefa é fazer um pedido para o cliente...",
  "system_message": "# Regras Gerais\n- Analise a pagina toda sempre...",
  "llm_model": "gpt-4o",
  "temperature": 0.1,
  "callback_url": "https://sua-api.com/webhook/browser-use",
  "headless": true,
  "use_vision": true,
  "request_id": "pedido-123"
}
```

O resultado será enviado para o `callback_url` quando a tarefa for concluída.

## Manutenção

### Reiniciar o serviço

```bash
systemctl restart browser-use-api
```

### Visualizar logs

```bash
journalctl -u browser-use-api -f
```

### Atualizar o código

```bash
cd /home/browseruse/browser-use
git pull
systemctl restart browser-use-api
```
