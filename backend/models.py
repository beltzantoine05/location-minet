from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey

from database import Base

class Association(Base):
    __tablename__ = "associations"
    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String, unique=True, index=True)
    representant= Column(String)
    email = Column(String)
    mot_de_passe_hash = Column(String)

class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)

    association_id = Column(Integer, ForeignKey("associations.id"))
    nom = Column(String)
    description = Column(Text)
    prix_location = Column(Float)
    caution = Column(Float)
    image_url = Column(String)
