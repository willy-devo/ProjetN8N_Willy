"""
Script d'envoi des APIs vers n8n pour indexation avec Gemini
Lance le workflow n8n qui génère les embeddings et indexe dans Redis
"""

import os
import json
import yaml
import re
import time
import requests
import hashlib

# ─────────────────────────────────────────────
# CONFIGURATION
# ─────────────────────────────────────────────

# URL du webhook n8n (Test URL pour tester, Production URL quand activé)
WEBHOOK_URL = "https://nexdigital.app.n8n.cloud/webhook/index-apis"
# Pour production : "https://nexdigital.app.n8n.cloud/webhook/index-apis"

API_CATALOGUE_PATH = r"C:\Users\salmane.el.hajouji\Desktop\agentic4api\api-catalogue"

DELAY_BETWEEN_CALLS = 1.0  # secondes entre chaque appel


# ─────────────────────────────────────────────
# PARSERS
# ─────────────────────────────────────────────

def parse_json(filepath, filename):
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    api_id = filename.replace(".json", "")
    endpoints = data.get("endpoints", [])
    if isinstance(endpoints, list):
        endpoint_strs = []
        for ep in endpoints:
            if isinstance(ep, dict):
                endpoint_strs.append(f"{ep.get('method','')} {ep.get('path','')}")
            else:
                endpoint_strs.append(str(ep))
        endpoints_str = ", ".join(endpoint_strs)
    else:
        endpoints_str = str(endpoints)

    return {
        "id": api_id,
        "name": data.get("name", data.get("id", api_id)),
        "description": data.get("description", ""),
        "team": data.get("team", ""),
        "endpoints": endpoints_str,
        "filename": f"api-catalogue/{filename}"
    }


def parse_yaml(filepath, filename):
    with open(filepath, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    api_id = filename.replace(".yaml", "").replace(".yml", "")
    if not isinstance(data, dict):
        return {"id": api_id, "name": api_id, "description": "", "team": "", "endpoints": "", "filename": f"api-catalogue/{filename}"}

    endpoints = data.get("endpoints", data.get("paths", []))
    if isinstance(endpoints, list):
        endpoints_str = ", ".join([
            f"{e.get('method','')} {e.get('path','')}" if isinstance(e, dict) else str(e)
            for e in endpoints
        ])
    elif isinstance(endpoints, dict):
        endpoints_str = ", ".join(endpoints.keys())
    else:
        endpoints_str = str(endpoints) if endpoints else ""

    return {
        "id": api_id,
        "name": data.get("name", data.get("title", api_id)),
        "description": data.get("description", ""),
        "team": data.get("team", data.get("x-team", "")),
        "endpoints": endpoints_str,
        "filename": f"api-catalogue/{filename}"
    }


def parse_md(filepath, filename):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    api_id = filename.replace(".md", "")
    name_match = re.search(r'^#\s+(.+)', content, re.MULTILINE)
    name = name_match.group(1).strip() if name_match else api_id

    desc_match = re.search(r'##\s+Description\n([\s\S]*?)(?:\n##|$)', content)
    description = desc_match.group(1).strip() if desc_match else ""

    team_match = re.search(r'##\s+Team\n([\s\S]*?)(?:\n##|$)', content)
    team = team_match.group(1).strip() if team_match else ""

    endpoint_lines = re.findall(r'-\s+(.+)', content)
    endpoints_str = ", ".join(endpoint_lines) if endpoint_lines else ""

    return {
        "id": api_id,
        "name": name,
        "description": description,
        "team": team,
        "endpoints": endpoints_str,
        "filename": f"api-catalogue/{filename}"
    }


def parse_all_files(folder_path):
    apis = []
    for filename in sorted(os.listdir(folder_path)):
        filepath = os.path.join(folder_path, filename)
        try:
            if filename.endswith(".json"):
                api = parse_json(filepath, filename)
            elif filename.endswith(".yaml") or filename.endswith(".yml"):
                api = parse_yaml(filepath, filename)
            elif filename.endswith(".md"):
                api = parse_md(filepath, filename)
            else:
                continue
            apis.append(api)
        except Exception as e:
            print(f"  ❌ Erreur parsing {filename} : {e}")
    return apis


# ─────────────────────────────────────────────
# ENVOI AU WEBHOOK N8N
# ─────────────────────────────────────────────

def send_to_n8n(api):
    response = requests.post(
        WEBHOOK_URL,
        json=api,
        headers={"Content-Type": "application/json"},
        timeout=30
    )
    response.raise_for_status()
    return response.json()


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────

if __name__ == "__main__":
    print("\n🚀 Envoi des APIs vers n8n pour indexation Gemini\n")
    print(f"  Webhook : {WEBHOOK_URL}")
    print(f"  Dossier : {API_CATALOGUE_PATH}\n")

    # Parser les fichiers
    print("📂 Parsing des fichiers...")
    apis = parse_all_files(API_CATALOGUE_PATH)
    print(f"✓ {len(apis)} APIs trouvées\n")

    # Envoyer chaque API
    success = 0
    errors = 0

    for i, api in enumerate(apis):
        print(f"[{i+1}/{len(apis)}] {api['name']}...")
        try:
            result = send_to_n8n(api)
            print(f"  ✅ Envoyé — réponse : {str(result)[:80]}")
            success += 1
        except Exception as e:
            print(f"  ❌ Erreur : {e}")
            errors += 1
        time.sleep(DELAY_BETWEEN_CALLS)

    print(f"\n{'='*50}")
    print(f"  ✅ Succès  : {success}/{len(apis)}")
    print(f"  ❌ Erreurs : {errors}/{len(apis)}")
    print(f"{'='*50}")
    print("\n🎉 Vérifie Redis Insight — tu dois voir les clés api:* apparaître !")