import streamlit as st
import folium
from folium.plugins import FastMarkerCluster
import requests
import time

# Constants
URL = "https://services.saucontds.com/forecasting-services/configuredTripStatus.ws?departureStopExternalId=7944277&destinationStopExternalId=7944280&serviceDate=2023-08-09&departureTime=07:00%20am&source=desktop&key=nUB*IQliXkm6Wh8cKIGi0LboTLCpsb1VfTTDMDank42jGJbDhHl59wDP7C38c5QDGn-0bTS0LhZBxnltjBQhdCA5517smVEBowRe20"

HEADERS = {
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.9,es;q=0.8',
    'Connection': 'keep-alive',
    'DNT': '1',
    'Referer': 'https://services.saucontds.com/customer-bus-tracker/?busTrackerId=38',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"'
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

    # Streamlit doesn't support Folium directly. We'll use folium_static to display maps.
    from streamlit_folium import folium_static
    folium_static(m)

    # Display last updated time and refresh button
    st.write(f"Last updated at: {time.strftime('%H:%M:%S')}")
    if st.button("Refresh Now!"):
        st.experimental_rerun()

if __name__ == "__main__":
    main()
