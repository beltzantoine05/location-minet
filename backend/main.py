from datetime import datetime, timezone
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
import models
from database import get_db
import schemas
from fastapi.middleware.cors import CORSMiddleware
import auth
from config import CORS_ORIGINS
from fastapi.security import OAuth2PasswordRequestForm

app = FastAPI(title="location MiNET API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/associations/me", response_model=schemas.AssociationResponse)
def read_current_association(current_asso: models.Association = Depends(auth.get_current_association)):
    return current_asso

@app.put("/associations/me", response_model=schemas.AssociationResponse)
def update_current_association(
    asso_update: schemas.AssociationUpdate,
    db: Session = Depends(get_db),
    current_asso: models.Association = Depends(auth.get_current_association),
):
    update_data = asso_update.model_dump(exclude_unset=True)
    # nom et email ne peuvent pas être vidés (None explicite)
    for champ in ("nom", "email"):
        if champ in update_data and update_data[champ] is None:
            raise HTTPException(status_code=422, detail=f"Le champ « {champ} » ne peut pas être vide")

    nouveau_nom = update_data.get("nom")
    if nouveau_nom and nouveau_nom != current_asso.nom:
        if db.query(models.Association).filter(models.Association.nom == nouveau_nom).first():
            raise HTTPException(status_code=409, detail="Une association porte déjà ce nom")

    for cle, valeur in update_data.items():
        setattr(current_asso, cle, valeur)
    db.commit()
    db.refresh(current_asso)
    return current_asso

@app.get("/associations/", response_model=list[schemas.AssociationResponse])
def get_association(db: Session = Depends(get_db)):
    asso = db.query(models.Association).all()
    return asso

# --- 1. SE CONNECTER ---
@app.post("/token", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    # On cherche l'utilisateur dans la base
    user = db.query(models.User).filter(models.User.username == form_data.username).first()

    # On vérifie le mot de passe
    if not user or not auth.verify_password(form_data.password, user.mot_de_passe_hash):
        raise HTTPException(status_code=401, detail="Identifiants incorrects", headers={"WWW-Authenticate": "Bearer"})

    # On génère le token
    access_token = auth.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}



@app.post("/items/", response_model=schemas.ItemResponse)
def create_item( item : schemas.ItemCreate, db: Session = Depends(get_db), current_asso: models.Association = Depends(auth.get_current_association)):
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
def delete_item(item_id: int, db: Session = Depends(get_db), current_asso: models.Association = Depends(auth.get_current_association)):
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if db_item is None: 
        raise HTTPException(status_code=404, detail="Item not found")
    if db_item.association_id != current_asso.id:
        raise HTTPException(status_code=403, detail="You are not authorized to delete this item")
    db.delete(db_item)
    db.commit()

    return {"message": "Item deleted successfully"}


@app.put("/items/{item_id}", response_model=schemas.ItemResponse)
def update_item(item_id: int, item: schemas.ItemUpdate, db: Session = Depends(get_db), current_asso: models.Association = Depends(auth.get_current_association)):
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

@app.get("/associations/{association_id}", response_model=schemas.AssociationResponse)
def get_association_by_id(association_id: int, db: Session = Depends(get_db)):
    db_asso = db.query(models.Association).filter(models.Association.id == association_id).first()
    if db_asso is None:
        raise HTTPException(status_code=404, detail="Association not found")
    return db_asso

@app.get("/associations/{association_id}/items", response_model= list[schemas.ItemResponse])
def get_associations_items(association_id: int, db: Session=Depends(get_db)):
    db_items= db.query(models.Item).filter(models.Item.association_id== association_id).all()
    
    return db_items

@app.delete("/associations/{association_id}")
def delete_association(association_id: int, db: Session = Depends(get_db), admin: models.User = Depends(auth.require_admin)):
    db_asso = db.query(models.Association).filter(models.Association.id == association_id).first()
    if db_asso is None:
        raise HTTPException(status_code=404, detail="Association not found")
    db.delete(db_asso)
    db.commit()
    return {"message": "Association deleted successfully"}

@app.post("/register", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user_in: schemas.UserCreate, db: Session = Depends(get_db)):
    # On vérifie si le username ou l'email existent déjà
    user_existant = db.query(models.User).filter(
        (models.User.username == user_in.username) | (models.User.email == user_in.email)
    ).first()
    if user_existant:
        raise HTTPException(status_code=400, detail="Un utilisateur avec ce nom ou cet email existe déjà")

    nouvel_utilisateur = models.User(
        username=user_in.username,
        email=user_in.email,
        mot_de_passe_hash=auth.get_password_hash(user_in.mot_de_passe),
        role="student",
    )

    db.add(nouvel_utilisateur)
    db.commit()
    db.refresh(nouvel_utilisateur)

    return nouvel_utilisateur

@app.get("/users/me", response_model=schemas.UserMeResponse)
def read_current_user(current_user: models.User = Depends(auth.get_current_user)):
    return current_user


