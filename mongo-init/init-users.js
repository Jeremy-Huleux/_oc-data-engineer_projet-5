// On se place sur la bonne base de données
db = db.getSiblingDB('healthcare_db');

// 1. Création de l'Admin (Admin Boris)
db.createUser({
  user: "admin",
  pwd: "securePassword123",
  roles: [{ role: "dbOwner", db: "healthcare_db" }]
});
print("--- ✅ Utilisateur 'admin' créé.");

// 2. Création du Backend (pour le script Python)
db.createUser({
  user: "app_backend",
  pwd: "backendPassword!",
  roles: [{ role: "readWrite", db: "healthcare_db" }]
});
print("--- ✅ Utilisateur 'app_backend' créé.");

// 3. Création de l'Analyste (pour la démo)
db.createUser({
  user: "data_analyst",
  pwd: "analystPassword!",
  roles: [{ role: "read", db: "healthcare_db" }]
});
print("--- ✅ Utilisateur 'data_analyst' créé.");