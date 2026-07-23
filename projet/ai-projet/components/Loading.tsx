"use client";

import { useEffect, useState } from "react";

const MESSAGES = [
  "Analyse de votre idée...",
  "Génération du cahier des charges...",
  "Conception de l'architecture...",
  "Création des tâches GitHub...",
  "Préparation du squelette de code...",
];

export default function Loading() {
  const [msgIdx, setMsgIdx] = useState(0);

  useEffect(() => {
    const id = setInterval(() => {
      setMsgIdx((prev) => (prev + 1) % MESSAGES.length);
    }, 2000);
    return () => clearInterval(id);
  }, []);

  return (
    <div className="typing-indicator" role="status" aria-label="Analyse en cours">
      <span className="typing-dot" aria-hidden="true" />
      <span className="typing-dot" aria-hidden="true" />
      <span className="typing-dot" aria-hidden="true" />
      <span className="typing-label">{MESSAGES[msgIdx]}</span>
    </div>
  );
}
