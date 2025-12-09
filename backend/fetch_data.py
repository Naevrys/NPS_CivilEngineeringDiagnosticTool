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


def fetch_campgrounds(limit=100):
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

def fetch_amenities(limit=200):
    """Fetch amenities for campgrounds from NPS API"""
    url = f"{URL}/campgrounds?limit={limit}&api_key={API_KEY}"
    response = requests.get(url)
    data = response.json()["data"]

    df = pd.DataFrame(data)

    df["amenities"] = df["amenities"].apply(lambda x: x if isinstance(x, dict) else {})
    df["camp_store"] = df["amenities"].apply(
        lambda x: ", ".join(x.get("campStore", [])) if isinstance(x.get("campStore", []), list)
        else x.get("campStore") if x.get("campStore") else None
    )
    df["toilets"] = df["amenities"].apply(lambda x: ", ".join(x.get("toilets", [])) if isinstance(x.get("toilets", []), list) else x.get("toilets"))
    df["showers"] = df["amenities"].apply(lambda x: ", ".join(x.get("showers", [])) if isinstance(x.get("showers", []), list) else x.get("showers"))
    df["water"] = df["amenities"].apply(lambda x: ", ".join(x.get("potableWater", [])) if isinstance(x.get("potableWater", []), list) else x.get("potableWater"))
    df["internet"] = df["amenities"].apply(lambda x: ", ".join(x.get("internetConnectivity", [])) if isinstance(x.get("internetConnectivity", []), list) else x.get("internetConnectivity"))
    df["firewood"] = df["amenities"].apply(lambda x: ", ".join(x.get("firewoodForSale", [])) if isinstance(x.get("firewoodForSale", []), list) else x.get("firewoodForSale"))
    df["food_storage"] = df["amenities"].apply(lambda x: ", ".join(x.get("foodStorageLockers", [])) if isinstance(x.get("foodStorageLockers", []), list) else x.get("foodStorageLockers"))
    df["cell_reception"] = df["amenities"].apply(lambda x: ", ".join(x.get("cellPhoneReception", [])) if isinstance(x.get("cellPhoneReception", []), list) else x.get("cellPhoneReception"))
    df["amphitheater"] = df["amenities"].apply(lambda x: ", ".join(x.get("amphitheater", [])) if isinstance(x.get("amphitheater", []), list) else x.get("amphitheater"))

    df["campground_code"] = df["id"]

    final_columns = [
        "campground_code",
        "camp_store",
        "toilets",
        "showers",
        "water",
        "internet",
        "firewood",
        "food_storage",
        "cell_reception",
        "amphitheater"
    ]
    df = df[final_columns]

    return df

def insert_amenities(df):
    with Session(engine) as session:
        for _, row in df.iterrows():
            statement = select(Amenity).where(Amenity.campground_code == row["campground_code"])
            exists = session.exec(statement).first()

            if not exists:
                amenity = Amenity(
                    campground_code=row["campground_code"],
                    camp_store=row["camp_store"],
                    toilets=row["toilets"],
                    showers=row["showers"],
                    water=row["water"],
                    internet=row["internet"],
                    firewood=row["firewood"],
                    food_storage=row["food_storage"],
                    cell_reception=row["cell_reception"],
                    amphitheater=row["amphitheater"]
                )
                session.add(amenity)
        session.commit()


# fetch parks
#parks_df = fetch_parks()
#insert_parks(parks_df)
#print(f"{len(parks_df)} parks fetched and inserted - duplicates skipped.")

# fetch campgrounds
#campgrounds_df = fetch_campgrounds(limit=100)
#insert_campgrounds(campgrounds_df)
#print(campgrounds_df)

# fetch amenities
#amenities_df = fetch_amenities(limit=200)
#insert_amenities(amenities_df)


