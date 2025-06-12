
#import streamlit as st
#import streamlit.components.v1 as components
#from st_bridge import bridge
#from streamlit_javascript import st_javascript

#with open("map.html", "r", encoding="utf-8") as f:
#        bokeh_map = f.read()

#components.html(f"""
#            {bokeh_map}
#        """, height=300, scrolling=False)

#data = bridge("my-bridge", default="Keine GKZs ausgewählt")

#gkz_list = []
#if data != 'Keine GKZs ausgewählt':
#    gkz_list = [elem for elem in data["selected_gkz"] if elem != '']

#st.write(gkz_list)

#from st_bridge import bridge, html
#import streamlit as st#

#data = bridge("my-bridge", default=None)

# Use "window.top" in your HTML/JS
#html("""
#<button onClick="window.top.stBridges.send('my-bridge', 'clicked!')">
#  Click me
#</button>
#""", unsafe_allow_html=True)

#if data:
#    st.write("Bridge data received:", data)

#import streamlit as st
#import streamlit.components.v1 as components

# Declare the component:
#my_component = components.declare_component("my_component", path="frontend/build")

# Use it:
#my_component(greeting="Hello", name="World")


import plotly.express as px
import streamlit as st

from plotly1 import plotly_events
# from plotly2 import plotly_events
#from plotly3 import plotly_events

df = px.data.iris()
fig = px.scatter(df, x="sepal_width", y="sepal_length", title="Sample Figure")

value = plotly_events(fig)
st.write("Received", value)