from tests.conftest import DEMANDE


def review(client, admin, demande_id, **json):
    return client.post(f"/admin/association-requests/{demande_id}/review", json=json, headers=admin)


def test_demande_necessite_connexion(client):
    assert client.post("/association-requests/", json=DEMANDE).status_code == 401


def test_demande_champs_invalides(client, make_user):
    headers = make_user("alice")
    assert client.post("/association-requests/", json={**DEMANDE, "description": "court"}, headers=headers).status_code == 422
    assert client.post("/association-requests/", json={**DEMANDE, "email": "pas-un-mail"}, headers=headers).status_code == 422


def test_une_seule_demande_en_attente(client, make_user):
    headers = make_user("alice")
    r = client.post("/association-requests/", json=DEMANDE, headers=headers)
    assert r.status_code == 201 and r.json()["status"] == "pending"
    assert client.post("/association-requests/", json={**DEMANDE, "nom": "Autre"}, headers=headers).status_code == 409


def test_nom_deja_pris_par_une_asso(client, asso_owner, make_user):
    bob = make_user("bob")
    assert client.post("/association-requests/", json=DEMANDE, headers=bob).status_code == 409


def test_user_avec_asso_ne_peut_pas_redemander(client, asso_owner):
    assert client.post("/association-requests/", json={**DEMANDE, "nom": "Autre"}, headers=asso_owner).status_code == 409


def test_mes_demandes(client, make_user):
    headers = make_user("alice")
    client.post("/association-requests/", json=DEMANDE, headers=headers)
    bob = make_user("bob")
    assert len(client.get("/association-requests/me", headers=headers).json()) == 1
    assert client.get("/association-requests/me", headers=bob).json() == []


def test_routes_admin_interdites_aux_non_admin(client, make_user):
    headers = make_user("alice")
    assert client.get("/admin/association-requests", headers=headers).status_code == 403
    assert client.post("/admin/association-requests/1/review", json={"decision": "approved"}, headers=headers).status_code == 403


def test_liste_admin_contient_le_demandeur_et_filtre(client, make_user, admin):
    headers = make_user("alice")
    client.post("/association-requests/", json=DEMANDE, headers=headers)
    liste = client.get("/admin/association-requests", headers=admin).json()
    assert liste[0]["demandeur_username"] == "alice"
    assert liste[0]["demandeur_email"] == "alice@imt-bs.eu"
    assert client.get("/admin/association-requests?status_filter=approved", headers=admin).json() == []


def test_acceptation_cree_l_asso_et_notifie(client, make_user, admin):
    headers = make_user("alice")
    demande = client.post("/association-requests/", json=DEMANDE, headers=headers).json()
    r = review(client, admin, demande["id"], decision="approved")
    assert r.status_code == 200 and r.json()["status"] == "approved"

    asso = client.get("/associations/me", headers=headers).json()
    assert asso["nom"] == "Club Photo"
    assert asso["description"] == DEMANDE["description"]
    notifs = client.get("/notifications/me", headers=headers).json()
    assert len(notifs) == 1 and "acceptée" in notifs[0]["message"]


def test_refus_exige_un_motif_puis_notifie(client, make_user, admin):
    headers = make_user("alice")
    demande = client.post("/association-requests/", json=DEMANDE, headers=headers).json()
    assert review(client, admin, demande["id"], decision="rejected").status_code == 422
    assert review(client, admin, demande["id"], decision="rejected", admin_comment="   ").status_code == 422

    r = review(client, admin, demande["id"], decision="rejected", admin_comment="Pas de statuts fournis")
    assert r.status_code == 200 and r.json()["status"] == "rejected"
    assert client.get("/associations/me", headers=headers).status_code == 403
    message = client.get("/notifications/me", headers=headers).json()[0]["message"]
    assert "refusée" in message and "Pas de statuts fournis" in message


def test_demande_deja_traitee_ou_inconnue(client, make_user, admin):
    headers = make_user("alice")
    demande = client.post("/association-requests/", json=DEMANDE, headers=headers).json()
    assert review(client, admin, demande["id"], decision="approved").status_code == 200
    assert review(client, admin, demande["id"], decision="approved").status_code == 409
    assert review(client, admin, 9999, decision="approved").status_code == 404


def test_apres_un_refus_on_peut_redemander(client, make_user, admin):
    headers = make_user("alice")
    demande = client.post("/association-requests/", json=DEMANDE, headers=headers).json()
    review(client, admin, demande["id"], decision="rejected", admin_comment="Incomplet")
    assert client.post("/association-requests/", json=DEMANDE, headers=headers).status_code == 201


def test_decision_invalide(client, make_user, admin):
    headers = make_user("alice")
    demande = client.post("/association-requests/", json=DEMANDE, headers=headers).json()
    assert review(client, admin, demande["id"], decision="peut-etre").status_code == 422
