from pydantic import BaseModel
from typing import Optional 

class AssociationCreate(BaseModel):
    nom: str
    representant: str
    email: str
    mot_de_passe: str

class AssociationResponse(BaseModel):
    id: int
    nom: str
    representant: str
    email: str

    class Config:
        from_attributes = True

class ItemCreate(BaseModel):
    nom: str
    description: str
    prix_location: float
    caution: float
    image_url: Optional[str] = None
    association_id: int

class ItemUpdate(BaseModel):
    nom: Optional[str] = None
    description: Optional[str] = None
    prix_location: Optional[float] = None
    caution: Optional[float] = None
    image_url: Optional[str] = None
    association_id: Optional[int] = None

class ItemResponse(BaseModel):
    id: int
    nom: str
    description: str
    prix_location: float
    caution: float
    image_url: Optional[str] = None
    association_id: int

    class Config:
        from_attributes = True