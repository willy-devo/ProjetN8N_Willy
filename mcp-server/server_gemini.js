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
const GEMINI_API_KEY = process.env.GEMINI_API_KEY;

// ── Health Check ──────────────────────────────────────────────────
app.get("/health", (req, res) => {
  res.json({ status: "ok", timestamp: new Date().toISOString() });
});

app.post("/tools/search_apis", async (req, res) => {
  try {
    const { query } = req.body;

    if (!query) return res.status(400).json({ error: "query is required" });

    // ── ÉTAPE 1 : Embedding de la query avec Gemini ──────────────
    const embedRes = await fetch(
      "https://generativelanguage.googleapis.com/v1beta/models/gemini-embedding-001:embedContent",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "x-goog-api-key": GEMINI_API_KEY, // Auth via header dédié Google
        },
        body: JSON.stringify({
          model: "models/gemini-embedding-001",
          content: {
            parts: [{ text: query }],
          },
          outputDimensionality: 3072,
          taskType: "RETRIEVAL_QUERY",
        }),
      }
    );

    const embedData = await embedRes.json();

    // Vérification que Gemini a bien retourné un embedding
    if (!embedData.embedding || !embedData.embedding.values) {
      return res.status(500).json({ error: "Gemini embed failed", detail: embedData });
    }

    const vector = embedData.embedding.values;

    // ── ÉTAPE 2 : Recherche sémantique dans Pinecone ──────────────
    const pineconeRes = await fetch(`${PINECONE_INDEX_HOST}/query`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Api-Key": PINECONE_API_KEY,
      },
      body: JSON.stringify({
        vector,
        topK: 5,
        includeMetadata: true,
      }),
    });

    const pineconeData = await pineconeRes.json();

    if (!pineconeData.matches) {
      return res.status(500).json({ error: "Pinecone query failed", detail: pineconeData });
    }

    // ── ÉTAPE 3 : Formatage et retour des résultats ───────────────
    res.json({
      results: pineconeData.matches.map((m) => ({
        id: m.id,
        score: m.score,
        metadata: m.metadata,
      })),
    });

  } catch (err) {
    console.error("search_apis error:", err);
    res.status(500).json({ error: err.message });
  }
});

// ── Démarrage du serveur ──────────────────────────────────────────
app.listen(PORT, () =>
  console.log(`MCP Server running on port ${PORT}`)
);