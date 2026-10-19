from tests.conftest import DEMANDE

ITEM = {"nom": "Table", "description": "Table pliante", "prix_location": 2.5, "caution": 20}


def test_consultation_publique_sans_compte(client, asso_owner):
    """Les visiteurs (la majorité) consultent catalogues et objets sans se connecter."""
    asso = client.get("/associations/me", headers=asso_owner).json()
    item = client.post("/items/", json=ITEM, headers=asso_owner).json()

    assert [a["nom"] for a in client.get("/associations/").json()] == ["Club Photo"]
    assert [i["id"] for i in client.get("/items/").json()] == [item["id"]]
    assert client.get(f"/items/{item['id']}").json()["nom"] == "Table"
    assert len(client.get(f"/associations/{asso['id']}/items").json()) == 1
    assert client.get("/items/9999").status_code == 404


def test_gestion_impossible_sans_asso(client, make_user):
    headers = make_user("alice")
    assert client.get("/associations/me", headers=headers).status_code == 403
    assert client.put("/associations/me", json={"description": "x"}, headers=headers).status_code == 403
    assert client.post("/items/", json=ITEM, headers=headers).status_code == 403


def test_gestion_impossible_sans_connexion(client):
    assert client.get("/associations/me").status_code == 401
    assert client.post("/items/", json=ITEM).status_code == 401
    assert client.delete("/items/1").status_code == 401


def test_crud_item_par_le_proprietaire(client, asso_owner):
    asso = client.get("/associations/me", headers=asso_owner).json()
    item = client.post("/items/", json=ITEM, headers=asso_owner).json()
    assert item["association_id"] == asso["id"]

    r = client.put(f"/items/{item['id']}", json={"prix_location": 5}, headers=asso_owner)
    assert r.status_code == 200 and r.json()["prix_location"] == 5 and r.json()["nom"] == "Table"

    assert client.delete(f"/items/{item['id']}", headers=asso_owner).status_code == 200
    assert client.get(f"/items/{item['id']}").status_code == 404


def test_item_valeurs_invalides(client, asso_owner):
    assert client.post("/items/", json={**ITEM, "prix_location": -1}, headers=asso_owner).status_code == 422
    assert client.post("/items/", json={**ITEM, "nom": "x"}, headers=asso_owner).status_code == 422


def test_une_asso_ne_touche_pas_aux_items_d_une_autre(client, asso_owner, make_user, admin):
    item = client.post("/items/", json=ITEM, headers=asso_owner).json()

    bob = make_user("bob")
    d = client.post("/association-requests/", json={**DEMANDE, "nom": "Club Ciné"}, headers=bob).json()
    client.post(f"/admin/association-requests/{d['id']}/review", json={"decision": "approved"}, headers=admin)

    assert client.put(f"/items/{item['id']}", json={"prix_location": 0}, headers=bob).status_code == 403
    assert client.delete(f"/items/{item['id']}", headers=bob).status_code == 403
    assert client.get(f"/items/{item['id']}").json()["prix_location"] == 2.5


def test_modifier_son_association(client, asso_owner):
    r = client.put("/associations/me", json={"description": "Nouvelle description"}, headers=asso_owner)
    assert r.status_code == 200
    assert r.json()["description"] == "Nouvelle description" and r.json()["nom"] == "Club Photo"

    r = client.put("/associations/me", json={"nom": "Photo & Vidéo", "email": "pv@imt-bs.eu"}, headers=asso_owner)
    assert r.json()["nom"] == "Photo & Vidéo" and r.json()["email"] == "pv@imt-bs.eu"


def test_modifier_son_association_validations(client, asso_owner, make_user, admin):
    bob = make_user("bob")
    d = client.post("/association-requests/", json={**DEMANDE, "nom": "Club Ciné"}, headers=bob).json()
    client.post(f"/admin/association-requests/{d['id']}/review", json={"decision": "approved"}, headers=admin)

    assert client.put("/associations/me", json={"nom": "Club Ciné"}, headers=asso_owner).status_code == 409
    assert client.put("/associations/me", json={"nom": "Club Photo"}, headers=asso_owner).status_code == 200  # garder son propre nom
    assert client.put("/associations/me", json={"nom": None}, headers=asso_owner).status_code == 422
    assert client.put("/associations/me", json={"email": "pas-un-mail"}, headers=asso_owner).status_code == 422


def test_suppression_d_une_asso_reservee_aux_admins(client, asso_owner, admin):
    asso = client.get("/associations/me", headers=asso_owner).json()
    assert client.delete(f"/associations/{asso['id']}").status_code == 401
    assert client.delete(f"/associations/{asso['id']}", headers=asso_owner).status_code == 403
    assert client.delete(f"/associations/{asso['id']}", headers=admin).status_code == 200
    assert client.get("/associations/").json() == []


def test_suppression_d_une_asso_supprime_ses_items(client, asso_owner, admin):
    asso = client.get("/associations/me", headers=asso_owner).json()
    client.post("/items/", json=ITEM, headers=asso_owner)
    assert client.delete(f"/associations/{asso['id']}", headers=admin).status_code == 200
    assert client.get("/items/").json() == []
    assert client.get("/users/me", headers=asso_owner).json()["association"] is None


def test_consulter_une_association_par_id(client, asso_owner):
    asso = client.get("/associations/me", headers=asso_owner).json()
    r = client.get(f"/associations/{asso['id']}")
    assert r.status_code == 200 and r.json()["nom"] == "Club Photo"
    assert client.get("/associations/9999").status_code == 404
