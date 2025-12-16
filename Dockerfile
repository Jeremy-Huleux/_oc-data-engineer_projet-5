# On part d'une image Python légère officielle
FROM python:3.9-slim

# On définit le dossier de travail à l'intérieur du conteneur
WORKDIR /app

# On copie le fichier des dépendances
COPY requirements.txt .

# On installe les librairies nécessaires
RUN pip install --no-cache-dir -r requirements.txt

# Copie du code source ET des tests
COPY . .

# --- Etape Clé : On lance les tests automatiquement ---
# Si cette commande échoue, le build Docker s'arrêtera ici.
RUN python test_migration.py

# La commande par défaut quand le conteneur se lance
CMD ["python", "migrate.py"]