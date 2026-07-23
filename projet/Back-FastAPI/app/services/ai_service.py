"""
Service IA — Analyse de projet.

Actuellement : fonction mock qui retourne des données réalistes.
Pour intégrer Groq plus tard, remplacer le corps de `analyze_project`
par un appel réel à l'API Groq (voir commentaires TODO ci-dessous).

Extension future prévue :
    - Groq API (LLaMA 3)
    - Génération UML (PlantUML / Mermaid)
    - Export PDF (WeasyPrint / ReportLab)
"""

import json
import os
import textwrap
from app.schemas.analysis_schema import AnalysisData, CahierDesCharges


# ──────────────────────────── Mock Data ──────────────────────────────────────

def _build_mock_response(idea: str) -> dict:
    """
    Construit une réponse mock réaliste basée sur l'idée fournie.
    Remplacer cette fonction par un appel à Groq en production.
    """
    idea_lower = idea.lower()

    # Détection générique du domaine pour personnaliser la mock
    domain_keywords = {
        "chaussure": ("vente", "e-commerce"),
        "santé": ("médical", "healthcare"),
        "restaurant": ("restauration", "food"),
        "école": ("éducation", "edtech"),
        "livre": ("bibliothèque", "reading"),
    }
    domain = "application"
    for kw, (d, _) in domain_keywords.items():
        if kw in idea_lower:
            domain = d
            break

    return {
        "cahier_des_charges": {
            "description": (
                f"Plateforme web complète pour {idea.strip()}. "
                "Solution moderne, scalable et sécurisée répondant aux besoins "
                "des utilisateurs et des gestionnaires."
            ),
            "objectifs": [
                f"Développer une interface utilisateur intuitive pour {domain}",
                "Garantir une expérience utilisateur fluide sur tous les appareils",
                "Assurer la scalabilité et la performance de la plateforme",
                "Mettre en place un système de gestion des données fiable",
                "Fournir des tableaux de bord analytiques en temps réel",
            ],
            "utilisateurs": [
                "Administrateur système — gestion globale de la plateforme",
                "Utilisateur final — consommation des services",
                "Manager — supervision et rapports",
                "Visiteur — consultation sans authentification",
            ],
            "fonctionnalites": [
                "Authentification et gestion des rôles (JWT + OAuth2)",
                "Tableau de bord avec KPIs et graphiques dynamiques",
                "Gestion CRUD complète des entités principales",
                "Moteur de recherche et filtres avancés",
                "Système de notifications en temps réel (WebSocket)",
                "Export des données (PDF, Excel, CSV)",
                "API RESTful documentée (Swagger / OpenAPI)",
                "Gestion des médias et fichiers (upload, preview)",
                "Historique des actions (audit log)",
                "Mode sombre / clair (Dark Mode)",
            ],
            "contraintes": [
                "Conformité RGPD pour la gestion des données personnelles",
                "Temps de réponse API < 200ms pour les opérations courantes",
                "Disponibilité 99.9% (SLA production)",
                "Support multi-navigateurs (Chrome, Firefox, Safari, Edge)",
                "Design responsive mobile-first",
                "Couverture de tests unitaires ≥ 80%",
                "Déploiement via Docker + CI/CD (GitHub Actions)",
            ],
            "technologies": [
                "Frontend: Next.js 14 + TypeScript + Tailwind CSS",
                "Backend: FastAPI + Python 3.11",
                "Base de données: PostgreSQL + Redis (cache)",
                "ORM: SQLAlchemy + Alembic (migrations)",
                "Auth: JWT + OAuth2 (Google, GitHub)",
                "Tests: Pytest (backend) + Vitest (frontend)",
                "DevOps: Docker, Docker Compose, GitHub Actions",
                "Cloud: Vercel (frontend) + Railway/Render (backend)",
                "IA: Groq API (LLaMA 3.3 70B)",
            ],
        },
        "diagramme_simple": textwrap.dedent("""
            ┌─────────────────────────────────────────────────────────┐
            │                    ARCHITECTURE                          │
            └─────────────────────────────────────────────────────────┘

            ┌──────────────┐     HTTPS      ┌──────────────────────┐
            │   Browser    │ ─────────────► │  Next.js Frontend    │
            │  (Client)    │ ◄───────────── │  (Vercel CDN)        │
            └──────────────┘                └──────────┬───────────┘
                                                       │ REST API
                                                       ▼
            ┌──────────────────────────────────────────────────────┐
            │                  FastAPI Backend                      │
            │   ┌────────────┐  ┌──────────┐  ┌────────────────┐  │
            │   │  /api/auth │  │/api/data │  │ /api/analyze   │  │
            │   └────────────┘  └────┬─────┘  └───────┬────────┘  │
            │                        │                  │           │
            │              ┌─────────▼──────┐  ┌───────▼───────┐  │
            │              │  PostgreSQL DB  │  │   Groq API    │  │
            │              │  (Data Store)  │  │  (LLaMA 3)    │  │
            │              └────────────────┘  └───────────────┘  │
            └──────────────────────────────────────────────────────┘
        """).strip(),
        "taches_github": [
            "feat: Initialisation du projet Next.js + configuration Tailwind",
            "feat: Mise en place de la structure FastAPI avec routeurs modulaires",
            "feat: Création des schémas Pydantic pour toutes les entités",
            "feat: Intégration de l'API Groq pour l'analyse de projet",
            "feat: Développement du composant ProjectForm avec validation",
            "feat: Développement du composant ResultCard avec onglets",
            "feat: Implémentation du système d'authentification JWT",
            "feat: Connexion PostgreSQL avec SQLAlchemy + Alembic",
            "feat: Tableau de bord avec graphiques (Recharts/Chart.js)",
            "feat: Système de notifications WebSocket temps réel",
            "feat: Export PDF des résultats d'analyse (WeasyPrint)",
            "feat: Génération de diagrammes UML (Mermaid / PlantUML)",
            "feat: Tests unitaires backend (Pytest) — couverture 80%",
            "feat: Tests E2E frontend (Playwright/Cypress)",
            "chore: Configuration Docker + docker-compose.yml",
            "chore: Pipeline CI/CD GitHub Actions (test + deploy)",
            "docs: Documentation API Swagger complète",
            "docs: Guide de déploiement production (README)",
        ],
        "squelette_code": {
            "backend/": {
                "app/": {
                    "main.py": "# Point d'entrée FastAPI",
                    "routers/": {
                        "analysis.py": "# Route POST /api/analyze",
                        "auth.py": "# Route POST /api/auth/login | register [FUTUR]",
                        "projects.py": "# Routes CRUD /api/projects [FUTUR]",
                    },
                    "services/": {
                        "ai_service.py": "# Service Groq IA",
                        "auth_service.py": "# Service JWT [FUTUR]",
                        "pdf_service.py": "# Service export PDF [FUTUR]",
                        "uml_service.py": "# Service génération UML [FUTUR]",
                    },
                    "schemas/": {
                        "analysis_schema.py": "# Modèles Pydantic analyse",
                        "auth_schema.py": "# Modèles Pydantic auth [FUTUR]",
                        "project_schema.py": "# Modèles Pydantic projets [FUTUR]",
                    },
                    "models/": {
                        "user.py": "# Modèle SQLAlchemy User [FUTUR]",
                        "project.py": "# Modèle SQLAlchemy Project [FUTUR]",
                    },
                    "database/": {
                        "connection.py": "# Connexion PostgreSQL [FUTUR]",
                        "migrations/": "# Alembic migrations [FUTUR]",
                    },
                    "core/": {
                        "config.py": "# Variables d'environnement",
                        "security.py": "# Helpers JWT [FUTUR]",
                        "exceptions.py": "# Gestionnaire d'erreurs global",
                    },
                },
                "requirements.txt": "# Dépendances Python",
                "Dockerfile": "# Image Docker backend",
                ".env.example": "# Variables d'env",
            },
            "frontend/": {
                "app/": {
                    "page.tsx": "# Page principale",
                    "layout.tsx": "# Layout global",
                    "globals.css": "# Styles globaux",
                    "dashboard/page.tsx": "# Dashboard [FUTUR]",
                    "projects/page.tsx": "# Liste projets [FUTUR]",
                    "auth/login/page.tsx": "# Login [FUTUR]",
                },
                "components/": {
                    "ProjectForm.tsx": "# Formulaire analyse",
                    "ResultCard.tsx": "# Affichage résultats",
                    "Loading.tsx": "# Loader animé",
                    "Navbar.tsx": "# Navigation [FUTUR]",
                    "Sidebar.tsx": "# Sidebar dashboard [FUTUR]",
                },
                "lib/": {
                    "api.ts": "# Client Axios",
                    "auth.ts": "# Helpers auth [FUTUR]",
                    "utils.ts": "# Utilitaires",
                },
                "types/": {
                    "analysis.ts": "# Types TypeScript",
                    "auth.ts": "# Types auth [FUTUR]",
                },
            },
        },
    }


