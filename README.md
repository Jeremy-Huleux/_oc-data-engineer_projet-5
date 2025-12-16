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
    cd _oc-data-engineer_projet-5
    ```

2.  **Vérification du Build et des Tests Unitaires (Recommandé) :**
    *Pour s'assurer que le code est stable avant le déploiement, nous exécutons les tests unitaires pendant la construction de l'image. Utilisez cette commande pour forcer la réexécution des tests et voir les logs en détail :*
    
    ```bash
    docker-compose build --no-cache --progress=plain
    ```

    **Pourquoi cette commande ?**
    * `--no-cache` : Force Docker à relancer les tests même si le code n'a pas changé (évite les "faux positifs").
    * `--progress=plain` : Affiche la sortie standard complète pour confirmer visuellement le message : `Ran 5 tests in ... OK`.

3.  **Lancer la migration via Docker :**
    ```bash
    docker-compose up -d
    ```
    *Le script Python va automatiquement nettoyer les données CSV et les insérer dans MongoDB.*

4.  **Vérification finale :**
    * **URL MongoDB :** `localhost:27017`
    * **Base de données :** `healthcare_db`
    * **Collection :** `patients`

## ⚙️ Logique de Migration (ETL)
Le script `migrate.py` effectue les opérations suivantes :
1.  **Extract :** Lecture du fichier `healthcare_dataset.csv`.
2.  **Transform :**
    * Nettoyage des noms de colonnes (snake_case).
    * Standardisation des textes (Title Case) pour corriger les erreurs de saisie (ex: "bobby jackson" -> "Bobby Jackson").
    * Typage des dates.
3.  **Load :** Insertion des documents propres dans MongoDB.

## 🔒 Sécurité
Trois profils utilisateurs ont été créés pour sécuriser la base `healthcare_db` :

| Utilisateur | Rôle MongoDB | Permissions | Usage |
| :--- | :--- | :--- | :--- |
| **`admin`** | `dbOwner` | Lecture, Écriture, Administration | **Maintenance.** Gestion des index, des utilisateurs et du schéma. |
| **`app_backend`** | `readWrite` | Lecture, Écriture | **Microservice ETL.** Utilisé par le script Python pour la migration automatique. |
| **`data_analyst`** | `read` | Lecture Seule | **Reporting.** Permet d'analyser les données sans risque de modification ou de suppression accidentelle. |

### Connexion et Vérification
Pour tester la sécurité via **MongoDB Compass** :

* **Accès Administrateur (Full Access) :**
    ```text
    mongodb://admin_boris:securePassword123@localhost:27017/healthcare_db
    ```

* **Accès Analyste (Lecture Seule) :**
    *Ce profil permet de vérifier la sécurité : essayez de supprimer un document avec ce compte, MongoDB bloquera l'opération.*
    ```text
    mongodb://data_analyst:analystPassword!@localhost:27017/healthcare_db
    ```

> **Note de sécurité pour la Production :**
> Dans cet environnement de démonstration, les mots de passe sont visibles dans le code. Pour un déploiement réel (AWS), nous utiliserions **AWS Secrets Manager** ou des variables d'environnement injectées au runtime pour ne jamais exposer les identifiants en clair.

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