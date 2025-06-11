
import streamlit as st
import streamlit.components.v1 as components
from st_bridge import bridge
from streamlit_javascript import st_javascript

with open("map.html", "r", encoding="utf-8") as f:
        bokeh_map = f.read()

components.html(f"""
            {bokeh_map}
        """, height=300, scrolling=False)

data = bridge("my-bridge", default="Keine GKZs ausgewählt")

gkz_list = []
if data != 'Keine GKZs ausgewählt':
    gkz_list = [elem for elem in data["selected_gkz"] if elem != '']

st.write(gkz_list)

