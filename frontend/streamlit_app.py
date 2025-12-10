import streamlit as st
import requests
import pandas as pd

URL = "http://127.0.0.1:8000"

st.title("National Park Campground Analysis Tool")

option = st.sidebar.selectbox(
    "View Data",
    ["None", "View All Data", "Search Campground by ID", "Search Amenities by Campground Code"]
)

query_option = st.sidebar.selectbox(
    "Run a Query",
    [
        "None",
        "Query 1: Campgrounds < 30 Sites",
        "Query 2: Total Sites in a Park",
        "Query 3: Tent and RV Spots per Park",
        "Query 4: Campgrounds Above Average Sites",
        "Query 5: Lookup Campground by ID/Name",
        "Query 6: Amenities of Largest Campgrounds",
        "Query 7: Campgrounds with Fewest Total Sites",
        "Query 8: Amenities for Low-Capacity Campgrounds",
        "Query 9: Campground Shower Availability",
        "Query 10: Parks with Campgrounds > 25 Tent Spots"
    ]
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

elif option == "Search Campground by ID":
    campground_id_input = st.text_input("Enter Campground ID (integer)")
    if campground_id_input:
        try:
            campground_id = int(campground_id_input)
            response = requests.get(f"{URL}/campgrounds/{campground_id}")
            if response.status_code == 200:
                campground = response.json()
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

# Queries
if query_option == "Query 1: Campgrounds < 30 Sites":
    st.header("Query 1: Campgrounds with fewer than 30 sites")
    response = requests.get(f"{URL}/campgrounds/")
    if response.status_code == 200:
        campgrounds = response.json()
        filtered = [c for c in campgrounds if c["total_sites"] < 30]
        if filtered:
            df = pd.DataFrame(filtered)
            st.dataframe(df)
        else:
            st.write("No campgrounds found with fewer than 30 sites.")
    else:
        st.error("Failed to load campgrounds.")

if query_option == "Query 2: Total Sites in a Park":
    st.header("Query 2: Total Sites in a Park")
    park_code_input = st.text_input("Enter Park Code (e.g., yell, zion)")
    if st.button("Run Query 2"):
        response = requests.get(f"{URL}/parks/{park_code_input}/campgrounds")
        if response.status_code == 200:
            campgrounds = response.json()
            total_sites = sum(c["total_sites"] for c in campgrounds)
            st.write(f"Total sites in park {park_code_input}: {total_sites}")
        else:
            st.error("Park not found or failed to load campgrounds.")
    

if query_option == "Query 3: Tent and RV Spots per Park":
    st.header("Query 3: Tent and RV Spots per Park")

    response_camp = requests.get(f"{URL}/campgrounds/")
    response_parks = requests.get(f"{URL}/parks/")

    if response_camp.status_code == 200 and response_parks.status_code == 200:
        campgrounds = response_camp.json()
        parks = response_parks.json()

        data = []
        for park in parks:
            park_code = park["park_code"]
            park_name = park["park_name"]
            park_camps = [c for c in campgrounds if c["park_code"] == park_code]
            total_tent = sum(c["tent_spots"] for c in park_camps)
            total_rv = sum(c["rv_spots"] for c in park_camps)
            data.append({
                "Park Name": park_name,
                "Total Tent Spots": total_tent,
                "Total RV Spots": total_rv
            })

        df = pd.DataFrame(data)
        st.dataframe(df)

    else:
        st.error("Failed to load parks or campgrounds.")

if query_option == "Query 4: Campgrounds Above Average Sites":
    st.header("Query 4: Campgrounds with Above-Average Total Sites")

    response_camp = requests.get(f"{URL}/campgrounds/")
    if response_camp.status_code == 200:
        campgrounds = response_camp.json()

        if campgrounds:
            avg_sites = sum(c["total_sites"] for c in campgrounds) / len(campgrounds)
            st.write(f"Average total sites across all campgrounds: {avg_sites:.2f}")

            above_avg = [c for c in campgrounds if c["total_sites"] > avg_sites]
            if above_avg:
                df = pd.DataFrame(above_avg)[["campground_name", "total_sites", "park_code"]]
                st.dataframe(df)
            else:
                st.write("No campgrounds above average total sites found.")
        else:
            st.write("No campgrounds available to analyze.")
    else:
        st.error("Failed to load campgrounds.")

if query_option == "Query 5: Lookup Campground by ID/Name":
    st.header("Query 5: Lookup Campground")
    
    campground_id_input = st.text_input("Enter Campground ID (integer)")
    campground_name_input = st.text_input("Or enter Campground Name")
    
    if st.button("Run Query 5"):
        response = requests.get(f"{URL}/campgrounds/")
        if response.status_code == 200:
            campgrounds = response.json()
            
            results = []
            for c in campgrounds:
                if (campground_id_input and str(c["campground_id"]) == campground_id_input) or \
                   (campground_name_input and c["campground_name"].lower() == campground_name_input.lower()):
                    results.append(c)
            
            if results:
                df = pd.DataFrame(results)
                st.dataframe(df)
            else:
                st.write("No matching campgrounds found.")
        else:
            st.error("Failed to load campgrounds.")

if query_option == "Query 6: Amenities of Largest Campgrounds":
    st.header("Query 6: Amenities of Largest Campgrounds")
    
    top_n = st.number_input("Number of largest campgrounds to display", min_value=1, value=10)
    
    response_camp = requests.get(f"{URL}/campgrounds/")
    if response_camp.status_code == 200:
        campgrounds = response_camp.json()
        
        if campgrounds:
            largest_camps = sorted(campgrounds, key=lambda x: x["total_sites"], reverse=True)[:top_n]
            
            results = []
            for camp in largest_camps:
                response_amen = requests.get(f"{URL}/amenities/{camp['campground_code']}")
                if response_amen.status_code == 200:
                    amenities = response_amen.json()

                    if isinstance(amenities, dict):
                        merged = {**camp, **amenities}
                    elif isinstance(amenities, list) and amenities:
                        merged = {**camp, **amenities[0]}
                    else:
                        merged = camp
                    results.append(merged)
                else:
                    results.append(camp)  
            
            if results:
                df = pd.DataFrame(results)
                st.dataframe(df)
            else:
                st.write("No data found for largest campgrounds.")
        else:
            st.write("No campgrounds found.")
    else:
        st.error("Failed to load campgrounds.")

if query_option == "Query 7: Campgrounds with Fewest Total Sites":
    st.header("Query 7: Campgrounds with the Fewest Total Sites")
    
    response = requests.get(f"{URL}/campgrounds/")
    if response.status_code == 200:
        campgrounds = response.json()

        sorted_camps = sorted(campgrounds, key=lambda x: x["total_sites"])[:50]
        if sorted_camps:
            df = pd.DataFrame(sorted_camps)
            st.dataframe(df)
        else:
            st.write("No campgrounds found.")
    else:
        st.error("Failed to load campgrounds.")

if query_option == "Query 8: Amenities for Low-Capacity Campgrounds":
    st.header("Query 8: Amenities for Low-Capacity Campgrounds")
    
    response = requests.get(f"{URL}/campgrounds/")
    if response.status_code == 200:
        campgrounds = response.json()

        avg_sites = sum(c["total_sites"] for c in campgrounds) / len(campgrounds)
        low_capacity_camps = [c for c in campgrounds if c["total_sites"] < avg_sites]
        
        if low_capacity_camps:
            all_amenities = []
            for camp in low_capacity_camps:
                code = camp["campground_code"]
                amen_resp = requests.get(f"{URL}/amenities/{code}")
                if amen_resp.status_code == 200:
                    amen = amen_resp.json()

                    if isinstance(amen, list):
                        for a in amen:
                            a["campground_name"] = camp["campground_name"]
                            all_amenities.append(a)
                    else:
                        amen["campground_name"] = camp["campground_name"]
                        all_amenities.append(amen)
            if all_amenities:
                df = pd.DataFrame(all_amenities)
                st.dataframe(df)
            else:
                st.write("No amenities found for low-capacity campgrounds.")
        else:
            st.write("No low-capacity campgrounds found.")
    else:
        st.error("Failed to load campgrounds.")

if query_option == "Query 9: Campground Shower Availability":
    st.header("Query 9: Campground Shower Availability")
    
    response = requests.get(f"{URL}/campgrounds/")
    if response.status_code == 200:
        campgrounds = response.json()
        filtered_camps = []
        
        for camp in campgrounds:
            code = camp["campground_code"]
            amen_resp = requests.get(f"{URL}/amenities/{code}")
            if amen_resp.status_code == 200:
                amen = amen_resp.json()
                # Handle if amenities returned as list
                if isinstance(amen, list):
                    for a in amen:
                        if a.get("showers"):
                            camp_copy = camp.copy()
                            camp_copy["showers"] = a.get("showers")
                            filtered_camps.append(camp_copy)
                else:
                    if amen.get("showers"):
                        camp_copy = camp.copy()
                        camp_copy["showers"] = amen.get("showers")
                        filtered_camps.append(camp_copy)
        
        # Order by total_sites descending
        filtered_camps.sort(key=lambda x: x["total_sites"], reverse=True)
        
        if filtered_camps:
            df = pd.DataFrame(filtered_camps)
            st.dataframe(df)
        else:
            st.write("No campgrounds with showers found.")
    else:
        st.error("Failed to load campgrounds.")

if query_option == "Query 10: Parks with Campgrounds > 25 Tent Spots":
    st.header("Query 10: Parks with Campgrounds with More Than 25 Tent Spots")
    
    # Get all campgrounds
    response_camp = requests.get(f"{URL}/campgrounds/")
    # Get all parks
    response_parks = requests.get(f"{URL}/parks/")

    if response_camp.status_code == 200 and response_parks.status_code == 200:
        campgrounds = response_camp.json()
        parks = response_parks.json()
        df_camp = pd.DataFrame(campgrounds)
        df_parks = pd.DataFrame(parks)[["park_code", "park_name"]]

        # Filter campgrounds with tent_spots > 25
        filtered_camp = df_camp[df_camp["tent_spots"] > 25]

        if not filtered_camp.empty:
            # Merge to get park names
            merged = filtered_camp.merge(df_parks, on="park_code", how="left")

            # Group by park to show park info + list of qualifying campgrounds
            grouped = merged.groupby(["park_code", "park_name"]).agg(
                campgrounds_with_25_tent_spots=("campground_name", list),
                num_campgrounds=("campground_name", "count")
            ).reset_index()

            st.dataframe(grouped)
        else:
            st.write("No campgrounds found with more than 25 tent spots.")
    else:
        st.error("Failed to load campgrounds or parks data.")



