from sqlalchemy.orm import Session
from sqlalchemy import and_
from app import db_models, models
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

def get_user(db: Session, user_id: int):
    return db.query(db_models.User).filter(db_models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(db_models.User).filter(db_models.User.email == email).first()

def create_user(db: Session, user: models.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = db_models.User(
            email=user.email,
            username=user.username,
            full_name=user.full_name,
            hashed_password=hashed_password,
            role=user.role
            )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_product(db: Session, product_id: int):
    return db.query(db_models.Product).filter(db_models.Product.id == product_id).first()

def get_products(db: Session, skip: int = 0, limit: int = 100, category: str = None):
    query = db.query(db_models.Product)
    if category:
        query = query.filter(db_models.Product.category == category)
    return query.offset(skip).limit(limit).all()

def create_product

