# **Introduction**

*Problem Statement:*

One of the main attractions of the National Parks in the United States is being able to stay directly within them, often in campgrounds among the wilderness. However, these campgrounds can only hold so many people, and only come with so many amenities. It is the duty of civil engineers to help create, maintain, develop and improve public infrastructure like campgrounds. With so many parks experiencing vast numbers of visitors every year, it is important that campground data is easy to find and organized as well. A tool that explicitly tracks this data across the different parks and campgrounds would be invaluable.  
*Solution:*  
    A system that will help engineers make better decisions by providing them with accurate, relevant, and easily obtainable information. It will allow engineers to gather all the data into one area and more efficiently identify both negative and positive trends. Engineers will be able to pinpoint which campgrounds are lacking in what they offer and develop plans to improve them. The data this tool presents could also aid engineers in creating relationships and correlations between demand/capacity and the amenities that each campground offers.  
*Features and Analytical Capabilities:*  
Key features include the ability to identify campsites that lack important amenities and compare campgrounds across different parks. It may also help pinpoint campgrounds that are over or under utilized.

# **System Design**						*ER Diagram*

![][image1]  
            *Client-Server Architecture Diagram*

*Relational Schema:*

NationalPark(  
    park\_id INT PRIMARY KEY,  
    park\_name TEXT NOT NULL,  
    state TEXT NOT NULL,  
    park\_code TEXT UNIQUE NOT NULL  
)

Campground(  
    campground\_id INT PRIMARY KEY,  
    campground\_code TEXT UNIQUE NOT NULL,  
    campground\_name TEXT NOT NULL,  
    total\_sites INT,  
    tent\_spots INT,  
    rv\_spots INT,  
    park\_code TEXT NOT NULL,  
    FOREIGN KEY (park\_code) REFERENCES NationalPark(park\_code)  
)

Amenity(  
    amenity\_id INT PRIMARY KEY,  
    campground\_code TEXT UNIQUE NOT NULL,  
    camp\_store TEXT,  
    toilets TEXT,  
    showers TEXT,  
    water TEXT,  
    internet TEXT,  
    firewood TEXT,  
    food\_storage TEXT,  
    cell\_reception TEXT,  
    amphitheater TEXT,  
    FOREIGN KEY (campground\_code) REFERENCES Campground(campground\_code)  
)

*API Endpoint Documentation:*

| Endpoint | Method | Description |
| ----- | ----- | ----- |
| `/` | GET | API health check |
| `/parks/` | GET | Get all parks |
| `/parks/{park_code}` | GET | Get a park by code |
| `/parks/{park_code}/campgrounds` | GET | Get all campgrounds for a park |
| `/campgrounds/` | GET | Get all campgrounds |
| `/campgrounds/{campground_id}` | GET | Get campground by ID |
| `/amenities/` | GET | Get all amenities |
| `/amenities/{campground_code}` | GET | Get amenities for a campground |

# **Data Implementation**

*Schema Definition:*

CREATE TABLE nationalpark (  
    park\_id INTEGER PRIMARY KEY,  
    park\_name TEXT NOT NULL,  
    state TEXT NOT NULL,  
    park\_code TEXT NOT NULL UNIQUE  
);

CREATE TABLE campground (  
    campground\_id INTEGER PRIMARY KEY,  
    campground\_code TEXT NOT NULL UNIQUE,  
    campground\_name TEXT NOT NULL,  
    total\_sites INTEGER NOT NULL,  
    tent\_spots INTEGER NOT NULL,  
    rv\_spots INTEGER NOT NULL,  
    park\_code TEXT NOT NULL,  
    FOREIGN KEY (park\_code) REFERENCES nationalpark(park\_code)  
);

CREATE TABLE amenity (  
    amenity\_id INTEGER PRIMARY KEY,  
    campground\_code TEXT NOT NULL UNIQUE,  
    camp\_store TEXT,  
    toilets TEXT,  
    showers TEXT,  
    water TEXT,  
    internet TEXT,  
    firewood TEXT,  
    food\_storage TEXT,  
    cell\_reception TEXT,  
    amphitheater TEXT,  
    FOREIGN KEY (campground\_code) REFERENCES campground(campground\_code)  
);

