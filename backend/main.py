from database import SessionLocal
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session 
import models 
from database import engine
import schemas
from fastapi.middleware.cors import CORSMiddleware

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI(title="location MiNET API")
origins = [
    "http://localhost:5173",
    "http://localhost:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

@app.get("/items/{item_id}", response_model=schemas.ItemResponse)
def get_item(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()

    if db_item is None: 
        raise HTTPException(status_code=404, detail="Item not found")
    
    return db_item

@app.delete("/items/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if db_item is None: 
        raise HTTPException(status_code=404, detail="Item not found")
    
    db.delete(db_item)
    db.commit()

    return {"message": "Item deleted successfully"}


@app.put("/items/{item_id}", response_model=schemas.ItemResponse)
def update_item(item_id: int, item: schemas.ItemUpdate, db: Session = Depends(get_db)):
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    
    update_data = item.model_dump(exclude_unset=True)

    for cle, valeur in update_data.items():
        setattr(db_item, cle, valeur)
    
    db.commit()
    db.refresh(db_item)
    return db_item

@app.get("/association/{association_id}/items", response_model= list[schemas.ItemResponse])
def get_associations_items(association_id: int, db: Session=Depends(get_db)):
    db_items= db.query(models.Item).filter(models.Item.association_id== association_id).all()
    
    return db_items


