from pydantic import BaseModel

class AddressBase(BaseModel):
    """
        Added response schema for Address model
    """
    id: int
    coordinates: str
    address: str
    

    class Config:
        orm_mode = True


class AddressCreate(BaseModel):
    """
        Added request schema for create Address
    """
    coordinates: str
    address: str