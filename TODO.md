# TODO : location-minet

Voir [ROADMAP.md](ROADMAP.md) pour l'ordre et les objectifs de chaque phase.
Légende : 🔴 bloquant · 🟠 important · 🟡 amélioration

## Phase 0 : Remettre le projet d'aplomb
- [x] 🔴 Supprimer `backend/dev_database.db` et `backend/location_minet.db` (ancien schéma) pour recréer la base
- [ ] 🟠 Commiter les changements en cours (`backend/*`, `frontend/src/App.jsx`) une fois la phase 1 testée
- [x] 🟡 Nettoyer `backend/main.py` : retirer les imports en double (`auth`, `HTTPException`) et le `oauth2_scheme` inutilisé
- [x] 🟡 Ajouter `.idea/` au `.gitignore`

## Commandes backend (depuis `backend/`)
```bash
cp .env.example .env            # puis remplir SECRET_KEY (python -c "import secrets; print(secrets.token_urlsafe(64))")
uv venv --clear --python 3.14 venv && uv pip install --python venv/bin/python -r requirement.txt
venv/bin/alembic upgrade head   # crée/met à jour la base
venv/bin/python create_admin.py <username> <email> <mot_de_passe>
venv/bin/uvicorn main:app --reload
venv/bin/python -m pytest       # tests
venv/bin/alembic revision --autogenerate -m "description"   # après un changement de models.py
```
Note : `create_all` n'est plus appelé, la base se crée uniquement via `alembic upgrade head`.

## Phase 1 : Migration User ↔ Association
> Flux retenu : un utilisateur connecté fait une **demande de création d'asso** (formulaire) → un admin (humain ou agent IA, via un compte `role=admin`) l'accepte ou la refuse → l'utilisateur reçoit une notification et gère ensuite la page de son asso.
> Backend terminé et testé (34 tests `pytest`) : `AssociationRequest` et `Notification` dans `models.py`, routes `/association-requests/`, `/admin/association-requests`, `/admin/association-requests/{id}/review`, `/notifications/me` (+ `?non_lues=true`, `/unread-count`, `/read-all`), `/users/me` (avec `role` et `association`, `null` pour la plupart des utilisateurs), `PUT /associations/me`, script `backend/create_admin.py`.
- [x] 🔴 Décider du flux de création d'une asso (une asso créée à l'inscription ? par un admin ? par un user connecté ?)
- [x] 🔴 `main.py` `/register` : remplacer `mot_de_passe=` par `mot_de_passe_hash=`
- [x] 🔴 `main.py` `POST /associations/` : supprimer `mot_de_passe` / `representant`, définir `representant_id` à partir de l'utilisateur connecté (route protégée)
- [x] 🔴 `main.py` `GET /associations/me` : garder une seule déclaration, la placer **avant** `/associations/{association_id}/...`, renvoyer `current_user.association_dirigee` (404 si le user n'a pas d'asso)
- [x] 🔴 `main.py` items (`create`, `update`, `delete`) : utiliser `current_user.association_dirigee.id` au lieu de `current_user.id`, et renvoyer 403 si l'utilisateur n'a pas d'asso
- [x] 🟠 Routes items : `current_asso` reçoit maintenant vraiment une `Association` (via `auth.get_current_association`), le nom est donc cohérent
- [x] 🟠 Tester le scénario complet dans `/docs` : register → token → créer asso → CRUD objets

- [x] 🔴 Réparer le venv `backend/venv` : recréé avec `uv` (Python 3.14), `email-validator` et `httpx` ajoutés à `requirement.txt`. Pour le réinstaller : `uv venv --clear --python 3.14 venv && uv pip install --python venv/bin/python -r requirement.txt`
- [ ] 🔴 Créer le premier compte admin avec `create_admin.py` (voir commandes ci-dessus, à faire par toi : tu choisis le mot de passe)
- [x] 🟠 Agent IA admin : reporté à une update post-mise en prod (voir [BACKLOG.md](BACKLOG.md)). En attendant, modération par un compte `role=admin`
- [x] 🟠 Notifications : on garde le système interne uniquement (`GET /notifications/me`). L'email est reporté en post-prod (voir [BACKLOG.md](BACKLOG.md))
- [ ] 🟠 Front : formulaire de demande (nom, email, description, justification) et suivi de son statut
- [ ] 🟠 Front : page admin (liste des demandes en attente, accepter/refuser avec motif)
- [ ] 🟠 Front : affichage des notifications (cloche dans la `Navbar`) et dashboard réservé aux utilisateurs qui ont une asso (`/associations/me` renvoie 403 sinon)
- [x] 🟡 `PUT /associations/me` : modifier nom, email et description de son asso

