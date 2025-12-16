# Projet Migration MongoDB - DataSoluTech

## 📋 Contexte
Ce projet vise à migrer des données de santé depuis des fichiers CSV vers une base de données **MongoDB** conteneurisée avec **Docker**, afin d'assurer la scalabilité et la portabilité des données pour notre client.

## 🛠️ Stack Technique
* **Langage :** Python 3.9
* **Base de données :** MongoDB 5.0
* **Conteneurisation :** Docker & Docker Compose
* **Librairies :** Pandas, PyMongo

## 🚀 Comment lancer le projet

1.  **Cloner le dépôt :**
    ```bash
    git clone https://github.com/Jeremy-Huleux/_oc-data-engineer_projet-5.git
    cd projet_data_migration
    ```

2.  **Lancer la migration via Docker :**
    ```bash
    docker-compose up --build
    ```
    *Le script Python va automatiquement nettoyer les données CSV et les insérer dans MongoDB.*

3.  **Vérification :**
    * MongoDB est accessible sur `localhost:27017`.
    * Base de données : `healthcare_db`
    * Collection : `patients`

## ⚙️ Logique de Migration (ETL)
Le script `migrate.py` effectue les opérations suivantes :
1.  **Extract :** Lecture du fichier `healthcare_dataset.csv`.
2.  **Transform :**
    * Nettoyage des noms de colonnes (snake_case).
    * Standardisation des textes (Title Case) pour corriger les erreurs de saisie (ex: "bobby jackson" -> "Bobby Jackson").
    * Typage des dates.
3.  **Load :** Insertion des documents propres dans MongoDB.

## 🔒 Sécurité
*(Ici, tu peux copier la partie sur les Rôles décrite plus haut)*

## Structure d'un document patient (Collection : patients)
```JSON
{
  "_id": "ObjectId('...')",
  "name": "String (ex: 'Bobby Jackson')",
  "age": "Integer (ex: 30)",
  "gender": "String (ex: 'Male')",
  "blood_type": "String (ex: 'B-')",
  "medical_condition": "String (ex: 'Cancer')",
  "date_of_admission": "Date (YYYY-MM-DD)",
  "doctor": "String",
  "hospital": "String",
  "insurance_provider": "String",
  "billing_amount": "Double (ex: 18856.28)",
  "room_number": "Integer",
  "admission_type": "String (ex: 'Urgent')",
  "discharge_date": "Date (YYYY-MM-DD)",
  "medication": "String",
  "test_results": "String (ex: 'Normal')"
}
```