from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy import Column, String, Integer, Numeric, create_engine

class Base(DeclarativeBase):
    pass 

# declare orms
class Items(Base):
    __tablename__ = "items_table"

    id = Column(Integer, primary_key=True)
    item_name = Column(String(50))
    category = Column(String(20))
    price = Column(Numeric(precision=5, scale=2))
    status = Column(String(20))

# create engine and session maker
engine = create_engine("sqlite:///items.db", echo=True)
LocalSession = sessionmaker(bind=engine)