## Phase 2 : Sécurité
- [x] 🔴 `SECRET_KEY` sortie de `auth.py` vers `backend/.env` (lu par `config.py`, l'app refuse de démarrer sans elle), `.env` ignoré par git, modèle dans `backend/.env.example`
- [x] 🔴 Protéger `DELETE /associations/{id}` (réservé aux admins pour l'instant)
- [x] 🟠 Utiliser le champ `role` : créer une dépendance `require_admin`
- [x] 🟠 `/register` : vérifier aussi l'unicité de l'**email** (le message le mentionne, le code ne teste que le username)
- [x] 🟠 Remplacer `datetime.utcnow()` par `datetime.now(timezone.utc)` dans `auth.py`
- [x] 🟡 Origines CORS configurables via `CORS_ORIGINS` dans le `.env`
- [x] 🟡 Nouvelle clé secrète générée (l'ancienne reste dans l'historique git mais n'est plus utilisée)

## Phase 3 : Frontend
- [ ] 🔴 `App.jsx` : renommer le composant `app` en `App`
- [ ] 🟠 `api/client.js` : ajouter un intercepteur de requête qui met `Authorization: Bearer <token>`, et un intercepteur de réponse qui gère le 401
- [ ] 🟠 `Dashboard.jsx` : retirer les `headers: { Authorization }` répétés et utiliser `useAuth()` (`asso`, `loading`, `isAuthenticated`) au lieu de refaire `/associations/me` et lire le `localStorage`
- [ ] 🟠 Créer une page `Register.jsx` (+ route `/register` + lien depuis `Login`), avec affichage de l'erreur de domaine email
- [ ] 🟠 `Login.jsx` : adapter les libellés (« nom d'utilisateur » et non plus « nom d'association »)
- [ ] 🟠 `Home.jsx` : supprimer `asso.description` ou ajouter le champ côté backend ; renommer `testerConnexionBackend`
- [ ] 🟡 Ajouter une route protégée (composant `ProtectedRoute`) pour `/dashboard`
- [ ] 🟡 URL de l'API dans `.env` Vite (`VITE_API_URL`) au lieu de `http://localhost:8000` en dur
- [ ] 🟡 Corriger la faute `apiCLient` dans `client.js`

## Phase 4 : Fonctionnalités
- [ ] 🟠 Implémenter `pages/Catalogue.jsx` (vide) et la route `/asso/:id` (le lien existe sur `Home`)
- [ ] 🟠 Gérer l'image des objets (champ `image_url` dans les formulaires, affichage dans le dashboard et le catalogue)
- [ ] 🟡 Page `Contact.jsx` (placeholder)
- [ ] 🟡 Page `Mention.jsx` (placeholder)
- [ ] 🟡 Ajouter `description` (et logo) au modèle `Association` + schémas
- [ ] 🟡 Le bouton « Catalogue » de la Navbar pointe vers `/` : lui donner une vraie destination
- [ ] 🟡 Idées : demandes de location / réservations, recherche et filtres

## Phase 5 : Qualité et production
- [ ] 🟠 Écrire un `README.md` racine : installation, lancement back (`uvicorn main:app --reload`) et front (`npm run dev`), variables d'environnement
- [x] 🟠 Alembic en place (`backend/migrations/`, migration initiale) à la place de `create_all`
- [x] 🟠 Tests backend : 34 tests `pytest` dans `backend/tests/` (auth, demandes, notifications, objets, droits)
- [ ] 🟡 Découper `main.py` en routers (`routers/auth.py`, `routers/associations.py`, `routers/items.py`)
- [ ] 🟡 Nettoyer `requirement.txt` (renommer en `requirements.txt`, retirer les dépendances inutilisées comme `ecdsa`/`PyYAML` si non requises)
- [ ] 🟡 Lancer `npm run lint` et corriger les avertissements
- [ ] 🟡 Config de production (CORS, base de données, déploiement)
