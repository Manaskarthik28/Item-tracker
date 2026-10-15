from fastapi import FastAPI, Depends, Request, Response
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from config.settings import Settings
from security.jwt import encode_token, decode_token
from models.db_models import engine, Items, Base
from session.db_session import get_session
from sqlalchemy.orm import Session
from schema.pydantic_schema import AddItem, ItemResponse, User

# create settings object
settings = Settings()
# create orm tables on launch
Base.metadata.create_all(engine)
app = FastAPI()

# CORS ORIGINS frontend middleware order
origins = [
    "http://localhost:3000",
]

# add middlewares
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_headers=["*"],
    allow_methods=["*"],
)

# get the public paths allowed
public_paths = [
    "/docs",
    "/login",
    "/",
    "/openapi.json",
]

# JWT Middleware order 
@app.middleware("http")
async def check_header(request: Request, call_next):
    # check the path before validating header
    if request.url.path in public_paths:
        return await call_next(request)
    # extract the token
    header = request.headers.get("Authorization", "")
    if not header:
        return Response(status_code=401, content="Unauthorized missing token or invalid token")
    token = header[6:].strip()
    # decode the token here
    payload = decode_token(token, settings.JWT_SECRET, settings.ALGO)
    if payload == "Error":
        return Response(status_code=401, content="Unauthorized token Signature Invalid")
    response = await call_next(request)
    return response

@app.post("/login")
def login(user: User):
    # check if empty or white spaces
    if user.username.strip() == ""  or user.password.strip() == "":
        return Response(status_code=404, content="username or password missing")
    # check if creds match
    if user.username != settings.USER_NAME or user.password != settings.PASSWORD:
        return Response(status_code=404, content="Invalid username or password")
    # prepare payload for user object
    user = {
        "sub": user.username,
        "password": user.password
    }
    token = encode_token(user, settings.JWT_SECRET, settings.ALGO)
    return {"token": token}

# get items
@app.get("/items", response_model=ItemResponse | dict[str, str])
def get_items(db: Session = Depends(get_session)):
    try:
        result = db.query(Items).all()
        return {"status": 200, "response": result}
    except:
        return {"response": "error in fetching data"}
    

# add items
@app.post("/items")
def add_items(addItem: AddItem, db:Session = Depends(get_session)):
    try:
        result = Items(item_name=addItem.item_name, category=addItem.category, price=addItem.price, status=addItem.status)
        db.add(result)
        db.commit()
        return {"status": 201, "response": "record created"}
    except:
        db.rollback()
        return Response(status_code=404, content="error in adding item")

# delete items
@app.delete("/items/{id}")
def delete_item(id: int, db:Session = Depends(get_session)):
    try:
        result = db.query(Items).filter_by(id=id).first()
        db.delete(result)
        db.commit()
        return {"status": 200, "response": "Item deleted successfully"}
    except:
        db.rollback
        raise Response(status_code=404, content="Failed to delete item")

@app.get("/")
def health():
    return {"response": "app is running"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)