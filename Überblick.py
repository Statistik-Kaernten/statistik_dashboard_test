import streamlit as st

import streamlit.components.v1 as components
from st_bridge import bridge
import os
import time

def p5js_sketch(sketch_file, js_params=None, height=200, width=200):
    sketch = '<script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.5.0/p5.min.js"></script>'
    
    sketch += '<script>'
    if js_params:
        sketch += js_params + "\n"
    sketch += open(sketch_file, 'r', encoding='utf-8').read()
    sketch += '</script>'
    components.html(sketch, height=height, width=width)
    
st.header("This is my P5js sketch")
st.text("Click somewhere")

p5js_sketch(
    sketch_file="sketch.js",
    js_params="""
        // sketch params are embedded at the beginning of the sketch without any change.
        const WIDTH=200;
        const HEIGHT=200;
        const BACKGROUND_COLOR='red';
        CIRCLE_COLOR='yellow';
        CIRCLE_SIZE=30;
    """,
    width=250,  # a little bigger than the sketch canvas
    height=250,
)
time.sleep(3)
data = bridge("my-bridge", default="no value yet!")
st.write(data)