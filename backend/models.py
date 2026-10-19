from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    # Role de l'utilisateur ('student' pour les randoms et 'admin' pour les gérants du compte de l'asso
    role = Column(String, index=True, default="student")
    mot_de_passe_hash = Column(String)
    # Pour retrouver facilement l'asso qu'il gère
    association_dirigee = relationship("Association", back_populates="representant", uselist=False)
    demandes_association = relationship("AssociationRequest", foreign_keys="AssociationRequest.user_id", back_populates="demandeur")
    notifications = relationship("Notification", back_populates="user")

class Association(Base):
    __tablename__ = "associations"
    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String, unique=True, index=True)
    email = Column(String)
    description = Column(Text)
    # La clé étrangère vers User pour avoir son représentant (une asso par utilisateur)
    representant_id = Column(Integer, ForeignKey("users.id"), unique=True)
    representant = relationship("User", back_populates="association_dirigee")
    # Relation pour le catalogue de l'asso
    items = relationship("Item", back_populates="association", cascade="all, delete-orphan")

class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)

    #Clé étrangère vers l'asso qui détient l'item
    association_id = Column(Integer, ForeignKey("associations.id"))
    nom = Column(String)
    description = Column(Text)
    prix_location = Column(Float)
    caution = Column(Float)
    image_url = Column(String)
    # Pour retrouver facilement l'asso propriétaire
    association = relationship("Association", back_populates="items")


class AssociationRequest(Base):
    """Demande de création d'une association, à valider par un admin."""
    __tablename__ = "association_requests"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    nom = Column(String)
    email = Column(String)
    description = Column(Text)
    # Justification donnée par le demandeur (rôle dans l'asso, statuts, etc.)
    justification = Column(Text)
    # 'pending', 'approved' ou 'rejected'
    status = Column(String, index=True, default="pending")
    # Commentaire de l'admin (obligatoire en cas de refus)
    admin_comment = Column(Text)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    reviewed_at = Column(DateTime)
    reviewed_by_id = Column(Integer, ForeignKey("users.id"))

    demandeur = relationship("User", foreign_keys=[user_id], back_populates="demandes_association")
    reviewed_by = relationship("User", foreign_keys=[reviewed_by_id])

    # Exposés dans la liste admin pour savoir qui demande
    @property
    def demandeur_username(self):
        return self.demandeur.username

    @property
    def demandeur_email(self):
        return self.demandeur.email


class Notification(Base):
    """Notification interne affichée à l'utilisateur (ex : décision sur sa demande)."""
    __tablename__ = "notifications"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    message = Column(Text)
    lu = Column(Boolean, default=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="notifications")
