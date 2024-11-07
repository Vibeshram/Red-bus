import streamlit as st
import pandas as pd 
import mysql.connector as db
from datetime import time  # Import the time class for time range selection

# Main header of the webpage
st.title("Welcome to RedBus!")
st.write("Pick your bus, enjoy the ride.")

# Add a horizontal line for separation
st.markdown("---")

# Select box for location
state_option = st.selectbox(
    'Select your preferred location to travel:',
    ('select here', 'kerala', 'assam', 'west_bengal_ctc', 'bihar', 'chandigarh', 'jammu_and_kashmir', 
     'kaac_transport', 'kadamba', 'north_bengal', 'punjab', 'west_bengal_stc')
)

st.write('You selected:', state_option)

# Connect to the database
connection = db.connect(
    host='localhost',
    user='root',
    password='Ram@1496',
    database='redbus'
)

# Query for selected state
if state_option != 'select here':
    query = f"""SELECT * FROM `{state_option}`"""  # Replace state_option with your actual table name
    state_df = pd.read_sql(query, connection)  # Fetch data into a DataFrame

    # Select box for bus route, populated from the DataFrame's 'Route Name' column
    bus_route_option = st.selectbox(
        'Select your preferred bus route to travel:',
        ['select here'] + state_df['route_name'].unique().tolist()
    )

    st.write('You selected:', bus_route_option)

    bus_type_option = st.selectbox(
        'Select your preferred bus type to travel:',
        ['select here'] + state_df['bus_type'].unique().tolist()
    )

    st.write("You selected:", bus_type_option)

    # departure_time range sliders with unique keys
    departure_time_from_option = st.slider(
        "Select departure time from:",
        value=(time(0, 0)),  # Default start at midnight
        format="HH:mm",
        key="departure_time_from"
    )
    departure_time_to_option = st.slider(
        "Select departure time to:",
        value=(time(23, 59)),  # Default end at 23:59
        format="HH:mm",
        key="departure_time_to"  # Unique key
    )
    st.write("Your selected time range:", departure_time_from_option, "to", departure_time_to_option)

    # arrival time range sliders with unique keys
    arrival_time_from_option = st.slider(
        "Select arrival time from:",
        value=(time(0, 0)),  # Default start at midnight
        format="HH:mm",
        key="arrival_time_from"
    )
    arrival_time_to_option = st.slider(
        "Select arrival time to:",
        value=(time(23, 59)),  # Default end at 23:59
        format="HH:mm",
        key="arrival_time_to"  # Unique key
    )
    st.write("Your selected time range:", arrival_time_from_option, "to", arrival_time_to_option)

    # duration time range sliders with unique keys
    duration_time_from_option = st.slider(
        "Select duration time from:",
        value=(time(0, 0)),  # Default start at midnight
        format="HH:mm",
        key="duration_time_from"
    )
    duration_time_to_option = st.slider(
        "Select duration time to:",
        value=(time(23, 59)),  # Default end at 23:59
        format="HH:mm",
        key="duration_time_to"  # Unique key
    )
    st.write("Your selected time range:", duration_time_from_option, "to", duration_time_to_option)

    star_rating_from_option = st.slider(
        "select rating from:",
        min_value=0.0,
        max_value=5.0,
        value = (0.0),
        key = "rating_from"
    )

    star_rating_to_option = st.slider(
        "select rating to:",
        min_value=0.0,
        max_value=5.0,
        value = (5.0),
        key = "rating_to"
    )

    st.write("Your selected rating range:", star_rating_from_option, "to", star_rating_to_option)

    price_from_option = st.slider(
        "select price from:",
        min_value = 0.0,
        max_value = 10000.0,
        value = (0.0),
        step=100.0,
        key = "price_from"
    )

    price_to_option = st.slider(
        "select price to:",
        min_value = 0.0,
        max_value = 10000.0,
        value = (10000.0),
        step=100.0,
        key = "price_to"
    )

    st.write("Your selected price from", price_from_option, "to", price_to_option) 

    seat_availability_from_option = st.slider(
        "select required seat from:",
        min_value = 0,
        max_value = 60,
        value = 0,
        key = 'seat_required_from'
    )

    seat_availability_to_option = st.slider(
        "select required seat to:",
        min_value = 0,
        max_value = 60,
        value = 60,
        key = 'seat_required_to'
    )

    st.write("Number of seets you have selected from range", seat_availability_from_option, "to", seat_availability_to_option)


    # Only query if a specific route is selected
    if bus_route_option != 'select here':
        route_query = f"""
        SELECT * FROM `{state_option}`
        WHERE route_name = '{bus_route_option}'
        AND bus_type = '{bus_type_option}' 
        AND departure_time BETWEEN '{departure_time_from_option}' AND '{departure_time_to_option}'
        AND arrival_time BETWEEN '{arrival_time_from_option}' AND '{arrival_time_to_option}'
        AND duration BETWEEN '{duration_time_from_option}' AND '{duration_time_to_option}'
        AND star_rating BETWEEN '{star_rating_from_option}' AND '{star_rating_to_option}'
        AND price BETWEEN '{price_from_option}' AND '{price_to_option}'
        AND seats_available BETWEEN '{seat_availability_from_option}' AND '{seat_availability_to_option}'
        """
    # Fetch and display filtered data
    filtered_df = pd.read_sql(route_query, connection)

    if filtered_df.empty:
        st.error("Sorry for your inconvenience. No buses available at the moment.")
    else:
        st.dataframe(filtered_df)

# Close the connection after use
connection.close()
