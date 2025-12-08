from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship

# National parks
class NationalPark(SQLModel, table=True):
    park_id: Optional[int] = Field(default=None, primary_key=True)
    park_name: str = Field(index=True)
    state: str

    campgrounds: List["Campground"] = Relationship(back_populates="park")

# campgrounds 
class Campground(SQLModel, table=True):
    campground_id: Optional[int] = Field(default=None, primary_key=True)
    campground_name: str
    total_sites: int
    tent_spots: Optional[int] = None
    rv_spots: Optional[int] = None
    wheelchair_accessible: bool
    park_id: int = Field(foreign_key="nationalpark.park_id")

    park: Optional[NationalPark] = Relationship(back_populates="campgrounds")
    amenities: List["Amenity"] = Relationship(back_populates="campground")

# amenities
class Amenity(SQLModel, table=True):
    amenity_id: Optional[int] = Field(default=None, primary_key=True)
    amenity_name: str
    availability: Optional[str] = None
    campground_id: int = Field(foreign_key="campground.campground_id")

   
    campground: Optional[Campground] = Relationship(back_populates="amenities")