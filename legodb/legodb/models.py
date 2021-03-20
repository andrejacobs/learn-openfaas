from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class LegoSet(Base):
    __tablename__ = 'legosets'
    id = Column('pkID', Integer, primary_key=True, nullable=False)
    legoID = Column('LegoID', Integer, unique=True, nullable=False)
    description = Column('Description',String(200))
    productURL = Column('ProductURL',String(4096))
    imageURL = Column('ImageURL',String(4096))


def database_session(host, port, user, password, schema):
    engine = create_engine(f"mariadb+mariadbconnector://{user}:{password}@{host}:{port}/{schema}?charset=utf8mb4")
    
    Session = sessionmaker(bind=engine)
    Base.metadata.create_all(engine)
    
    session = Session()
    return session


def get_all_legosets(session):
    legosets = session.query(LegoSet).all()
    return legosets


def create_legoset(json):
    legoID = json.get('legoID', None)
    if legoID is None:
        return None
    description = json.get('description', None)
    if description is None:
        return None
    productURL = json.get('productURL', None)
    imageURL = json.get('imageURL', None)

    legoset = LegoSet(legoID=legoID, description=description, productURL=productURL, imageURL=imageURL)
    return legoset
