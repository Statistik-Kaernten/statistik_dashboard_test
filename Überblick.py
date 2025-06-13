import streamlit as st
import pandas as pd
import pydeck as pdk

# Sample data
data = pd.DataFrame({
    'lat': [37.7749, 34.0522],
    'lon': [-122.4194, -118.2437],
    'city': ['San Francisco', 'Los Angeles']
})

# Define the layer
layer = pdk.Layer(
    "ScatterplotLayer",
    data,
    get_position='[lon, lat]',
    get_color='[200, 30, 0, 160]',
    get_radius=10000,
    pickable=True  # Enables hover
)

# Define the tooltip
tooltip = {"html": "<b>City:</b> {city}", "style": {"color": "white"}}

# Create deck.gl map
st.pydeck_chart(pdk.Deck(
    map_style='mapbox://styles/mapbox/light-v9',
    initial_view_state=pdk.ViewState(
        latitude=36.5,
        longitude=-120,
        zoom=5,
        pitch=50,
    ),
    layers=[layer],
    tooltip=tooltip
))