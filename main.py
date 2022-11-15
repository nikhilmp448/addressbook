from typing import List
from fastapi import Depends, FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from database import SessionLocal
import crud, models, schemas
from database import engine


models.Base.metadata.create_all(bind=engine)
app = FastAPI()

# Setup Database Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/address/", response_model=List[schemas.AddressBase], tags=['Get your Address'])
def read_addr(limit: int = 50, db: Session = Depends(get_db)):

    address = crud.AddressRepo.get_address(db, limit=limit)
    return address


@app.post("/address/", response_model=schemas.AddressBase, tags=['Create your Address'])
def create_addr(request: schemas.AddressCreate, db: Session = Depends(get_db)):

    return crud.AddressRepo.create_address(db=db, request=request)


@app.put("/address/{address_id}", response_model=schemas.AddressBase, tags=['Update your Address'])
def update_addr(address_id: int, request: schemas.AddressCreate, db: Session = Depends(get_db)):
    
    db_item = crud.AddressRepo.fetch_by_id(db, address_id)
    if db_item:
        update_item_encoded = jsonable_encoder(request)
        db_item.coordinates = update_item_encoded['coordinates']
        db_item.address = update_item_encoded['address']
        return crud.AddressRepo.update(db=db, item_data=db_item)
    else:
        raise HTTPException(status_code=400, detail="Address not found with the given ID")


@app.delete('/address/{address_id}', tags=['Delete your Address'])
def delete_addr(address_id: int, db: Session = Depends(get_db)):

    db_item = crud.AddressRepo.fetch_by_id(db, address_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Address not found with the given ID")
    crud.AddressRepo.delete(db, address_id)
    return "Address deleted successfully!"