# Agentic4API

---

## Architecture

```
┌─────────────┐     ┌──────────┐     ┌────────────┐     ┌──────────┐
│  Chat UI    │────▶│   Kong   │────▶│ MCP Server │────▶│ Pinecone │
│ (Chainlit / │     │ Gateway  │     │  (Express) │     │  Vector  │
│  n8n cloud) │     │  :8000   │     │   :3000    │     │    DB    │
└─────────────┘     └──────────┘     └─────┬──────┘     └──────────┘
                          │                │
                          │                ▼
                          │          ┌──────────┐
                          └─────────▶│  Mistral │
                              /llm   │   API    │
                                     └──────────┘
```

- **Kong Gateway** : point d'entrée unique, gère l'auth API Key et route `/mcp` vers le serveur MCP, `/llm` vers Mistral.
- **MCP Server** : reçoit une question → embedding Mistral (1024 dims) → recherche Pinecone → top 5 APIs.
- **Pinecone** : index vectoriel des endpoints OpenAPI.
- **LangGraph + Chainlit** : agent conversationnel local qui consomme le MCP via Kong.

---

## Arborescence (fichiers importants)

```
Agentic4API/
├── docker-compose.yml          → orchestre Kong, MCP, Redis, Chat
├── kong-setup.ps1              → configure services/routes/plugins Kong
├── .env                        → clés API (à créer, voir plus bas)
│
├── mcp-server/
│   ├── server.js               → cœur RAG : query → Mistral → Pinecone
│   ├── package.json
│   └── Dockerfile
│
├── LangGraph/                  → agent conversationnel (remplace n8n)
│   ├── agent.py                → graph LangGraph + tracing LangSmith
│   ├── tools.py                → tool search_apis (appelle Kong /mcp)
│   ├── chat.py                 → interface Chainlit
│   ├── Dockerfile
│   └── requirements_langgraph.txt
│
├── api-catalogue/              → 70 APIs OpenAPI (jeu de base)
├── api-catalogue-150/          → 90 APIs (jeu intermédiaire)
├── api-catalogue-500/          → ~430 APIs (jeu complet)
│
├── send_apis_to_n8n.py         → push catalogue → n8n webhook (indexation)
├── evaluate_rag.py             → mesures RAGAS (faithfulness, relevancy)
├── Golden_Dataset.json         → questions/APIs attendues pour l'éval
└── evaluate/                   → notebook Jupyter d'évaluation
```

---

## Configuration `.env`

Crée un fichier `.env` à la racine :

```env
# Mistral — embeddings + LLM (https://console.mistral.ai/api-keys)
MISTRAL_API_KEY=ta_cle_mistral

# Pinecone — base vectorielle (https://app.pinecone.io)
PINECONE_API_KEY=ta_cle_pinecone
PINECONE_INDEX_HOST=https://<ton-index>.svc.<region>.pinecone.io

# Kong — clé interne pour authentifier les agents
KONG_API_KEY=n8n-internal-key-2025
```

> **Index Pinecone requis** : dimension `1024`, metric `cosine` (matche `mistral-embed`).

---

## Configuration du tunnel vers le port 8000

```powershell
npx untun@latest tunnel http://localhost:8000
```

## Démarrage A→Z avec Docker

### 1. Prérequis
- Docker Desktop
- PowerShell (Windows) ou bash (Linux/macOS)

### 2. Lancer la stack
```powershell
docker compose up -d
```

Démarre dans l'ordre : `kong-db` → `kong-migration` (init DB, s'arrête) → `kong` + `mcp-server` + `redis` + `chat`.

### 3. Vérifier que tout est healthy
```powershell
docker compose ps
```
Tous les services doivent être en `Up (healthy)`. `kong-migration` en `Exited (0)` est **normal**.

### 4. Configurer Kong (une seule fois)
```powershell
.\kong-setup.ps1
```
Crée les services `mistral-llm` et `mcp-server`, les routes `/llm` et `/mcp`, le plugin `key-auth`, et le consumer `n8n-agent` avec sa clé.

### 5. Tester
```powershell
# Health du MCP via Kong
curl.exe -s -H "apikey: n8n-internal-key-2025" http://localhost:8000/mcp/health

# Recherche sémantique
curl.exe -s -X POST `
  -H "apikey: n8n-internal-key-2025" `
  -H "Content-Type: application/json" `
  -d "{\"query\": \"créer une commande client\"}" `
  http://localhost:8000/mcp/tools/search_apis
```

### 6. Accéder aux interfaces

| Service | URL |
|---|---|
| Chat (Chainlit) | http://localhost:8080 |
| Kong Manager | http://localhost:8002 |
| Kong Admin API | http://localhost:8001 |
| Kong Proxy | http://localhost:8000 |
| Redis Insight | http://localhost:8003 |

---

## Composants principaux

### Kong Gateway
Point d'entrée unique. Authentifie via header `apikey`, route les requêtes, et **injecte automatiquement** la clé Mistral côté serveur (les agents ne la voient jamais). La config est persistée dans le volume Docker `kong_data` — un `docker compose down` ne fait **pas** perdre la configuration.

### MCP Server (`mcp-server/server.js`)
Express minimaliste exposant deux endpoints :
- `GET /health` — pour les healthchecks
- `POST /tools/search_apis` — flux complet `query → embedding Mistral → Pinecone topK=5`

### Catalogue API
Trois jeux de fichiers OpenAPI 3.0 enrichis (`x-team`, `x-domain`, `x-status`, versionnage `v1`→`v4` avec deprecation). Le jeu `api-catalogue-500` est le catalogue de production.

### Indexation Pinecone (`send_apis_to_n8n.py`)
Script Python qui parcourt un dossier de catalogue et envoie chaque API à un webhook n8n qui se charge du chunking, de l'embedding et de l'upsert Pinecone.

### LangGraph + Chainlit (`LangGraph/`)
Alternative locale au n8n cloud : `agent.py` définit un graph avec un seul tool `search_apis`, `chat.py` lance l'UI sur le port 8080. Inclut le tracing LangSmith automatique.

### Évaluation RAG (`evaluate_rag.py` + `Golden_Dataset.json`)
Mesure la qualité du RAG via RAGAS (`faithfulness`, `answer_relevancy`, `context_precision`, `context_recall`) sur un golden dataset de questions/APIs attendues.

---

## Commandes utiles

```powershell
# Voir les logs en temps réel d'un service
docker compose logs -f mcp-server

# Redémarrer un service après modification du code
docker compose up -d --build mcp-server

# Tout arrêter (config Kong conservée)
docker compose down

# Tout arrêter ET supprimer les volumes (config Kong perdue)
docker compose down -v
```

---

## Pièges courants

- **PowerShell** : `curl` est un alias de `Invoke-WebRequest`. Utiliser `curl.exe`.
- **`jq` qui plante** : ajouter `-s` à curl pour supprimer la barre de progression.
- **`kong-setup` en 409 Conflict** : config déjà créée, normal en cas de relance.
- **MCP renvoie `Mistral embed failed`** : `MISTRAL_API_KEY` invalide → relancer `docker compose down && up -d` après modif `.env`.
- **Index Pinecone vide** : `search_apis` renvoie `[]` → indexer d'abord via `send_apis_to_n8n.py`.
