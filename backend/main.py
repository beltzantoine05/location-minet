from database import SessionLocal
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session 
import models 
from database import engine
import schemas
from fastapi.middleware.cors import CORSMiddleware
import auth
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import JWTError, jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_association(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Invalid token authentication",
        headers={"www-Authenticate": "Bearer"}
    )

    try:
        payload = jwt.decode(token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
        nom_asso: str = payload.get("sub")
        if nom_asso is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    asso = db.query(models.Association).filter(models.Association.nom == nom_asso).first()
    if asso is None:
        raise credentials_exception
    return asso

app = FastAPI(title="location MiNET API")
origins = [
    "http://localhost:5173",
    "http://localhost:3000"
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
    hashed_password = auth.get_password_hash(asso.mot_de_passe)
    
    db_asso = models.Association(
        nom = asso.nom,
        representant = asso.representant,
        email = asso.email,
        mot_de_passe_hash = hashed_password,
    )

    db.add(db_asso)
    db.commit()
    db.refresh(db_asso)
    
    return db_asso

@app.get("/associations/", response_model=list[schemas.AssociationResponse])
def get_association(db: Session = Depends(get_db)):
    asso = db.query(models.Association).all()
    return asso

@app.post("/token", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    
    asso = db.query(models.Association).filter(models.Association.nom == form_data.username).first()

    if not asso or not auth.verify_password(form_data.password, asso.mot_de_passe_hash):
        raise HTTPException(status_code=401, detail="Incorrect username or password", headers={"www-Authenticate": "Bearer"},)

    access_token = auth.create_access_token(data={"sub": asso.nom})

    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/items/", response_model=schemas.ItemResponse)
def create_item( item : schemas.ItemCreate, db: Session = Depends(get_db), current_asso: models.Association = Depends(get_current_association)):
    db_item = models.Item(
        nom = item.nom,
        description = item.description,
        prix_location = item.prix_location,
        caution = item.caution,
        image_url = item.image_url,
        association_id = current_asso.id,
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
def delete_item(item_id: int, db: Session = Depends(get_db), current_asso: models.Association = Depends(get_current_association)):
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if db_item is None: 
        raise HTTPException(status_code=404, detail="Item not found")
    if db_item.association_id != current_asso.id:
        raise HTTPException(status_code=403, detail="You are not authorized to delete this item")
    db.delete(db_item)
    db.commit()

    return {"message": "Item deleted successfully"}


@app.put("/items/{item_id}", response_model=schemas.ItemResponse)
def update_item(item_id: int, item: schemas.ItemUpdate, db: Session = Depends(get_db), current_asso: models.Association = Depends(get_current_association)):
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    if db_item.association_id != current_asso.id:
        raise HTTPException(status_code=403, detail="You are not authorized to update this item")
    update_data = item.model_dump(exclude_unset=True)

    for cle, valeur in update_data.items():
        setattr(db_item, cle, valeur)
    
    db.commit()
    db.refresh(db_item)
    return db_item

@app.get("/associations/{association_id}/items", response_model= list[schemas.ItemResponse])
def get_associations_items(association_id: int, db: Session=Depends(get_db)):
    db_items= db.query(models.Item).filter(models.Item.association_id== association_id).all()
    
    return db_items

@app.get("/associations/me", response_model=schemas.AssociationResponse)
def read_current_association(current_asso: models.Association = Depends(get_current_association)):
    return current_asso

