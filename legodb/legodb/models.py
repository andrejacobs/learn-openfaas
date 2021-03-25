from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import and_


Base = declarative_base()


class LegoSet(Base):
    __tablename__ = 'legosets'
    id = Column('pkID', Integer, primary_key=True, nullable=False)
    legoID = Column('LegoID', Integer, unique=True, nullable=False)
    description = Column('Description',String(200))
    productURL = Column('ProductURL',String(4096))
    imageURL = Column('ImageURL',String(4096))
    imagePath = Column('ImagePath',String(4096))


def get_all_legosets(session):
    legosets = session.query(LegoSet).all()
    return legosets


def get_legosets_that_need_an_image_download(session, limit=10):
    legosets = session.query(LegoSet).filter(
        and_(
            LegoSet.imageURL.is_not(None),
            LegoSet.imagePath.is_(None)
        )
    ).limit(limit)
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
