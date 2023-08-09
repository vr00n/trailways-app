import streamlit as st
import requests
import time
import pandas as pd

# Constants
URL = "https://services.saucontds.com/forecasting-services/configuredTripStatus.ws?departureStopExternalId=7944277&destinationStopExternalId=7944280&serviceDate=2023-08-09&departureTime=07:00%20am&source=desktop&key=nUB*IQliXkm6Wh8cKIGi0LboTLCpsb1VfTTDMDank42jGJbDhHl59wDP7C38c5QDGn-0bTS0LhZBxnltjBQhdCA5517smVEBowRe20"

HEADERS = {
    #... [headers remain unchanged]
}

# Function to fetch data
def fetch_data():
    response = requests.get(URL, headers=HEADERS)
    return response.json()

# Display map using st.map()
def display_map(data):
    # Extracting the vehicle's current position
    current_position = {
        "latitude": data['coachPosition']['latitude'],
        "longitude": data['coachPosition']['longitude']
    }
    
    # Extracting the vehicle's path
    path_data = data['coachPosition']['vehiclePath']
    df_path = pd.DataFrame(path_data).rename(columns={"lat": "latitude", "lng": "longitude"})
    
    # Rendering the map
    map_data = pd.DataFrame([current_position])
    st.map(map_data)

    # If you'd also like to display the path, you can do:
    st.map(df_path)

# Main Streamlit app
def main():
    st.title("Bus Tracker")

    data = fetch_data()
    display_map(data)

    # Display last updated time and refresh button
    st.write(f"Last updated at: {time.strftime('%H:%M:%S')}")
    if st.button("Refresh Now!"):
        st.experimental_rerun()

if __name__ == "__main__":
    main()
