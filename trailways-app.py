import streamlit as st
import requests
import time
import pandas as pd

BASE_URL = "https://services.saucontds.com/forecasting-services/configuredTripStatus.ws?departureStopExternalId=7944277&destinationStopExternalId=7944280&source=desktop"
API_KEY_URL = "https://services.saucontds.com/forecasting-services/public/publicSchedule/json?companyLocationID=122679566&encryptedUserId=kWUGO2NlflrXUj4Uf8KQzbDT-PoiE3XZ0Hty6ZzkdNJnVTev6hDSVR-NfBe5GLNqMq40Tt3QIvTB5VP2m3gXyTAOvDMx*nhr5r7*20"

HEADERS = {
    # Your headers here (kept unchanged)
}

def retrieve_api_key():
    response = requests.get(API_KEY_URL)
    data = response.json()
    return data["key"]

def fetch_data(service_date, departure_time):
    key = retrieve_api_key()
    url = f"{BASE_URL}&serviceDate={service_date}&departureTime={departure_time}&key={key}"
    response = requests.get(url, headers=HEADERS)
    return response.json()

def display_map(data):
    vehicle_path = data['coachPosition']['vehiclePath']
    df_path = pd.DataFrame(vehicle_path)
    df_path.columns = ['lat', 'lon']  # Rename columns to be recognized by st.map
    st.map(df_path)

def main():
    st.title("Bus Tracker")

    # Input for date and time
    service_date = st.sidebar.date_input("Service Date")
    departure_time = st.sidebar.time_input("Departure Time")

    # Display a countdown timer for key retrieval
    countdown_time = 600  # 10 minutes in seconds
    st.sidebar.header("Next Key Retrieval In:")
    timer_text = st.sidebar.empty()
    for remaining_seconds in range(countdown_time, 0, -1):
        minutes, seconds = divmod(remaining_seconds, 60)
        timer_text.text(f"{minutes:02}:{seconds:02}")
        time.sleep(1)

    # Fetch and display data
    data = fetch_data(service_date.strftime('%Y-%m-%d'), departure_time.strftime('%I:%M %p'))
    display_map(data)

if __name__ == "__main__":
    main()