# ──────────────────────── Public Interface ───────────────────────────────────

def analyze_project(idea: str) -> AnalysisData:
    """
    Analyse une idée de projet et retourne un rapport structuré.

    Actuellement mock — pour intégrer Groq :
    ---------------------------------------
    TODO:
        1. Installer : pip install groq
        2. Ajouter GROQ_API_KEY dans .env
        3. Remplacer le corps par :

            from groq import Groq

            client = Groq(api_key=os.environ["GROQ_API_KEY"])
            prompt = _build_groq_prompt(idea)

            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"},
                temperature=0.7,
            )
            raw = json.loads(completion.choices[0].message.content)
            return AnalysisData(**raw)

    Args:
        idea: Description textuelle de l'idée de projet.

    Returns:
        AnalysisData: Rapport d'analyse complet validé par Pydantic.
    """
    raw = _build_mock_response(idea)
    return AnalysisData(**raw)


def _build_groq_prompt(idea: str) -> str:
    """
    Construit le prompt pour l'API Groq.
    Prêt à l'emploi dès l'intégration de la vraie API.
    """
    return f"""
Tu es un architecte logiciel expert. Analyse l'idée de projet suivante et retourne
un JSON structuré avec les champs exacts ci-dessous. Ne retourne QUE le JSON, sans markdown.

Idée du projet : {idea}

Format JSON requis :
{{
  "cahier_des_charges": {{
    "description": "string",
    "objectifs": ["string"],
    "utilisateurs": ["string"],
    "fonctionnalites": ["string"],
    "contraintes": ["string"],
    "technologies": ["string"]
  }},
  "diagramme_simple": "string (ASCII art ou texte structuré)",
  "taches_github": ["string (format: feat/fix/chore: description)"],
  "squelette_code": {{}}
}}

Réponds UNIQUEMENT avec le JSON valide.
""".strip()
