import streamlit as st

pages = {
    "Überblick": [
        st.Page("Überblick.py", title="Überblick"),
    ],
    "Tourismus": [
        st.Page("sites/1_Tourismus_Saisonen.py", title="Tourismus Saisonen"),
        st.Page("sites/2_Tourismus_Regionen.py", title="Tourismus Regionen"),
        st.Page("sites/3_Tourismus_Details.py", title="Tourismus Details"),
        st.Page("sites/4_Tourismus_Betriebe_Betten.py", title="Tourismus Betriebe Betten"),
    ],
    "Bevölkerung": [
        st.Page("sites/5_Bevoelkerung.py", title="Bevölkerung"),
    ],
    #"TestSite": [
    #    st.Page("sites/Test.py", title="TestSite"),
    #],
}

pg = st.navigation(pages, position='sidebar')
pg.run()