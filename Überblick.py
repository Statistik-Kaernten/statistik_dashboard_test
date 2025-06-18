import streamlit as st
import pandas as pd
#import numpy as np
import pydeck as pdk
import geopandas as gpd
#from shapely.geometry import Polygon
from data import *

UNSELECTED = [100, 0, 200, 255]
SELECTED = [245, 0, 245, 255]

def set_colors(df: pd.DataFrame, gkz_list: list[str]):
    df['Color'] = df['GKZ'].apply(lambda x: SELECTED if x in gkz_list else UNSELECTED)
    return df

gdf = gpd.read_file('data/ktn_data.json')

gkz_list = []
tooltip = {"html": "{GEMNAM}", "style": {"color": "white"}}


regio = [str(regio) for regio in getSelectionItems() if regio != 'Gkz']
regio.append('Eigene Auswahl')

with st.sidebar:
    region = st.selectbox('Region:', regio)
    if region != 'Eigene Auswahl':
        sub_region = st.selectbox(f'{region}', [str(gkz) for gkz in getSubRegion(region)])
        gkz_list = [str(subreg) for subreg in getGkz(region, sub_region)]
    else:
        gkz_list = []

gdf = set_colors(gdf, gkz_list)
geojson = gdf.__geo_interface__ 

chart = pdk.Deck(
        map_provider=None, #'carto'
        map_style='light',
        initial_view_state=pdk.ViewState(
            latitude=46.94,
            longitude=13.81,
            zoom=6.5,
            max_zoom=6.5,
            min_zoom=6.5,
        ),
        layers=[
             pdk.Layer(
                    "GeoJsonLayer",
                    data=geojson,       
                    stroked=True,
                    filled=True,
                    drag_pan=False,
                    id = "properties.GKZ",
                    get_fill_color="properties.Color",
                    get_line_color=[0, 0, 0, 255],
                    line_width_min_pixels=0.5,
                    pickable=True
                )
        ],
        tooltip=tooltip
    )
with st.sidebar:
    if region != 'Eigene Auswahl':
        st.pydeck_chart(chart, height=250, use_container_width=True)
    else:
        event = st.pydeck_chart(chart, on_select="rerun", selection_mode="multi-object", height=250, use_container_width=True)
        try: 
            for elem in event.selection["objects"]["properties.GKZ"]:
                gkz_list.append(f'{elem["properties"]["GKZ"]}')
        except:
            pass
st.write(gkz_list)
#event.selection

df = gdf[gdf["GKZ"].isin(gkz_list)]
#df = df.groupby(["Jahr"]).agg({'Anzahl': 'sum'}).reset_index()
#heat_df = heat_df.sort_values('Anzahl', ascending=False)
#st.write(heat_df)
st.write(df)