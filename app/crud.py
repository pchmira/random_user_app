from sqlalchemy.orm import Session
from . import models, schemas
from sqlalchemy.sql import func

def create_user(db: Session, user: schemas.UserCreate):
    existing = db.query(models.User).filter(models.User.email == user.email).first()
    if existing:
        return existing
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_random_user(db: Session):
    return db.query(models.User).order_by(func.random()).first()

def get_users(db: Session, skip: int = 0, limit: int = 50):
    return db.query(models.User).offset(skip).limit(limit).all()
