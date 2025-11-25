# 🚀 Guide de Déploiement

Ce guide explique comment déployer l'application Mobaryat sur différentes plateformes.

## 📋 Table des Matières

1. [Déploiement Local](#déploiement-local)
2. [Déploiement sur Heroku](#déploiement-sur-heroku)
3. [Déploiement sur Railway](#déploiement-sur-railway)
4. [Déploiement sur VPS (Linux)](#déploiement-sur-vps)
5. [Déploiement avec Docker](#déploiement-avec-docker)
6. [Configuration Nginx](#configuration-nginx)

---

## 🖥️ Déploiement Local

### Windows
```bash
# Double-cliquez sur start.bat
# Ou dans le terminal:
.\start.bat
```

### Linux/Mac
```bash
chmod +x start.sh
./start.sh
```

---

## ☁️ Déploiement sur Heroku

### 1. Prérequis
- Compte Heroku: https://signup.heroku.com/
- Heroku CLI: https://devcenter.heroku.com/articles/heroku-cli

### 2. Créer un Procfile
```bash
# Procfile
web: gunicorn app:app
```

### 3. Ajouter gunicorn aux dépendances
```bash
echo "gunicorn" >> requirements.txt
```

### 4. Déployer
```bash
# Se connecter à Heroku
heroku login

# Créer une nouvelle app
heroku create mobaryat-app

# Pousser le code
git init
git add .
git commit -m "Initial commit"
git push heroku main

# Ouvrir l'app
heroku open
```

### 5. Variables d'Environnement
```bash
heroku config:set API_FOOTBALL_KEY=votre_cle
```

---

## 🚂 Déploiement sur Railway

### 1. Créer un compte
- Allez sur https://railway.app/
- Connectez-vous avec GitHub

### 2. Nouveau Projet
1. Cliquez sur "New Project"
2. Sélectionnez "Deploy from GitHub repo"
3. Choisissez votre repository
4. Railway détectera automatiquement Flask

### 3. Variables d'Environnement
1. Allez dans "Variables"
2. Ajoutez:
   - `API_FOOTBALL_KEY`: votre_cle_api
   - `PORT`: 5000

### 4. Déployer
Railway déploiera automatiquement à chaque push!

---

## 🖥️ Déploiement sur VPS (Linux)

### 1. Prérequis
```bash
# Mettre à jour le système
sudo apt update && sudo apt upgrade -y

# Installer Python et pip
sudo apt install python3 python3-pip python3-venv -y

# Installer nginx
sudo apt install nginx -y
```

### 2. Cloner le Projet
```bash
cd /var/www/
sudo git clone <votre-repo> mobaryat
cd mobaryat
```

### 3. Créer un Environnement Virtuel
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn
```

### 4. Créer un Service Systemd
```bash
sudo nano /etc/systemd/system/mobaryat.service
```

Contenu:
```ini
[Unit]
Description=Mobaryat Flask App
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/mobaryat
Environment="PATH=/var/www/mobaryat/venv/bin"
Environment="API_FOOTBALL_KEY=votre_cle"
ExecStart=/var/www/mobaryat/venv/bin/gunicorn --workers 3 --bind 127.0.0.1:5000 app:app

[Install]
WantedBy=multi-user.target
```

### 5. Démarrer le Service
```bash
sudo systemctl daemon-reload
sudo systemctl start mobaryat
sudo systemctl enable mobaryat
sudo systemctl status mobaryat
```

### 6. Configurer Nginx
```bash
sudo nano /etc/nginx/sites-available/mobaryat
```

Contenu:
```nginx
server {
    listen 80;
    server_name votre-domaine.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /var/www/mobaryat/static;
        expires 30d;
    }
}
```

Activer le site:
```bash
sudo ln -s /etc/nginx/sites-available/mobaryat /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 7. SSL avec Let's Encrypt
```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d votre-domaine.com
```

---

## 🐳 Déploiement avec Docker

### 1. Créer un Dockerfile
```dockerfile
# Dockerfile
FROM python:3.9-slim

WORKDIR /app

# Copier les fichiers
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Créer les dossiers nécessaires
RUN mkdir -p cache templates static/css static/js static/logos scrapers

# Exposer le port
EXPOSE 5000

# Variables d'environnement
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Commande de démarrage
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "3", "app:app"]
```

### 2. Créer docker-compose.yml
```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - API_FOOTBALL_KEY=${API_FOOTBALL_KEY}
    volumes:
      - ./cache:/app/cache
      - ./static:/app/static
    restart: unless-stopped
```

### 3. Créer .dockerignore
```
__pycache__
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
.git
.gitignore
.vscode
.idea
cache/*
*.log
```

### 4. Build et Run
```bash
# Build l'image
docker build -t mobaryat .

# Run avec docker-compose
docker-compose up -d

# Voir les logs
docker-compose logs -f

# Arrêter
docker-compose down
```

---

## 🔧 Configuration Nginx (Standalone)

### Configuration Complète
```nginx
# /etc/nginx/sites-available/mobaryat
server {
    listen 80;
    server_name mobaryat.com www.mobaryat.com;

    # Redirection vers HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name mobaryat.com www.mobaryat.com;

    # SSL Certificates
    ssl_certificate /etc/letsencrypt/live/mobaryat.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/mobaryat.com/privkey.pem;
    
    # SSL Configuration
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    # Logs
    access_log /var/log/nginx/mobaryat_access.log;
    error_log /var/log/nginx/mobaryat_error.log;

    # Max upload size
    client_max_body_size 10M;

    # Proxy to Flask
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    # Static files
    location /static {
        alias /var/www/mobaryat/static;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # Cache files
    location /cache {
        deny all;
    }

    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_proxied any;
    gzip_comp_level 6;
    gzip_types text/plain text/css text/xml text/javascript application/json application/javascript application/xml+rss;
}
```

---

## 🔒 Sécurité

### 1. Variables d'Environnement
Ne committez jamais les clés API! Utilisez des fichiers `.env`:

```bash
# .env
API_FOOTBALL_KEY=votre_cle_secrete
SECRET_KEY=votre_secret_flask
DEBUG=False
```

Dans `app.py`:
```python
from dotenv import load_dotenv
import os

load_dotenv()

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['DEBUG'] = os.getenv('DEBUG', 'False') == 'True'
```

### 2. Firewall
```bash
# UFW (Ubuntu)
sudo ufw allow 22
sudo ufw allow 80
sudo ufw allow 443
sudo ufw enable
```

### 3. Fail2ban
```bash
sudo apt install fail2ban -y
sudo systemctl enable fail2ban
sudo systemctl start fail2ban
```

---

## 📊 Monitoring

### 1. Logs Applicatifs
```python
# Dans app.py
import logging
from logging.handlers import RotatingFileHandler

handler = RotatingFileHandler('app.log', maxBytes=10000000, backupCount=3)
handler.setLevel(logging.INFO)
app.logger.addHandler(handler)
```

### 2. Supervisor (Process Manager)
```bash
sudo apt install supervisor -y

# /etc/supervisor/conf.d/mobaryat.conf
[program:mobaryat]
command=/var/www/mobaryat/venv/bin/gunicorn --workers 3 --bind 127.0.0.1:5000 app:app
directory=/var/www/mobaryat
user=www-data
autostart=true
autorestart=true
stderr_logfile=/var/log/mobaryat/err.log
stdout_logfile=/var/log/mobaryat/out.log
```

---

## 🔄 Mise à Jour

### Mise à jour manuelle
```bash
cd /var/www/mobaryat
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart mobaryat
```

### Script de mise à jour automatique
```bash
# update.sh
#!/bin/bash
cd /var/www/mobaryat
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart mobaryat
echo "Mise à jour terminée!"
```

---

## 📞 Support

Pour plus d'aide:
- GitHub Issues
- Documentation Flask
- Documentation Nginx
- Community Forums

Bon déploiement! 🚀