# --- DEMANDES DE CREATION D'ASSOCIATION ---
@app.post("/association-requests/", response_model=schemas.AssociationRequestResponse, status_code=status.HTTP_201_CREATED)
def create_association_request(
    demande: schemas.AssociationRequestCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    if current_user.association_dirigee is not None:
        raise HTTPException(status_code=409, detail="Vous gérez déjà une association")

    en_attente = db.query(models.AssociationRequest).filter(
        models.AssociationRequest.user_id == current_user.id,
        models.AssociationRequest.status == "pending",
    ).first()
    if en_attente:
        raise HTTPException(status_code=409, detail="Vous avez déjà une demande en attente")

    if db.query(models.Association).filter(models.Association.nom == demande.nom).first():
        raise HTTPException(status_code=409, detail="Une association porte déjà ce nom")

    db_demande = models.AssociationRequest(user_id=current_user.id, **demande.model_dump())
    db.add(db_demande)
    db.commit()
    db.refresh(db_demande)
    return db_demande

@app.get("/association-requests/me", response_model=list[schemas.AssociationRequestResponse])
def get_my_association_requests(db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    return (
        db.query(models.AssociationRequest)
        .filter(models.AssociationRequest.user_id == current_user.id)
        .order_by(models.AssociationRequest.created_at.desc())
        .all()
    )

@app.get("/admin/association-requests", response_model=list[schemas.AssociationRequestAdminResponse])
def list_association_requests(
    status_filter: str | None = None,
    db: Session = Depends(get_db),
    admin: models.User = Depends(auth.require_admin),
):
    query = db.query(models.AssociationRequest)
    if status_filter:
        query = query.filter(models.AssociationRequest.status == status_filter)
    return query.order_by(models.AssociationRequest.created_at.asc()).all()

@app.post("/admin/association-requests/{request_id}/review", response_model=schemas.AssociationRequestAdminResponse)
def review_association_request(
    request_id: int,
    review: schemas.AssociationRequestReview,
    db: Session = Depends(get_db),
    admin: models.User = Depends(auth.require_admin),
):
    demande = db.query(models.AssociationRequest).filter(models.AssociationRequest.id == request_id).first()
    if demande is None:
        raise HTTPException(status_code=404, detail="Demande introuvable")
    if demande.status != "pending":
        raise HTTPException(status_code=409, detail="Cette demande a déjà été traitée")

    if review.decision == "rejected" and not review.admin_comment:
        raise HTTPException(status_code=422, detail="Un motif est obligatoire pour refuser une demande")

    if review.decision == "approved":
        # Le demandeur peut avoir obtenu une asso entre-temps, ou le nom a pu être pris
        if demande.demandeur.association_dirigee is not None:
            raise HTTPException(status_code=409, detail="Le demandeur gère déjà une association")
        if db.query(models.Association).filter(models.Association.nom == demande.nom).first():
            raise HTTPException(status_code=409, detail="Une association porte déjà ce nom")
        db.add(models.Association(
            nom=demande.nom,
            email=demande.email,
            description=demande.description,
            representant_id=demande.user_id,
        ))
        message = f"Votre demande de création de l'association « {demande.nom} » a été acceptée. Vous pouvez maintenant gérer sa page."
    else:
        message = f"Votre demande de création de l'association « {demande.nom} » a été refusée. Motif : {review.admin_comment}"

    demande.status = review.decision
    demande.admin_comment = review.admin_comment
    demande.reviewed_at = datetime.now(timezone.utc)
    demande.reviewed_by_id = admin.id
    db.add(models.Notification(user_id=demande.user_id, message=message))
    db.commit()
    db.refresh(demande)
    return demande


# --- NOTIFICATIONS ---
@app.get("/notifications/me", response_model=list[schemas.NotificationResponse])
def get_my_notifications(
    non_lues: bool = False,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    query = db.query(models.Notification).filter(models.Notification.user_id == current_user.id)
    if non_lues:
        query = query.filter(models.Notification.lu.is_(False))
    return query.order_by(models.Notification.created_at.desc(), models.Notification.id.desc()).all()

@app.get("/notifications/me/unread-count", response_model=schemas.UnreadCount)
def get_my_unread_count(db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    nb = db.query(models.Notification).filter(
        models.Notification.user_id == current_user.id,
        models.Notification.lu.is_(False),
    ).count()
    return {"non_lues": nb}

@app.post("/notifications/read-all", response_model=schemas.UnreadCount)
def mark_all_notifications_read(db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    db.query(models.Notification).filter(
        models.Notification.user_id == current_user.id,
        models.Notification.lu.is_(False),
    ).update({"lu": True})
    db.commit()
    return {"non_lues": 0}

@app.post("/notifications/{notification_id}/read", response_model=schemas.NotificationResponse)
def mark_notification_read(notification_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    notif = db.query(models.Notification).filter(
        models.Notification.id == notification_id,
        models.Notification.user_id == current_user.id,
    ).first()
    if notif is None:
        raise HTTPException(status_code=404, detail="Notification introuvable")
    notif.lu = True
    db.commit()
    db.refresh(notif)
    return notif
