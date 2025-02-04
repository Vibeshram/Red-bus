import streamlit as st
import pandas as pd
import mysql.connector as db

Navigator = st.sidebar.selectbox(
    'Navigator',
    ['Home', 'Select bus']
)

# Initialize `price_df` globally so it can be accessed in "Search"
price_df = pd.DataFrame()

if Navigator == "Home":
    st.title("Welcome to redbus!")
    st.header("Choose your bus and enjoy your ride")

elif Navigator == "Select bus":
    state_option = st.selectbox(
        'Select your preferred location to travel:',
        ('select here', 'kerala', 'assam', 'west_bengal_ctc', 'bihar', 'chandigarh', 
         'jammu_and_kashmir', 'kaac_transport', 'kadamba', 'north_bengal', 'punjab', 'west_bengal_stc')
    )

    if state_option and state_option != 'select here':
        connection = db.connect(
            host='localhost',
            user='root',
            password='Ram@1496',
            database='redbus'
        )

        query = f"""SELECT * FROM `{state_option}`"""
        state_df = pd.read_sql(query, connection)

        bus_route_option = st.selectbox(
            'Select your preferred bus route:',
            ['select here'] + state_df['route_name'].unique().tolist() if not state_df.empty else ['select here']
        )

        if bus_route_option != 'select here':
            bus_route_df = state_df[state_df['route_name'] == bus_route_option]

            bus_type_option_1 = st.selectbox('Select AC/NON-AC:', ['select here', 'AC', 'NON AC'])
            if bus_type_option_1 != 'select here':
                if bus_type_option_1 == 'NON AC':
                    bus_type_1_df = bus_route_df[bus_route_df['bus_type'].str.contains('NON|Non', case=False, na=False)]
                else:
                    bus_type_1_df = bus_route_df[~bus_route_df['bus_type'].str.contains('NON|Non', case=False, na=False)]

                bus_type_option_2 = st.selectbox('Select seater/sleeper/push back:', ['select here', 'Seater', 'Sleeper', 'Push Back'])
                if bus_type_option_2 != 'select here':
                    if bus_type_option_2 == 'Seater':
                        bus_type_2_df = bus_type_1_df[bus_type_1_df['bus_type'].str.contains('Seater', case=False, na=False)]
                    elif bus_type_option_2 == 'Sleeper':
                        bus_type_2_df = bus_type_1_df[bus_type_1_df['bus_type'].str.contains('Sleeper', case=False, na=False)]
                    elif bus_type_option_2 == 'Push Back':
                        bus_type_2_df = bus_type_1_df[bus_type_1_df['bus_type'].str.contains('Push Back', case=False, na=False)]

                    rating = st.selectbox('Select preferred ratings:', ['select here', 1, 2, 3, 4, 5])
                    if rating != 'select here':
                        rating_df = bus_type_2_df[bus_type_2_df['star_rating'] >= rating]

                        col1, col2 = st.columns(2)
                        with col1:
                            price_from_option = st.slider("Select price from:", 0.0, 10000.0, 0.0, 100.0, key="price_from")
                        with col2:
                            price_to_option = st.slider("Select price to:", 0.0, 10000.0, 10000.0, 100.0, key="price_to")

                        if 'price' in rating_df.columns:
                            price_df = rating_df[
                                (rating_df['price'] >= price_from_option) & 
                                (rating_df['price'] <= price_to_option)
                            ]
                        if st.button('Search'):
                            if price_df.empty:
                                st.error("Sorry for your inconvenience. No buses available at the moment.")
                            else:
                                st.dataframe(price_df)
            
            
        


        
