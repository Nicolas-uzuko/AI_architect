"use client";

import { useState, useCallback, useRef, useEffect } from "react";
import ResultCard from "@/components/ResultCard";
import Loading from "@/components/Loading";
import { analyzeProject, listProjects, getProjectDetails } from "@/lib/api";
import type { AnalysisData, ProjectRead } from "@/types/analysis";

// ─── Types locaux ─────────────────────────────────────────────────────────────

interface ChatMessage {
  id: string;
  role: "user" | "assistant";
  content?: string;
  data?: AnalysisData;
  error?: string;
  isLoading?: boolean;
}

// ─── Suggestions d'accueil ────────────────────────────────────────────────────

const SUGGESTIONS = [
  {
    icon: "🛒",
    text: "Application de gestion de vente de chaussures en ligne",
  },
  {
    icon: "📚",
    text: "Plateforme e-learning pour développeurs avec quiz et certificats",
  },
  {
    icon: "🍕",
    text: "Système de réservation de restaurants avec menu digital",
  },
  {
    icon: "📊",
    text: "Dashboard analytique temps réel pour boutique e-commerce",
  },
];

// ─── Component ────────────────────────────────────────────────────────────────

export default function HomePage() {
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [inputValue, setInputValue] = useState("");
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [history, setHistory] = useState<ProjectRead[]>([]);
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const chatEndRef = useRef<HTMLDivElement>(null);

  const fetchHistory = useCallback(async () => {
    try {
      const data = await listProjects();
      setHistory(data.items);
    } catch (error) {
      console.error("Erreur lors du chargement de l'historique:", error);
    }
  }, []);

  // Fetch history on mount
  useEffect(() => {
    fetchHistory();
  }, [fetchHistory]);

  // Auto-resize textarea
  useEffect(() => {
    const ta = textareaRef.current;
    if (!ta) return;
    ta.style.height = "auto";
    ta.style.height = `${Math.min(ta.scrollHeight, 200)}px`;
  }, [inputValue]);

  // Scroll to bottom on new messages
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleAnalyze = useCallback(async (idea: string) => {
    if (!idea.trim() || isAnalyzing) return;

    const userMsgId = crypto.randomUUID();
    const aiMsgId = crypto.randomUUID();

    // Add user message
    setMessages((prev) => [
      ...prev,
      { id: userMsgId, role: "user", content: idea },
      { id: aiMsgId, role: "assistant", isLoading: true },
    ]);
    setInputValue("");
    setIsAnalyzing(true);

    try {
      const response = await analyzeProject({ idea });

      if (response.success && response.data) {
        setMessages((prev) =>
          prev.map((m) =>
            m.id === aiMsgId
              ? { ...m, isLoading: false, data: response.data! }
              : m,
          ),
        );
        // Refresh history after a successful analysis
        await fetchHistory();
      } else {
        setMessages((prev) =>
          prev.map((m) =>
            m.id === aiMsgId
              ? {
                  ...m,
                  isLoading: false,
                  error: response.error ?? "Erreur inconnue",
                }
              : m,
          ),
        );
      }
    } catch (err) {
      const msg =
        err instanceof Error
          ? err.message
          : "Impossible de contacter le serveur. Vérifiez que le backend FastAPI est lancé sur le port 8000.";
      setMessages((prev) =>
        prev.map((m) =>
          m.id === aiMsgId ? { ...m, isLoading: false, error: msg } : m,
        ),
      );
    } finally {
      setIsAnalyzing(false);
      setTimeout(() => textareaRef.current?.focus(), 100);
    }
  }, [isAnalyzing, fetchHistory]);

  const loadPastProject = async (id: string) => {
    setMessages([]);
    setInputValue("");
    setIsAnalyzing(true);
    
    // Set a temporary loading message
    const loadMsgId = crypto.randomUUID();
    setMessages([{ id: loadMsgId, role: "assistant", isLoading: true }]);

    try {
      const details = await getProjectDetails(id);
      
      const userMsgId = crypto.randomUUID();
      const aiMsgId = crypto.randomUUID();

      const msgs: ChatMessage[] = [
        { id: userMsgId, role: "user", content: details.project.idea }
      ];

      if (details.latest_analysis) {
        msgs.push({
          id: aiMsgId,
          role: "assistant",
          data: details.latest_analysis.result_json,
        });
      } else {
         msgs.push({
          id: aiMsgId,
          role: "assistant",
          error: "Aucune analyse trouvée pour ce projet.",
        });
      }
      setMessages(msgs);
    } catch (error) {
      setMessages([{
        id: crypto.randomUUID(),
        role: "assistant",
        error: "Erreur lors du chargement du projet."
      }]);
    } finally {
      setIsAnalyzing(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleAnalyze(inputValue);
    }
  };

  const handleNewChat = () => {
    setMessages([]);
    setInputValue("");
    textareaRef.current?.focus();
  };

  const hasMessages = messages.length > 0;

  return (
    <div className="app-shell">

      {/* ── Sidebar ── */}
      <aside className={`sidebar ${sidebarOpen ? "" : "collapsed"}`} aria-label="Navigation">
        {/* Logo */}
        <div className="sidebar-logo">
          <div className="sidebar-logo-icon">AI</div>
          <span className="sidebar-logo-text">Project Architect</span>
        </div>

        {/* New chat */}
        <button className="sidebar-new-btn" onClick={handleNewChat} aria-label="Nouvelle analyse">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" aria-hidden="true">
            <path d="M12 5v14M5 12h14" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
          </svg>
          Nouvelle analyse
        </button>

        <div className="sidebar-divider" />

        {/* History */}
        <p className="sidebar-section-label">Récents</p>
        <nav className="sidebar-history" aria-label="Historique des analyses">
          {history.length === 0 && (
             <div className="sidebar-history-item-text" style={{padding: '0.5rem 1rem', opacity: 0.5, fontSize: '0.85rem'}}>Aucun historique</div>
          )}
          {history.map((item) => (
            <div 
              key={item.id} 
              className="sidebar-history-item" 
              role="button" 
              tabIndex={0}
              onClick={() => loadPastProject(item.id)}
            >
              <span className="sidebar-history-item-icon">💬</span>
              <span className="sidebar-history-item-text">{item.title}</span>
            </div>
          ))}
        </nav>

        {/* Bottom */}
        <div className="sidebar-bottom">
          <button className="sidebar-bottom-item">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" aria-hidden="true">
              <circle cx="12" cy="12" r="3" stroke="currentColor" strokeWidth="2" />
              <path d="M12 1v4M12 19v4M4.22 4.22l2.83 2.83M16.95 16.95l2.83 2.83M1 12h4M19 12h4M4.22 19.78l2.83-2.83M16.95 7.05l2.83-2.83" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
            </svg>
            Paramètres
          </button>
        </div>
      </aside>

      {/* ── Main content ── */}
      <div className="main-content">

        {/* Topbar */}
        <header className="topbar">
          <button
            className="topbar-toggle"
            onClick={() => setSidebarOpen((v) => !v)}
            aria-label={sidebarOpen ? "Fermer la sidebar" : "Ouvrir la sidebar"}
            aria-expanded={sidebarOpen}
          >
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" aria-hidden="true">
              <line x1="3" y1="6" x2="21" y2="6" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
              <line x1="3" y1="12" x2="21" y2="12" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
              <line x1="3" y1="18" x2="21" y2="18" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
            </svg>
          </button>

          {hasMessages && (
            <span className="topbar-title">AI Project Architect</span>
          )}

          {hasMessages && (
            <button className="topbar-new-btn" onClick={handleNewChat} aria-label="Nouvelle analyse">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" aria-hidden="true">
                <path d="M12 5v14M5 12h14" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
              </svg>
              Nouveau
            </button>
          )}
        </header>

        {/* Chat scroll area */}
        <div className="chat-scroll" role="main">

          {/* Welcome screen */}
          {!hasMessages && (
            <div className="welcome-screen">
              <div className="welcome-logo" aria-hidden="true">
                <svg width="28" height="28" viewBox="0 0 24 24" fill="none">
                  <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"
                    stroke="white" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                </svg>
              </div>
              <h1 className="welcome-title">Que voulez-vous construire ?</h1>
              <p className="welcome-subtitle">
                Décrivez votre idée de projet et obtenez en quelques secondes un cahier des charges complet, une architecture et des tâches GitHub.
              </p>
              <div className="suggestions-grid" role="list" aria-label="Suggestions de projets">
                {SUGGESTIONS.map((s, i) => (
                  <div
                    key={i}
                    className="suggestion-card"
                    role="listitem"
                    tabIndex={0}
                    onClick={() => {
                      setInputValue(s.text);
                      textareaRef.current?.focus();
                    }}
                    onKeyDown={(e) => {
                      if (e.key === "Enter") {
                        setInputValue(s.text);
                        textareaRef.current?.focus();
                      }
                    }}
                    aria-label={`Suggestion : ${s.text}`}
                  >
                    <span className="suggestion-card-icon">{s.icon}</span>
                    <span className="suggestion-card-text">{s.text}</span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Chat messages */}
          {hasMessages && (
            <div className="chat-messages" aria-live="polite" aria-label="Messages">
              {messages.map((msg) => (
                <div
                  key={msg.id}
                  className={`message-row ${msg.role}`}
                >
                  {/* Avatar */}
                  <div className={`message-avatar ${msg.role === "user" ? "user" : "ai"}`} aria-hidden="true">
                    {msg.role === "user" ? "U" : "AI"}
                  </div>

                  {/* Body */}
                  <div className="message-body">
                    <p className="message-role">
                      {msg.role === "user" ? "Vous" : "AI Project Architect"}
                    </p>

                    {/* User bubble */}
                    {msg.role === "user" && (
                      <div className="user-bubble">{msg.content}</div>
                    )}

                    {/* AI: loading */}
                    {msg.role === "assistant" && msg.isLoading && (
                      <Loading />
                    )}

                    {/* AI: error */}
                    {msg.role === "assistant" && msg.error && (
                      <div className="error-inline" role="alert">
                        <svg className="error-inline-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" aria-hidden="true">
                          <circle cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="2" />
                          <line x1="15" y1="9" x2="9" y2="15" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
                          <line x1="9" y1="9" x2="15" y2="15" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
                        </svg>
                        <span className="error-inline-text">{msg.error}</span>
                      </div>
                    )}

                    {/* AI: result */}
                    {msg.role === "assistant" && msg.data && (
                      <div className="result-wrapper">
                        <div className="ai-content" style={{ marginBottom: "0.75rem" }}>
                          ✅ Voici l&apos;architecture complète de votre projet :
                        </div>
                        <ResultCard data={msg.data} />
                      </div>
                    )}
                  </div>
                </div>
              ))}
              <div ref={chatEndRef} aria-hidden="true" />
            </div>
          )}
        </div>

        {/* ── Input Bar ── */}
        <div className="input-bar-wrapper">
          <div className="input-bar" role="form" aria-label="Formulaire d'analyse">
            <textarea
              ref={textareaRef}
              className="input-bar-textarea"
              placeholder="Décrivez votre idée de projet..."
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyDown={handleKeyDown}
              disabled={isAnalyzing}
              rows={1}
              aria-label="Description du projet"
              aria-multiline="true"
            />
            <div className="input-bar-footer">
              <div className="input-bar-left">
                <button className="input-tool-btn" type="button" tabIndex={-1}>
                  <svg width="13" height="13" viewBox="0 0 24 24" fill="none" aria-hidden="true">
                    <circle cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="2" />
                    <path d="M12 8v4l3 3" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
                  </svg>
                  Groq · LLaMA 3
                </button>
              </div>
              <button
                className={`send-btn ${isAnalyzing ? "loading" : ""}`}
                onClick={() => handleAnalyze(inputValue)}
                disabled={!inputValue.trim() || isAnalyzing}
                aria-label="Analyser le projet"
                type="button"
              >
                {isAnalyzing ? (
                  <span className="send-spinner" aria-hidden="true" />
                ) : (
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" aria-hidden="true">
                    <path d="M22 2L11 13M22 2L15 22l-4-9-9-4 20-7z" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" />
                  </svg>
                )}
              </button>
            </div>
          </div>
          <p className="input-disclaimer">
            AI Project Architect peut faire des erreurs. Vérifiez les informations importantes.
          </p>
        </div>
      </div>
    </div>
  );
}
