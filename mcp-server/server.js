// ─────────────────────────────────────────────────────────────────
// MCP Server — Agentic4API
// Serveur Express custom exposant les outils utilisés par les agents AI
// Tous les appels transitent via Kong Gateway (/mcp)
// ─────────────────────────────────────────────────────────────────

const express = require("express");
const app = express();
app.use(express.json()); // Permet de lire le body JSON des requêtes POST

const PORT = process.env.PORT || 3000;
const PINECONE_API_KEY = process.env.PINECONE_API_KEY;     
const PINECONE_INDEX_HOST = process.env.PINECONE_INDEX_HOST; 
const MISTRAL_API_KEY = process.env.MISTRAL_API_KEY;

// ── Health Check ──────────────────────────────────────────────────
app.get("/health", (req, res) => {
  res.json({ status: "ok", timestamp: new Date().toISOString() });
});

app.post("/tools/search_apis", async (req, res) => {
  try {
    const { query } = req.body;

    if (!query) return res.status(400).json({ error: "query is required" });

    // ── ÉTAPE 1 : Embedding de la query ──────────────
    const embedRes = await fetch("https://api.mistral.ai/v1/embeddings", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${MISTRAL_API_KEY}`,
      },
      body: JSON.stringify({
        model: "mistral-embed",
        input: [query],
      }),
    });

    const embedData = await embedRes.json();

    // Vérification que Mistral a bien retourné un embedding
    if (!embedData.data) {
      return res.status(500).json({ error: "Mistral embed failed", detail: embedData });
    }

    const vector = embedData.data[0].embedding;

    // ── ÉTAPE 2 : Recherche sémantique dans Pinecone ──────────────
    const pineconeRes = await fetch(`${PINECONE_INDEX_HOST}/query`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Api-Key": PINECONE_API_KEY,
      },
      body: JSON.stringify({
        vector,              // Le vecteur généré par Mistral
        topK: 5,             // Nombre max de résultats retournés
        includeMetadata: true, // Inclure les métadonnées (nom, description, endpoints)
      }),
    });

    const pineconeData = await pineconeRes.json();

    // ── ÉTAPE 3 : Formatage et retour des résultats ───────────────
   
    res.json({
      results: pineconeData.matches.map((m) => ({
        id: m.id,
        score: m.score,
        metadata: m.metadata,
      })),
    });

  } catch (err) {
    // Gestion des erreurs réseau ou inattendues
    console.error("search_apis error:", err);
    res.status(500).json({ error: err.message });
  }
});

// ── Démarrage du serveur ──────────────────────────────────────────
app.listen(PORT, () =>
  console.log(`MCP Server running on port ${PORT}`)
);