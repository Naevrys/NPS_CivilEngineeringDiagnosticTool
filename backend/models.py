from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship

# national parks
class NationalPark(SQLModel, table=True):
    park_id: Optional[int] = Field(default=None, primary_key=True)
    park_name: str
    state: str
    park_code: str = Field(index=True, unique=True)

    campgrounds: List["Campground"] = Relationship(back_populates="park")

# campgrounds 
class Campground(SQLModel, table=True):
    campground_id: Optional[int] = Field(default=None, primary_key=True)  
    campground_code: str = Field(index=True, unique=True)  
    campground_name: str
    total_sites: int
    tent_spots: int
    rv_spots: int
    park_code: str = Field(foreign_key="nationalpark.park_code")  

    park: Optional[NationalPark] = Relationship(back_populates="campgrounds")

# amenities
class Amenity(SQLModel, table=True):
    amenity_id: Optional[int] = Field(default=None, primary_key=True)  
    campground_code: str = Field(foreign_key="campground.campground_code", 
                                 index=True, unique=True)  
    toilets: Optional[str] = None
    showers: Optional[str] = None
    trash: Optional[str] = None
    water: Optional[str] = None
    internet: Optional[str] = None
    firewood: Optional[str] = None
    food_storage: Optional[str] = None
    cell_reception: Optional[str] = None
    amphitheater: Optional[str] = None

