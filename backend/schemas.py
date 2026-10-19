from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator
from datetime import datetime
from typing import Literal, Optional

# --- UTILISATEURS (Comptes) ---
class UserCreate(BaseModel):
    username: str = Field(..., min_length=2, max_length=50)
    email: EmailStr
    mot_de_passe: str = Field(..., min_length=8)

    @field_validator('email')
    @classmethod
    def validate_campus_email(cls, v):
        allowed_domains = ["telecom-sudparis.eu", "imt-bs.eu"]
        domain = v.split('@')[1]
        if domain not in allowed_domains:
            raise ValueError(f"Veuillez utiliser une adresse du campus ({', '.join(allowed_domains)})")
        return v

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    role: str

    model_config = ConfigDict(from_attributes=True)

# --- ASSOCIATIONS ---
class AssociationCreate(BaseModel):
    nom: str = Field(..., min_length=2, max_length=100)
    email: EmailStr # Email de contact public de l'asso
    description: Optional[str] = None

class AssociationUpdate(BaseModel):
    nom: Optional[str] = Field(None, min_length=2, max_length=100)
    email: Optional[EmailStr] = None
    description: Optional[str] = None

class AssociationResponse(BaseModel):
    id: int
    nom: str
    email: str
    description: Optional[str] = None
    representant_id: int

    model_config = ConfigDict(from_attributes=True)

class UserMeResponse(UserResponse):
    # None pour la majorité des utilisateurs : ils consultent seulement le matériel
    association: Optional[AssociationResponse] = Field(None, validation_alias="association_dirigee")

# --- DEMANDES DE CREATION D'ASSOCIATION ---
class AssociationRequestCreate(BaseModel):
    nom: str = Field(..., min_length=2, max_length=100)
    email: EmailStr # Email de contact public de l'asso
    description: str = Field(..., min_length=10)
    justification: str = Field(..., min_length=10) # Role du demandeur dans l'asso, etc.

class AssociationRequestReview(BaseModel):
    decision: Literal["approved", "rejected"]
    admin_comment: Optional[str] = None

    @field_validator('admin_comment')
    @classmethod
    def strip_comment(cls, v):
        return v.strip() if v else v

class AssociationRequestResponse(BaseModel):
    id: int
    user_id: int
    nom: str
    email: str
    description: str
    justification: str
    status: str
    admin_comment: Optional[str] = None
    created_at: datetime
    reviewed_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

class AssociationRequestAdminResponse(AssociationRequestResponse):
    demandeur_username: str
    demandeur_email: str

# --- NOTIFICATIONS ---
class NotificationResponse(BaseModel):
    id: int
    message: str
    lu: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class UnreadCount(BaseModel):
    non_lues: int

# --- CATALOGUE (Items) ---
class ItemBase(BaseModel):
    nom: str = Field(..., min_length=2)
    description: str
    prix_location: float = Field(..., ge=0.0)
    caution: float = Field(..., ge=0.0)
    image_url: Optional[str] = None

class ItemCreate(ItemBase):
    pass # L'ID de l'asso sera injecté automatiquement par le backend

class ItemUpdate(BaseModel):
    nom: Optional[str] = Field(None, min_length=2)
    description: Optional[str] = None
    prix_location: Optional[float] = Field(None, ge=0.0)
    caution: Optional[float] = Field(None, ge=0.0)
    image_url: Optional[str] = None

class ItemResponse(ItemBase):
    id: int
    association_id: int

    model_config = ConfigDict(from_attributes=True)

# --- AUTHENTIFICATION ---
class Token(BaseModel):
    access_token: str
    token_type: str