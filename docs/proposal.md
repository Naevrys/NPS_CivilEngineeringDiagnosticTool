# **IEE 305 Term Project Proposal**

**Due Date:** November 25th, 11:59 PM **Points:** 50

---

## **1\. Group Information (3 points)**

**Project Title:** Analysis tool to help civil engineers make decisions on infrastructure surrounding National Park campgrounds and their amenities

**Selected API Option:**  National Parks System 

**Group Members:**

removed because this repo is public

---

## **2\. Industrial Engineering Problem Statement (10 points)**

### **Problem Context (1-2 paragraphs)**

	A big “perk” of the National Parks in the states is being able to stay directly within them, in campgrounds among the wilderness. But, these campgrounds can only hold so many people, and only come with so many amenities. It is the duty of civil engineers to help create, maintain, develop and improve public infrastructure like campgrounds. With so many parks experiencing vast numbers of visitors every year, it is important that campground data is easy to find and organized as well. A tool that explicitly tracks this data across the different parks would be invaluable.

### **Solution Approach (1 paragraph)**

	This system will help engineers make better decisions by providing them with accurate, relevant, and on demand information. It will allow engineers to gather all the data into one easily accessible area and more readily identify both negative and positive trends. Engineers will be able to pinpoint which campgrounds are lacking in what they offer and develop plans to improve them. The data this tool presents could also aid engineers in creating relationships and correlations between demand/capacity and the amenities that each campground offers.

### **Target Users and Use Cases**

**Target Users:** Civil engineers that work with park planning and infrastructure (particularly surrounding visitors and campgrounds)

**Primary Use Cases:** 1\. Locating which campgrounds have the most amenities

2\. Locating which campgrounds lack essential amenities

3\. Locate campgrounds that lack accessibility

---

## **3\. Entity-Relationship Model (10 points)**

### **ER Diagram**

**![][image1]**

### **Entity Descriptions**

**Entity 1: National Park** \- **Description:** A national park within the U.S. 

\- **Attributes:** \-

park\_id (PRIMARY KEY) \- Integer, unique identifier to track distinct parks   
name \- String, the park’s full name   
state \- String, the state that the park is located in

**Entity 2: Campground**\- **Description:** a single campground in one of the parks

 \- **Attributes:** \- 

campground\_id (PRIMARY KEY) \- Integer, unique identifier for campgrounds 

campground\_name \- String, full campground name 

total\_sites\- Int, number of people allowed to stay in the campground at one time

Tent\_spots \- Int \# of tent camping areas in campground

rv\_spots  \- Int, \# of rv spots available in campground

wheelchair\_accessible \- boolean, states whether or not the campground is wheelchair friendly

Park\_id \- Int, foreign key, national park that the campground belongs to

**Entity 3: Amenity** \- **Description:** amenity at a specific campground

 \- **Attributes:** \- 

amenity\_id (PRIMARY KEY) \- Integer, unique identifier for each amenity

amenity\_name \- String, name of amenity, e.g. showers

Availability \- String, is the amenity available at a given campground, or type of amenity available

campground\_id \- Foreign Key, is the amenity available in this given campground

### **Relationship Descriptions**

**Relationship 1: National Park ↔ campground** \- **Type:** One National Park to many campgrounds(1:N)- **Description:** Each national park contains many campgrounds but each campground only belongs to one national park 

**Relationship 2: campground ↔ amenity** \- **Type:** Many campgrounds have many amenities (M:N) \- **Description:** A campground has many amenities and an amenity may be found at many campgrounds

---

## **4\. Relational Data Model (10 points)**

### **Table Schemas**

**Table 1: national\_park**

**CREATE** **TABLE** national\_park (  
    park\_id INTEGER NOT NULL **PRIMARY** **KEY**,  
    park\_name TEXT **NOT** **NULL**,  
    state TEXT **NOT** **NULL**,  
);

**Table 2: campground**

**CREATE** **TABLE** campground (  
    campground\_id INTEGER **PRIMARY** **KEY**,  
    campground\_name TEXT **NOT** **NULL**,  
    total\_sites INTEGER **NOT** **NULL**,  
    tent\_spots INTEGER,  
    rv\_spots INTEGER,  
    Wheelchair\_accessible BOOL **NOT** **NULL**,  
    park\_id INTEGER **NOT** **NULL**,  
    **FOREIGN** **KEY** (park\_id) **REFERENCES** national\_park(park\_id)  
);

**Table 3: amenity**

**CREATE** **TABLE** amenity (  
	amenity\_id INTEGER NOT NULL PRIMARY KEY,  
amenity\_name TEXT NOT NULL,  
availability TEXT,  
campground\_id INTEGER,  
    **FOREIGN** **KEY** (campground\_id) **REFERENCES** campground(campground\_id)  
);

### **Normalization Analysis (3NF)**

**First Normal Form (1NF):** \- ✅ All attributes contain atomic values \- **Justification:** 

All of my tables meet the qualifications for 1NF because every attribute contains atomic values and there are no multivalued attributes.

**Second Normal Form (2NF):** \- ✅ No partial dependencies \- **Functional Dependencies:** \- Table 1: park name and state depend on park id 

