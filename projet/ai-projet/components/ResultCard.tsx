"use client";

import { useState } from "react";
import type { AnalysisData, SkeletonNode } from "@/types/analysis";

interface ResultCardProps {
  data: AnalysisData;
}

type Tab = "cahier" | "diagramme" | "taches" | "squelette";

const TABS: { id: Tab; label: string; icon: string }[] = [
  { id: "cahier", label: "Cahier des charges", icon: "📋" },
  { id: "diagramme", label: "Architecture", icon: "🏗️" },
  { id: "taches", label: "Tâches GitHub", icon: "✅" },
  { id: "squelette", label: "Squelette code", icon: "🗂️" },
];

// ─── Sub-components ──────────────────────────────────────────────────────

function Badge({ text, variant = "default" }: { text: string; variant?: "default" | "tech" | "constraint" }) {
  return <span className={`badge badge-${variant}`}>{text}</span>;
}

function SectionBlock({
  title,
  icon,
  items,
  variant,
}: {
  title: string;
  icon: string;
  items: string[];
  variant?: "default" | "tech" | "constraint";
}) {
  return (
    <div className="section-block">
      <h3 className="section-block-title">
        <span>{icon}</span> {title}
      </h3>
      <div className="badges-list">
        {items.map((item, i) => (
          <Badge key={i} text={item} variant={variant} />
        ))}
      </div>
    </div>
  );
}

function SkeletonTree({
  node,
  depth = 0,
}: {
  node: SkeletonNode;
  depth?: number;
}) {
  return (
    <ul className="skeleton-tree" style={{ paddingLeft: depth === 0 ? 0 : "1.25rem" }}>
      {Object.entries(node).map(([key, value]) => (
        <li key={key} className="skeleton-item">
          {typeof value === "string" ? (
            <span className="skeleton-file">
              <span className="skeleton-file-icon">📄</span>
              <span className="skeleton-file-name">{key}</span>
              <span className="skeleton-file-comment">{value}</span>
            </span>
          ) : (
            <>
              <span className="skeleton-dir">
                <span className="skeleton-dir-icon">📁</span>
                <span className="skeleton-dir-name">{key}</span>
              </span>
              <SkeletonTree node={value as SkeletonNode} depth={depth + 1} />
            </>
          )}
        </li>
      ))}
    </ul>
  );
}

function CopyButton({ text }: { text: string }) {
  const [copied, setCopied] = useState(false);

  const handleCopy = async () => {
    await navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <button
      className={`copy-btn ${copied ? "copied" : ""}`}
      onClick={handleCopy}
      aria-label="Copier le contenu"
    >
      {copied ? (
        <>
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none">
            <path d="M20 6L9 17l-5-5" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
          </svg>
          Copié !
        </>
      ) : (
        <>
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none">
            <rect x="9" y="9" width="13" height="13" rx="2" ry="2" stroke="currentColor" strokeWidth="2" />
            <path d="M5 15H4a2 2 0 01-2-2V4a2 2 0 012-2h9a2 2 0 012 2v1" stroke="currentColor" strokeWidth="2" />
          </svg>
          Copier
        </>
      )}
    </button>
  );
}

// ─── Main Component ───────────────────────────────────────────────────────

export default function ResultCard({ data }: ResultCardProps) {
  const [activeTab, setActiveTab] = useState<Tab>("cahier");
  const { cahier_des_charges: cdc, diagramme_simple, taches_github, squelette_code } = data;

  return (
    <div className="result-card">
      {/* Success Banner */}
      <div className="result-banner">
        <div className="result-banner-icon">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
            <path d="M22 11.08V12a10 10 0 11-5.93-9.14" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
            <polyline points="22 4 12 14.01 9 11.01" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
          </svg>
        </div>
        <div>
          <p className="result-banner-title">Analyse terminée avec succès !</p>
          <p className="result-banner-sub">
            {taches_github.length} tâches · {cdc.fonctionnalites.length} fonctionnalités · {cdc.technologies.length} technologies identifiées
          </p>
        </div>
      </div>

      {/* Tabs */}
      <div className="tabs-nav" role="tablist" aria-label="Sections du rapport">
        {TABS.map((tab) => (
          <button
            key={tab.id}
            role="tab"
            aria-selected={activeTab === tab.id}
            aria-controls={`tab-${tab.id}`}
            className={`tab-btn ${activeTab === tab.id ? "active" : ""}`}
            onClick={() => setActiveTab(tab.id)}
          >
            <span>{tab.icon}</span>
            <span>{tab.label}</span>
          </button>
        ))}
      </div>

      {/* Tab Content */}
      <div className="tab-content">

        {/* ── Cahier des charges ── */}
        {activeTab === "cahier" && (
          <div id="tab-cahier" role="tabpanel" className="tab-panel">
            <div className="cdc-description">
              <h3 className="cdc-desc-title">Description du projet</h3>
              <p className="cdc-desc-text">{cdc.description}</p>
            </div>

            <div className="cdc-grid">
              <SectionBlock title="Objectifs" icon="🎯" items={cdc.objectifs} />
              <SectionBlock title="Utilisateurs cibles" icon="👥" items={cdc.utilisateurs} />
              <SectionBlock title="Fonctionnalités" icon="⚡" items={cdc.fonctionnalites} />
              <SectionBlock title="Contraintes" icon="⚠️" items={cdc.contraintes} variant="constraint" />
              <SectionBlock title="Stack technologique" icon="🛠️" items={cdc.technologies} variant="tech" />
            </div>
          </div>
        )}

        {/* ── Diagramme ── */}
        {activeTab === "diagramme" && (
          <div id="tab-diagramme" role="tabpanel" className="tab-panel">
            <div className="diagram-header">
              <h3 className="diagram-title">Diagramme d&apos;architecture</h3>
              <CopyButton text={diagramme_simple} />
            </div>
            <div className="diagram-block">
              <pre className="diagram-pre">{diagramme_simple}</pre>
            </div>
          </div>
        )}

        {/* ── Tâches GitHub ── */}
        {activeTab === "taches" && (
          <div id="tab-taches" role="tabpanel" className="tab-panel">
            <div className="tasks-header">
              <h3 className="tasks-title">
                Issues GitHub{" "}
                <span className="tasks-count">{taches_github.length}</span>
              </h3>
              <CopyButton text={taches_github.map((t, i) => `${i + 1}. ${t}`).join("\n")} />
            </div>
            <div className="tasks-list">
              {taches_github.map((task, index) => {
                const type = task.split(":")[0].toLowerCase();
                const typeColor =
                  type === "feat"
                    ? "var(--color-accent)"
                    : type === "chore"
                      ? "var(--color-warning)"
                      : type === "docs"
                        ? "var(--color-info)"
                        : "var(--color-danger)";
                return (
                  <div key={index} className="task-item">
                    <span className="task-number">#{index + 1}</span>
                    <span className="task-type" style={{ color: typeColor }}>
                      {task.split(":")[0]}
                    </span>
                    <span className="task-text">
                      {task.includes(":") ? task.substring(task.indexOf(":") + 1).trim() : task}
                    </span>
                  </div>
                );
              })}
            </div>
          </div>
        )}

        {/* ── Squelette ── */}
        {activeTab === "squelette" && (
          <div id="tab-squelette" role="tabpanel" className="tab-panel">
            <div className="skeleton-header">
              <h3 className="skeleton-title">Structure du projet</h3>
              <span className="skeleton-hint">Cliquez pour explorer</span>
            </div>
            <div className="skeleton-container">
              <SkeletonTree node={squelette_code} />
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
