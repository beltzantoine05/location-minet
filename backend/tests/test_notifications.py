from tests.conftest import DEMANDE


def _demande_et_refus(client, headers, admin, nom):
    d = client.post("/association-requests/", json={**DEMANDE, "nom": nom}, headers=headers).json()
    client.post(f"/admin/association-requests/{d['id']}/review", json={"decision": "rejected", "admin_comment": "non"}, headers=admin)


def test_compteur_et_filtre_non_lues(client, make_user, admin):
    headers = make_user("alice")
    assert client.get("/notifications/me/unread-count", headers=headers).json() == {"non_lues": 0}
    _demande_et_refus(client, headers, admin, "Asso A")
    _demande_et_refus(client, headers, admin, "Asso B")
    assert client.get("/notifications/me/unread-count", headers=headers).json() == {"non_lues": 2}

    premiere = client.get("/notifications/me", headers=headers).json()[0]
    r = client.post(f"/notifications/{premiere['id']}/read", headers=headers)
    assert r.status_code == 200 and r.json()["lu"] is True
    assert client.get("/notifications/me/unread-count", headers=headers).json() == {"non_lues": 1}
    assert len(client.get("/notifications/me?non_lues=true", headers=headers).json()) == 1
    assert len(client.get("/notifications/me", headers=headers).json()) == 2


def test_tout_marquer_comme_lu(client, make_user, admin):
    headers = make_user("alice")
    _demande_et_refus(client, headers, admin, "Asso A")
    _demande_et_refus(client, headers, admin, "Asso B")
    assert client.post("/notifications/read-all", headers=headers).json() == {"non_lues": 0}
    assert client.get("/notifications/me?non_lues=true", headers=headers).json() == []


def test_on_ne_touche_pas_aux_notifications_des_autres(client, make_user, admin):
    alice, bob = make_user("alice"), make_user("bob")
    _demande_et_refus(client, alice, admin, "Asso A")
    notif_id = client.get("/notifications/me", headers=alice).json()[0]["id"]
    assert client.post(f"/notifications/{notif_id}/read", headers=bob).status_code == 404
    assert client.post("/notifications/read-all", headers=bob).status_code == 200
    assert client.get("/notifications/me/unread-count", headers=alice).json() == {"non_lues": 1}
    assert client.get("/notifications/me", headers=bob).json() == []


def test_notifications_necessitent_connexion(client):
    assert client.get("/notifications/me").status_code == 401
    assert client.get("/notifications/me/unread-count").status_code == 401
    assert client.post("/notifications/read-all").status_code == 401
