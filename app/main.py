from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from . import models, schemas, crud, database
from .database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/advertisement/", response_model=schemas.AdvertisementResponse)
def create_ad(ad: schemas.AdvertisementCreate, db: Session = Depends(get_db)):
    return crud.create_advertisement(db, ad)

@app.get("/advertisement/{ad_id}", response_model=schemas.AdvertisementResponse)
def read_ad(ad_id: int, db: Session = Depends(get_db)):
    ad = crud.get_advertisement(db, ad_id)
    if not ad:
        raise HTTPException(status_code=404, detail="Advertisement not found")
    return ad

@app.patch("/advertisement/{ad_id}", response_model=schemas.AdvertisementResponse)
def update_ad(ad_id: int, ad: schemas.AdvertisementCreate, db: Session = Depends(get_db)):
    return crud.update_advertisement(db, ad_id, ad)

@app.delete("/advertisement/{ad_id}")
def delete_ad(ad_id: int, db: Session = Depends(get_db)):
    crud.delete_advertisement(db, ad_id)
    return {"message": "Advertisement deleted"}

@app.get("/advertisement/", response_model=list[schemas.AdvertisementResponse])
def search_ads(
    title: str = Query(None),
    author: str = Query(None),
    db: Session = Depends(get_db)
):
    return crud.search_advertisements(db, title, author)