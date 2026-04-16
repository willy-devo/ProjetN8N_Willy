# Documentation des Schémas de Données - Magasin-Elec-Global

Ce document définit la structure des données stockées dans `/catalog/storage/`. Ces schémas sont conçus pour être consommés par le backend Python et indexés par les agents de recherche sémantique.

## Inventaire des Produits (`products.json`)

Ce fichier est la source de vérité pour le catalogue matériel. Les descriptions sont optimisées pour permettre une recherche par intention (NLP).

### Schéma Technique
| Champ | Type | Description |
| :--- | :--- | :--- |
| `id` | string | Identifiant unique du produit (ex: PROD-101). |
| `name` | string | Nom commercial complet. |
| `brand` | string | Marque du fabricant. |
| `category` | string | Segment de marché (Laptops, Components, Audio, etc.). |
| `price` | float | Prix de vente unitaire en EUR. |
| `specs` | object | Dictionnaire des caractéristiques techniques clés. |
| `description` | string | Description narrative riche pour l'analyse sémantique. |
| `stock` | integer | Quantité physique disponible en entrepôt. |

### Exemple de donnée
```json
{
  "products": [
    {
      "id": "PROD-101",
      "name": "TitanBook Pro 16",
      "brand": "TechCorp",
      "category": "Laptops",
      "price": 2499.00,
      "specs": {
        "processor": "Octa-core 3.8GHz",
        "ram": "32GB DDR5",
        "storage": "1TB SSD NVMe",
        "display": "OLED 120Hz"
      },
      "description": "Station de travail mobile conçue pour les professionnels créatifs. Son écran à haute fréquence de rafraîchissement offre une fluidité exceptionnelle pour le montage vidéo et le design 3D.",
      "stock": 15
    }
  ]
}
```

## Inventaire des Employés (`employees.json`)

### Schéma Technique
| Champ | Type | Description |
| :--- | :--- | :--- |
| `emp_id` | string | Matricule unique de l'employé (ex: EMP-442). |
| `full_name` | string | Prénom et Nom de famille. |
| `role` | string | Intitulé officiel du poste de travail. |
| `department` | string | Département (IT, Logistics, Sales, HR, Finance). |
| `skills` | array | Liste de compétences techniques et savoir-faire clés. |
| `clearance` | integer | Niveau d'accréditation (1: Public, 5: Admin). |
| `biography` | string | Texte narratif riche détaillant l'expérience et l'expertise. |

```json
{
  "employees": [
    {
      "emp_id": "EMP-442",
      "full_name": "Alice Martin",
      "role": "Cloud Architect",
      "department": "IT Infrastructure",
      "skills": [
        "AWS",
        "Kubernetes",
        "API Gateway",
        "Python",
        "Terraform"
      ],
      "clearance": 4,
      "biography": "Experte en conception d'architectures distribuées avec plus de 10 ans d'expérience. Alice supervise la migration vers le micro-services et l'automatisation de la passerelle API Kong pour l'ensemble du groupe."
    }
  ]
}
```

## Gestion des Commandes (`orders.json`)

Ce fichier assure la liaison entre les clients et les produits vendus. Il permet de suivre l'état des transactions et l'historique d'achat pour l'analyse sémantique.

### Schéma Technique
| Champ | Type | Description |
| :--- | :--- | :--- |
| `order_id` | string | Référence unique de la commande (ex: CMD-2026-X1). |
| `customer_id` | string | Identifiant du client ayant passé la commande. |
| `items` | array | Liste d'objets contenant `product_id` et `quantity`. |
| `total_amount` | float | Montant total de la transaction en EUR. |
| `status` | string | État de la commande (pending, shipped, delivered, cancelled). |
| `payment_method`| string | Moyen de paiement utilisé (CB, PayPal, Transfer). |
| `created_at` | string | Horodatage de la commande au format ISO 8601. |

### Exemple de donnée
```json
{
  "orders": [
    {
      "order_id": "CMD-2026-X1",
      "customer_id": "CUST-99",
      "items": [
        {
          "product_id": "PROD-101",
          "quantity": 1
        },
        {
          "product_id": "PROD-778",
          "quantity": 2
        }
      ],
      "total_amount": 3598.98,
      "status": "shipped",
      "payment_method": "CB",
      "created_at": "2026-04-14T10:30:00Z"
    }
  ]
}
```


## Gestion des Clients (`customers.json`)


### Schéma Technique
| Champ | Type | Description |
| :--- | :--- | :--- |
| `customer_id` | string | Identifiant unique du client (ex: CUST-001). |
| `full_name` | string | Prénom et Nom du client. |
| `email` | string | Adresse de contact (clé de liaison pour les notifications). |
| `segment` | string | Classification commerciale (VIP, Standard, Nouveau). |
| `loyalty_points`| integer | Points cumulés dans le programme de fidélité. |
| `interests` | array | Liste de centres d'intérêt pour le ciblage sémantique. |
| `metadata` | object | Informations additionnelles (date de création, langue). |


### Exemple de donnée
```json
{
  "customers": [
    {
      "customer_id": "CUST-001",
      "full_name": "Jean Dupont",
      "email": "j.dupont@email.com",
      "segment": "VIP",
      "loyalty_points": 1500,
      "interests": [
        "Gaming", 
        "High-End Components", 
        "Streaming"
      ],
      "metadata": {
        "account_created": "2024-01-15",
        "preferred_language": "fr"
      }
    }
  ]
}
```
