import streamlit as st
import pandas as pd
import numpy as np
#from dbConnection import dbConnection



df = pd.DataFrame(
    np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
    columns=["lat", "lon"],
)
st.map(df, size=5, color="#F56D8D")