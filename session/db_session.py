from models.db_models import LocalSession

def get_session():
    try:
        db = LocalSession()
        yield db 
    finally:
        db.close()