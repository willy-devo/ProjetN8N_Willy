# ─────────────────────────────────────────────────────────────────
# agent.py — Agent Discovery / Agentic4API
# Remplace : "AI Agent" + "Simple Memory" dans N8N
#
# Nouveautés :
#   - LangSmith : tracing automatique via variables d'env
#   - Visualisation : export PNG du graph via Mermaid.ink
# ─────────────────────────────────────────────────────────────────

import os
from typing import Annotated, Optional
from dotenv import load_dotenv

from langchain_mistralai import ChatMistralAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.runnables.graph import MermaidDrawMethod
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver
from typing_extensions import TypedDict

from tools import search_apis

load_dotenv()

# ── LangSmith Tracing (auto-activé via env vars) ─────────────────
# Si LANGCHAIN_TRACING_V2=true et LANGCHAIN_API_KEY sont définies,
# LangChain envoie automatiquement chaque step vers smith.langchain.com.
# Aucun code supplémentaire nécessaire — c'est géré nativement.
if os.getenv("LANGCHAIN_TRACING_V2", "").lower() == "true":
    project = os.getenv("LANGCHAIN_PROJECT", "agentic4api-discovery")
    print(f"📊 LangSmith tracing activé — projet: {project}")


# ── System Prompt ─────────────────────────────────────────────────
SYSTEM_PROMPT = """
Tu es l'Agent Discovery d'Agentic4API, expert en APIs internes Devoteam nexDigital.
Ton rôle est d'identifier les ENDPOINTS précis qui correspondent au besoin de l'utilisateur.

## Stratégie de recherche — OBLIGATOIRE
Avant d'appeler search_apis, reformule TOUJOURS la query en combinant :
  [verbe d'action] + [ressource métier] + [méthode HTTP]

Exemples de reformulation :
  - "je veux créer une commande"       → query: "créer commande POST order"
  - "annuler une commande"             → query: "annuler supprimer commande DELETE cancel"
  - "lister les produits du panier"    → query: "liste items panier GET cart items"
  - "authentifier un utilisateur"      → query: "login authentification token POST auth"
  - "vérifier le stock d'un produit"   → query: "stock disponibilité produit GET inventory"

## Règles de reclassement IMPORTANTES
- Le score vectoriel de Pinecone est indicatif — ne t'y fie pas aveuglément.
- Si une API a "commandes" dans son nom ET la question parle de commandes → elle est #1.
- Si une API a "Order" dans son nom et la question parle de créer/annuler des commandes → score 99%.
- Analyse TOUS les résultats avant de répondre.
- Une API dont le nom correspond exactement au besoin prime toujours sur le score vectoriel.

## Règles de Déduplication et de Versioning (CRITIQUE)
- DÉDUPLICATION STRICTE : Tu ne dois JAMAIS lister plusieurs versions d'un même endpoint conceptuel dans ta réponse (ex: interdiction d'afficher à la fois `/v3/orders/{id}` et `/v4/orders/{id}`).
- Garde UNIQUEMENT la version la plus récente d'un endpoint (v4 > v3 > v2 > v1) parmi les résultats trouvés.
- Ignore silencieusement les anciennes versions d'un même chemin dans ton affichage final.
- Exception : Si (et seulement si) la version récente ne permet pas de faire l'action demandée (ex: recherche par customer_id disparue en v4) MAIS qu'une ancienne version deprecated le permettait, tu peux afficher l'ancienne version en précisant bien qu'il s'agit d'un mode dégradé/obsolète.

## Règles de scoring
- Score ≥ 85% : endpoint EXACT pour le besoin → afficher en premier, marquer ✅
- Score 70-84% : endpoint PARTIEL → mentionner les limites, marquer ⚠️
- Score < 70%  : ne pas afficher sauf si aucune autre option, marquer ℹ️

## Format de réponse OBLIGATOIRE
Pour chaque API retournée :

**[Nom de l'API]** — Score: [X%] [✅/⚠️/ℹ️]
- 📋 Description: [description courte. Mentionne si l'API remplace une ancienne version]
- 🔗 Endpoint recommandé: [METHOD] [/path]
- 👥 Équipe: [équipe responsable]
- 💡 Pourquoi cette API: [1 phrase justifiant le choix métier et technique]

## Si aucun endpoint trouvé (tous scores < 70%)
- Dire clairement qu'aucun endpoint existant ne correspond.
- Suggérer 2-3 termes de recherche alternatifs à essayer.
- Ne JAMAIS inventer un endpoint absent des métadonnées.

## Contexte entreprise
- Les APIs sont versionnées (v1, v2, v3, v4...).
- Maximum 3 APIs par réponse sauf demande explicite.
- Chaque API appartient à une équipe Devoteam nexDigital.

Réponds toujours en français.
"""


