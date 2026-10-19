"""Crée (ou promeut) un compte administrateur : python create_admin.py <username> <email> <mot_de_passe>
(la base doit exister : alembic upgrade head)"""
import sys

import auth
import models
from database import SessionLocal


def main(username: str, email: str, mot_de_passe: str):
    db = SessionLocal()
    try:
        user = db.query(models.User).filter(models.User.username == username).first()
        if user is None:
            user = models.User(
                username=username,
                email=email,
                mot_de_passe_hash=auth.get_password_hash(mot_de_passe),
            )
            db.add(user)
        user.role = "admin"
        db.commit()
        print(f"Admin « {username} » prêt.")
    finally:
        db.close()


if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    main(*sys.argv[1:])