*Normalization Analysis & Functional Dependencies:*

### **NationalPark Table (3NF)**

*Attributes*: park\_id (PK), park\_name, state, park\_code (UK)

### *Functional Dependencies*

- park\_id → park\_name, state, park\_code  
- park\_code → park\_id, park\_name, state 

### *Normalization*

- 1NF: All attributes are atomic.  
- 2NF: No partial dependencies.  
  3NF: No transitive dependencies.

# **Campground Table  (3NF)**

*Attributes*: campground\_id (PK), campground\_code (UK), campground\_name, total\_sites, tent\_spots, rv\_spots, park\_code (FK)

### *Functional Dependencies*

- campground\_id → campground\_code, campground\_name, total\_sites, tent\_spots, rv\_spots, park\_code  
- campground\_code → campground\_id, campground\_name, total\_sites, tent\_spots, rv\_spots, park\_code

### *Normalization*

- 1NF: All values are atomic.  
- 2NF: No partial dependencies.  
- 3NF: No transitive dependencies


# **Amenity Table  (3NF)**

*Attributes*: amenity\_id (PK), campground\_code (FK, UK), camp\_store, toilets, showers, water, internet, firewood, food\_storage, cell\_reception, amphitheater

### *Functional Dependencies*

* amenity\_id → all amenity attributes  
* campground\_code → all amenity attributes

### *Normalization*

- 1NF: All values are atomic.  
- 2NF: No partial dependencies.  
- 3NF: Attributes describe only the campground’s amenities and do not depend on each other.




*Data loading approach:*  
	One-time fetch to populate the database, this is the fastest and most efficient way to implement the project. After setting up the necessary schema/models, I fetched the data for each table a little at a time until everything was populated correctly. I did not populate my tables with all of the available data from the NPS API because it likely would have negatively impacted runtime and performance. 

My final record counts are:  
NationalPark: 51 | Campground: 100 Amenity: 200 

No Indexing strategy, I used autoincrementation to generate an ID for each record in every table. 

# **SQL Query Demonstration**

	**Note \- I did not populate my tables/db with ALL of the campgrounds and amenities that exist within the NPS API, as it would have significantly impacted runtime and productivity. Results may be odd due to a small data sample.**

1. **Business Question:** Which campgrounds have fewer than 30 sites?

   SELECT campground\_name, total\_sites

   FROM campground

   WHERE total\_sites \< 30;

**Sample results:**

| campID | totalSites | campCode | campName | parkCode |
| :---- | :---- | :---- | :---- | :---- |
| 1 | 18 | EA81BC45-C361-437F-89B8-5C89FB0D0F86 | 277 North Campground | amis |
| 2 | 16 | 1241C56B-7003-4FDF-A449-29DA8BCB0A41 | Abrams Creek Campground | grsm |
| 3 | 2 | ABDC6E2A-9959-4A4C-9DB6-EEF66E7C95B8 | Adirondack Shelters | cato |

**Explanation**: Basic Filtering

2. **Business Question:** How many total campsites exist within a given national park?

   SELECT np.park\_name,

          SUM(c.total\_sites) AS total\_sites\_in\_park

   FROM nationalpark np

   JOIN campground c 

       ON np.park\_code \= c.park\_code

   WHERE np.park\_code \= :park\_code   \-- parameterized

   GROUP BY np.park\_name;

   

**Sample results:**

| Park code | Total Sites |
| :---- | :---- |
| yell | 432 |
| grsm | 71 |
| cato | 2 |

**Explanation**: JOIN \+ Filtering

3. **Business Question:** How many tent and RV spots are available per park?  
   

   SELECT p.park\_name,  
          SUM(c.tent\_spots) AS total\_tent\_spots,  
          SUM(c.rv\_spots) AS total\_rv\_spots  
   FROM campground c  
   JOIN nationalpark p  
     ON c.park\_code \= p.park\_code  
   GROUP BY p.park\_name;  
   

**Sample results:**

