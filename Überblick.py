import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import geopandas as gpd
#from shapely.geometry import Polygon
from data import *

with st.sidebar:
    # Slider for pitch (tilt angle)
    pitch = st.checkbox("Tilt", value=False)

    # Optional: Slider for bearing (rotation)
    #bearing = st.slider("Adjust Map Bearing (Rotation)", min_value=0, max_value=360, value=0, step=10)
    elevation = st.checkbox('Show elevation', value=False)

    heatmap = st.checkbox('Heat-Map', value=False)



if pitch == False:
    pitched = 0
else:
    pitched = 25
gdf = gpd.read_file('data/ktn_data.json')
#gdf["lon"] = gdf.apply(lambda row: Polygon(row["geometry"]).centroid.x, axis=1)
#gdf["lat"] = gdf.apply(lambda row: Polygon(row["geometry"]).centroid.y, axis=1)
df = get_data('t_bev1.csv', 2025, 2025)

df = df.groupby(["Jahr", "gkz"]).agg({'Anzahl': 'sum'}).reset_index()
df["gkz"] = df["gkz"].astype(str)
#df["Anzahl"] = df["Anzahl"]
if heatmap:
    df["Color"] = df["Anzahl"].apply(lambda x: 
                                    [255, 0, 0, 255] if x > 50000 else 
                                    [255, 69, 0, 255] if x > 10000 else
                                    [255, 140, 0, 255] if x > 5000 else  
                                    [255, 185, 0, 255] if x > 2500 else 
                                    [255, 255, 0, 255] if x > 1000 else
                                    [235, 235, 235, 255])
else:
    df["Color"] = '[255, 255, 255, 255]'

chart_data = pd.merge(gdf, df, left_on='GKZ', right_on='gkz')
geojson = chart_data.__geo_interface__ 

#chart_data = pd.DataFrame(
#    np.random.randn(1000, 2) / [50, 50] + [46.74, 13.51],
#    columns=["lat", "lon"],
#)
tooltip = {"html": "<b>Gemeinde:</b> {GEMNAM}<br/><b>Anzahl:</b> {Anzahl}", "style": {"color": "white"}}


chart = pdk.Deck(
        map_provider=None,
        map_style='light_no_labels',
        initial_view_state=pdk.ViewState(
            latitude=46.94,
            longitude=13.81,
            zoom=7.5,
            pitch=pitched,
            #bearing=bearing,
            max_zoom=9,
            min_zoom=7.5
        ),
        layers=[
             pdk.Layer(
                    "GeoJsonLayer",
                    data=geojson,
                    stroked=True,
                    filled=True,
                    id = "properties.GKZ",
                    get_fill_color="properties.Color",#"properties.Color",
                    get_line_color=[0, 0, 0, 255],
                    line_width_min_pixels=1,
                    get_elevation="properties.Anzahl",
                    pickable=True,
                    extruded=elevation,
                )
            #pdk.Layer(
            #    "HexagonLayer",
            #    data=chart_data,
            #    get_position="[lon, lat]",
            #    radius=3000,
            #    #elevation_scale=4,
            #    height="Anzahl",
            #    pickable=True,
            #    extruded=True,
            #),
            #pdk.Layer(
            #    "ScatterplotLayer",
            #    data=chart_data,
            #    get_position="[lon, lat]",
            #    get_color="[200, 30, 0, 160]",
            #    get_radius=200,
            #),
        ],tooltip=tooltip
    )


event = st.pydeck_chart(chart, on_select="rerun", selection_mode="multi-object")
#event.selection
gkz_list = []
for elem in event.selection["objects"]["properties.GKZ"]:
    gkz_list.append(f'{elem["properties"]["gkz"]}')
#st.write(gkz_list)
df = df[df["gkz"].isin(gkz_list)]
df = df.groupby(["Jahr"]).agg({'Anzahl': 'sum'}).reset_index()
st.write(df)