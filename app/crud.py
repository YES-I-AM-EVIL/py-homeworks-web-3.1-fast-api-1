from sqlalchemy.orm import Session
from . import models, schemas

def create_advertisement(db: Session, ad: schemas.AdvertisementCreate):
    db_ad = models.Advertisement(**ad.model__dump())
    db.add(db_ad)
    db.commit()
    db.refresh(db_ad)
    return db_ad

def get_advertisement(db: Session, ad_id: int):
    return db.query(models.Advertisement).filter(models.Advertisement.id == ad_id).first()

def update_advertisement(db: Session, ad_id: int, ad_data: schemas.AdvertisementCreate):
    db.query(models.Advertisement).filter(models.Advertisement.id == ad_id).update(ad_data.model_dump())
    db.commit()
    return get_advertisement(db, ad_id)

def delete_advertisement(db: Session, ad_id: int):
    db.query(models.Advertisement).filter(models.Advertisement.id == ad_id).delete()
    db.commit()

def search_advertisements(db: Session, title: str = None, author: str = None):
    query = db.query(models.Advertisement)
    if title:
        query = query.filter(models.Advertisement.title.ilike(f"%{title}%"))
    if author:
        query = query.filter(models.Advertisement.author.ilike(f"%{author}%"))
    return query.all()