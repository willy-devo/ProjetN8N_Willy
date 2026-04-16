# Manuel des Conventions de Nommage et Standards API

Ce guide assure la cohérence du catalogue pour permettre à l'**Agent Architect** de générer des contrats valides et à l'**Agent Discovery** de naviguer sans erreur entre les services.

## 1. Identifiants Uniques (UID)
Tous les identifiants doivent respecter le format préfixé :
* **Produits :** `PROD-[0-9]{3}` (ex: PROD-101)
* **Clients :** `CUST-[0-9]{3}` (ex: CUST-001)
* **Employés :** `EMP-[0-9]{3}` (ex: EMP-001)
* **Commandes :** `CMD-[YYYY]-[0-9]{3}` (ex: CMD-2026-001)

## 2. Standards OpenAPI (YAML)
Pour garantir une intégration fluide avec Kong et Mistral :
* **Casing :** Utiliser le `snake_case` pour les noms de champs et le `kebab-case` pour les URLs (ex: `/product-search`).
* **Pluralité :** Les ressources doivent être au pluriel (ex: `/orders` et non `/order`).
* **Versions :** Le header `x-api-version` est obligatoire pour toute évolution de contrat.

## 3. Structure des fichiers JSON
* Les racines des fichiers de stockage doivent porter le nom de la ressource au pluriel :
  ```json
  { "products": [...] }

## 4. Gestion des Erreurs et Statuts
* Les réponses d'erreur doivent suivre le format :
  ```json
  { "error": { "code": "NOT_FOUND", "message": "Détails ici", "at": "ISO-8601" } }