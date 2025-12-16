# 🚑 Projet Migration MongoDB - DataSoluTech

## 📋 Contexte
Ce projet a pour objectif de migrer des données de santé depuis des fichiers CSV vers une base de données **MongoDB** conteneurisée avec **Docker**, garantissant ainsi **scalabilité** et **portabilité** des données pour notre client.

---

## 🛠️ Stack Technique
- **Langage :** Python 3.9
- **Base de données :** MongoDB 5.0
- **Conteneurisation :** Docker & Docker Compose
- **Librairies :** Pandas, PyMongo

---

## 🚀 Lancer le projet

1. **Cloner le dépôt**
```bash
git clone https://github.com/Jeremy-Huleux/_oc-data-engineer_projet-5.git
```

2. **Vérification du Build et des Tests Unitaires (recommandé)**
```bash
docker-compose build --no-cache --progress=plain
```
> L'option `--no-cache` force la réexécution des tests et `--progress=plain` permet de voir les logs détaillés : `Ran 5 tests ... OK`.

3. **Lancer la migration via Docker**
```bash
docker-compose up --build
```
> Le script Python nettoie automatiquement les CSV et les insère dans MongoDB .

4. **Vérification finale**
- **URL MongoDB :** `localhost:27017`
- **Base de données :** `healthcare_db`
- **Collection :** `patients`

---

## 🔄 Logique de Migration (ETL)
Le script `migrate.py` suit le processus ETL :

1. **Extract** : Lecture du fichier `healthcare_dataset.csv`.
2. **Transform** :
   - Nettoyage des noms de colonnes (snake_case)
   - Standardisation des textes (Title Case) pour corriger les erreurs de saisie (`"bobby jackson"` → `"Bobby Jackson"`)
   - Typage des dates
3. **Load** : Insertion des documents propres dans MongoDB

---

## 🔒 Sécurité
Trois profils utilisateurs sont créés pour sécuriser `healthcare_db` :

| Utilisateur       | Rôle MongoDB   | Permissions          | Usage                                         |
|------------------|----------------|--------------------|-----------------------------------------------|
| **`admin`**       | `dbOwner`      | Lecture, Écriture, Administration | Maintenance : gestion des index, des utilisateurs et du schéma |
| **`app_backend`** | `readWrite`    | Lecture, Écriture   | Microservice ETL : migration automatique via Python |
| **`data_analyst`**| `read`         | Lecture seule       | Reporting : analyse des données sans risque de modification |

### Connexion et Vérification 🔑

**Accès Administrateur (Full Access) :**
```text
mongodb://admin_boris:securePassword123@localhost:27017/healthcare_db
```

**Accès Analyste (Lecture Seule) :**
> Testez la sécurité : essayez de supprimer un document avec ce compte, MongoDB bloquera l’opération.
```text
mongodb://data_analyst:analystPassword!@localhost:27017/healthcare_db
```

> ⚠️ Note de sécurité pour la production :  
> Dans cet environnement de démonstration, les mots de passe sont visibles dans le code. En production, utilisez AWS Secrets Manager ou des variables d’environnement injectées au runtime pour sécuriser vos identifiants.

---

## 🗂️ Structure d’un document patient (Collection : patients)
```json
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

