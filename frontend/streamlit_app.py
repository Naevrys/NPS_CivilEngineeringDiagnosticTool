import streamlit as st
import requests
import pandas as pd

URL = "http://127.0.0.1:8000"

st.title("National Park Campground Analysis Tool")

option = st.sidebar.selectbox(
    "Choose an option",
    ["View All Data", "Search Campground by ID", "Search Amenities by Campground Code"]
)

if option == "View All Data":
    st.header("All National Parks")
    response_parks = requests.get(f"{URL}/parks/")
    if response_parks.status_code == 200:
        df_parks = pd.DataFrame(response_parks.json())
        st.dataframe(df_parks)
    else:
        st.error("Failed to load parks.")

    st.header("All Campgrounds")
    response_camp = requests.get(f"{URL}/campgrounds/")
    if response_camp.status_code == 200:
        df_camp = pd.DataFrame(response_camp.json())
        st.dataframe(df_camp)
    else:
        st.error("Failed to load campgrounds.")

    st.header("All Amenities")
    response_amen = requests.get(f"{URL}/amenities/")
    if response_amen.status_code == 200:
        df_amen = pd.DataFrame(response_amen.json())
        st.dataframe(df_amen)
    else:
        st.error("Failed to load amenities.")

campground_id_input = st.text_input("Enter Campground ID (integer)")
if campground_id_input:
    try:
        campground_id = int(campground_id_input)
        response = requests.get(f"{URL}/campgrounds/{campground_id}")
        if response.status_code == 200:
            campground = response.json()
            # Wrap in list to make DataFrame
            df = pd.DataFrame([campground])
            st.dataframe(df)
        elif response.status_code == 404:
            st.error("Campground not found")
        else:
            st.error(f"Server error: {response.status_code}")
            st.text(response.text)
    except ValueError:
        st.error("Please enter a valid integer.")

elif option == "Search Amenities by Campground Code":
    st.header("Search Amenities")
    campground_code = st.text_input("Enter Campground Code")
    if st.button("Search"):
        response = requests.get(f"{URL}/amenities/{campground_code}")
        if response.status_code == 200:
            amenities = response.json()
            df = pd.DataFrame(amenities if isinstance(amenities, list) else [amenities])
            st.dataframe(df)
        else:
            st.error("Amenities not found.")
