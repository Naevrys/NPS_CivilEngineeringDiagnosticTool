import requests
import pandas as pd
from sqlmodel import Session, select
from database import engine
from models import NationalPark, Campground, Amenity

API_KEY = "7oNHFQNnkjTgDskGf5BhIMgp1aCChakTy7lX43S6"
URL = "https://developer.nps.gov/api/v1"

def fetch_parks():
    """Fetch all official National Parks from NPS API"""
    url = f"{URL}/parks?limit=500&api_key={API_KEY}"
    data = requests.get(url).json()["data"]
    df = pd.DataFrame(data)
    df = df[df['designation'] == 'National Park']
    df = df[['fullName', 'states', 'parkCode', 'id']]
    df.columns = ['park_name', 'state', 'park_code', 'api_id']
    return df

def insert_parks(parks_df):
    with Session(engine) as session:
        for _, row in parks_df.iterrows():
            statement = select(NationalPark).where(NationalPark.park_code == row["park_code"])
            exists = session.exec(statement).first()
            
            if not exists:
                park = NationalPark(
                    park_name=row["park_name"],
                    state=row["state"],
                    park_code=row["park_code"]
                )
                session.add(park)
        session.commit()


def fetch_campgrounds(limit=50):
    """Fetch campgrounds from NPS API, correctly extracting nested fields"""
    url = f"{URL}/campgrounds?limit={limit}&api_key={API_KEY}"
    response = requests.get(url)
    data = response.json()["data"]

    df = pd.DataFrame(data)
    df["campsites"] = df["campsites"].apply(lambda x: x if isinstance(x, dict) else {})
    df["total_sites"] = df["campsites"].apply(lambda x: x.get("totalSites", 0))
    df["tent_spots"] = df["campsites"].apply(lambda x: x.get("tentOnly", 0))
    df["rv_spots"] = df["campsites"].apply(lambda x: x.get("rvOnly", 0))
    df["campground_code"] = df["id"]  
    df = df.rename(columns={
        "name": "campground_name",
        "parkCode": "park_code"
    })

    final_columns = [
        "campground_code",
        "campground_name",
        "total_sites",
        "tent_spots",
        "rv_spots",
        "park_code"
    ]
    df = df[final_columns]

    return df

def insert_campgrounds(df):
    with Session(engine) as session:
        for _, row in df.iterrows():
            statement = select(Campground).where(Campground.campground_code == row["campground_code"])
            exists = session.exec(statement).first()
            
            if not exists:
                campground = Campground(
                    campground_code=row["campground_code"],  
                    campground_name=row["campground_name"],
                    total_sites=row["total_sites"],
                    tent_spots=row["tent_spots"],
                    rv_spots=row["rv_spots"],
                    park_code=row["park_code"]
                )
                session.add(campground)
        session.commit()


# fetch parks
# parks_df = fetch_parks()
#insert_parks(parks_df)
#print(f"{len(parks_df)} parks fetched and inserted - duplicates skipped.")

campgrounds_df = fetch_campgrounds(limit=50)
insert_campgrounds(campgrounds_df)
print(campgrounds_df)