| parkName | TotalTentSpots | TotalRvSpots |
| :---- | :---- | :---- |
| Acadia National Park | 221 | 60 |
| Biscayne National Park | 60 | 0 |
| Great Basin National Park | 4 | 1 |

**Explanation**: JOIN \+ Aggregation

4. **Business Question:** Which campgrounds have above-average total sites?

   WITH avg\_sites AS (

       SELECT AVG(total\_sites) AS avg\_total\_sites

       FROM campground

   )

   SELECT campground\_name, total\_sites

   FROM campground, avg\_sites

   WHERE total\_sites \> avg\_total\_sites;

   

**Sample results:**

| campName | totalSites | parkCode |
| :---- | :---- | :---- |
| Alley Spring Campground | 146 | ozar |
| Antelope Point RV Park | 104 | glca |
| Bear Island Campground | 40 | bicy |

**Explanation**: Subquery / CTE \+ Filtering

5. **Business Question:** Look up a campground by ID/Name.

   SELECT \*

   FROM campground

   WHERE campground\_id \= :campground\_id

      OR campground\_name \= :campground\_name;

   

**Sample results:**

For “16”

| ID | totalSites | rvSpots | tentSpots | campCode | campName | parkCode |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| 16 | 21 | 0 | 21 | BC707FA3-F575-4734-8E62-34689982F615 | Atwell Mill Campground | seki |

For “Bay Creek Campground”

| ID | totalSites | rvSpots | tentSpots | campCode | campName | parkCode |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| 40 | 11 | 0 | 0 | C4A9305D-DB55-4BA5-9798-223AA716F350 | Bay Creek Campground | ozar |

For “Bonita Canyon Campground”

| ID | totalSites | rvSpots | tentSpots | campCode | campName | parkCode |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| 73 | 23 | 0 | 0 | 8D97B7B6-3DB4-4355-8755-2248F20D2E30 | Bonita Canyon Campground | chir |

**Explanation**: Parameterized Lookup

6. **Business Question:** What amenities do the largest campgrounds have?

   SELECT c.campground\_name,

          c.total\_sites,

          a.camp\_store,

          a.toilets,

          a.showers,

          a.water,

          a.internet,

          a.firewood,

          a.food\_storage,

          a.cell\_reception,

          a.amphitheater

   FROM campground c

   JOIN amenity a

       ON c.campground\_code \= a.campground\_code

   ORDER BY c.total\_sites DESC

   LIMIT 10;

**Sample results: Hard to demonstrate because of many columns, so I will only include camp name, park code and SOME of the amenities**

| campName | parkCode | store | showers | cellReception | toilets |
| :---- | :---- | :---- | :---- | :---- | :---- |
| Bridge Bay Campground | yell | Yes \- seasonal | None | Yes \- seasonal | Flush Toilets \- seasonal |
| Blackwoods Campground | acad | No | None | no | Flush Toilets \- seasonal |
| Big Meadows Campground | shen | Yes \- seasonal | Coin-Operated \- Seasonal | no | Flush Toilets \- seasonal |

**Explanation**: JOIN \+ ORDER BY \+ Limit

7. **Business Question:** Which campgrounds have the fewest total sites?

   SELECT campground\_name, total\_sites

   FROM campground

   ORDER BY total\_sites ASC

   LIMIT 50;

   

**Sample results:**

| campID | totalSites | rvSpots | tentSpots | campCode | campName | parkcode |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| 9 | 0 | 0 | 0 | B0B25595-CE24-4E9C-B0CD-93912216F113 | American Memorial Park | amme |
| 56 | 1 | 0 | 0 | 1CE97109-25B0-4A15-B4B9-3525EF22C1C5 | Big Spring Brook Hut | kaww |
| 10 | 7 | 0 | 7 | E7CC7363-9C34-42ED-B3F0-769BB39E9400 | Anacapa Island Campground | chis |

**Explanation**: Aggregation \+ Sorting

8. **Business Question:** What amenities do low-capacity campgrounds lack?

   WITH low\_capacity AS (

       SELECT campground\_code, campground\_name

       FROM campground

       WHERE total\_sites \< (

           SELECT AVG(total\_sites) FROM campground

       )

   )

   SELECT l.campground\_name,

          a.\*

   FROM low\_capacity l

   LEFT JOIN amenity a

       ON l.campground\_code \= a.campground\_code;

   

