# On part d'une image Python légère officielle
FROM python:3.9-slim

# On définit le dossier de travail à l'intérieur du conteneur
WORKDIR /app

# On copie le fichier des dépendances
COPY requirements.txt .

# On installe les librairies nécessaires
RUN pip install --no-cache-dir -r requirements.txt

# On copie tout le reste du dossier (le script migrate.py) dans le conteneur
COPY . .

# La commande par défaut quand le conteneur se lance
CMD ["python", "migrate.py"]