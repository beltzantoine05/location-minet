from tests.conftest import PASSWORD, login


def test_register_ok_et_role_student(client):
    r = client.post("/register", json={"username": "alice", "email": "alice@imt-bs.eu", "mot_de_passe": PASSWORD})
    assert r.status_code == 201
    assert r.json()["role"] == "student"
    assert "mot_de_passe" not in r.text


def test_register_username_ou_email_deja_pris(client, make_user):
    make_user("alice")
    assert client.post("/register", json={"username": "alice", "email": "autre@imt-bs.eu", "mot_de_passe": PASSWORD}).status_code == 400
    assert client.post("/register", json={"username": "autre", "email": "alice@imt-bs.eu", "mot_de_passe": PASSWORD}).status_code == 400


def test_register_refuse_domaine_hors_campus(client):
    r = client.post("/register", json={"username": "eve", "email": "eve@gmail.com", "mot_de_passe": PASSWORD})
    assert r.status_code == 422


def test_register_mot_de_passe_trop_court(client):
    r = client.post("/register", json={"username": "eve", "email": "eve@imt-bs.eu", "mot_de_passe": "court"})
    assert r.status_code == 422


def test_login_mauvais_mot_de_passe(client, make_user):
    make_user("alice")
    assert client.post("/token", data={"username": "alice", "password": "faux"}).status_code == 401
    assert client.post("/token", data={"username": "inconnu", "password": PASSWORD}).status_code == 401


def test_route_protegee_sans_token_ou_token_invalide(client):
    assert client.get("/users/me").status_code == 401
    assert client.get("/users/me", headers={"Authorization": "Bearer nimportequoi"}).status_code == 401


def test_users_me_sans_association(client, make_user):
    """Cas le plus courant : un utilisateur qui consulte seulement le matériel."""
    headers = make_user("alice")
    r = client.get("/users/me", headers=headers)
    assert r.status_code == 200
    body = r.json()
    assert body["username"] == "alice" and body["role"] == "student"
    assert body["association"] is None


def test_users_me_avec_association(client, asso_owner):
    body = client.get("/users/me", headers=asso_owner).json()
    assert body["association"]["nom"] == "Club Photo"
