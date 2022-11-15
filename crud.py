from sqlalchemy.orm import Session
import models, schemas


class AddressRepo:
    """
        Add Services for crud operations
    """
    def get_address(db: Session, limit: int = 50):
        return db.query(models.Address).limit(limit).all()

    def create_address(db: Session, request: schemas.AddressCreate):
        db_address = models.Address(**request.dict())
        db.add(db_address)
        db.commit()
        db.refresh(db_address)
        return db_address

    def fetch_by_id(db: Session,_id):
        return db.query(models.Address).filter(models.Address.id == _id).first()

    async def update(db: Session,item_data):
        updated_item = db.merge(item_data)
        db.commit()
        return updated_item

    async def delete(db: Session,item_id):
        db_item= db.query(models.Address).filter_by(id=item_id).first()
        db.delete(db_item)
        db.commit()