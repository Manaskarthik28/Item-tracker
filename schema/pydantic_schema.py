from pydantic import BaseModel, ConfigDict

class Item(BaseModel):
    id: int
    item_name: str 
    category: str 
    price: int
    status: str

    model_config = ConfigDict(from_attributes=True)

class AddItem(BaseModel):
    item_name: str 
    category: str 
    price: int
    status: str 

class ItemResponse(BaseModel):
    status: int 
    response: list[Item]

class User(BaseModel):
    username: str 
    password: str