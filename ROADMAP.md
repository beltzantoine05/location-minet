# Roadmap : location-minet

Objectif : terminer la migration `User` ↔ `Association`, rendre l'app utilisable de bout en bout, puis la sécuriser et la fiabiliser.
Le détail des tâches à cocher est dans [TODO.md](TODO.md).

## Phase 0 : Remettre le projet d'aplomb (prérequis)
**But :** repartir d'une base propre et démarrable.
- Commiter ou trier les modifications en cours (`backend/*`, `App.jsx`).
- Supprimer les anciens `.db` (ils ont l'ancien schéma) et recréer la base.
- Nettoyer `main.py` (imports en double, routes dupliquées).

**Critère de sortie :** `uvicorn main:app` démarre, `/docs` s'affiche, la base se crée sans erreur.

## Phase 1 : Finir la migration User ↔ Association (bloquant)
**But :** que l'inscription, la connexion et le dashboard fonctionnent.
- Corriger `POST /register` (`mot_de_passe_hash`).
- Décider comment une association est créée et liée à un utilisateur (voir TODO).
- Corriger `POST /associations/`.
- Corriger `GET /associations/me` (renvoyer l'association de l'utilisateur, une seule déclaration).
- Corriger les vérifications de propriété des objets (`create/update/delete item`).

**Critère de sortie :** scénario complet via `/docs` : register → token → créer asso → créer, modifier, supprimer un objet.

## Phase 2 : Sécurité
**But :** retirer les failles évidentes avant tout déploiement.
- `SECRET_KEY` et config via `.env`.
- Protéger `DELETE /associations/{id}` et utiliser le champ `role`.
- Remplacer `datetime.utcnow()`.
- Gérer proprement les doublons username/email au register.

**Critère de sortie :** aucune route d'écriture accessible sans authentification ni droits.

## Phase 3 : Frontend aligné sur le nouveau backend
**But :** un front cohérent et sans duplication.
- Intercepteur axios pour le header `Authorization` (et gestion du 401).
- `Dashboard` et `Login` utilisent `AuthContext` au lieu du `localStorage` direct.
- Page d'inscription, textes de login à jour.
- Corriger `App.jsx` (nom du composant), la route `/asso/:id` et la page `Catalogue`.
- Variable d'environnement Vite pour l'URL de l'API.

**Critère de sortie :** parcours visiteur et parcours asso complets dans le navigateur, sans erreur console.

## Phase 4 : Fonctionnalités manquantes
**But :** compléter le produit.
- Page catalogue d'une association (`/asso/:id`).
- Images des objets (`image_url`, upload ou URL).
- Pages `Contact` et `Mentions légales`.
- Description pour les associations (affichée sur `Home` mais absente du modèle).
- Pistes ensuite : réservations/demandes de location, recherche et filtres.

## Phase 5 : Qualité et mise en production
**But :** pouvoir faire évoluer le projet sereinement.
- Migrations Alembic à la place de `create_all`.
- Tests backend (pytest + `TestClient`) pour auth et CRUD.
- README racine (installation, lancement, variables d'environnement).
- Découper `main.py` en routers, nettoyer `requirement.txt`.
- CORS et configuration de production, déploiement.

## Ordre conseillé
`Phase 0 → 1 → 2 → 3 → 4 → 5`. Les phases 1 et 3 sont liées : le front ne peut être testé que quand `/associations/me` marche.
