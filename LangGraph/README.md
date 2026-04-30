# Agentic4API — Agent Discovery LangGraph

Remplace le workflow N8N Chat par un agent LangGraph avec interface Chainlit.

## Équivalences N8N → LangGraph

| Composant N8N         | Fichier LangGraph        |
|-----------------------|--------------------------|
| Chat Trigger          | `chat.py` (Chainlit)     |
| AI Agent              | `agent.py` (LangGraph)   |
| HTTP Request          | `tools.py` (Tool Python) |
| Simple Memory         | MemorySaver (intégré)    |

## Prérequis

- Docker Compose lancé (`docker compose up -d`)
- Python 3.11+
- Fichier `.env` rempli

## Installation

```bash
# 1. Copier et remplir le .env
cp .env.example .env

# 2. Installer les dépendances
pip install -r requirements_langgraph.txt

# 3. Vérifier la connexion MCP Server → Pinecone
python tools.py

# 4. Tester l'agent seul en console
python agent.py

# 5. Lancer l'interface chat
chainlit run chat.py
```

## Accès

- Interface chat : http://localhost:8080
- Kong Admin     : http://localhost:8001
- Kong GUI       : http://localhost:8002
