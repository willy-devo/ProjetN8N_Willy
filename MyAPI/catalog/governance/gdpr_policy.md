# Politique de Confidentialité et Gouvernance des Données (RGPD)

Ce document définit les règles de manipulation des données à caractère personnel (DCP) au sein de l'écosystème Magasin-Elec-Global. Il sert de base de référence pour l'évaluation de la conformité des agents IA.

## 1. Classification des Données
| Catégorie | Type de données | Niveau de sensibilité |
| :--- | :--- | :--- |
| **Identité** | `full_name`, `customer_id` | Modéré |
| **Contact** | `email` | Élevé (PII) |
| **Comportement** | `interests`, `loyalty_points` | Faible |
| **Transaction** | `total_amount`, `payment_method` | Élevé (Financier) |

## 2. Principes d'accès pour l'IA Agentique
* **Minimisation :** L'Agent Discovery ne doit jamais extraire l'adresse email d'un client sauf si l'intention de l'utilisateur est explicitement "Contacter le client".
* **Masquage par défaut :** Lors de la génération de rapports, les emails doivent être partiellement masqués (ex: j.d***@email.com).
* **Interdiction de stockage :** Les agents ne doivent pas stocker de copies locales des fichiers `.json` après traitement.

## 3. Droits des Personnes
L'infrastructure doit supporter via ses APIs :
1. **Droit d'accès :** Consultation des données via `customers.yaml`.
2. **Droit à l'oubli :** Suppression logique des données dans `storage/` sur requête.
3. **Portabilité :** Extraction formatée en JSON pour le client.

## 4. Audit et Contrôle
Toutes les requêtes transitant par la passerelle **Kong** sont logguées pour assurer la traçabilité des accès aux données personnelles.