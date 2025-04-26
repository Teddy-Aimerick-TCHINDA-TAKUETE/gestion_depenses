# Base image officielle Python
FROM python:3.11-slim

# Installer les dépendances système nécessaires pour mysqlclient
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Définition du répertoire de travail
WORKDIR /app

# Copier les dépendances
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --upgrade pip --no-cache-dir && \
    pip install -r requirements.txt --no-cache-dir

# Copier tout le code du projet Django dans le conteneur
COPY . /gestion_depenses

# Port d’exposition de Django
EXPOSE 8000

# Commande à exécuter pour démarrer le serveur Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]