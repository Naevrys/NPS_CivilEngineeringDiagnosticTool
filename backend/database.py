from sqlmodel import SQLModel, create_engine, Session
from .models import NationalPark, Campground, Amenity

sqlite_filename = "database/nps_campgrounds.db"
sqlite_url = f"sqlite:///{sqlite_filename}"

engine = create_engine(sqlite_url, echo=True)

def create_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session



# uncomment to creat DB
#create_db()

#Campground.__table__.drop(engine, checkfirst=True)
#Campground.__table__.create(engine, checkfirst=True)

#Amenity.__table__.drop(engine, checkfirst=True)
#Amenity.__table__.create(engine, checkfirst=True)


