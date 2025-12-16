import pandas as pd
from pymongo import MongoClient
import os
import sys

#Configuration
# On utilise une variable d'environnement pour l'url, avec une valeur par default
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = "healthcare_db"
COLLECTION_NAME = "patients"
CSV_FILE = "healthcare_dataset.csv"

def run_migration() :
  print("--- 🚀 Démarrage de la migration...")
  
  # Étape 1 : extraction
  if not os.path.exists(CSV_FILE):
    print(f"--- ❌ ERREUR : Le fichier {CSV_FILE} est introuvable.")
    sys.exit(1)
    
  print(f"--- 📥 Lecture du fichier CSV : {CSV_FILE}")
  try:
    df = pd.read_csv(CSV_FILE, parse_dates=["Date of Admission", "Discharge Date"])
    print(f"      -> {len(df)} lignes chargées.")
  except Exception as e:
    print(f"--- ❌ Erreur lors de la lecture du CSV : {e}")
    sys.exit(1)
    
  # Étape 2 : transformation
  print("--- ⚙️  Nettoyage et standardisation des données...")
  
    #1 : standardisation des colonnes en snake_case
  df.columns = [c.lower().replace(" ", "_") for c in df.columns]
                  #Compréhension de la liste
    #2 : nettoyage des textes en title
  text_cols = ['name', 'gender', 'medical_condition', 'doctor', 'hospital', 'insurance_provider', 'admission_type', 'medication']
  for col in text_cols :
    if col in df.columns :
                        #String : mets en Titre 
      df[col] = df[col].str.title().str.strip() # .strip() enlève les espaces inutiles au début/fin
      
  # Étape 3 : chargement
  print(f"--- 🔌 Connexion à MongoDB ({MONGO_URI})...")
  try:
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]
    
    #verification de la connexion
    client.server_info()
    print(f"        --> Connexion réussie.")
  except Exception as e:
    print(f"❌ Impossible de se connecter à MongoDB : {e}")
    sys.exit(1)
    
  # On vide la collection avant d'importer pour éviter les doublons lors des tests
  deleted = collection.delete_many({})
  print(f"--- 🧹 Nettoyage pré-migration : {deleted.deleted_count} anciens documents supprimés.")
  
  # Conversion du Dataframe en dictionnaire pour MongoDB
  data_dict = df.to_dict("records")
  
  print(f"--- 📤 Insertion de {len(data_dict)} documents dans la base '{DB_NAME}', collection '{COLLECTION_NAME}'...")
  try:
    result = collection.insert_many(data_dict)
    print(f"  --- ✅ Succès ! {len(result.inserted_ids)} documents insérés.")
  except Exception as e:
    print(f"--- ❌ Erreur lors de l'insertion : {e}")
  
  # Vérification final (Test d'intégrité)
  count_in_db = collection.count_documents({})
  if count_in_db == len(df):
    print("--- ✨ Vérification d'intégrité : OK (Nombre de documents correspond).")
  else:
    print(f"--- ⚠️ Attention : {len(df)} lignes CSV vs {count_in_db} documents en base.")
    
if __name__ == "__main__":
  run_migration()