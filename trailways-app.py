import streamlit as st
from folium.plugins import FastMarkerCluster
import requests
import time
from streamlit_folium import folium_static

# Constants
URL = "https://services.saucontds.com/forecasting-services/configuredTripStatus.ws?departureStopExternalId=7944277&destinationStopExternalId=7944280&serviceDate=2023-08-09&departureTime=07:00%20am&source=desktop&key=nUB*IQliXkm6Wh8cKIGi0LboTLCpsb1VfTTDMDank42jGJbDhHl59wDP7C38c5QDGn-0bTS0LhZBxnltjBQhdCA5517smVEBowRe20"

HEADERS = {
    #... [headers remain unchanged]
}

# Function to fetch data
def fetch_data():
    response = requests.get(URL, headers=HEADERS)
    return response.json()

# Function to create and display map
def create_map(data):
    m = folium.Map(location=[data['coachPosition']['latitude'], data['coachPosition']['longitude']], zoom_start=13)
    
    # Add vehicle position
    folium.Marker(
        [data['coachPosition']['latitude'], data['coachPosition']['longitude']],
        popup=f"Bus: {data['coachPosition']['name']}<br>Location: {data['coachPosition']['streetLocation']}",
        icon=folium.Icon(color='red', icon='bus')
    ).add_to(m)

    # Add path
    vehicle_path = [(point['lat'], point['lng']) for point in data['coachPosition']['vehiclePath']]
    folium.PolyLine(vehicle_path, color="blue", weight=2.5, opacity=1).add_to(m)

    return m

# Main Streamlit app
def main():
    st.title("Bus Tracker")

    data = fetch_data()
    m = create_map(data)

    # Render the Folium map with the streamlit-folium plugin
    folium_static(m)

    # Display last updated time and refresh button
    st.write(f"Last updated at: {time.strftime('%H:%M:%S')}")
    if st.button("Refresh Now!"):
        st.experimental_rerun()

if __name__ == "__main__":
    main()
