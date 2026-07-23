import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "AI Project Architect — Transformez vos idées en architecture professionnelle",
  description:
    "Plateforme SaaS alimentée par IA qui génère automatiquement un cahier des charges, diagramme d'architecture, tâches GitHub et squelette de code à partir d'une idée de projet.",
  keywords: ["IA", "architecture logicielle", "cahier des charges", "SaaS", "Groq", "LLaMA"],
  authors: [{ name: "AI Project Architect" }],
  openGraph: {
    title: "AI Project Architect",
    description: "Transformez votre idée en architecture professionnelle en quelques secondes.",
    type: "website",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="fr" suppressHydrationWarning style={{ height: "100%" }}>
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link
          href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500&display=swap"
          rel="stylesheet"
        />
      </head>
      <body style={{ height: "100%" }}>{children}</body>
    </html>
  );
}
