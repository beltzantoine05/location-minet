import os
import tempfile

# Doit être posé AVANT l'import de l'app : base jetable et clé de test (jamais le .env réel)
_tmp_dir = tempfile.mkdtemp(prefix="location_minet_tests_")
os.environ["SECRET_KEY"] = "cle-de-test-uniquement"
os.environ["DATABASE_URL"] = f"sqlite:///{_tmp_dir}/test.db"

import pytest
from fastapi.testclient import TestClient

import auth
import models
from database import Base, SessionLocal, engine
from main import app


@pytest.fixture(autouse=True, scope="session")
def bcrypt_rapide():
    """bcrypt à 4 tours au lieu de 12 : mêmes hash, 250x plus rapide, uniquement pour les tests."""
    original = auth.bcrypt.gensalt
    auth.bcrypt.gensalt = lambda rounds=4, prefix=b"2b": original(rounds=4, prefix=prefix)
    yield
    auth.bcrypt.gensalt = original


@pytest.fixture(autouse=True)
def reset_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def db():
    session = SessionLocal()
    yield session
    session.close()


PASSWORD = "motdepasse123"


@pytest.fixture
def make_user(client):
    """Crée un utilisateur via l'API et renvoie ses headers d'authentification."""
    def _make(username: str, domain: str = "imt-bs.eu"):
        r = client.post("/register", json={"username": username, "email": f"{username}@{domain}", "mot_de_passe": PASSWORD})
        assert r.status_code == 201, r.text
        return login(client, username)
    return _make


def login(client, username: str, password: str = PASSWORD):
    r = client.post("/token", data={"username": username, "password": password})
    assert r.status_code == 200, r.text
    return {"Authorization": f"Bearer {r.json()['access_token']}"}


@pytest.fixture
def admin(client, db):
    db.add(models.User(username="admin", email="admin@imt-bs.eu", role="admin", mot_de_passe_hash=auth.get_password_hash(PASSWORD)))
    db.commit()
    return login(client, "admin")


DEMANDE = {
    "nom": "Club Photo",
    "email": "photo@imt-bs.eu",
    "description": "Club de photographie du campus",
    "justification": "Je suis le président du club",
}


@pytest.fixture
def asso_owner(client, make_user, admin):
    """Un utilisateur dont la demande d'association a été acceptée."""
    headers = make_user("alice")
    demande = client.post("/association-requests/", json=DEMANDE, headers=headers).json()
    r = client.post(f"/admin/association-requests/{demande['id']}/review", json={"decision": "approved"}, headers=admin)
    assert r.status_code == 200, r.text
    return headers
