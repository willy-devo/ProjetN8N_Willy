#!/usr/bin/env python3
"""
Génère 150 fichiers JSON/YAML/MD pour le catalogue API Agentic4API
Domaines : E-commerce, Finance, RH, Logistique, CRM, Analytics, Sécurité, Communication
Inclut : faux positifs sémantiques + versionnage complexe
"""

import json
import os

OUTPUT_DIR = "api-catalogue-150"
os.makedirs(OUTPUT_DIR, exist_ok=True)

APIS = [

# ════════════════════════════════════════════════════════
# DOMAINE 1 — E-COMMERCE (déjà existantes + nouvelles)
# ════════════════════════════════════════════════════════

{
  "id": "order-api-v4", "filename": "order-api-v4.json",
  "name": "Order API v4",
  "description": "Gestion des commandes e-commerce. Création, suivi, modification et annulation des commandes clients. Version actuelle recommandée.",
  "team": "Equipe Commerce", "version": "v4",
  "endpoints": [
    {"method": "POST", "path": "/v4/orders", "description": "Créer une nouvelle commande"},
    {"method": "GET", "path": "/v4/orders/{id}", "description": "Récupérer une commande"},
    {"method": "PUT", "path": "/v4/orders/{id}", "description": "Modifier une commande"},
    {"method": "PUT", "path": "/v4/orders/{id}/cancel", "description": "Annuler une commande"},
    {"method": "GET", "path": "/v4/orders?customerId={id}", "description": "Lister les commandes d'un client"},
    {"method": "DELETE", "path": "/v4/orders/{id}", "description": "Supprimer une commande"},
  ]
},
{
  "id": "order-api-v3", "filename": "order-api-v3.json",
  "name": "Order API v3",
  "description": "Version précédente de l'API commandes. Deprecated — migrer vers v4. Gestion des commandes sans support des commandes partielles.",
  "team": "Equipe Commerce", "version": "v3",
  "endpoints": [
    {"method": "POST", "path": "/v3/orders"},
    {"method": "GET", "path": "/v3/orders/{id}"},
    {"method": "PUT", "path": "/v3/orders/{id}/status"},
    {"method": "DELETE", "path": "/v3/orders/{id}"},
  ]
},
{
  "id": "order-api-v2", "filename": "order-api-v2.json",
  "name": "Order API v2",
  "description": "Version legacy de l'API commandes. Obsolète depuis 2022. Ne supporte pas les remises ni les commandes multi-vendeurs.",
  "team": "Equipe Commerce", "version": "v2",
  "endpoints": [
    {"method": "POST", "path": "/v2/orders"},
    {"method": "GET", "path": "/v2/orders/{id}"},
    {"method": "PUT", "path": "/v2/orders/{id}"},
  ]
},
{
  "id": "cart-api", "filename": "cart-api.json",
  "name": "Cart API",
  "description": "Gestion du panier d'achat. Ajout, suppression et mise à jour des articles avant commande. Gère les sessions anonymes.",
  "team": "Equipe Commerce", "version": "v1",
  "endpoints": [
    {"method": "GET", "path": "/v1/cart/{userId}"},
    {"method": "POST", "path": "/v1/cart/{userId}/items"},
    {"method": "PUT", "path": "/v1/cart/{userId}/items/{itemId}"},
    {"method": "DELETE", "path": "/v1/cart/{userId}/items/{itemId}"},
    {"method": "POST", "path": "/v1/cart/{userId}/checkout"},
  ]
},
{
  "id": "wishlist-api", "filename": "wishlist-api.json",
  "name": "Wishlist API",
  "description": "Gestion des listes de souhaits clients. Ajouter, supprimer des produits désirés. Similaire au panier mais sans intention d'achat immédiate.",
  "team": "Equipe Commerce", "version": "v1",
  "endpoints": [
    {"method": "GET", "path": "/v1/wishlists/{userId}"},
    {"method": "POST", "path": "/v1/wishlists/{userId}/items"},
    {"method": "DELETE", "path": "/v1/wishlists/{userId}/items/{itemId}"},
    {"method": "POST", "path": "/v1/wishlists/{userId}/share"},
  ]
},
{
  "id": "pricing-api", "filename": "pricing-api.json",
  "name": "Pricing API",
  "description": "Gestion des prix et promotions. Calcul des remises, codes promo et règles tarifaires dynamiques.",
  "team": "Equipe Commerce", "version": "v1",
  "endpoints": [
    {"method": "GET", "path": "/v1/pricing/product/{productId}"},
    {"method": "POST", "path": "/v1/pricing/calculate"},
    {"method": "POST", "path": "/v1/pricing/promo/validate"},
    {"method": "GET", "path": "/v1/pricing/rules"},
    {"method": "PUT", "path": "/v1/pricing/rules/{id}"},
  ]
},
{
  "id": "discount-api", "filename": "discount-api.json",
  "name": "Discount API",
  "description": "Gestion des remises et codes de réduction. Création et validation des promotions. Faux positif avec Pricing API — Discount gère les campagnes, Pricing calcule les prix finaux.",
  "team": "Equipe Marketing", "version": "v1",
  "endpoints": [
    {"method": "POST", "path": "/v1/discounts"},
    {"method": "GET", "path": "/v1/discounts/{code}"},
    {"method": "PUT", "path": "/v1/discounts/{id}/activate"},
    {"method": "PUT", "path": "/v1/discounts/{id}/deactivate"},
    {"method": "GET", "path": "/v1/discounts/campaigns"},
  ]
},
{
  "id": "review-api", "filename": "review-api.json",
  "name": "Review API",
  "description": "Gestion des avis et notations produits. Soumission, modération et agrégation des reviews clients.",
  "team": "Equipe Catalog", "version": "v1",
  "endpoints": [
    {"method": "POST", "path": "/v1/reviews"},
    {"method": "GET", "path": "/v1/reviews/product/{productId}"},
    {"method": "PUT", "path": "/v1/reviews/{id}/moderate"},
    {"method": "DELETE", "path": "/v1/reviews/{id}"},
    {"method": "GET", "path": "/v1/reviews/stats/{productId}"},
  ]
},
{
  "id": "rating-api", "filename": "rating-api.json",
  "name": "Rating API",
  "description": "Système de notation numérique des produits et services. Calcul des scores moyens et tendances. Faux positif avec Review API — Rating gère uniquement les étoiles, Review gère le texte complet.",
  "team": "Equipe Catalog", "version": "v1",
  "endpoints": [
    {"method": "POST", "path": "/v1/ratings"},
    {"method": "GET", "path": "/v1/ratings/product/{productId}"},
    {"method": "GET", "path": "/v1/ratings/average/{productId}"},
    {"method": "GET", "path": "/v1/ratings/distribution/{productId}"},
  ]
},
{
  "id": "search-api", "filename": "search-api.json",
  "name": "Search API",
  "description": "Recherche full-text sur le catalogue produits et commandes. Supporte les filtres, facettes et tri par pertinence.",
  "team": "Equipe Platform", "version": "v1",
  "endpoints": [
    {"method": "GET", "path": "/v1/search?q={query}"},
    {"method": "GET", "path": "/v1/search/products?category={cat}"},
    {"method": "GET", "path": "/v1/search/orders?status={status}"},
    {"method": "POST", "path": "/v1/search/advanced"},
  ]
},
{
  "id": "product-catalog-api", "filename": "product-catalog-api.json",
  "name": "Product Catalog API",
  "description": "Gestion du catalogue produits. CRUD complet sur les produits, catégories et attributs. Faux positif avec Search API — Catalog gère les données, Search les interroge.",
  "team": "Equipe Catalog", "version": "v2",
  "endpoints": [
    {"method": "GET", "path": "/v2/products"},
    {"method": "POST", "path": "/v2/products"},
    {"method": "GET", "path": "/v2/products/{id}"},
    {"method": "PUT", "path": "/v2/products/{id}"},
    {"method": "DELETE", "path": "/v2/products/{id}"},
    {"method": "GET", "path": "/v2/categories"},
  ]
},
{
  "id": "inventory-api", "filename": "inventory-api.json",
  "name": "Inventory API",
  "description": "Gestion des stocks et inventaires produits. Suivi en temps réel, alertes de rupture et réapprovisionnement automatique.",
  "team": "Equipe Logistique", "version": "v3",
  "endpoints": [
    {"method": "GET", "path": "/v3/inventory"},
    {"method": "GET", "path": "/v3/inventory/{productId}"},
    {"method": "PUT", "path": "/v3/inventory/{productId}/stock"},
    {"method": "POST", "path": "/v3/inventory/alerts"},
    {"method": "POST", "path": "/v3/inventory/restock"},
  ]
},
{
  "id": "warehouse-api", "filename": "warehouse-api.json",
  "name": "Warehouse API",
  "description": "Gestion des entrepôts et emplacements physiques. Suivi des mouvements de stock entre entrepôts. Faux positif avec Inventory — Warehouse gère les lieux physiques, Inventory les quantités.",
  "team": "Equipe Logistique", "version": "v1",
  "endpoints": [
    {"method": "GET", "path": "/v1/warehouses"},
    {"method": "GET", "path": "/v1/warehouses/{id}/stock"},
    {"method": "POST", "path": "/v1/warehouses/transfer"},
    {"method": "GET", "path": "/v1/warehouses/{id}/locations"},
  ]
},
{
  "id": "shipping-api", "filename": "shipping-api.json",
  "name": "Shipping API",
  "description": "Gestion des expéditions et livraisons. Calcul des frais de port, suivi colis et gestion des retours.",
  "team": "Equipe Logistique", "version": "v1",
  "endpoints": [
    {"method": "POST", "path": "/v1/shipping/estimate"},
    {"method": "POST", "path": "/v1/shipping/create"},
    {"method": "GET", "path": "/v1/shipping/{trackingId}"},
    {"method": "PUT", "path": "/v1/shipping/{trackingId}/cancel"},
    {"method": "POST", "path": "/v1/shipping/return"},
  ]
},
{
  "id": "delivery-api", "filename": "delivery-api.json",
  "name": "Delivery API",
  "description": "Gestion des créneaux et planification de livraison. Réservation de plages horaires et gestion des livreurs. Faux positif avec Shipping — Delivery gère le planning, Shipping les colis.",
  "team": "Equipe Logistique", "version": "v1",
  "endpoints": [
    {"method": "GET", "path": "/v1/delivery/slots?date={date}"},
    {"method": "POST", "path": "/v1/delivery/book"},
    {"method": "PUT", "path": "/v1/delivery/{id}/reschedule"},
    {"method": "GET", "path": "/v1/delivery/tracking/{id}"},
  ]
},
{
  "id": "return-api", "filename": "return-api.json",
  "name": "Return API",
  "description": "Gestion des retours produits et remboursements. Création des demandes de retour, validation et suivi.",
  "team": "Equipe Commerce", "version": "v1",
  "endpoints": [
    {"method": "POST", "path": "/v1/returns"},
    {"method": "GET", "path": "/v1/returns/{id}"},
    {"method": "PUT", "path": "/v1/returns/{id}/approve"},
    {"method": "PUT", "path": "/v1/returns/{id}/reject"},
    {"method": "GET", "path": "/v1/returns?orderId={id}"},
  ]
},

# ════════════════════════════════════════════════════════
# DOMAINE 2 — UTILISATEURS & IDENTITÉ (faux positifs)
# ════════════════════════════════════════════════════════

{
  "id": "user-api", "filename": "user-api.json",
  "name": "User API",
  "description": "Gestion des utilisateurs et profils. Inscription, mise à jour et suppression des comptes utilisateurs de la plateforme.",
  "team": "Equipe Identity", "version": "v2",
  "endpoints": [
    {"method": "POST", "path": "/v2/users/register"},
    {"method": "POST", "path": "/v2/users/login"},
    {"method": "GET", "path": "/v2/users/{id}"},
    {"method": "PUT", "path": "/v2/users/{id}"},
    {"method": "DELETE", "path": "/v2/users/{id}"},
  ]
},
{
  "id": "customer-profile-api", "filename": "customer-profile-api.json",
  "name": "Customer Profile API",
  "description": "Gestion des profils clients enrichis. Données personnelles, préférences, historique d'achat et conformité RGPD. Faux positif avec User API — Customer Profile cible les acheteurs, User API tous les comptes.",
  "team": "Equipe Identity", "version": "v1",
  "endpoints": [
    {"method": "GET", "path": "/v1/customers/{id}"},
    {"method": "PUT", "path": "/v1/customers/{id}"},
    {"method": "DELETE", "path": "/v1/customers/{id}"},
    {"method": "GET", "path": "/v1/customers/{id}/preferences"},
    {"method": "PUT", "path": "/v1/customers/{id}/gdpr/delete"},
  ]
},
{
  "id": "account-api", "filename": "account-api.json",
  "name": "Account API",
  "description": "Gestion des comptes et organisations. Comptes multi-utilisateurs, rôles et facturation. Faux positif avec User API — Account gère les organisations, User les individus.",
  "team": "Equipe Identity", "version": "v1",
  "endpoints": [
    {"method": "POST", "path": "/v1/accounts"},
    {"method": "GET", "path": "/v1/accounts/{id}"},
    {"method": "PUT", "path": "/v1/accounts/{id}"},
    {"method": "GET", "path": "/v1/accounts/{id}/members"},
    {"method": "POST", "path": "/v1/accounts/{id}/members/invite"},
  ]
},
{
  "id": "employee-api", "filename": "employee-api.json",
  "name": "Employee API",
  "description": "Gestion des employés et ressources humaines. Profils, contrats, congés et évaluations. Faux positif avec User API — Employee cible les collaborateurs internes.",
  "team": "Equipe RH", "version": "v1",
  "endpoints": [
    {"method": "POST", "path": "/v1/employees"},
    {"method": "GET", "path": "/v1/employees/{id}"},
    {"method": "PUT", "path": "/v1/employees/{id}"},
    {"method": "GET", "path": "/v1/employees/{id}/contracts"},
    {"method": "GET", "path": "/v1/employees/{id}/leaves"},
  ]
},
{
  "id": "auth-api", "filename": "auth-api.json",
  "name": "Auth API",
  "description": "Authentification et autorisation. Gestion des tokens JWT, OAuth2 et refresh tokens.",
  "team": "Equipe Identity", "version": "v2",
  "endpoints": [
    {"method": "POST", "path": "/v2/auth/login"},
    {"method": "POST", "path": "/v2/auth/logout"},
    {"method": "POST", "path": "/v2/auth/refresh"},
    {"method": "GET", "path": "/v2/auth/me"},
    {"method": "POST", "path": "/v2/auth/forgot-password"},
    {"method": "POST", "path": "/v2/auth/reset-password"},
  ]
},
{
  "id": "sso-api", "filename": "sso-api.json",
  "name": "SSO API",
  "description": "Single Sign-On pour les applications internes. Authentification centralisée SAML/OIDC. Faux positif avec Auth API — SSO gère la fédération d'identité, Auth les tokens applicatifs.",
  "team": "Equipe Identity", "version": "v1",
  "endpoints": [
    {"method": "GET", "path": "/v1/sso/login?provider={provider}"},
    {"method": "GET", "path": "/v1/sso/callback"},
    {"method": "POST", "path": "/v1/sso/logout"},
    {"method": "GET", "path": "/v1/sso/providers"},
  ]
},
{
  "id": "permission-api", "filename": "permission-api.json",
  "name": "Permission API",
  "description": "Gestion fine des permissions et rôles RBAC. Attribution des droits par ressource et action. Faux positif avec Auth API — Permission gère les droits, Auth l'authentification.",
  "team": "Equipe Identity", "version": "v1",
  "endpoints": [
    {"method": "GET", "path": "/v1/permissions/user/{userId}"},
    {"method": "POST", "path": "/v1/permissions/assign"},
    {"method": "DELETE", "path": "/v1/permissions/revoke"},
    {"method": "GET", "path": "/v1/roles"},
    {"method": "POST", "path": "/v1/roles"},
  ]
},
{
  "id": "session-api", "filename": "session-api.json",
  "name": "Session API",
  "description": "Gestion des sessions utilisateurs actives. Révocation, durée de vie et appareils connectés.",
  "team": "Equipe Identity", "version": "v1",
  "endpoints": [
    {"method": "GET", "path": "/v1/sessions/user/{userId}"},
    {"method": "DELETE", "path": "/v1/sessions/{sessionId}"},
    {"method": "DELETE", "path": "/v1/sessions/user/{userId}/all"},
    {"method": "GET", "path": "/v1/sessions/devices/{userId}"},
  ]
},

# ════════════════════════════════════════════════════════
# DOMAINE 3 — FINANCE & PAIEMENT
# ════════════════════════════════════════════════════════

{
  "id": "payment-api", "filename": "payment-api.json",
  "name": "Payment API",
  "description": "Traitement des paiements et transactions. Carte bancaire, PayPal, virement. Gestion des remboursements.",
  "team": "Equipe Finance", "version": "v2",
  "endpoints": [
    {"method": "POST", "path": "/v2/payments"},
    {"method": "GET", "path": "/v2/payments/{id}"},
    {"method": "POST", "path": "/v2/payments/{id}/refund"},
    {"method": "GET", "path": "/v2/payments?orderId={id}"},
    {"method": "POST", "path": "/v2/payments/capture"},
  ]
},
{
  "id": "billing-api", "filename": "billing-api.json",
  "name": "Billing API",
  "description": "Gestion de la facturation et des abonnements récurrents. Cycles de facturation, relances et impayés. Faux positif avec Payment API — Billing gère les cycles, Payment les transactions.",
  "team": "Equipe Finance", "version": "v1",
  "endpoints": [
    {"method": "GET", "path": "/v1/billing/subscriptions/{customerId}"},
    {"method": "POST", "path": "/v1/billing/subscriptions"},
    {"method": "PUT", "path": "/v1/billing/subscriptions/{id}/cancel"},
    {"method": "GET", "path": "/v1/billing/invoices/{customerId}"},
    {"method": "POST", "path": "/v1/billing/retry/{invoiceId}"},
  ]
},
{
  "id": "invoice-api", "filename": "invoice-api.json",
  "name": "Invoice API",
  "description": "Génération et gestion des factures. Création, envoi et archivage des factures clients. Faux positif avec Billing API — Invoice gère les documents, Billing les cycles.",
  "team": "Equipe Finance", "version": "v1",
  "endpoints": [
    {"method": "POST", "path": "/v1/invoices"},
    {"method": "GET", "path": "/v1/invoices/{id}"},
    {"method": "GET", "path": "/v1/invoices/{id}/pdf"},
    {"method": "POST", "path": "/v1/invoices/{id}/send"},
    {"method": "PUT", "path": "/v1/invoices/{id}/void"},
  ]
},
{
  "id": "wallet-api", "filename": "wallet-api.json",
  "name": "Wallet API",
  "description": "Portefeuille électronique client. Crédits, rechargement et utilisation du solde. Faux positif avec Payment API — Wallet gère le solde interne, Payment les transactions externes.",
  "team": "Equipe Finance", "version": "v1",
  "endpoints": [
    {"method": "GET", "path": "/v1/wallets/{userId}"},
    {"method": "POST", "path": "/v1/wallets/{userId}/topup"},
    {"method": "POST", "path": "/v1/wallets/{userId}/debit"},
    {"method": "GET", "path": "/v1/wallets/{userId}/transactions"},
  ]
},
{
  "id": "tax-api", "filename": "tax-api.json",
  "name": "Tax API",
  "description": "Calcul des taxes et TVA selon les régions. Conformité fiscale internationale et déclarations.",
  "team": "Equipe Finance", "version": "v1",
  "endpoints": [
    {"method": "POST", "path": "/v1/tax/calculate"},
    {"method": "GET", "path": "/v1/tax/rates?country={code}"},
    {"method": "POST", "path": "/v1/tax/validate-vat"},
    {"method": "GET", "path": "/v1/tax/reports?period={period}"},
  ]
},
{
  "id": "fraud-detection-api", "filename": "fraud-detection-api.json",
  "name": "Fraud Detection API",
  "description": "Détection des transactions frauduleuses en temps réel. Scoring de risque et blocage automatique.",
  "team": "Equipe Finance", "version": "v1",
  "endpoints": [
    {"method": "POST", "path": "/v1/fraud/score"},
    {"method": "POST", "path": "/v1/fraud/report"},
    {"method": "GET", "path": "/v1/fraud/rules"},
    {"method": "PUT", "path": "/v1/fraud/rules/{id}"},
  ]
},
{
  "id": "subscription-api", "filename": "subscription-api.json",
  "name": "Subscription API",
  "description": "Gestion des abonnements produits et services. Plans tarifaires, upgrades et résiliations. Faux positif avec Billing API — Subscription gère les plans, Billing les paiements.",
  "team": "Equipe Commerce", "version": "v2",
  "endpoints": [
    {"method": "GET", "path": "/v2/subscriptions/{customerId}"},
    {"method": "POST", "path": "/v2/subscriptions"},
    {"method": "PUT", "path": "/v2/subscriptions/{id}/upgrade"},
    {"method": "PUT", "path": "/v2/subscriptions/{id}/downgrade"},
    {"method": "DELETE", "path": "/v2/subscriptions/{id}"},
  ]
},

# ════════════════════════════════════════════════════════
# DOMAINE 4 — COMMUNICATION & NOTIFICATIONS
# ════════════════════════════════════════════════════════

{
  "id": "notification-api", "filename": "notification-api.json",
  "name": "Notification API",
  "description": "Envoi de notifications multicanal (email, SMS, push) pour les utilisateurs de la plateforme.",
  "team": "Equipe Platform", "version": "v1",
  "endpoints": [
    {"method": "POST", "path": "/v1/notifications/send"},
    {"method": "POST", "path": "/v1/notifications/schedule"},
    {"method": "GET", "path": "/v1/notifications/{id}"},
    {"method": "GET", "path": "/v1/notifications"},
    {"method": "DELETE", "path": "/v1/notifications/{id}"},
    {"method": "GET", "path": "/v1/notifications/stats"},
  ]
},
{
  "id": "email-api", "filename": "email-api.json",
  "name": "Email API",
  "description": "Envoi d'emails transactionnels et marketing. Templates, tracking d'ouverture et gestion des bounces. Faux positif avec Notification API — Email API se spécialise uniquement sur l'email.",
  "team": "Equipe Platform", "version": "v2",
  "endpoints": [
    {"method": "POST", "path": "/v2/emails/send"},
    {"method": "POST", "path": "/v2/emails/batch"},
    {"method": "GET", "path": "/v2/emails/{id}/status"},
    {"method": "GET", "path": "/v2/emails/templates"},
    {"method": "POST", "path": "/v2/emails/templates"},
  ]
},
{
  "id": "sms-api", "filename": "sms-api.json",
  "name": "SMS API",
  "description": "Envoi de SMS transactionnels et OTP. Gestion des numéros courts et tracking des livraisons. Faux positif avec Notification API — SMS API se spécialise sur la messagerie SMS.",
  "team": "Equipe Platform", "version": "v1",
  "endpoints": [
    {"method": "POST", "path": "/v1/sms/send"},
    {"method": "POST", "path": "/v1/sms/otp/send"},
    {"method": "POST", "path": "/v1/sms/otp/verify"},
    {"method": "GET", "path": "/v1/sms/{id}/status"},
  ]
},
{
  "id": "push-api", "filename": "push-api.json",
  "name": "Push Notification API",
  "description": "Notifications push mobiles iOS et Android. Gestion des tokens, segments et campagnes push. Faux positif avec Notification API — Push API se spécialise sur les appareils mobiles.",
  "team": "Equipe Platform", "version": "v1",
  "endpoints": [
    {"method": "POST", "path": "/v1/push/send"},
    {"method": "POST", "path": "/v1/push/register-device"},
    {"method": "DELETE", "path": "/v1/push/unregister-device"},
    {"method": "POST", "path": "/v1/push/campaigns"},
    {"method": "GET", "path": "/v1/push/campaigns/{id}/stats"},
  ]
},
{
  "id": "messaging-api", "filename": "messaging-api.json",
  "name": "Messaging API",
  "description": "Messagerie interne entre utilisateurs. Chat en temps réel, historique et modération. Faux positif avec Notification API — Messaging est bidirectionnel, Notification est unidirectionnel.",
  "team": "Equipe Platform", "version": "v1",
  "endpoints": [
    {"method": "POST", "path": "/v1/messages"},
    {"method": "GET", "path": "/v1/messages/conversations/{userId}"},
    {"method": "GET", "path": "/v1/messages/{conversationId}"},
    {"method": "DELETE", "path": "/v1/messages/{id}"},
  ]
},
{
  "id": "alert-api", "filename": "alert-api.json",
  "name": "Alert API",
  "description": "Alertes système et monitoring. Notifications d'incidents, pannes et seuils dépassés. Faux positif avec Notification API — Alert cible les équipes techniques, Notification les clients.",
  "team": "Equipe Platform", "version": "v1",
  "endpoints": [
    {"method": "POST", "path": "/v1/alerts"},
    {"method": "GET", "path": "/v1/alerts?status=active"},
    {"method": "PUT", "path": "/v1/alerts/{id}/acknowledge"},
    {"method": "PUT", "path": "/v1/alerts/{id}/resolve"},
    {"method": "GET", "path": "/v1/alerts/rules"},
  ]
},
{
  "id": "webhook-api", "filename": "webhook-api.json",
  "name": "Webhook API",
  "description": "Gestion des webhooks. Enregistrement, validation et diffusion d'événements vers des endpoints externes.",
  "team": "Equipe Platform", "version": "v1",
  "endpoints": [
    {"method": "POST", "path": "/v1/webhooks"},
    {"method": "GET", "path": "/v1/webhooks/{id}"},
    {"method": "PUT", "path": "/v1/webhooks/{id}"},
    {"method": "DELETE", "path": "/v1/webhooks/{id}"},
    {"method": "POST", "path": "/v1/webhooks/{id}/test"},
  ]
},

# ════════════════════════════════════════════════════════
# DOMAINE 5 — ANALYTICS & BI
# ════════════════════════════════════════════════════════

{
  "id": "analytics-api", "filename": "analytics-api.json",
  "name": "Analytics API",
  "description": "Agrégation et reporting des données métier. Rapports ventes, trafic et comportement utilisateur en temps réel.",
  "team": "Equipe Data", "version": "v1",
  "endpoints": [
    {"method": "GET", "path": "/v1/analytics/sales"},
    {"method": "GET", "path": "/v1/analytics/traffic"},
    {"method": "GET", "path": "/v1/analytics/conversion"},
    {"method": "POST", "path": "/v1/analytics/reports"},
    {"method": "GET", "path": "/v1/analytics/dashboard"},
  ]
},
{
  "id": "reporting-api", "filename": "reporting-api.json",
  "name": "Reporting API",
  "description": "Génération de rapports personnalisés et exports. PDF, Excel et tableaux de bord planifiés. Faux positif avec Analytics API — Reporting génère des documents, Analytics agrège des métriques.",
  "team": "Equipe Data", "version": "v1",
  "endpoints": [
    {"method": "POST", "path": "/v1/reports/generate"},
    {"method": "GET", "path": "/v1/reports/{id}"},
    {"method": "GET", "path": "/v1/reports/{id}/download"},
    {"method": "POST", "path": "/v1/reports/schedule"},
    {"method": "GET", "path": "/v1/reports/templates"},
  ]
},
{
  "id": "metrics-api", "filename": "metrics-api.json",
  "name": "Metrics API",
  "description": "Collecte et agrégation de métriques techniques et business. KPIs temps réel et historiques. Faux positif avec Analytics API — Metrics est orienté ingénierie, Analytics orienté business.",
  "team": "Equipe Data", "version": "v1",
  "endpoints": [
    {"method": "POST", "path": "/v1/metrics"},
    {"method": "GET", "path": "/v1/metrics/{name}?from={ts}&to={ts}"},
    {"method": "GET", "path": "/v1/metrics/kpis"},
    {"method": "POST", "path": "/v1/metrics/query"},
  ]
},
{
  "id": "event-tracking-api", "filename": "event-tracking-api.json",
  "name": "Event Tracking API",
  "description": "Collecte des événements utilisateurs pour l'analyse comportementale. Clics, pages vues, funnels.",
  "team": "Equipe Data", "version": "v1",
  "endpoints": [
    {"method": "POST", "path": "/v1/events/track"},
    {"method": "POST", "path": "/v1/events/batch"},
    {"method": "GET", "path": "/v1/events/funnels/{funnelId}"},
    {"method": "GET", "path": "/v1/events/sessions/{userId}"},
  ]
},
{
  "id": "ab-testing-api", "filename": "ab-testing-api.json",
  "name": "A/B Testing API",
  "description": "Gestion des expérimentations et tests A/B. Création de variantes, assignation et analyse des résultats.",
  "team": "Equipe Data", "version": "v1",
  "endpoints": [
    {"method": "POST", "path": "/v1/experiments"},
    {"method": "GET", "path": "/v1/experiments/{id}"},
    {"method": "POST", "path": "/v1/experiments/{id}/assign"},
    {"method": "POST", "path": "/v1/experiments/{id}/convert"},
    {"method": "GET", "path": "/v1/experiments/{id}/results"},
  ]
},
{
  "id": "data-export-api", "filename": "data-export-api.json",
  "name": "Data Export API",
  "description": "Export massif de données en CSV, JSON ou Parquet. Jobs asynchrones et liens de téléchargement sécurisés.",
  "team": "Equipe Data", "version": "v1",
  "endpoints": [
    {"method": "POST", "path": "/v1/exports"},
    {"method": "GET", "path": "/v1/exports/{jobId}/status"},
    {"method": "GET", "path": "/v1/exports/{jobId}/download"},
    {"method": "DELETE", "path": "/v1/exports/{jobId}"},
  ]
},

# ════════════════════════════════════════════════════════
# DOMAINE 6 — CRM & MARKETING
# ════════════════════════════════════════════════════════

{
  "id": "crm-contact-api", "filename": "crm-contact-api.json",
  "name": "CRM Contact API",
  "description": "Gestion des contacts CRM. Création, enrichissement et segmentation des contacts clients et prospects.",
  "team": "Equipe CRM", "version": "v1",
  "endpoints": [
    {"method": "POST", "path": "/v1/crm/contacts"},
    {"method": "GET", "path": "/v1/crm/contacts/{id}"},
    {"method": "PUT", "path": "/v1/crm/contacts/{id}"},
    {"method": "DELETE", "path": "/v1/crm/contacts/{id}"},
    {"method": "POST", "path": "/v1/crm/contacts/search"},
  ]
},
{
  "id": "lead-api", "filename": "lead-api.json",
  "name": "Lead API",
  "description": "Gestion des prospects et leads commerciaux. Scoring, qualification et assignation aux commerciaux. Faux positif avec CRM Contact — Lead gère les prospects non-clients, Contact gère tous les contacts.",
  "team": "Equipe CRM", "version": "v1",
  "endpoints": [
    {"method": "POST", "path": "/v1/leads"},
    {"method": "GET", "path": "/v1/leads/{id}"},
    {"method": "PUT", "path": "/v1/leads/{id}/qualify"},
    {"method": "PUT", "path": "/v1/leads/{id}/assign"},
    {"method": "GET", "path": "/v1/leads/score/{id}"},
  ]
},
{
  "id": "campaign-api", "filename": "campaign-api.json",
  "name": "Campaign API",
  "description": "Gestion des campagnes marketing multicanal. Création, planification et suivi des performances.",
  "team": "Equipe Marketing", "version": "v1",
  "endpoints": [
    {"method": "POST", "path": "/v1/campaigns"},
    {"method": "GET", "path": "/v1/campaigns/{id}"},
    {"method": "PUT", "path": "/v1/campaigns/{id}/launch"},
    {"method": "PUT", "path": "/v1/campaigns/{id}/pause"},
    {"method": "GET", "path": "/v1/campaigns/{id}/stats"},
  ]
},
{
  "id": "loyalty-points-api", "filename": "loyalty-points-api.json",
  "name": "Loyalty Points API",
  "description": "Gestion des points de fidélité clients. Accumulation, consultation et utilisation des points de récompense.",
  "team": "Equipe CRM", "version": "v1",
  "endpoints": [
    {"method": "GET", "path": "/v1/loyalty/{customerId}"},
    {"method": "POST", "path": "/v1/loyalty/earn"},
    {"method": "POST", "path": "/v1/loyalty/redeem"},
    {"method": "GET", "path": "/v1/loyalty/{customerId}/history"},
  ]
},
{
  "id": "referral-api", "filename": "referral-api.json",
  "name": "Referral API",
  "description": "Programme de parrainage et codes de référence. Création des codes, tracking et récompenses.",
  "team": "Equipe Marketing", "version": "v1",
  "endpoints": [
    {"method": "POST", "path": "/v1/referrals/generate"},
    {"method": "GET", "path": "/v1/referrals/{code}"},
    {"method": "POST", "path": "/v1/referrals/validate"},
    {"method": "GET", "path": "/v1/referrals/{userId}/stats"},
  ]
},
{
  "id": "segmentation-api", "filename": "segmentation-api.json",
  "name": "Segmentation API",
  "description": "Segmentation automatique des clients. Création de segments basés sur le comportement et les attributs.",
  "team": "Equipe CRM", "version": "v1",
  "endpoints": [
    {"method": "POST", "path": "/v1/segments"},
    {"method": "GET", "path": "/v1/segments/{id}/members"},
    {"method": "PUT", "path": "/v1/segments/{id}/rules"},
    {"method": "POST", "path": "/v1/segments/preview"},
  ]
},

# ════════════════════════════════════════════════════════
# DOMAINE 7 — RH & ORGANISATION
# ════════════════════════════════════════════════════════

{
  "id": "hr-api", "filename": "hr-api.json",
  "name": "HR API",
  "description": "API RH centrale. Gestion des dossiers employés, organigramme et processus RH.",
  "team": "Equipe RH", "version": "v1",
  "endpoints": [
    {"method": "GET", "path": "/v1/hr/employees"},
    {"method": "POST", "path": "/v1/hr/employees"},
    {"method": "GET", "path": "/v1/hr/org-chart"},
    {"method": "GET", "path": "/v1/hr/departments"},
  ]
},
{
  "id": "payroll-api", "filename": "payroll-api.json",
  "name": "Payroll API",
  "description": "Gestion de la paie et des bulletins de salaire. Calcul des rémunérations, charges et virements.",
  "team": "Equipe RH", "version": "v1",
  "endpoints": [
    {"method": "POST", "path": "/v1/payroll/run"},
    {"method": "GET", "path": "/v1/payroll/{employeeId}/slips"},
    {"method": "GET", "path": "/v1/payroll/{employeeId}/slips/{month}"},
    {"method": "POST", "path": "/v1/payroll/simulate"},
  ]
},
{
  "id": "leave-api", "filename": "leave-api.json",
  "name": "Leave API",
  "description": "Gestion des congés et absences. Demandes, validations et soldes de congés.",
  "team": "Equipe RH", "version": "v1",
  "endpoints": [
    {"method": "POST", "path": "/v1/leaves/request"},
    {"method": "GET", "path": "/v1/leaves/{employeeId}"},
    {"method": "PUT", "path": "/v1/leaves/{id}/approve"},
    {"method": "PUT", "path": "/v1/leaves/{id}/reject"},
    {"method": "GET", "path": "/v1/leaves/{employeeId}/balance"},
  ]
},
{
  "id": "recruitment-api", "filename": "recruitment-api.json",
  "name": "Recruitment API",
  "description": "Gestion du recrutement et des candidatures. Offres d'emploi, candidats et processus de sélection.",
  "team": "Equipe RH", "version": "v1",
  "endpoints": [
    {"method": "POST", "path": "/v1/jobs"},
    {"method": "GET", "path": "/v1/jobs"},
    {"method": "POST", "path": "/v1/jobs/{id}/apply"},
    {"method": "GET", "path": "/v1/jobs/{id}/candidates"},
    {"method": "PUT", "path": "/v1/candidates/{id}/status"},
  ]
},
{
  "id": "performance-api", "filename": "performance-api.json",
  "name": "Performance API",
  "description": "Évaluations de performance et objectifs. OKRs, feedback 360° et plans de développement.",
  "team": "Equipe RH", "version": "v1",
  "endpoints": [
    {"method": "POST", "path": "/v1/performance/reviews"},
    {"method": "GET", "path": "/v1/performance/{employeeId}"},
    {"method": "POST", "path": "/v1/performance/objectives"},
    {"method": "PUT", "path": "/v1/performance/objectives/{id}/progress"},
  ]
},
{
  "id": "training-api", "filename": "training-api.json",
  "name": "Training API",
  "description": "Gestion de la formation professionnelle. Catalogue de formations, inscriptions et suivi des compétences.",
  "team": "Equipe RH", "version": "v1",
  "endpoints": [
    {"method": "GET", "path": "/v1/trainings"},
    {"method": "POST", "path": "/v1/trainings/{id}/enroll"},
    {"method": "GET", "path": "/v1/trainings/{employeeId}/completed"},
    {"method": "GET", "path": "/v1/skills/{employeeId}"},
  ]
},

# ════════════════════════════════════════════════════════
# DOMAINE 8 — INFRASTRUCTURE & PLATFORM
# ════════════════════════════════════════════════════════

{
  "id": "file-storage-api", "filename": "file-storage-api.json",
  "name": "File Storage API",
  "description": "Stockage et gestion de fichiers. Upload, téléchargement et organisation des documents.",
  "team": "Equipe Platform", "version": "v1",
  "endpoints": [
    {"method": "POST", "path": "/v1/files/upload"},
    {"method": "GET", "path": "/v1/files/{id}"},
    {"method": "DELETE", "path": "/v1/files/{id}"},
    {"method": "GET", "path": "/v1/files/{id}/download"},
    {"method": "POST", "path": "/v1/files/presigned-url"},
  ]
},
{
  "id": "media-api", "filename": "media-api.json",
  "name": "Media API",
  "description": "Gestion des médias images et vidéos. Upload, redimensionnement, optimisation et CDN. Faux positif avec File Storage — Media traite les fichiers multimédias, Storage tous les types.",
  "team": "Equipe Platform", "version": "v1",
  "endpoints": [
    {"method": "POST", "path": "/v1/media/upload"},
    {"method": "GET", "path": "/v1/media/{id}"},
    {"method": "POST", "path": "/v1/media/{id}/resize"},
    {"method": "GET", "path": "/v1/media/{id}/cdn-url"},
    {"method": "DELETE", "path": "/v1/media/{id}"},
  ]
},
{
  "id": "config-api", "filename": "config-api.json",
  "name": "Config API",
  "description": "Gestion de la configuration applicative. Feature flags, paramètres et variables d'environnement.",
  "team": "Equipe Platform", "version": "v1",
  "endpoints": [
    {"method": "GET", "path": "/v1/config/{key}"},
    {"method": "PUT", "path": "/v1/config/{key}"},
    {"method": "GET", "path": "/v1/config/features"},
    {"method": "PUT", "path": "/v1/config/features/{flag}/toggle"},
  ]
},
{
  "id": "health-api", "filename": "health-api.json",
  "name": "Health Check API",
  "description": "Monitoring de la santé des services. Status, disponibilité et métriques de performance.",
  "team": "Equipe Platform", "version": "v1",
  "endpoints": [
    {"method": "GET", "path": "/v1/health"},
    {"method": "GET", "path": "/v1/health/services"},
    {"method": "GET", "path": "/v1/health/dependencies"},
    {"method": "GET", "path": "/v1/health/metrics"},
  ]
},
{
  "id": "audit-log-api", "filename": "audit-log-api.json",
  "name": "Audit Log API",
  "description": "Journal d'audit et traçabilité des actions. Enregistrement de toutes les opérations sensibles.",
  "team": "Equipe Security", "version": "v1",
  "endpoints": [
    {"method": "GET", "path": "/v1/audit/logs"},
    {"method": "GET", "path": "/v1/audit/logs?userId={id}"},
    {"method": "GET", "path": "/v1/audit/logs?resource={type}"},
    {"method": "POST", "path": "/v1/audit/export"},
  ]
},
{
  "id": "rate-limit-api", "filename": "rate-limit-api.json",
  "name": "Rate Limit API",
  "description": "Gestion des limites de débit par client et endpoint. Configuration des quotas et blacklists.",
  "team": "Equipe Platform", "version": "v1",
  "endpoints": [
    {"method": "GET", "path": "/v1/rate-limits/{clientId}"},
    {"method": "PUT", "path": "/v1/rate-limits/{clientId}"},
    {"method": "DELETE", "path": "/v1/rate-limits/{clientId}/reset"},
    {"method": "POST", "path": "/v1/rate-limits/blacklist"},
  ]
},
{
  "id": "api-key-api", "filename": "api-key-api.json",
  "name": "API Key API",
  "description": "Gestion des clés API et tokens d'accès. Création, révocation et rotation des clés.",
  "team": "Equipe Security", "version": "v1",
  "endpoints": [
    {"method": "POST", "path": "/v1/api-keys"},
    {"method": "GET", "path": "/v1/api-keys"},
    {"method": "DELETE", "path": "/v1/api-keys/{id}"},
    {"method": "POST", "path": "/v1/api-keys/{id}/rotate"},
  ]
},

# ════════════════════════════════════════════════════════
# DOMAINE 9 — SUPPLY CHAIN & B2B
# ════════════════════════════════════════════════════════

{
  "id": "supplier-api", "filename": "supplier-api.json",
  "name": "Supplier API",
  "description": "Gestion des fournisseurs et partenaires B2B. Catalogue fournisseurs, contrats et évaluations.",
  "team": "Equipe Supply", "version": "v1",
  "endpoints": [
    {"method": "POST", "path": "/v1/suppliers"},
    {"method": "GET", "path": "/v1/suppliers/{id}"},
    {"method": "PUT", "path": "/v1/suppliers/{id}"},
    {"method": "GET", "path": "/v1/suppliers/{id}/products"},
    {"method": "POST", "path": "/v1/suppliers/{id}/evaluate"},
  ]
},
{
  "id": "purchase-order-api", "filename": "purchase-order-api.json",
  "name": "Purchase Order API",
  "description": "Gestion des bons de commande fournisseurs. Création, validation et suivi des achats B2B. Faux positif avec Order API — Purchase Order concerne les achats internes, Order les ventes clients.",
  "team": "Equipe Supply", "version": "v1",
  "endpoints": [
    {"method": "POST", "path": "/v1/purchase-orders"},
    {"method": "GET", "path": "/v1/purchase-orders/{id}"},
    {"method": "PUT", "path": "/v1/purchase-orders/{id}/approve"},
    {"method": "GET", "path": "/v1/purchase-orders?supplierId={id}"},
    {"method": "PUT", "path": "/v1/purchase-orders/{id}/receive"},
  ]
},
{
  "id": "contract-api", "filename": "contract-api.json",
  "name": "Contract API",
  "description": "Gestion des contrats B2B et partenariats. Création, signature électronique et suivi des échéances.",
  "team": "Equipe Supply", "version": "v1",
  "endpoints": [
    {"method": "POST", "path": "/v1/contracts"},
    {"method": "GET", "path": "/v1/contracts/{id}"},
    {"method": "POST", "path": "/v1/contracts/{id}/sign"},
    {"method": "GET", "path": "/v1/contracts/expiring"},
  ]
},
{
  "id": "quote-api", "filename": "quote-api.json",
  "name": "Quote API",
  "description": "Génération et gestion des devis commerciaux. Création, envoi et conversion en commande. Faux positif avec Order API — Quote précède la commande, Order la concrétise.",
  "team": "Equipe Commerce", "version": "v1",
  "endpoints": [
    {"method": "POST", "path": "/v1/quotes"},
    {"method": "GET", "path": "/v1/quotes/{id}"},
    {"method": "POST", "path": "/v1/quotes/{id}/send"},
    {"method": "POST", "path": "/v1/quotes/{id}/convert-to-order"},
    {"method": "PUT", "path": "/v1/quotes/{id}/expire"},
  ]
},

# ════════════════════════════════════════════════════════
# DOMAINE 10 — SUPPORT & SERVICE CLIENT
# ════════════════════════════════════════════════════════

{
  "id": "ticket-api", "filename": "ticket-api.json",
  "name": "Ticket API",
  "description": "Gestion des tickets de support client. Création, assignation, escalade et résolution des incidents.",
  "team": "Equipe Support", "version": "v1",
  "endpoints": [
    {"method": "POST", "path": "/v1/tickets"},
    {"method": "GET", "path": "/v1/tickets/{id}"},
    {"method": "PUT", "path": "/v1/tickets/{id}/assign"},
    {"method": "PUT", "path": "/v1/tickets/{id}/escalate"},
    {"method": "PUT", "path": "/v1/tickets/{id}/close"},
    {"method": "POST", "path": "/v1/tickets/{id}/comments"},
  ]
},
{
  "id": "knowledge-base-api", "filename": "knowledge-base-api.json",
  "name": "Knowledge Base API",
  "description": "Base de connaissances et FAQ. Gestion des articles, recherche et suggestions automatiques.",
  "team": "Equipe Support", "version": "v1",
  "endpoints": [
    {"method": "GET", "path": "/v1/kb/articles"},
    {"method": "POST", "path": "/v1/kb/articles"},
    {"method": "GET", "path": "/v1/kb/articles/{id}"},
    {"method": "GET", "path": "/v1/kb/search?q={query}"},
    {"method": "GET", "path": "/v1/kb/suggest?ticketId={id}"},
  ]
},
{
  "id": "chatbot-api", "filename": "chatbot-api.json",
  "name": "Chatbot API",
  "description": "Chatbot de support automatisé. Réponses FAQ, escalade vers humain et historique des conversations.",
  "team": "Equipe Support", "version": "v1",
  "endpoints": [
    {"method": "POST", "path": "/v1/chatbot/message"},
    {"method": "GET", "path": "/v1/chatbot/sessions/{sessionId}"},
    {"method": "POST", "path": "/v1/chatbot/escalate"},
    {"method": "GET", "path": "/v1/chatbot/intents"},
  ]
},
{
  "id": "survey-api", "filename": "survey-api.json",
  "name": "Survey API",
  "description": "Gestion des enquêtes de satisfaction. Création, envoi et analyse des résultats NPS et CSAT.",
  "team": "Equipe Support", "version": "v1",
  "endpoints": [
    {"method": "POST", "path": "/v1/surveys"},
    {"method": "POST", "path": "/v1/surveys/{id}/send"},
    {"method": "POST", "path": "/v1/surveys/{id}/respond"},
    {"method": "GET", "path": "/v1/surveys/{id}/results"},
    {"method": "GET", "path": "/v1/surveys/nps"},
  ]
},

# ════════════════════════════════════════════════════════
# DOMAINE 11 — LOCALISATION & GÉO
# ════════════════════════════════════════════════════════

{
  "id": "geolocation-api", "filename": "geolocation-api.json",
  "name": "Geolocation API",
  "description": "Services de géolocalisation et cartographie. Conversion d'adresses, calcul de distances et zones de livraison.",
  "team": "Equipe Platform", "version": "v1",
  "endpoints": [
    {"method": "POST", "path": "/v1/geo/geocode"},
    {"method": "POST", "path": "/v1/geo/reverse-geocode"},
    {"method": "POST", "path": "/v1/geo/distance"},
    {"method": "POST", "path": "/v1/geo/delivery-zone"},
  ]
},
{
  "id": "localization-api", "filename": "localization-api.json",
  "name": "Localization API",
  "description": "Traductions et localisation du contenu. Gestion des langues, devises et formats régionaux. Faux positif avec Geolocation — Localization gère les textes, Geolocation les coordonnées.",
  "team": "Equipe Platform", "version": "v1",
  "endpoints": [
    {"method": "GET", "path": "/v1/l10n/translations/{lang}"},
    {"method": "GET", "path": "/v1/l10n/currencies"},
    {"method": "POST", "path": "/v1/l10n/translate"},
    {"method": "GET", "path": "/v1/l10n/formats/{country}"},
  ]
},
{
  "id": "store-locator-api", "filename": "store-locator-api.json",
  "name": "Store Locator API",
  "description": "Localisation des points de vente et magasins. Recherche par proximité, horaires et disponibilités.",
  "team": "Equipe Commerce", "version": "v1",
  "endpoints": [
    {"method": "GET", "path": "/v1/stores/nearby?lat={lat}&lng={lng}"},
    {"method": "GET", "path": "/v1/stores/{id}"},
    {"method": "GET", "path": "/v1/stores/{id}/hours"},
    {"method": "GET", "path": "/v1/stores/{id}/stock/{productId}"},
  ]
},

# ════════════════════════════════════════════════════════
# DOMAINE 12 — SÉCURITÉ & COMPLIANCE
# ════════════════════════════════════════════════════════

{
  "id": "encryption-api", "filename": "encryption-api.json",
  "name": "Encryption API",
  "description": "Chiffrement et déchiffrement des données sensibles. Gestion des clés et conformité RGPD.",
  "team": "Equipe Security", "version": "v1",
  "endpoints": [
    {"method": "POST", "path": "/v1/encrypt"},
    {"method": "POST", "path": "/v1/decrypt"},
    {"method": "POST", "path": "/v1/keys/generate"},
    {"method": "DELETE", "path": "/v1/keys/{id}"},
  ]
},
{
  "id": "gdpr-api", "filename": "gdpr-api.json",
  "name": "GDPR API",
  "description": "Conformité RGPD et droits des utilisateurs. Droit à l'oubli, portabilité et consentements.",
  "team": "Equipe Security", "version": "v1",
  "endpoints": [
    {"method": "POST", "path": "/v1/gdpr/delete-request"},
    {"method": "POST", "path": "/v1/gdpr/export-request"},
    {"method": "GET", "path": "/v1/gdpr/consents/{userId}"},
    {"method": "PUT", "path": "/v1/gdpr/consents/{userId}"},
    {"method": "GET", "path": "/v1/gdpr/requests/{id}/status"},
  ]
},
{
  "id": "compliance-api", "filename": "compliance-api.json",
  "name": "Compliance API",
  "description": "Vérifications de conformité réglementaire. KYC, AML et validations légales. Faux positif avec GDPR API — Compliance couvre toutes les réglementations, GDPR uniquement la protection des données.",
  "team": "Equipe Security", "version": "v1",
  "endpoints": [
    {"method": "POST", "path": "/v1/compliance/kyc/verify"},
    {"method": "GET", "path": "/v1/compliance/kyc/{userId}/status"},
    {"method": "POST", "path": "/v1/compliance/aml/check"},
    {"method": "GET", "path": "/v1/compliance/reports"},
  ]
},
{
  "id": "vulnerability-api", "filename": "vulnerability-api.json",
  "name": "Vulnerability API",
  "description": "Gestion des vulnérabilités et patches de sécurité. Scan, reporting et suivi de remédiation.",
  "team": "Equipe Security", "version": "v1",
  "endpoints": [
    {"method": "POST", "path": "/v1/vulnerabilities/scan"},
    {"method": "GET", "path": "/v1/vulnerabilities"},
    {"method": "PUT", "path": "/v1/vulnerabilities/{id}/remediate"},
    {"method": "GET", "path": "/v1/vulnerabilities/report"},
  ]
},

# ════════════════════════════════════════════════════════
# DOMAINE 13 — CATALOGUE PRODUITS AVANCÉ
# ════════════════════════════════════════════════════════

{
  "id": "recommendation-api", "filename": "recommendation-api.json",
  "name": "Recommendation API",
  "description": "Recommandations personnalisées de produits. Algorithmes collaboratifs et basés sur le contenu.",
  "team": "Equipe Data", "version": "v1",
  "endpoints": [
    {"method": "GET", "path": "/v1/recommendations/{userId}"},
    {"method": "GET", "path": "/v1/recommendations/similar/{productId}"},
    {"method": "GET", "path": "/v1/recommendations/trending"},
    {"method": "POST", "path": "/v1/recommendations/feedback"},
  ]
},
{
  "id": "bundle-api", "filename": "bundle-api.json",
  "name": "Bundle API",
  "description": "Gestion des offres groupées et kits produits. Création, tarification et disponibilité des bundles.",
  "team": "Equipe Catalog", "version": "v1",
  "endpoints": [
    {"method": "POST", "path": "/v1/bundles"},
    {"method": "GET", "path": "/v1/bundles/{id}"},
    {"method": "GET", "path": "/v1/bundles/{id}/price"},
    {"method": "GET", "path": "/v1/bundles/{id}/availability"},
  ]
},
{
  "id": "variant-api", "filename": "variant-api.json",
  "name": "Variant API",
  "description": "Gestion des variantes produits. Tailles, couleurs, options et combinaisons d'attributs.",
  "team": "Equipe Catalog", "version": "v1",
  "endpoints": [
    {"method": "GET", "path": "/v1/products/{id}/variants"},
    {"method": "POST", "path": "/v1/products/{id}/variants"},
    {"method": "PUT", "path": "/v1/variants/{id}"},
    {"method": "GET", "path": "/v1/variants/{id}/stock"},
  ]
},

# ════════════════════════════════════════════════════════
# DOMAINE 14 — OPÉRATIONS & WORKFLOW
# ════════════════════════════════════════════════════════

{
  "id": "workflow-api", "filename": "workflow-api.json",
  "name": "Workflow API",
  "description": "Orchestration de workflows métier. Définition, exécution et suivi des processus automatisés.",
  "team": "Equipe Platform", "version": "v1",
  "endpoints": [
    {"method": "POST", "path": "/v1/workflows"},
    {"method": "POST", "path": "/v1/workflows/{id}/start"},
    {"method": "GET", "path": "/v1/workflows/{id}/status"},
    {"method": "PUT", "path": "/v1/workflows/{id}/cancel"},
    {"method": "GET", "path": "/v1/workflows/{id}/history"},
  ]
},
{
  "id": "task-api", "filename": "task-api.json",
  "name": "Task API",
  "description": "Gestion des tâches et files d'attente asynchrones. Création, priorité et monitoring des jobs.",
  "team": "Equipe Platform", "version": "v1",
  "endpoints": [
    {"method": "POST", "path": "/v1/tasks"},
    {"method": "GET", "path": "/v1/tasks/{id}"},
    {"method": "PUT", "path": "/v1/tasks/{id}/cancel"},
    {"method": "GET", "path": "/v1/tasks/queue/stats"},
  ]
},
{
  "id": "schedule-api", "filename": "schedule-api.json",
  "name": "Schedule API",
  "description": "Planification de tâches récurrentes. Cron jobs, déclencheurs temporels et gestion des fuseaux horaires. Faux positif avec Task API — Schedule planifie, Task exécute.",
  "team": "Equipe Platform", "version": "v1",
  "endpoints": [
    {"method": "POST", "path": "/v1/schedules"},
    {"method": "GET", "path": "/v1/schedules/{id}"},
    {"method": "PUT", "path": "/v1/schedules/{id}/pause"},
    {"method": "PUT", "path": "/v1/schedules/{id}/resume"},
    {"method": "DELETE", "path": "/v1/schedules/{id}"},
  ]
},
{
  "id": "integration-api", "filename": "integration-api.json",
  "name": "Integration API",
  "description": "Connecteurs vers systèmes tiers. ERP, CRM externes, marketplaces et plateformes partenaires.",
  "team": "Equipe Platform", "version": "v1",
  "endpoints": [
    {"method": "GET", "path": "/v1/integrations"},
    {"method": "POST", "path": "/v1/integrations/{name}/connect"},
    {"method": "DELETE", "path": "/v1/integrations/{name}/disconnect"},
    {"method": "GET", "path": "/v1/integrations/{name}/sync"},
    {"method": "GET", "path": "/v1/integrations/{name}/status"},
  ]
},

# ════════════════════════════════════════════════════════
# DOMAINE 15 — MOBILE & DEVICE
# ════════════════════════════════════════════════════════

{
  "id": "device-api", "filename": "device-api.json",
  "name": "Device API",
  "description": "Gestion des appareils mobiles enregistrés. Tokens de notification, appareils de confiance et sessions.",
  "team": "Equipe Mobile", "version": "v1",
  "endpoints": [
    {"method": "POST", "path": "/v1/devices/register"},
    {"method": "DELETE", "path": "/v1/devices/{deviceId}"},
    {"method": "GET", "path": "/v1/devices/{userId}"},
    {"method": "PUT", "path": "/v1/devices/{deviceId}/trust"},
  ]
},
{
  "id": "app-version-api", "filename": "app-version-api.json",
  "name": "App Version API",
  "description": "Gestion des versions de l'application mobile. Vérification des mises à jour et notes de version.",
  "team": "Equipe Mobile", "version": "v1",
  "endpoints": [
    {"method": "GET", "path": "/v1/app/version/latest"},
    {"method": "POST", "path": "/v1/app/version/check"},
    {"method": "GET", "path": "/v1/app/version/{version}/changelog"},
    {"method": "GET", "path": "/v1/app/version/force-update"},
  ]
},
{
  "id": "offline-sync-api", "filename": "offline-sync-api.json",
  "name": "Offline Sync API",
  "description": "Synchronisation des données en mode hors-ligne. Gestion des conflits et réconciliation des données.",
  "team": "Equipe Mobile", "version": "v1",
  "endpoints": [
    {"method": "POST", "path": "/v1/sync/push"},
    {"method": "GET", "path": "/v1/sync/pull?since={timestamp}"},
    {"method": "POST", "path": "/v1/sync/resolve-conflict"},
    {"method": "GET", "path": "/v1/sync/status/{deviceId}"},
  ]
},

]