**Sample results: Hard to demonstrate because of columns, so I will only include a few of the columns…**

| campName | showers | water | firewood | cell | toilets |
| :---- | :---- | :---- | :---- | :---- | :---- |
| **277 North Campground** | **None** | **No water** | **No** | **Yes \- year round** | **Vault Toilets \- year round** |
| **Back Country Camping \- Green Run** | **None** | **No water** | **Yes \- seasonal** | **Yes \- year round** | **Vault Toilets \- year round** |
| **Bayside Drive-in Campground** | **Cold- Seasonal, Free \- Seasonal** | **Yes \- year round** | **Yes \- seasonal** | **Yes \- year round** | **Vault Toilets \- year round** |

**Explanation**: JOIN \+ Subquery

9. **Business Question:** List campgrounds that provide showers, ordered by total sites.

   SELECT c.campground\_name, c.total\_sites, a.showers

   FROM Campground c

   JOIN Amenity a ON c.campground\_code \= a.campground\_code

   WHERE a.showers IS NOT NULL

   ORDER BY c.total\_sites DESC;

   

**Sample results:**

| campCode | campName | parkCode | showers |
| :---- | :---- | :---- | :---- |
| **1A5B19B8-BF1F-4803-8D87-2D4091D59A4D** | **Bridge Bay Campground** | **yell** | **none** |
| **48F2732E-4251-4D81-875C-8E52839620B5** | **Apgar Campground** | **glac** | **Free \- Seasonal** |
| **3CCB0AF7-A364-4490-A788-EE00700BD108** | **Antelope Point RV Park** | **glca** | **Hot \- Year Round, Free \- Year Round** |

**Explanation**: JOIN \+ Filtering \+ ORDER BY

10. **Business Question:** Which parks have at least one campground with more than 25 tent spots?

    SELECT park\_code, COUNT(\*) AS num\_campgrounds

    FROM campground

    WHERE tent\_spots \> 25

    GROUP BY park\_code

    HAVING COUNT(\*) \>= 1;

    

**Sample results:**

| parkCode | parkName | Campgrounds | numCampgrounds |
| :---- | :---- | :---- | :---- |
| **acad** | **Acadia National Park** | **Blackwoods Campground** | **1** |
| **bisc** | **Biscayne National Park** | **Boca Chica Campground** | **1** |
| **shen** | **Shenandoah National Park** | **Big Meadows Campground** | **1** |

**Explanation**: GROUP By \+ Having

# 

# 

# 

# 

# 

# 

# 

# 

# **Backend API Implementation**

*FastAPI Structure and Organization:*

# **backend/main.py** \- In this file, I handled CORS middleware and implemented all my endpoints.

# **backend/database.py** \- Here, I set up the SQLModel database engine, this is where all my tables are created.

# **backend/models.py** \- The ORM models for SQLModel

# **backend/fetch\_data.py** \- Used to populate my tables with data from the NPS API.

# **requirements**.txt \- lists requirements for running the projects, including imports and their versions.

*Endpoint Design and RESTful principles:*

# Endpoints are all organized by /parks, /campgrounds, and /amenities, to align with my database tables. 

# Only allows for GET requests, on collection and item level. 

*Error Handling:*  
	I made good use of FastAPI’s HTTPException for the standard error messages. Additionally, I implemented descriptive error messages to alert users of invalid or missing data.

- Using CORS Middleware to allow cross-origin requests from frontend  
- SQLModel ORM allows for database consistency and type safety  
- Session management handled via context manager to ensure proper connection handling

# **Frontend Implementation**

*User Interface Design and features:*   
	The frontend is implemented using Streamlit, which offers a clean and interactive interface for users to peruse park data. Features include:

- View parks, campgrounds, amenities  
- Search for specific campgrounds  
- Search for amenities by campground  
- Execute predefined SQL queries

*Frontend Backend Interaction:*  
	The frontend communicates with the FastAPI backend through the requests library within Python. All actions trigger the appropriate GET requests.  
