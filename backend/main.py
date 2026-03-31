from database import SessionLocal
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session 
import models 
from database import engine
import schemas

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI(title="location MiNET API")
models.Base.metadata.create_all(bind=engine)


@app.post("/associations/", response_model=schemas.AssociationResponse)
def create_association(asso : schemas.AssociationCreate, db: Session = Depends(get_db)):
    db_asso = models.Association(
        nom = asso.nom,
        representant = asso.representant,
        email = asso.email,
        mot_de_passe_hash = asso.mot_de_passe,
    )

    db.add(db_asso)
    db.commit()
    db.refresh(db_asso)
    
    return db_asso

@app.get("/association/", response_model=list[schemas.AssociationResponse])
def get_association(db: Session = Depends(get_db)):
    asso = db.query(models.Association).all()
    return asso

@app.post("/items/", response_model=schemas.ItemResponse)
def create_item( item : schemas.ItemCreate, db: Session = Depends(get_db)):
    db_item = models.Item(
        nom = item.nom,
        description = item.description,
        prix_location = item.prix_location,
        caution = item.caution,
        image_url = item.image_url,
        association_id = item.association_id,
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@app.get("/items/", response_model=list[schemas.ItemResponse])
def get_items(db: Session = Depends(get_db)):
    item = db.query(models.Item).all()
    return item

