National Park Campground Analysis Tool
Overview

This application provides a tool for analyzing National Park campgrounds and their amenities. Users can view all parks, campgrounds, and amenities, search for specific campgrounds or amenities, and run predefined queries to analyze campground capacities and features.

The system consists of a FastAPI backend and a Streamlit frontend.

-------------------------------------------------------------------------------------------------------------

Setup Instructions

1. Installation and Environment Setup

a. Ensure Python 3.10+ is installed on your system.
b. Install VSCode or your preferred IDE.
c. Clone the project repository:
    - git clone <repository-url>
      cd NPS_CivilEngineeringDiagnosticTool
    - Or download from GitHub
    - Install required dependencies, listed in backend/requirements.txt

2. Database Setup
    - Initialize the database and tables by running: 
        python backend/database.py
    - Populate the database with data from the NPS API using fetch_data.py. You can control how much data    to  load by modifying any limits in the script: 
        python backend/fetch_data.py

3. Start the Backend API

    a. Run the FastAPI backend:
         uvicorn backend.main:app --reload
    - The API will be available at: http://127.0.0.1:8000
    - Verify endpoints at http://127.0.0.1:8000/docs

4. Start the Frontend 

    a. Run the Streamlit frontend: 
        streamlit run frontend/streamlit_app.py

    IMPORTANT: ALWAYS start the backend API before running the frontend. 

-------------------------------------------------------------------------------------------------------------

Usage Examples

Find a Specific Campground and Its Amenities
    Navigate to View All Data to locate a campground’s code using CTRL+F.
    Copy the campground code and paste it into Search Amenities by Campground Code to view its amenities.
    
Calculate Total Campsites in a Park
    Navigate to Run a Query → Query 2 in the frontend.
    Enter the park code to see the total number of campsites for that park.

Identify Campgrounds with Shower Accessibility
    Navigate to Run a Query → Query 9 to list campgrounds that have shower amenities, ordered by total site capacity.

Analyze Campgrounds by Capacity or Amenities
    Use the Query dropdown in the frontend to run predefined queries, including:
    Campgrounds with fewer than 30 sites
    Largest campgrounds and their amenities
    Parks with campgrounds with more than 25 tent spots
    Low-capacity campgrounds and their available amenities


