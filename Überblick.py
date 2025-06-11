'''
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
#st.write("HELLO")
'''
import streamlit as st
from streamlit_js_eval import streamlit_js_eval

st.title("Minimal JS ↔ Streamlit Example")

# This JS expression will run in the browser
js_code = "[1, 2, 3, 4, 5].map(x => x * 10)"

# Evaluate JS and get the result back into Python
result = streamlit_js_eval(js_expressions=js_code, key="js1")

# Display the result
if result:
    st.success(f"Received from JS: {result}")
else:
    st.info("Waiting for JS to run...")
