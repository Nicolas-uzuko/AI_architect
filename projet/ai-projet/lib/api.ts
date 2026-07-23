/**
 * Client API centralisé — Axios
 *
 * Architecture prête pour :
 *  - Authentification JWT (intercepteur de token)
 *  - Refresh automatique du token
 *  - Rate limiting côté client
 *  - Logging des requêtes
 */

import axios, {
  AxiosError,
  AxiosResponse,
  InternalAxiosRequestConfig,
} from "axios";
import type { AnalysisRequest, AnalysisResponse, ProjectList, ProjectDetailsResponse } from "@/types/analysis";

// ─────────────────────────── Configuration ────────────────────────────────

const BASE_URL =
  process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

/** Instance Axios principale */
const apiClient = axios.create({
  baseURL: BASE_URL,
  timeout: 60_000, // 60s — l'IA peut prendre du temps
  headers: {
    "Content-Type": "application/json",
    Accept: "application/json",
  },
  withCredentials: false, // true quand les cookies HTTP-only seront utilisés
});

// ─────────────────────────── Intercepteurs ────────────────────────────────

/**
 * Intercepteur de requête.
 *
 * TODO (Auth JWT) :
 *   const token = localStorage.getItem("access_token");
 *   if (token) config.headers.Authorization = `Bearer ${token}`;
 */
apiClient.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    // TODO: Ajouter le token JWT ici
    // const token = getAccessToken();
    // if (token) config.headers.Authorization = `Bearer ${token}`;
    return config;
  },
  (error: AxiosError) => Promise.reject(error),
);

/**
 * Intercepteur de réponse — gestion centralisée des erreurs.
 *
 * TODO (Auth JWT) :
 *   401 → rafraîchir le token et relancer la requête
 *   403 → rediriger vers /auth/login
 */
apiClient.interceptors.response.use(
  (response: AxiosResponse) => response,
  async (error: AxiosError) => {
    const status = error.response?.status;

    if (status === 401) {
      // TODO: Tenter un refresh du token JWT
      // const refreshed = await refreshAccessToken();
      // if (refreshed) return apiClient.request(error.config!);
      // window.location.href = "/auth/login";
    }

    if (status === 429) {
      console.warn("Rate limit atteint — réessayez dans quelques instants");
    }

    return Promise.reject(error);
  },
);

// ─────────────────────────── API Methods ──────────────────────────────────

/**
 * Analyse une idée de projet via l'IA.
 *
 * @param payload - L'idée de projet en texte libre
 * @returns Le rapport d'analyse complet
 * @throws AxiosError si la requête échoue
 */
export async function analyzeProject(
  payload: AnalysisRequest,
): Promise<AnalysisResponse> {
  const response = await apiClient.post<AnalysisResponse>(
    "/api/analyze",
    payload,
  );
  return response.data;
}

/**
 * Vérifie que l'API backend est opérationnelle.
 */
export async function healthCheck(): Promise<{ status: string }> {
  const response = await apiClient.get<{ status: string }>("/api/health");
  return response.data;
}

export async function listProjects(page: number = 1, pageSize: number = 20): Promise<ProjectList> {
  const response = await apiClient.get<ProjectList>(`/api/projects?page=${page}&page_size=${pageSize}`);
  return response.data;
}

export async function getProjectDetails(id: string): Promise<ProjectDetailsResponse> {
  const response = await apiClient.get<ProjectDetailsResponse>(`/api/projects/${id}`);
  return response.data;
}

export default apiClient;
