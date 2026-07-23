# 🏗️ AI Project Architect

**AI Project Architect** est une application SaaS qui permet aux développeurs, entrepreneurs et chefs de projet de transformer une simple idée en texte libre en un cahier des charges structuré et une architecture logicielle complète en quelques secondes, grâce à l'Intelligence Artificielle (Groq / LLaMA 3).

---

## ✨ Fonctionnalités

- **Génération par IA** : Saisissez une idée (ex: "Une plateforme e-learning") et obtenez une analyse complète.
- **Cahier des charges structuré** : Objectifs, utilisateurs cibles, fonctionnalités clés, contraintes techniques.
- **Architecture & Squelette de code** : Génération d'un arbre de fichiers complet et d'un diagramme d'architecture conceptuel.
- **Tâches GitHub** : Liste prête à l'emploi d'issues/tâches pour démarrer le développement.
- **Historique Persistant** : Sauvegarde automatique de vos analyses en base de données PostgreSQL pour pouvoir les consulter plus tard.

---

## 🛠️ Stack Technique

### Frontend
- **Framework** : [Next.js 15](https://nextjs.org/) (App Router, React 19)
- **Langage** : TypeScript
- **Style** : CSS Vanilla moderne (Design System sur-mesure, UI responsive, Dark Mode natif)

### Backend
- **Framework** : [FastAPI](https://fastapi.tiangolo.com/) (Python 3.13)
- **Base de données** : PostgreSQL 
- **ORM** : SQLAlchemy 2.x (Asynchrone) + Alembic pour les migrations
- **Validation** : Pydantic v2
- **IA** : API Groq (Modèle LLaMA 3.3 70B)

---

## 🚀 Installation & Démarrage local

### Prérequis
- [Node.js](https://nodejs.org/) (v18+)
- [Python](https://www.python.org/) (v3.10+)
- [PostgreSQL](https://www.postgresql.org/) (v14+) en cours d'exécution.

---

### 1. Backend (FastAPI)

1. **Aller dans le dossier backend :**
   ```bash
   cd Back-FastAPI
   ```

2. **Créer et activer un environnement virtuel (recommandé) :**
   ```bash
   python -m venv .venv
   # Windows :
   .venv\Scripts\activate
   # Mac/Linux :
   source .venv/bin/activate
   ```

3. **Installer les dépendances :**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurer l'environnement :**
   Copiez le fichier `.env.example` (ou modifiez le fichier `.env` existant) pour y ajouter vos identifiants PostgreSQL et votre clé API Groq :
   ```env
   DATABASE_URL=postgresql+psycopg://utilisateur:motdepasse@localhost:5432/ai_project_architect
   GROQ_API_KEY=votre_cle_api_groq
   ```

5. **Préparer la base de données :**
   Assurez-vous que la base de données `ai_project_architect` existe dans PostgreSQL, puis appliquez les migrations :
   ```bash
   alembic upgrade head
   ```

6. **Lancer le serveur :**
   ```bash
   uvicorn app.main:app --reload
   ```
   > L'API sera accessible sur [http://localhost:8000](http://localhost:8000). La documentation Swagger est disponible sur [http://localhost:8000/docs](http://localhost:8000/docs).

---

### 2. Frontend (Next.js)

1. **Aller dans le dossier frontend :**
   ```bash
   cd ai-projet
   ```

2. **Installer les dépendances :**
   ```bash
   npm install
   ```

3. **Configurer l'environnement (Optionnel) :**
   Créez un fichier `.env.local` si vous souhaitez changer l'URL de l'API :
   ```env
   NEXT_PUBLIC_API_URL=http://localhost:8000
   ```

4. **Lancer le serveur de développement :**
   ```bash
   npm run dev
   ```
   > L'application frontend sera accessible sur [http://localhost:3000](http://localhost:3000).

---

## 📁 Structure du projet

```
projet/
├── ai-projet/                 # 💻 FRONTEND (Next.js)
│   ├── app/                   # App router (pages, layout, styles)
│   ├── components/            # Composants React réutilisables (ResultCard, Loading...)
│   ├── lib/                   # Utilitaires (client API Axios)
│   └── types/                 # Interfaces TypeScript
│
└── Back-FastAPI/              # ⚙️ BACKEND (FastAPI)
    ├── alembic/               # Migrations de base de données
    ├── app/
    │   ├── core/              # Configuration & Dépendances
    │   ├── models/            # Modèles SQLAlchemy (User, Project, Analysis)
    │   ├── repositories/      # Logique d'accès aux données (DB I/O)
    │   ├── routers/           # Endpoints de l'API (Routes)
    │   ├── schemas/           # Schémas Pydantic (Validation)
    │   └── services/          # Logique métier et Appels IA
    ├── requirements.txt       # Dépendances Python
    └── .env                   # Variables d'environnement
```

---

## 🤝 Contribution
Toute contribution est la bienvenue ! N'hésitez pas à ouvrir une *issue* ou soumettre une *Pull Request*.
