import streamlit as st
import requests
import time
import pandas as pd

# Base URL without the dynamic parameters (serviceDate and departureTime)
BASE_URL = "https://services.saucontds.com/forecasting-services/configuredTripStatus.ws?departureStopExternalId=7944277&destinationStopExternalId=7944280&source=desktop&key=nUB*IQliXkm6Wh8cKIGi0LboTLCpsb1VfTTDMDank42jGJbDhHl59wDP7C38c5QDGn-0bTS0LhZBxnltjBQhdCA5517smVEBowRe20"

HEADERS = {
    #... [headers remain unchanged]
}

# Function to fetch data
def fetch_data(service_date, departure_time):
    # Construct the full URL using the user's input
    url = f"{BASE_URL}&serviceDate={service_date}&departureTime={departure_time}"
    response = requests.get(url, headers=HEADERS)
    return response.json()

# Display map using st.map()
def display_map(data):
    # Extracting the vehicle's current position
    current_position = {
        "latitude": data['coachPosition']['latitude'],
        "longitude": data['coachPosition']['longitude']
    }
    
    # Extracting the vehicle's path and renaming columns
    path_data = data['coachPosition']['vehiclePath']
    df_path = pd.DataFrame(path_data).rename(columns={"lat": "latitude", "lng": "longitude"})
    
    # Rendering the map
    map_data = pd.DataFrame([current_position])
    st.map(map_data)

    # Displaying the path:
    st.map(df_path)

# Main Streamlit app
def main():
    st.title("Bus Tracker")
    
    # User inputs for service date and departure time
    service_date = st.date_input("Service Date", value=pd.to_datetime("2023-08-09"))
    departure_time = st.time_input("Departure Time", value=pd.to_datetime("07:00").time())
    
    # Format the user input for URL
    formatted_date = service_date.strftime('%Y-%m-%d')
    formatted_time = departure_time.strftime('%I:%M %p')

    # Fetch and display data
    data = fetch_data(formatted_date, formatted_time)
    display_map(data)

    # Display last updated time and refresh button
    st.write(f"Last updated at: {time.strftime('%H:%M:%S')}")
    if st.button("Refresh Now!"):
        st.experimental_rerun()

if __name__ == "__main__":
    main()
