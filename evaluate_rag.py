"""
Script d'évaluation RAG - Agentic4API
Compare les performances de 2 agents :
  - Agent A : Mistral + Pinecone (local via ngrok)
  - Agent B : Gemini Pro + Redis Cloud (n8n Collaborative)
"""

import json
import os
import time
import requests
from typing import Optional
from datasets import Dataset
from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_precision,
    context_recall,
)

# ─────────────────────────────────────────────
# CONFIGURATION
# ─────────────────────────────────────────────

AGENTS = {
    "mistral_pinecone": {
        "name": "Mistral + Pinecone (Local)",
        # Remplace l'URL ngrok à chaque redémarrage ngrok
        "url": "https://respect-phoenix-creamer.ngrok-free.dev/webhook/fb81ea57-3ffa-4e60-b8b2-a7c83326dbbb/chat",
        "model": "mistral-small",
        "vector_store": "pinecone"
    },
    "gemini_redis": {
        "name": "Gemini Pro + Redis (Cloud)",
        # URL fixe n8n Collaborative
        "url": "https://nexdigital.app.n8n.cloud/webhook/fb81ea57-3ffa-4e60-b8b2-a7c83326dbbb/chat",
        "model": "gemini-pro",
        "vector_store": "redis"
    }
}

GOLDEN_DATASET_PATH = "golden_dataset.json"
RESULTS_PATH = "evaluation_results_comparison.json"
TOP_K = 4

ALL_APIS = [
    "order-api", "auth-api", "cart-api", "inventory-api",
    "pricing-api", "review-api", "search-api", "shipping-api",
    "user-api", "webhook-api", "analytics-api", "notification-api"
]


# ─────────────────────────────────────────────
# APPEL AGENT
# ─────────────────────────────────────────────

def call_agent(url: str, question: str, timeout: int = 30) -> dict:
    """
    Appelle un agent via son URL de chat n8n.
    Le format Hosted Chat de n8n attend : { "chatInput": "..." }
    """
    try:
        response = requests.post(
            url,
            json={"chatInput": question},
            headers={"Content-Type": "application/json"},
            timeout=timeout
        )
        response.raise_for_status()
        data = response.json()

        # n8n Hosted Chat retourne : { "output": "..." }
        answer = data.get("output", data.get("response", data.get("text", "")))
        contexts = data.get("contexts", data.get("sources", [answer]))

        if isinstance(contexts, str):
            contexts = [contexts]
        if not contexts:
            contexts = [answer]

        return {"answer": answer, "contexts": contexts, "error": None}

    except requests.exceptions.Timeout:
        return {"answer": "", "contexts": [""], "error": "timeout"}
    except Exception as e:
        return {"answer": "", "contexts": [""], "error": str(e)}


# ─────────────────────────────────────────────
# MÉTRIQUES DE RETRIEVAL
# ─────────────────────────────────────────────

def extract_apis_from_answer(answer: str) -> list[str]:
    answer_lower = answer.lower()
    return [api for api in ALL_APIS if api.replace("-", " ") in answer_lower or api in answer_lower]


def precision_at_k(retrieved: list[str], expected: list[str], k: int) -> float:
    if not expected:
        return 1.0 if not retrieved else 0.0
    hits = sum(1 for api in retrieved[:k] if api in expected)
    return hits / k if k > 0 else 0.0


def recall_at_k(retrieved: list[str], expected: list[str], k: int) -> float:
    if not expected:
        return 1.0
    hits = sum(1 for api in expected if api in retrieved[:k])
    return hits / len(expected)


def mrr_score(retrieved: list[str], expected: list[str]) -> float:
    if not expected:
        return 1.0
    for i, api in enumerate(retrieved):
        if api in expected:
            return 1.0 / (i + 1)
    return 0.0


# ─────────────────────────────────────────────
# ÉVALUATION D'UN AGENT
# ─────────────────────────────────────────────

