import pandas as pd
from pymongo import MongoClient
import os
import sys

# --- CONFIGURATION ---
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = "healthcare_db"
COLLECTION_NAME = "patients"
CSV_FILE = "healthcare_dataset.csv"

# --- FONCTIONS (ENCAPSULATION) ---

def load_data(filepath):
    """Extraction : Lit le fichier CSV."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Le fichier {filepath} est introuvable.")
    try:
        # On lit tout en string d'abord pour éviter les erreurs de parsing auto, on typera après
        df = pd.read_csv(filepath)
        return df
    except Exception as e:
        raise Exception(f"Erreur lecture CSV : {e}")

def transform_data(df):
    """Transformation : Nettoyage et Standardisation."""
    # 1. Copie pour éviter les warnings
    df_clean = df.copy()

    # 2. Standardisation des colonnes (Snake case)
    df_clean.columns = [c.lower().replace(' ', '_') for c in df_clean.columns]
                          # Compréhension de la liste (Fait lower + replace pour chaque colonne des colonnes de df_clean)
    # 3. Nettoyage des textes (Title Case + Strip)
    # On determine les colonnes à nettoyer dans une liste
    text_cols = ['name', 'gender', 'medical_condition', 'doctor', 'hospital', 'insurance_provider', 'admission_type', 'medication']
    for col in text_cols:
        if col in df_clean.columns:
                                                          # On met en Title Case
            df_clean[col] = df_clean[col].astype(str).str.title().str.strip()
                                                                              # Strip permet de retirer les espaces inutiles au debut et à la fin
    # 4. Gestion des Dates
    date_cols = ['date_of_admission', 'discharge_date']
    for col in date_cols:
        if col in df_clean.columns:
            df_clean[col] = pd.to_datetime(df_clean[col], errors='coerce')

    # 5. Gestion des doublons (Suppression des lignes 100% identiques)
    df_clean = df_clean.drop_duplicates()
    
    return df_clean

def load_to_mongo(df, uri, db_name, col_name):
    """Chargement : Envoi vers MongoDB."""
    client = MongoClient(uri)
    db = client[db_name]
    collection = db[col_name]
    
    ## /!\ ---- Important à supprimer en prod ---- /!\ 
    # Reset pour éviter les doublons en dev
    collection.delete_many({})
    ## /!\ ---- Important à supprimer en prod ---- /!\ 
    
    data_dict = df.to_dict("records")
    if data_dict:
        collection.insert_many(data_dict)
        return len(data_dict)
    return 0

# --- EXÉCUTION PRINCIPALE ---
def main():
    print("--- 🚀 Démarrage du microservice ETL...")
    try:
        # Etape 1 : Extract
        df_raw = load_data(CSV_FILE)
        print(f"  --- 📥 Données brutes chargées : {len(df_raw)} lignes.")

        # Etape 2 : Transform
        df_clean = transform_data(df_raw)
        print(f"  --- ⚙️ Données transformées : {len(df_clean)} lignes.")

        # Etape 3 : Load
        count = load_to_mongo(df_clean, MONGO_URI, DB_NAME, COLLECTION_NAME)
        print(f"  --- ✅ Succès ! {count} documents insérés dans MongoDB.")

    except Exception as e:
        print(f"--- ❌ Erreur critique : {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()