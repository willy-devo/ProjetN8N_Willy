# ─────────────────────────────────────────────────────────────────
# chat.py — Interface Chat Chainlit / Agentic4API
#
# Nouveautés :
#   - Affichage du graph LangGraph (PNG) au démarrage de la session
#   - Fallback Mermaid texte si l'API Mermaid.ink est inaccessible
# ─────────────────────────────────────────────────────────────────

import os
import uuid
import chainlit as cl
from agent import run_agent, save_graph_visualization, get_graph_mermaid


# ── Génération du graph (une seule fois au démarrage du process) ──
GRAPH_PATH = "/app/graph.png"
_graph_generated = save_graph_visualization(GRAPH_PATH)


# ── Démarrage d'une nouvelle session ─────────────────────────────
@cl.on_chat_start
async def on_chat_start():
    thread_id = str(uuid.uuid4())
    cl.user_session.set("thread_id", thread_id)

    # Construit la liste d'éléments à attacher au message de bienvenue
    elements = []

    if _graph_generated and os.path.exists(GRAPH_PATH):
        # PNG disponible → affichage inline
        elements.append(
            cl.Image(
                path=GRAPH_PATH,
                name="Architecture LangGraph",
                display="inline",
            )
        )
    else:
        # Fallback : on affiche le code Mermaid en bloc
        mermaid = get_graph_mermaid()
        if mermaid:
            elements.append(
                cl.Text(
                    name="graph.mmd",
                    content=f"```mermaid\n{mermaid}\n```",
                    display="inline",
                )
            )

    welcome = (
        "👋 Bonjour ! Je suis l'**Agent Discovery** d'Agentic4API.\n\n"
        "Je peux vous aider à trouver les APIs et endpoints du catalogue "
        "**Devoteam nexDigital**.\n\n"
        "**Exemples de questions :**\n"
        "- *Quelle API utiliser pour créer une commande ?*\n"
        "- *Comment authentifier un utilisateur ?*\n"
        "- *Je veux vérifier le stock d'un produit*\n\n"
        "🧭 Architecture du graph d'orchestration ci-dessous :"
    )

    await cl.Message(content=welcome, elements=elements).send()


# ── Réception d'un message utilisateur ───────────────────────────
@cl.on_message
async def on_message(message: cl.Message):
    thread_id = cl.user_session.get("thread_id", "default")

    async with cl.Step(name="🔍 Recherche dans le catalogue...") as step:
        step.input = message.content

        response = await run_agent(
            user_message=message.content,
            thread_id=thread_id,
        )

        step.output = f"Réponse générée ({len(response)} caractères)"

    await cl.Message(content=response).send()


# ── Fin de session ────────────────────────────────────────────────
@cl.on_chat_end
async def on_chat_end():
    thread_id = cl.user_session.get("thread_id", "inconnu")
    print(f"Session terminée : {thread_id}")