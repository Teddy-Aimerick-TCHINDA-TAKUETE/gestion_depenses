# 💰 Gestion de Finances - Projet Django + Docker + Kubernetes

Ce projet est une application web de gestion de dépenses et revenus développée avec **Django**, **MySQL**, **Docker** et **Kubernetes**. Il permet à un utilisateur de :

- Ajouter, modifier, supprimer des **dépenses** et **revenus**
- Voir la **liste des transactions**
- Visualiser des **statistiques** de ses finances
- Gérer son **compte utilisateur** (inscription, connexion, déconnexion)

---

## 🔧 Technologies utilisées

- 🐍 **Django** (framework backend)
- 🐬 **MySQL** (base de données)
- 🐳 **Docker** (virtualisation des services)
- ☸️ **Kubernetes** (orchestration des conteneurs)
- 🧰 **Docker Compose** (environnement local simplifié)

---

## 🗂️ Structure du projet

```
gestion_finances/
│
├── finances/                     # Application Django principale
│   ├── models.py          # Revenus, Dépenses, Catégories
│   ├── views.py          # Gestion des utilisateurs
│   ├── templates/           # Fichiers HTML
│   └── ...
│
├── docker-compose.yml       # Déploiement local multi-conteneurs
├── Dockerfile               # Image de l'application Django
├── requirements.txt         # Dépendances Python
├── deployment.yml                     # Fichiers de déploiement Kubernetes
├── service.yml
│
└── README.md
```

---

## ⚙️ Installation en local avec Docker

### 1. Cloner le dépôt
```bash
git clone https://github.com/Teddy-Aimerick-TCHINDA-TAKUETE/gestion_depenses.git
cd gestion_depenses
```

### 2. Lancer avec Docker Compose
```bash
docker-compose up --build
```

### 3. Accéder à l’application
> http://localhost:8000

---

## 🚀 Déploiement sur Kubernetes

1. Créer une image Docker :
```bash
docker build -t gestion-finances .
```

2. Pousser sur Docker Hub (optionnel) :
```bash
docker tag gestion-finances votre_user/gestion-finances
docker push votre_user/gestion-finances
```

3. Appliquer les fichiers de déploiement :
```bash
kubectl apply -f deployment.yml
kubectl apply -f service.yml
```

---

## 🔐 Fonctionnalités principales

| Fonction                  | Description                          |
|---------------------------|--------------------------------------|
| 🔐 Authentification       | Inscription / Connexion              |
| ➕ Ajouter une dépense     | Formulaire dédié                     |
| ✏️ Modifier une dépense    | Accessible via un bouton "Modifier"  |
| ❌ Supprimer une dépense   | Confirmation via boîte de dialogue   |
| 📊 Statistiques           | Vue récapitulative (revenus/dépenses) |
| 👤 Mon compte             | Modification des infos utilisateurs  |

---

## 🖼️ Captures d’écran

> 📌 **À insérer manuellement :**

- Page de connexion ✅
- Tableau des dépenses ✅
- Boîte de confirmation suppression (SweetAlert) ✅
- Dashboard des revenus ✅
- Exemple d’architecture Docker ou Kubernetes ✅

---

## ✅ TODO / Améliorations futures

- [ ] Export PDF ou Excel des données
- [ ] Ajouter la gestion des **catégories**
- [ ] Ajouter des notifications
- [ ] Intégrer un front Angular ou React

---

## 👨‍💻 Auteur

> Projet réalisé par **Teddy** dans le cadre d’un apprentissage DevOps avec déploiement de projet Django via Docker et Kubernetes.

---

## 📝 Licence

Ce projet est libre sous licence MIT.
