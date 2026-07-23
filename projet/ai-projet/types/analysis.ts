/**
 * Types TypeScript pour la plateforme AI Project Architect.
 * Miroir exact des schémas Pydantic du backend FastAPI.
 *
 * Extension future prévue :
 *  - AuthUser, AuthToken (JWT)
 *  - ProjectRecord (PostgreSQL)
 *  - ExportOptions (PDF)
 *  - UMLDiagram (PlantUML)
 */

// ─────────────────────────── Request ──────────────────────────────────────

/** Payload envoyé au backend pour analyser une idée de projet */
export interface AnalysisRequest {
  idea: string;
}

// ─────────────────────────── Sub-types ────────────────────────────────────

/** Cahier des charges structuré du projet */
export interface CahierDesCharges {
  description: string;
  objectifs: string[];
  utilisateurs: string[];
  fonctionnalites: string[];
  contraintes: string[];
  technologies: string[];
}

/** Données complètes retournées par l'IA */
export interface AnalysisData {
  cahier_des_charges: CahierDesCharges;
  /** Représentation ASCII/textuelle de l'architecture */
  diagramme_simple: string;
  /** Liste des issues GitHub à créer */
  taches_github: string[];
  /** Structure de fichiers du projet (arbre JSON récursif) */
  squelette_code: SkeletonNode;
}

/** Nœud de l'arbre du squelette de code (récursif) */
export type SkeletonNode = {
  [key: string]: string | SkeletonNode;
};

// ─────────────────────────── Response ─────────────────────────────────────

/** Réponse standard de l'API */
export interface AnalysisResponse {
  success: boolean;
  data: AnalysisData | null;
  error: string | null;
}

// ─────────────────────────── UI State ─────────────────────────────────────

/** État de l'analyse dans le composant React */
export type AnalysisStatus = "idle" | "loading" | "success" | "error";

export interface AnalysisState {
  status: AnalysisStatus;
  data: AnalysisData | null;
  error: string | null;
}

// ─────────────────────────── Future Types ─────────────────────────────────
// Ces types seront utilisés lors des extensions futures

/** [FUTUR] Utilisateur authentifié */
export interface AuthUser {
  id: string;
  email: string;
  name: string;
  role: "admin" | "user";
  createdAt: string;
}

/** [FUTUR] Tokens JWT */
export interface AuthTokens {
  accessToken: string;
  refreshToken: string;
  expiresIn: number;
}

/** [FUTUR] Projet sauvegardé en base de données */
export interface ProjectRead {
  id: string;
  user_id: string;
  title: string;
  idea: string;
  status: string;
  created_at: string;
  updated_at: string;
}

export interface ProjectList {
  items: ProjectRead[];
  total: number;
  page: number;
  page_size: number;
}

export interface AnalysisRead {
  id: string;
  project_id: string;
  result_json: AnalysisData;
  model_used: string;
  created_at: string;
}

export interface ProjectDetailsResponse {
  project: ProjectRead;
  latest_analysis: AnalysisRead | null;
}

/** [FUTUR] Options d'export PDF */
export interface ExportOptions {
  format: "pdf" | "docx";
  includeUML: boolean;
  includeTasks: boolean;
  includeCode: boolean;
}