\- Table 2: all campground attributes are dependant on campground id 

\- Table 3: all amenity attributes are dependant on amenity id

**Third Normal Form (3NF):** \- ✅ No transitive dependencies \- **Justification:**

My tables meet the qualifications for 3NF because each table’s attributes (excluding foreign keys) depend only on  that table's primary key.

---

## **5\. Sample Scraped Data (5 points)**

### **Data Fetching Status**

* **API Endpoint(s) Used:** 

* /parks

* /campgrounds  
* /amenities/parksplaces

* **Total Records Fetched:** \~600 records

* **Data Transformation:** I will parse the data collected and map it to relational schema for the database. The data is collected and converted (if necessary) into text, integers, or boolean values and then added into the tables.

### **Sample Data (3+ records per table)**

**Table 1: national\_park**

| park\_id | park\_name | state |
| :---- | :---- | :---- |
| 1 | Yellowstone National Park | WY |
| 2 | Yosemite National Park | CA |
| 3 | Grand Canyon National Park | AZ |

**Table 2: campground**

| campground\_id | campground\_name | total\_sites | tent\_spots | rv\_spots | wheelchair\_accessible | park\_id |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| 1 | Upper Pines | 235 | 203 | 32 | True | 2 |
| 2 | Mammoth Campground | 85 | 85 | 0 | True | 1 |
| 3 | Mather Campground | 327 | 327 | 0 | True | 3 |

**Table 3: amenity**

| amenity\_id | amenity\_name | availability | camground\_id |
| :---- | :---- | :---- | :---- |
| 1 | Camp Store | Yes | 3 |
| 2 | Camp Store | No | 1 |
| 3 | Toilets | Flush Toilets | 2 |

---

## **6\. SQL Query Specifications (7 points)**

**Your 10 queries must collectively cover these 7 SQL concepts:** 1\. Basic Filtering (SELECT with WHERE) 2\. JOIN Operations (2+ tables, including at least one 3-table join) 3\. Aggregation Functions (COUNT, SUM, AVG, MIN, or MAX) 4\. GROUP BY with HAVING 5\. Subqueries or CTEs 6\. ORDER BY with LIMIT 7\. Parameterized Query (SQL injection prevention)

**Note:** Some queries can demonstrate multiple concepts simultaneously.

---

**Query 1:** \- Business Question: Which campgrounds have fewer than 30 sites?

\- SQL Concepts Demonstrated: Basic Filtering

**Query 2:** \- Business Question: How many total sites are in a given park?

\- SQL Concepts Demonstrated: JOIN operations and Filtering

**Query 3:** \- Business Question: How many amenities does each campground have in a given park?

\- SQL Concepts Demonstrated: JOIN, Aggregation, and Filtering

**Query 4:** \- Business Question: Which campgrounds have an above or below average number of amenities?

 \- SQL Concepts Demonstrated: Subqueries/CTEs, Aggregation, filtering

**Query 5:** \- Business Question: Which parks have campgrounds with the most campsites? 

\- SQL Concepts Demonstrated: Group by having, aggregation

**Query 6:** \- Business Question: Look up a campgrounds data by name/id.

\- SQL Concepts Demonstrated: Parameterized query, filtering

**Query 7:** \- Business Question: What amenities do the campgrounds with the largest capacities have (total sites)?

\- SQL Concepts Demonstrated: JOIN, Aggregation, ORDER 

**Query 8:** \- Business Question: Which campgrounds have the fewest amenities? 

\- SQL Concepts Demonstrated: Aggregation, filtering, ORDER by

**Query 9:** \- Business Question: What amenities do campgrounds with low capacities lack?

\- SQL Concepts Demonstrated: JOIN, Subquery, Filtering

**Query 10:** \- Business Question: List campgrounds by accessibility.

 \- SQL Concepts Demonstrated: FIltering, ORDER by

---

## **7\. API Integration Plan (2 points)**

**Primary API Endpoint(s):** \- /parks, /amenities/parksplaces, /campgrounds

**Authentication:** Yes, obtained for free through [NPS.gov](http://NPS.gov) documentation for the NPS api.

**Data Fetching Strategy:** One-Time Population

**Expected Record Counts:** \- Table 1: 63 \- Table 2: 1,421 \- Table 3: Up to 15,000

**Data Mapping:**

| API Field | Database Table | Database Column | Transformation |
| :---- | :---- | :---- | :---- |
| fullName | national\_park | park\_name | As is |
| totalSites | campground | total\_sites | As is |

---

## **8\. Technology Stack (3 points)**

**Backend:** \- Database Access: I will use SQLModel and likely requests \+ pandas for my backend work. 

**Frontend:** \- Framework: Streamlit \- Visualization: Plotly or Altair

**Justification:** I have chosen to go with SQLModel and requests \+ pandas because I am most familiar with them. For my frontend, I have decided to go with Streamlit because it integrates seamlessly with Python and is very quick/easy to set up. Similarly, I chose plotly/altair because they integrate well with Streamlit. 

[image1]: <data:image/png;base64,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>