# ════════════════════════════════════════════════════════
# GÉNÉRATION DES FICHIERS
# ════════════════════════════════════════════════════════

def generate_file(api):
    filename = api["filename"]
    filepath = os.path.join(OUTPUT_DIR, filename)

    data = {
        "id": api["id"],
        "name": api["name"],
        "version": api.get("version", "v1"),
        "description": api["description"],
        "team": api["team"],
        "authentication": "Bearer Token JWT",
        "base_url": f"/{api.get('version', 'v1')}/{api['id'].replace('-api', '').replace('-api-v2', '').replace('-api-v3', '').replace('-api-v4', '')}",
        "endpoints": api["endpoints"],
        "tags": [api["team"].lower().replace("equipe ", ""), api.get("version", "v1")]
    }

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    return filename

if __name__ == "__main__":
    print(f"\n🚀 Génération de {len(APIS)} APIs dans {OUTPUT_DIR}/\n")
    generated = []
    for api in APIS:
        fname = generate_file(api)
        generated.append(fname)
        print(f"  ✅ {fname}")

    print(f"\n{'='*50}")
    print(f"  ✅ {len(generated)} fichiers générés dans ./{OUTPUT_DIR}/")
    print(f"  📂 Prêt à indexer dans Pinecone et Redis !")
    print(f"{'='*50}\n")

    # Résumé par domaine
    domains = {}
    for api in APIS:
        team = api["team"]
        domains[team] = domains.get(team, 0) + 1
    print("  Répartition par équipe :")
    for team, count in sorted(domains.items(), key=lambda x: -x[1]):
        print(f"  {team:<25} : {count} APIs")
