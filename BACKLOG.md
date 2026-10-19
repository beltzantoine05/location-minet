# Backlog : idées pour les futures updates

Idées volontairement **hors périmètre de la v1**, à reprendre une fois le site en production.
Les tâches de la v1 sont dans [TODO.md](TODO.md), l'ordre dans [ROADMAP.md](ROADMAP.md).

Format : `- [ ] **Titre** : description (origine / contexte)`

## Modération et administration
- [ ] **Admin IA** : un agent IA qui traite les demandes de création d'association (`/admin/association-requests`). Pistes : compte `role=admin` dédié avec son propre token, ou clé d'API distincte avec des droits limités à la modération. À décider : l'IA tranche seule ou fait une pré-validation que l'humain confirme.
- [ ] **Historique et audit** : journal des décisions (qui a accepté/refusé, quand, pourquoi). `reviewed_by_id` et `reviewed_at` sont déjà stockés.
- [ ] **Gestion des rôles** : interface admin pour promouvoir ou rétrograder un utilisateur (aujourd'hui uniquement via `backend/create_admin.py`).

## Notifications
- [ ] **Notifications par email** : en plus de la notification interne (SMTP ou service d'envoi, modèles de mails, désinscription).
- [ ] **Préférences de notification** par utilisateur.
- [ ] **Notifications temps réel** (websocket ou polling) au lieu de les charger à l'ouverture de la page.

## Produit
- [ ] **Demandes de location / réservations** : calendrier de disponibilité, validation par l'asso, caution.
- [ ] **Recherche et filtres** dans les catalogues (nom, prix, asso).
- [ ] **Plusieurs représentants par association** (aujourd'hui une asso = un `User`, `representant_id` unique).
- [ ] **Logo d'association** et upload d'images pour les objets.
- [ ] **Possibilité de refaire une demande** avec historique des refus visible côté utilisateur.

## Technique
- [ ] **Pagination** de `GET /items/` et `GET /associations/` quand les catalogues grossiront.
- [ ] **Limitation des tentatives de connexion** (anti brute-force) sur `/token`.
- [ ] **Contrainte d'unicité en base** pour « une seule demande en attente par utilisateur » (aujourd'hui vérifiée seulement dans le code).
- [ ] **Authentification** : refresh token, réinitialisation du mot de passe, vérification de l'email campus.
- [ ] **Observabilité** : logs structurés, suivi d'erreurs.
- [ ] **CI** : lint et tests à chaque push.