*Data Visualization:*  
	All results are visualized with pandas’ DataFrames for a clean appearance, everything is in a table.   
*User Interaction Flow:*

- User selects a data viewing or query option from the sidebar  
- User provides inputs if prompted  
- Streamlit sends a request to the backend API  
- Backend processes the request, queries database, and returns results in JSON  
- Frontend parses the JSON and displays the results in a table


# **Setup & Usage Instructions**

1. Installation and Environment Setup  
   1. Ensure that Python 3.10+ is installed on your system.  
   2. Install VSCode, this is where you will run the program.  
   3. Clone the project repository (GitHub Link [here](https://github.com/Naevrys/NPS_CivilEngineeringDiagnosticTool))  
   4. Install required dependencies (listed in backend/requirements.txt)  
2. Database Setup  
   1. Run database.py to initialize the database and tables if they haven’t already been created.  
   2. Populate the databases by uncommenting the necessary lines in fetch\_data.py and running the script.  
   3. You can choose how much data is populated, if you want all the data, remove any limits provided in fetch\_data.py.  
3. Start the backend API  
   1. Start FastApi by writing: **uvicorn backend.main:app \--reload**

      into your terminal.

4. Start the Frontend  
   1. Move to the frontend, streamlit\_app.py, run the script and then in the terminal, write: **streamlit run frontend/streamlit\_app.py**  
   2. NOTE: FastAPI should ALWAYS be started *before* you run the frontend.

      

*Usage Scenarios:*  
	1: A user wants to find a specific campground and its amenities. If they don’t already know the UUID of the campground, they can look it up with CTRL+f by name and find the code in the “View All” section. Then copy the code and paste into “Search Amenities.”  
	2: A park ranger wants to find out how many total campsites their park has. They navigate to the frontend, then to query 2, where they enter their park code and get their park’s total sites.  
	3: A park operator wants to find out how many campgrounds have shower accessibility. They navigate to the frontend, then to Query 9, which lists campgrounds and their shower availability. 

# **Testing & Challenges**

*How I tested the system:*  
	Truly, I did not think about testing as much as I should have, I sort of tested as I went. Of course, I never wrote all the code and ran it at the end. I tried to do things modularly. For example, when creating the tables, I started with one, then the next, then the final. Similarly for data fetching, I started with fetching a small amount of data from the API until I was able to get everything to line up correctly, then I fetched a larger batch. I did try to implement some error messages to help identify where problems might be when I was debugging, and it definitely came in handy\!   
*Major Challenges:*  
	The most difficult challenge I faced was the NPS API itself, it is kind of terrible sometimes. I only realized once I began implementing everything that my initial plan was not possible, at least not with the time I had. I had to completely reformat my tables and get rid of some columns, like wheelChairAccessibility, because of the inconsistencies within NPS api.   
*My Solution:*  
	I majorly changed my SQLModel ORM, particularly my Amenity and Campground tables. I had to figure out how to map the data I wanted into the correct columns. I wanted to keep the amenities in the project, but I had to rethink how I implemented them. I couldn’t just use booleans or list all the campgrounds that had a specific amenity, so the amenity columns became strings because that’s what the NPS api provided. It is not ideal, but it works. This will require more work on the user’s end when it comes to analyzation, but at least all the data is there in an easily accessible area.   
*Lessons Learned:*  
	Number one, don’t do a group project alone when you only have a few days to complete the whole thing. Number two, don’t procrastinate. I really do wish I would have put more initial thought into my schema and queries, I absolutely should have looked more thoroughly at the NPS api documentation when I was developing my proposal, I would’ve saved myself so much time and work. I think it is definitely obvious that the project is rushed, I should have been more methodical and given myself more time or collaborated with others on this project. 

# 

# 

# 

# **AI Documentation**

Requests:  
“Develop API endpoints for my data.”  
“Help me create a client-server architecture diagram using mermaid.”  
“Create an ER-Diagram for my schema using mermaid.”  
“Create documentation for my API endpoints.”  
“Help me write setup and usage instructions for this application.”   
“Write a readME document for this program.”  


[image1]: <data:image/png;base64,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>