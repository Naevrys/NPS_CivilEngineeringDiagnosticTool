from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select
from .database import engine
from .models import NationalPark, Campground, Amenity

app = FastAPI(title = "National Park Campground Analysis Tool")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# endpoints

@app.get("/")
def root():
    return {"message": "National Park Analysis API is running."}

# get all parks
@app.get("/parks/")
def get_parks():
    with Session(engine) as session:
        parks = session.exec(select(NationalPark)).all()
        return parks

# get park by code 
@app.get("/parks/{park_code}")
def get_park(park_code: str):
    with Session(engine) as session:
        park = session.exec(
            select(NationalPark).where(NationalPark.park_code == park_code)
        ).first()

        if not park:
            raise HTTPException(status_code=404, detail="Park not found")

        return park

# get all campgrounds for a specific park
@app.get("/parks/{park_code}/campgrounds")
def get_campgrounds_for_park(park_code: str):
    with Session(engine) as session:
        campgrounds = session.exec(
            select(Campground).where(Campground.park_code == park_code)
        ).all()
        return campgrounds

# get all campgrounds
@app.get("/campgrounds/")
def get_all_campgrounds():
    with Session(engine) as session:
        campgrounds = session.exec(select(Campground)).all()
        return campgrounds

# get campground by ID
@app.get("/campgrounds/{campground_id}")
def get_single_campground(campground_id: int):
    with Session(engine) as session:
        campground = session.exec(
            select(Campground).where(Campground.campground_id == campground_id)
        ).first()

        if not campground:
            raise HTTPException(status_code=404, detail="Campground not found")

        return campground
    
# get all amenities
@app.get("/amenities/")
def get_all_amenities():
    with Session(engine) as session:
        amenities = session.exec(select(Amenity)).all()
        return amenities

# get amenities by campground code
@app.get("/amenities/{campground_code}")
def get_amenities_by_code(campground_code: str):
    with Session(engine) as session:
        amenities = session.exec(
            select(Amenity).where(Amenity.campground_code == campground_code)
        ).all()  

        if not amenities:
            raise HTTPException(status_code=404, detail="Amenities not found")

        return amenities