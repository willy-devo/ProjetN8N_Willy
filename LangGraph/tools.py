# ─────────────────────────────────────────────────────────────────
# tools.py — Agent Discovery / Agentic4API
# Remplace : Nœud "HTTP Request" dans N8N
#
# Ce fichier fait exactement ce que le nœud HTTP Request de N8N
# faisait : appeler le MCP Server via Kong avec une query en
# langage naturel, et récupérer les APIs pertinentes depuis Pinecone.
# ─────────────────────────────────────────────────────────────────

import os
import requests
from langchain_core.tools import tool
from dotenv import load_dotenv

load_dotenv()

# ── Configuration Kong ────────────────────────────────────────────
# Kong route /mcp → MCP Server → Mistral Embeddings → Pinecone
# Identique à ce que le nœud HTTP Request de N8N appelait
KONG_URL      = os.getenv("KONG_URL", "http://localhost:8000")
KONG_API_KEY  = os.getenv("KONG_API_KEY", "n8n-internal-key-2025")
MCP_ENDPOINT  = f"{KONG_URL}/mcp/tools/search_apis"


# ── Tool : search_apis ────────────────────────────────────────────
# Déclaré comme @tool pour que LangGraph puisse l'appeler
# automatiquement quand l'agent décide d'effectuer une recherche.
#
# Flux identique au nœud HTTP Request N8N :
#   query texte → POST /mcp/tools/search_apis → Pinecone → résultats
@tool
def search_apis(query: str) -> dict:
    """
    Recherche des APIs pertinentes dans le catalogue Devoteam nexDigital.
    Utilise la recherche sémantique Pinecone via le MCP Server et Kong.

    Args:
        query: Description du besoin en langage naturel.
               Reformule toujours en [verbe] + [ressource] + [méthode HTTP]
               Exemple : "créer commande POST" ou "lister produits panier GET"

    Returns:
        dict avec la liste des APIs trouvées et leurs scores de pertinence.
    """
    try:
        response = requests.post(
            MCP_ENDPOINT,
            json={"query": query},
            headers={
                "Content-Type": "application/json",
                # Clé Kong identique au consumer "n8n-agent" dans kong-setup.ps1
                "apikey": KONG_API_KEY,
            },
            timeout=15,
        )
        response.raise_for_status()
        data = response.json()

        # ── Formatage des résultats ───────────────────────────────
        # Pinecone retourne : id, score (0→1), metadata (nom, description, endpoints)
        # On enrichit chaque résultat avec un score en % pour l'affichage
        results = data.get("results", [])
        for r in results:
            # Convertir le score float Pinecone (ex: 0.87) en pourcentage (87%)
            r["score_pct"] = round(r.get("score", 0) * 100, 1)

        return {
            "results": results,
            "total": len(results),
            "query_sent": query,
        }

    except requests.exceptions.ConnectionError:
        # Kong ou MCP Server non démarrés → message clair pour le debug
        return {
            "error": "Impossible de joindre le MCP Server via Kong. "
                     "Vérifiez que 'docker compose up' est lancé.",
            "results": [],
            "total": 0,
        }
    except requests.exceptions.Timeout:
        return {
            "error": "Le MCP Server ne répond pas (timeout 15s). "
                     "Pinecone est peut-être saturé.",
            "results": [],
            "total": 0,
        }
    except Exception as e:
        return {
            "error": f"Erreur inattendue : {str(e)}",
            "results": [],
            "total": 0,
        }


# ── Test rapide en ligne de commande ─────────────────────────────
# Lance : python tools.py
# Vérifie que Kong → MCP Server → Pinecone répond correctement
if __name__ == "__main__":
    print("🔍 Test de connexion MCP Server via Kong...")
    print(f"   URL : {MCP_ENDPOINT}")
    print(f"   Clé : {KONG_API_KEY[:8]}...\n")

    result = search_apis.invoke({"query": "créer une commande POST order"})

    if "error" in result:
        print(f"❌ Erreur : {result['error']}")
    else:
        print(f"✅ {result['total']} API(s) trouvée(s) pour la query de test\n")
        for r in result["results"][:3]:
            meta = r.get("metadata", {})
            print(f"  • {meta.get('name', r['id'])} — {r['score_pct']}%")
            print(f"    {meta.get('description', '')[:80]}...")
