#!/bin/bash
# Script de configuração para o Browser Use API no Vultr
# Execute este script como root após criar uma instância no Vultr

# Atualiza o sistema
apt update && apt upgrade -y

# Instala as dependências para o Chrome
apt install -y wget gnupg2 apt-transport-https ca-certificates

# Instala o Chrome
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
apt install -y ./google-chrome-stable_current_amd64.deb

# Instala o Python e ferramentas necessárias
apt install -y python3-pip python3-venv git

# Cria um usuário para executar o serviço
useradd -m -s /bin/bash browseruse

# Muda para o diretório do usuário
cd /home/browseruse

# Clona o repositório Browser Use (substitua pelo seu repositório)
su - browseruse -c "git clone https://github.com/seu-usuario/browser-use.git"
cd /home/browseruse/browser-use

# Cria um ambiente virtual
su - browseruse -c "python3 -m venv /home/browseruse/browser_use_env"

# Instala as dependências
su - browseruse -c "source /home/browseruse/browser_use_env/bin/activate && pip install -r requirements.txt"
su - browseruse -c "source /home/browseruse/browser_use_env/bin/activate && pip install fastapi uvicorn requests"

# Cria o arquivo .env
cat > /home/browseruse/browser-use/.env << EOL
OPENAI_API_KEY=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
GOOGLE_API_KEY=AIzaSyDziAVXeMco5Vez2GoCHBnciph4WOUVofU
DEEPSEEK_API_KEY=sk-e0fe9106c3c14888b4322d8bf9f1b62f
EOL

# Ajusta as permissões
chown -R browseruse:browseruse /home/browseruse/browser-use
chmod 600 /home/browseruse/browser-use/.env

# Cria o diretório de logs
mkdir -p /home/browseruse/browser-use/logs
chown -R browseruse:browseruse /home/browseruse/browser-use/logs

# Cria o serviço systemd
cat > /etc/systemd/system/browser-use-api.service << EOL
[Unit]
Description=Browser Use API Service
After=network.target

[Service]
User=browseruse
WorkingDirectory=/home/browseruse/browser-use
ExecStart=/home/browseruse/browser_use_env/bin/python /home/browseruse/browser-use/api_server.py
Restart=always
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
EOL

# Habilita e inicia o serviço
systemctl enable browser-use-api
systemctl start browser-use-api

# Configura o firewall
apt install -y ufw
ufw allow 22/tcp  # SSH
ufw allow 8000/tcp  # API
ufw --force enable

# Instala o Nginx como proxy reverso
apt install -y nginx

# Configura o Nginx
cat > /etc/nginx/sites-available/browser-use << EOL
server {
    listen 80;
    server_name _;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOL

# Ativa o site Nginx
ln -s /etc/nginx/sites-available/browser-use /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default
nginx -t
systemctl restart nginx

echo "Configuração concluída! O Browser Use API está rodando em http://seu-ip:80"
echo "Verifique os logs com: journalctl -u browser-use-api -f"
