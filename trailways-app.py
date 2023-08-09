import streamlit as st
import folium
from folium.plugins import FastMarkerCluster
import requests
import time

# Function to fetch data
def fetch_data():
    # ... [the fetch_data function remains unchanged]

# Function to create and display map
def create_map(data):
    m = folium.Map(location=[data['coachPosition']['latitude'], data['coachPosition']['longitude']], zoom_start=13)
    
    # ... [rest of the mapping code remains unchanged]

    return m

# Main Streamlit app
def main():
    st.title("Bus Tracker")

    data = fetch_data()
    m = create_map(data)

    # Streamlit doesn't support Folium directly. We'll use folium_static to display maps.
    from streamlit_folium import folium_static
    folium_static(m)

    # Refresh every 15 seconds (Streamlit's native way)
    st.write(f"Last updated at: {time.strftime('%H:%M:%S')}")
    st.button("Refresh Now!")
    st.text("Map will auto-refresh every 15 seconds.")

if __name__ == "__main__":
    main()