def evaluate_agent(
    agent_key: str,
    agent_config: dict,
    golden_dataset: list[dict],
    use_ragas: bool = True,
    delay: float = 1.5
) -> dict:

    print(f"\n{'='*60}")
    print(f"  Agent : {agent_config['name']}")
    print(f"  URL   : {agent_config['url']}")
    print(f"{'='*60}\n")

    results = []
    ragas_data = {"question": [], "answer": [], "contexts": [], "ground_truth": []}
    errors = 0

    for i, item in enumerate(golden_dataset):
        print(f"[{i+1}/{len(golden_dataset)}] {item['id']} — {item['question'][:55]}...")

        start = time.time()
        response = call_agent(agent_config["url"], item["question"])
        elapsed = time.time() - start

        if response["error"]:
            print(f"  ❌ Erreur : {response['error']}")
            errors += 1

        answer = response["answer"]
        contexts = response["contexts"]
        retrieved_apis = extract_apis_from_answer(answer)

        p = precision_at_k(retrieved_apis, item["expected_apis"], TOP_K)
        r = recall_at_k(retrieved_apis, item["expected_apis"], TOP_K)
        m = mrr_score(retrieved_apis, item["expected_apis"])

        result = {
            "id": item["id"],
            "question": item["question"],
            "category": item["category"],
            "difficulty": item["difficulty"],
            "expected_apis": item["expected_apis"],
            "retrieved_apis": retrieved_apis,
            "answer": answer,
            "precision_at_k": round(p, 3),
            "recall_at_k": round(r, 3),
            "mrr": round(m, 3),
            "latency_s": round(elapsed, 2),
            "error": response["error"]
        }
        results.append(result)
        print(f"  ✓ P@{TOP_K}={p:.2f} | R@{TOP_K}={r:.2f} | MRR={m:.2f} | {elapsed:.1f}s")

        if use_ragas and answer:
            ragas_data["question"].append(item["question"])
            ragas_data["answer"].append(answer)
            ragas_data["contexts"].append(contexts)
            ragas_data["ground_truth"].append(item["expected_answer"])

        time.sleep(delay)

    # ── Moyennes globales ──
    n = len(results)
    summary = {
        "agent": agent_config["name"],
        "model": agent_config["model"],
        "vector_store": agent_config["vector_store"],
        "total_questions": n,
        "errors": errors,
        "avg_precision_at_k": round(sum(r["precision_at_k"] for r in results) / n, 3),
        "avg_recall_at_k": round(sum(r["recall_at_k"] for r in results) / n, 3),
        "avg_mrr": round(sum(r["mrr"] for r in results) / n, 3),
        "avg_latency_s": round(sum(r["latency_s"] for r in results) / n, 2),
    }

    # ── Par catégorie ──
    categories = set(r["category"] for r in results)
    by_category = {}
    for cat in categories:
        cat_r = [r for r in results if r["category"] == cat]
        by_category[cat] = {
            "count": len(cat_r),
            "avg_precision": round(sum(r["precision_at_k"] for r in cat_r) / len(cat_r), 3),
            "avg_recall": round(sum(r["recall_at_k"] for r in cat_r) / len(cat_r), 3),
            "avg_mrr": round(sum(r["mrr"] for r in cat_r) / len(cat_r), 3),
        }

    # ── Par difficulté ──
    difficulties = set(r["difficulty"] for r in results)
    by_difficulty = {}
    for diff in difficulties:
        diff_r = [r for r in results if r["difficulty"] == diff]
        by_difficulty[diff] = {
            "count": len(diff_r),
            "avg_precision": round(sum(r["precision_at_k"] for r in diff_r) / len(diff_r), 3),
            "avg_mrr": round(sum(r["mrr"] for r in diff_r) / len(diff_r), 3),
        }

    # ── RAGAS ──
    ragas_scores = {}
    if use_ragas and ragas_data["question"]:
        print(f"\n  📊 Calcul RAGAS pour {agent_config['name']}...")
        try:
            ds = Dataset.from_dict(ragas_data)
            ragas_result = evaluate(
                ds,
                metrics=[faithfulness, answer_relevancy, context_precision, context_recall],
            )
            ragas_scores = {
                "faithfulness": round(ragas_result["faithfulness"], 3),
                "answer_relevancy": round(ragas_result["answer_relevancy"], 3),
                "context_precision": round(ragas_result["context_precision"], 3),
                "context_recall": round(ragas_result["context_recall"], 3),
            }
            print(f"  ✓ {ragas_scores}")
        except Exception as e:
            print(f"  ⚠️  RAGAS error : {e}")

    return {
        "summary": summary,
        "by_category": by_category,
        "by_difficulty": by_difficulty,
        "ragas_scores": ragas_scores,
        "details": results
    }


