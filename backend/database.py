from sqlmodel import SQLModel, create_engine, Session
from .models import NationalPark, Campground, Amenity

DATABASE_URL = "sqlite:///../database/nps_campgrounds.db"

# Create the engine
engine = create_engine(DATABASE_URL, echo=True)

# Function to create all tables
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# Dependency for FastAPI endpoints to get a session
def get_session():
    with Session(engine) as session:
        yield session