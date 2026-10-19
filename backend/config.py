import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent

# Charge backend/.env (sans écraser les variables déjà présentes dans l'environnement)
load_dotenv(BASE_DIR / ".env")

# La clé n'a volontairement aucune valeur par défaut : sans elle, l'app refuse de démarrer
SECRET_KEY = os.environ.get("SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY manquante : copie backend/.env.example vers backend/.env et remplis-la")

DATABASE_URL = os.environ.get("DATABASE_URL", f"sqlite:///{BASE_DIR / 'dev_database.db'}")

CORS_ORIGINS = [
    origin.strip()
    for origin in os.environ.get("CORS_ORIGINS", "http://localhost:5173,http://localhost:3000").split(",")
    if origin.strip()
]