# ─────────────────────────────────────────────
# TABLEAU COMPARATIF
# ─────────────────────────────────────────────

def print_comparison(eval_a: dict, eval_b: dict):
    a = eval_a["summary"]
    b = eval_b["summary"]

    def delta(x, y):
        d = round(x - y, 3)
        return f"+{d}" if d > 0 else str(d)

    print(f"\n{'='*70}")
    print(f"  COMPARAISON FINALE")
    print(f"{'='*70}")
    print(f"  {'Métrique':<25} {'Agent A (Mistral)':<20} {'Agent B (Gemini)':<20} {'Δ'}")
    print(f"  {'─'*65}")
    print(f"  {'Precision@K':<25} {a['avg_precision_at_k']:<20} {b['avg_precision_at_k']:<20} {delta(b['avg_precision_at_k'], a['avg_precision_at_k'])}")
    print(f"  {'Recall@K':<25} {a['avg_recall_at_k']:<20} {b['avg_recall_at_k']:<20} {delta(b['avg_recall_at_k'], a['avg_recall_at_k'])}")
    print(f"  {'MRR':<25} {a['avg_mrr']:<20} {b['avg_mrr']:<20} {delta(b['avg_mrr'], a['avg_mrr'])}")
    print(f"  {'Latence (s)':<25} {a['avg_latency_s']:<20} {b['avg_latency_s']:<20} {delta(b['avg_latency_s'], a['avg_latency_s'])}")

    if eval_a["ragas_scores"] and eval_b["ragas_scores"]:
        ra, rb = eval_a["ragas_scores"], eval_b["ragas_scores"]
        print(f"\n  RAGAS")
        print(f"  {'─'*65}")
        for metric in ra:
            print(f"  {metric:<25} {ra[metric]:<20} {rb[metric]:<20} {delta(rb[metric], ra[metric])}")

    print(f"\n  PAR CATÉGORIE — Agent A (Mistral)")
    print(f"  {'─'*50}")
    for cat, m in eval_a["by_category"].items():
        print(f"  {cat:<20} P={m['avg_precision']} | R={m['avg_recall']} | MRR={m['avg_mrr']}")

    print(f"\n  PAR CATÉGORIE — Agent B (Gemini)")
    print(f"  {'─'*50}")
    for cat, m in eval_b["by_category"].items():
        print(f"  {cat:<20} P={m['avg_precision']} | R={m['avg_recall']} | MRR={m['avg_mrr']}")


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────

if __name__ == "__main__":
    print("\n🚀 Évaluation comparative Agentic4API\n")

    # Charger le golden dataset
    with open(GOLDEN_DATASET_PATH, "r", encoding="utf-8") as f:
        golden = json.load(f)
    print(f"  ✓ {len(golden)} questions chargées")

    # ── Évaluer les 2 agents ──
    # Pour tester rapidement un seul agent, commenter l'autre

    print("\n  [1/2] Évaluation Agent Mistral + Pinecone...")
    eval_mistral = evaluate_agent(
        agent_key="mistral_pinecone",
        agent_config=AGENTS["mistral_pinecone"],
        golden_dataset=golden,
        use_ragas=True,
        delay=1.5
    )

    print("\n  [2/2] Évaluation Agent Gemini + Redis...")
    eval_gemini = evaluate_agent(
        agent_key="gemini_redis",
        agent_config=AGENTS["gemini_redis"],
        golden_dataset=golden,
        use_ragas=True,
        delay=1.5
    )

    # ── Afficher la comparaison ──
    print_comparison(eval_mistral, eval_gemini)

    # ── Sauvegarder ──
    final = {
        "mistral_pinecone": eval_mistral,
        "gemini_redis": eval_gemini
    }
    with open(RESULTS_PATH, "w", encoding="utf-8") as f:
        json.dump(final, f, ensure_ascii=False, indent=2)
    print(f"\n  💾 Résultats sauvegardés → {RESULTS_PATH}")