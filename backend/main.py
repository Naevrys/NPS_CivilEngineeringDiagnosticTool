from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session, select
from database import engine, create_db, get_session
from models import NationalPark, Campground, Amenity

app = FastAPI(title = "Analysis tool to help civil engineers make " \
"decisions on infrastructure surrounding National Park campgrounds "
"and their amenities")

# endpoints

@app.get("/parks/", response_model=list[NationalPark])
def read_parks(session: Session = Depends(get_session)):
    """Return all national parks"""
    parks = session.exec(select(NationalPark)).all()
    return parks

@app.get("/campgrounds/", response_model=list[Campground])
def read_campgrounds(session: Session = Depends(get_session)):
    """Return all campgrounds"""
    campgrounds = session.exec(select(Campground)).all()
    return campgrounds

@app.get("/amenities/", response_model=list[Amenity])
def read_amenities(session: Session = Depends(get_session)):
    """Return all amenities"""
    amenities = session.exec(select(Amenity)).all()
    return amenities

@app.get("/campgrounds/{campground_id}", response_model=Campground)
def read_campground(campground_id: int, session: Session = Depends(get_session)):
    """Return a single campground by ID"""
    campground = session.get(Campground, campground_id)
    if not campground:
        raise HTTPException(status_code=404, detail="Campground not found")
    return campground

@app.get("/parks/{park_id}/campgrounds", response_model=list[Campground])
def read_park_campgrounds(park_id: int, session: Session = Depends(get_session)):
    """Return all campgrounds for a given park"""
    stmt = select(Campground).where(Campground.park_id == park_id)
    campgrounds = session.exec(stmt).all()
    return campgrounds

@app.get("/campgrounds/accessibility/", response_model=list[Campground])
def read_accessible_campgrounds(session: Session = Depends(get_session)):
    """Return all wheelchair accessible campgrounds"""
    stmt = select(Campground).where(Campground.wheelchair_accessible == True)
    campgrounds = session.exec(stmt).all()
    return campgrounds

@app.get("/parks/{park_id}/campgrounds/amenities/", response_model=dict)
def read_campgrounds_with_amenities(park_id: int, session: Session = Depends(get_session)):
    """Return campgrounds and their amenities for a given park"""
    stmt = select(Campground).where(Campground.park_id == park_id)
    campgrounds = session.exec(stmt).all()
    result = {}
    for cg in campgrounds:
        amenities_stmt = select(Amenity).where(Amenity.campground_id == cg.campground_id)
        amenities = session.exec(amenities_stmt).all()
        result[cg.campground_name] = [a.amenity_name for a in amenities]
    return result
