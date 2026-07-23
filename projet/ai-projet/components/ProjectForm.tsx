"use client";

import { useState, useRef, useCallback } from "react";

interface ProjectFormProps {
  onSubmit: (idea: string) => Promise<void>;
  isLoading: boolean;
}

const PLACEHOLDER_IDEAS = [
  "Créer une application web de gestion de vente de chaussures",
  "Développer une plateforme de e-learning pour les développeurs",
  "Construire un système de réservation de restaurants en ligne",
  "Créer un tableau de bord analytique pour une boutique en ligne",
  "Développer une application mobile de suivi fitness",
];

export default function ProjectForm({ onSubmit, isLoading }: ProjectFormProps) {
  const [idea, setIdea] = useState("");
  const [focused, setFocused] = useState(false);
  const [charCount, setCharCount] = useState(0);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const MAX_CHARS = 5000;
  const MIN_CHARS = 10;

  const handleChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    const value = e.target.value;
    if (value.length <= MAX_CHARS) {
      setIdea(value);
      setCharCount(value.length);
    }
  };

  const handleSubmit = useCallback(
    async (e: React.FormEvent) => {
      e.preventDefault();
      if (idea.trim().length < MIN_CHARS || isLoading) return;
      await onSubmit(idea.trim());
    },
    [idea, isLoading, onSubmit],
  );

  const handlePlaceholderClick = (placeholder: string) => {
    setIdea(placeholder);
    setCharCount(placeholder.length);
    textareaRef.current?.focus();
  };

  const isValid = idea.trim().length >= MIN_CHARS;
  const percentage = (charCount / MAX_CHARS) * 100;
  const counterColor =
    percentage > 90
      ? "var(--color-danger)"
      : percentage > 70
        ? "var(--color-warning)"
        : "var(--color-text-muted)";

  return (
    <div className="form-container">
      {/* Header */}
      <div className="form-header">
        <div className="form-icon">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
            <path
              d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
          </svg>
        </div>
        <div>
          <h2 className="form-title">Décrivez votre idée</h2>
          <p className="form-subtitle">
            Plus vous êtes précis, meilleure sera l&apos;analyse
          </p>
        </div>
      </div>

      {/* Suggestions */}
      <div className="suggestions">
        <p className="suggestions-label">💡 Exemples rapides :</p>
        <div className="suggestions-list">
          {PLACEHOLDER_IDEAS.slice(0, 3).map((placeholder, i) => (
            <button
              key={i}
              type="button"
              className="suggestion-chip"
              onClick={() => handlePlaceholderClick(placeholder)}
              disabled={isLoading}
            >
              {placeholder}
            </button>
          ))}
        </div>
      </div>

      {/* Form */}
      <form onSubmit={handleSubmit} className="form">
        <div className={`textarea-wrapper ${focused ? "focused" : ""} ${!isValid && idea.length > 0 ? "invalid" : ""}`}>
          <textarea
            ref={textareaRef}
            id="project-idea"
            value={idea}
            onChange={handleChange}
            onFocus={() => setFocused(true)}
            onBlur={() => setFocused(false)}
            placeholder="Ex: Créer une plateforme de gestion de projets avec suivi des tâches, collaboration en équipe et rapports d'avancement automatiques..."
            className="textarea"
            rows={6}
            disabled={isLoading}
            aria-label="Description de l'idée de projet"
            aria-describedby="char-counter"
          />
          {/* Gradient overlay bottom */}
          <div className="textarea-gradient" />
        </div>

        {/* Footer du textarea */}
        <div className="textarea-footer">
          <span className="textarea-hint">
            {!isValid && idea.length > 0
              ? `Minimum ${MIN_CHARS} caractères requis`
              : "Décrivez votre projet en détail"}
          </span>
          <span
            id="char-counter"
            className="char-counter"
            style={{ color: counterColor }}
          >
            {charCount} / {MAX_CHARS}
          </span>
        </div>

        {/* Submit */}
        <button
          type="submit"
          className={`submit-btn ${isLoading ? "loading" : ""} ${!isValid ? "disabled" : ""}`}
          disabled={!isValid || isLoading}
          aria-label="Analyser le projet avec l'IA"
        >
          {isLoading ? (
            <>
              <span className="btn-spinner" aria-hidden="true" />
              Analyse en cours...
            </>
          ) : (
            <>
              <svg
                width="20"
                height="20"
                viewBox="0 0 24 24"
                fill="none"
                aria-hidden="true"
              >
                <path
                  d="M13 10V3L4 14h7v7l9-11h-7z"
                  stroke="currentColor"
                  strokeWidth="2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                />
              </svg>
              Analyser le projet
            </>
          )}
        </button>
      </form>
    </div>
  );
}
