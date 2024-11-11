import streamlit as st
import pandas as pd
import mysql.connector as db
from datetime import datetime, timedelta

st.title("Welcome to redbus!")
st.header("Choose your bus and enjoy your ride")

Navigator = st.sidebar.selectbox(
    'Navigator',
    ['Home', 'Select bus']
)

if Navigator == "Select bus":
    # Select box for location
    state_option = st.selectbox(
        'Select your preferred location to travel:',
        ('select here', 'kerala', 'assam', 'west_bengal_ctc', 'bihar', 'chandigarh', 'jammu_and_kashmir', 
         'kaac_transport', 'kadamba', 'north_bengal', 'punjab', 'west_bengal_stc')
    )
    st.write('You selected:', state_option)

    # Initialize connection only if a specific state is selected
    if state_option != 'select here':
        # Connect to the database
        connection = db.connect(
            host='localhost',
            user='root',
            password='Ram@1496',
            database='redbus'
        )

        # Query for the selected state
        query = f"""SELECT * FROM `{state_option}`"""
        state_df = pd.read_sql(query, connection)  # Fetch data into a DataFrame

        # Select box for bus route, populated from the DataFrame's 'Route Name' column
        bus_route_option = st.selectbox(
            'Select your preferred bus route to travel:',
            ['select here'] + state_df['route_name'].unique().tolist()
        )
        st.write('You selected:', bus_route_option)

        # Select box for bus type, populated from the DataFrame's 'Bus Type' column
        bus_type_option = st.selectbox(
            'Select your preferred bus type to travel:',
            ['select here'] + state_df['bus_type'].unique().tolist()
        )
        st.write("You selected:", bus_type_option)

        # Generate a list of times in 15-minute intervals for 24 hours
        times = [(datetime.min + timedelta(minutes=15 * i)).strftime("%H:%M") for i in range(96)]
        
        # Create columns for "Departure time from" and "Departure time to"
        col1, col2 = st.columns(2)
        with col1:
            departure_time_from_option = st.selectbox('Departure time from:', times)
        with col2:
            departure_time_to_option = st.selectbox('Departure time to:', times)
        
        st.write("Your selected departure time from:", departure_time_from_option)
        st.write("Your selected departure time to:", departure_time_to_option)

        # Create columns for "Duration time from" and "Duration time to"
        col3, col4 = st.columns(2)
        with col3:
            duration_time_from_option = st.selectbox('Duration time from:', times)
        with col4:
            duration_time_to_option = st.selectbox('Duration time to:', times)
        
        st.write("Your selected duration time from:", duration_time_from_option)
        st.write("Your selected duration time to:", duration_time_to_option)

        # Select range for star rating
        star_rating_from_option = st.slider(
            "Select rating from:",
            min_value=0.0,
            max_value=5.0,
            value=0.0,
            key="rating_from"
        )

        star_rating_to_option = st.slider(
            "Select rating to:",
            min_value=0.0,
            max_value=5.0,
            value=5.0,
            key="rating_to"
        )

        st.write("Your selected rating range:", star_rating_from_option, "to", star_rating_to_option)

        # Select range for price
        price_from_option = st.slider(
            "Select price from:",
            min_value=0.0,
            max_value=10000.0,
            value=0.0,
            step=100.0,
            key="price_from"
        )

        price_to_option = st.slider(
            "Select price to:",
            min_value=0.0,
            max_value=10000.0,
            value=10000.0,
            step=100.0,
            key="price_to"
        )

        # Only query if a specific route is selected
        if bus_route_option != 'select here':
            route_query = f"""
            SELECT * FROM `{state_option}`
            WHERE route_name = '{bus_route_option}'
            AND bus_type = '{bus_type_option}' 
            AND departure_time BETWEEN '{departure_time_from_option}' AND '{departure_time_to_option}'
            AND duration BETWEEN '{duration_time_from_option}' AND '{duration_time_to_option}'
            AND star_rating BETWEEN '{star_rating_from_option}' AND '{star_rating_to_option}'
            AND price BETWEEN '{price_from_option}' AND '{price_to_option}'
            """
            # Fetch and display filtered data
            filtered_df = pd.read_sql(route_query, connection)

            if filtered_df.empty:
                st.error("Sorry for your inconvenience. No buses available at the moment.")
            else:
                st.dataframe(filtered_df)
                

        # Close the connection after use
        connection.close()