# ── State du Graph ────────────────────────────────────────────────
class AgentState(TypedDict):
    messages: Annotated[list, add_messages]


# ── LLM Mistral ───────────────────────────────────────────────────
llm = ChatMistralAI(
    model="mistral-small-latest",
    api_key=os.getenv("MISTRAL_API_KEY"),
    temperature=0,
).bind_tools([search_apis])


# ── Nœud Agent ────────────────────────────────────────────────────
def agent_node(state: AgentState) -> dict:
    messages = [SystemMessage(content=SYSTEM_PROMPT)] + state["messages"]
    response = llm.invoke(messages)
    return {"messages": [response]}


# ── Nœud Tools ────────────────────────────────────────────────────
tool_node = ToolNode(tools=[search_apis])


# ── Condition de routage ──────────────────────────────────────────
def route(state: AgentState) -> str:
    return tools_condition(state)


# ── Construction du Graph ─────────────────────────────────────────
def build_graph():
    graph = StateGraph(AgentState)
    graph.add_node("agent", agent_node)
    graph.add_node("tools", tool_node)
    graph.set_entry_point("agent")
    graph.add_conditional_edges(
        "agent",
        route,
        {"tools": "tools", END: END},
    )
    graph.add_edge("tools", "agent")

    memory = MemorySaver()
    return graph.compile(checkpointer=memory)


# Instance unique du graph
discovery_agent = build_graph()


# ── Visualisation du Graph ────────────────────────────────────────
# Génère un PNG du graph LangGraph via l'API publique mermaid.ink
# Pas de dépendance locale (pygraphviz, pyppeteer) requise.
def save_graph_visualization(output_path: str = "/app/graph.png") -> Optional[str]:
    """
    Exporte le graph LangGraph en PNG via Mermaid.ink.

    Args:
        output_path: chemin du fichier PNG à créer.

    Returns:
        Le chemin du fichier si succès, None si échec (offline, etc.).
    """
    try:
        png_bytes = discovery_agent.get_graph().draw_mermaid_png(
            draw_method=MermaidDrawMethod.API,
        )
        with open(output_path, "wb") as f:
            f.write(png_bytes)
        print(f"✅ Graph LangGraph exporté : {output_path}")
        return output_path
    except Exception as e:
        print(f"⚠️  Visualisation du graph indisponible : {e}")
        return None


# ── Mermaid texte (fallback hors-ligne) ──────────────────────────
def get_graph_mermaid() -> str:
    """Retourne la définition Mermaid du graph en texte (toujours dispo)."""
    try:
        return discovery_agent.get_graph().draw_mermaid()
    except Exception:
        return ""


# ── Fonction d'invocation ─────────────────────────────────────────
async def run_agent(user_message: str, thread_id: str = "default") -> str:
    config = {"configurable": {"thread_id": thread_id}}
    state = {"messages": [HumanMessage(content=user_message)]}

    result = await discovery_agent.ainvoke(state, config=config)

    last_message = result["messages"][-1]
    return last_message.content


# ── Test en ligne de commande ─────────────────────────────────────
if __name__ == "__main__":
    import asyncio

    async def test():
        print("🤖 Agent Discovery — Test console\n")
        print("=" * 50)

        # Génère le PNG dans le dossier courant pour tester
        save_graph_visualization("./graph.png")
        print("\nDéfinition Mermaid du graph :\n")
        print(get_graph_mermaid())
        print("=" * 50)

        questions = [
            "Quelle API utiliser pour créer une commande ?",
            "Et pour l'annuler ?",
        ]

        for q in questions:
            print(f"\n👤 {q}")
            response = await run_agent(q, thread_id="test-session")
            print(f"\n🤖 {response}")
            print("-" * 50)

    asyncio.run(test())