import streamlit as st
# PAGE CONFIG
st.set_page_config(page_title="Bevölkerung", layout="wide")
import altair as alt
from st_bridge import bridge
from data import *
from custom import *
from map import *
#from streamlit_bokeh import streamlit_bokeh
import streamlit.components.v1 as components
import pandas as pd
import time

insert_styling(255, 255, 255, 1, 143, 68, 163, 1, 'white') 
    
# CONSTANTS
START_JAHR: int = 2002
END_JAHR: int = 2051
DATA_JAHR: int = 2024
palette = get_cud_palette()

st.markdown(get_custom_css(), unsafe_allow_html=True)
#st.markdown("""<style>div[data-baseweb="select"] > div {
#    background-color: #8f44a3};</style>
#        """,
#    unsafe_allow_html=True)
### WATERMARK CONFIDENTIAL BEGIN
#st.markdown('<div class="watermark">CONFIDENTIAL</div>', unsafe_allow_html=True)
### WATERMARK CONFIDENTIAL END 

# # # SIDE BAR # # # 
with st.sidebar:

    # # # MAP BEGIN # # # 
    with open("map.html", "r", encoding="utf-8") as f:
        bokeh_map = f.read()

    components.html(f"""
            {bokeh_map}
        """, height=300, scrolling=False)
     # # # MAP END # # #
    altersgruppen = st.selectbox('Altersgruppe:', ['Erwerbsalter', 'Alter in 15 Jahresschritten', 'Alter in 5 Jahresschritten'])
    anteil_anzahl = st.radio("Anteil/Anzahl", ['Anteil', 'Anzahl'], label_visibility='hidden', index=1)

    selected_jahre: int = st.slider("Startjahr",
        min_value=START_JAHR,
        max_value=END_JAHR-1,
        value=(2014, 2024),
        step=1)
   
    select_start_jahr: int = selected_jahre[0]
    select_end_jahr: int = selected_jahre[1]
    ohne_umzuege = st.checkbox('Umzüge', value=True)
    animation = st.checkbox('Animation', value=False)
    
    st.write("<p style='text-align: center;'><em>Quelle: Landesstelle für Statistik.</em></p>", unsafe_allow_html=True)

    st.image("img/logo.png", use_container_width=True)

# # # END SIDE BAR # # #

### WATERMARK PROTOTYPE BEGIN
#st.markdown('<div class="watermark">PROTOTYPE</div>', unsafe_allow_html=True)
### WATERMARK PROTOTYPE END 
if altersgruppen == 'Erwerbsalter':
    altersgruppe = 'erwerbsalter'
elif altersgruppen == 'Alter in 5 Jahresschritten':
    altersgruppe = 'gruppe_5'
elif altersgruppen == 'Alter in 15 Jahresschritten':
    altersgruppe = 'gruppe_15'
########################
st.write('## Bevölkerung')

#st.write(f'### Bevölkerungspyramide - {select_end_jahr}')

data = bridge("my-bridge", default='Keine GKZs ausgewählt')
st.write(os.path.dirname(os.path.abspath(__file__)))
gkz_list = []
if data != 'Keine GKZs ausgewählt':
    gkz_list = [elem for elem in data["selected_gkz"] if elem != '']

col1, col2 = st.columns([1, 1])

with col1:
    if gkz_list is not None and len(gkz_list) > 0:
        st.plotly_chart(pop_chart(filterJahr(load_data('t_bev1.csv'), select_start_jahr, select_end_jahr), gkz_list, animation), use_container_width=True)
    else:
        st.write("Bitte Region auswählen.")

df = get_data('t_bev1.csv', select_start_jahr, select_end_jahr)

df['gkz'] = df['gkz'].astype(str)
df = df[df['gkz'].isin(gkz_list)]
df = df.groupby(['Jahr', f'{altersgruppe}']).agg({'Anzahl': 'sum'}).reset_index()

age_order = get_age_order(altersgruppe)
age_sort_map = {age: i for i, age in enumerate(age_order)} 
df['age_sort'] = df[f'{altersgruppe}'].map(age_sort_map)

if (anteil_anzahl == 'Anteil'):
    df['DISPLAY'] = df['Anzahl'] / df.groupby('Jahr')['Anzahl'].transform('sum') * 100
    df['DISPLAY_FORMATTED'] = df['DISPLAY'].apply(lambda x: handle_comma(str(round(x,1))))
else:
    df['DISPLAY'] = df['Anzahl']
    df['DISPLAY_FORMATTED'] = df['Anzahl'].apply(lambda x: add_thousand_dot(str(x)))

stacked_bar_chart = alt.Chart(df).mark_bar().encode(
        x=alt.X('Jahr:O', title='Jahr', axis=alt.Axis(labelAngle=45)),  
        y=alt.Y('DISPLAY:Q', title=f'{anteil_anzahl}'),
        color=alt.Color(f'{altersgruppe}:N', 
                        title='Altersgruppe', 
                        #sort='Alter', 
                        scale=alt.Scale(domain=age_order, range=palette),
                        legend=None#alt.Legend(orient='bottom',
                        #                direction='vertical',
                        #                columns=3)
                        ),
        order=alt.Order('age_sort', 
                        sort='ascending'),
        opacity=alt.condition(
            alt.datum.Jahr > DATA_JAHR,
            alt.value(0.5),
            alt.value(1.0)
        ),
        tooltip=[alt.Tooltip('Jahr:O', title='Jahr'), 
                alt.Tooltip(f'{altersgruppe}:N', title='Altersgruppe'),
                alt.Tooltip('DISPLAY_FORMATTED:N', title=f'{anteil_anzahl}')],
        ).properties(
                width=800,
                height=600
                ).configure_axis(
                    titleFontWeight='bold'
                ).configure_legend(
                    titleFontWeight='bold'  
                ).properties(
                usermeta={
                    "embedOptions": custom_locale
                }
            )

if not df.empty:
    with col2:
        st.write("### Bevölkerungsstand")
        st.altair_chart(stacked_bar_chart, use_container_width=True)
else:
    st.write("")

#### GEBURTEN ###
df_geb_all = filterJahr(load_data('t_bev2.csv'), select_start_jahr, select_end_jahr)

df_geb_all['GKZ'] = df_geb_all['GKZ'].astype(str)
df_geb_all = df_geb_all[df_geb_all['GKZ'].isin(gkz_list)]

df_geb = df_geb_all[df_geb_all['Jahr'] == select_end_jahr]

df_geb_m = df_geb[df_geb['Geschlecht'] == 1]
df_geb_w = df_geb[df_geb['Geschlecht'] == 2]

df_geb_m_top10 = df_geb_m.groupby(['Vorname']).agg({'Anzahl': 'sum'}).reset_index().sort_values(by='Anzahl', ascending=False).head(10)
df_geb_w_top10 = df_geb_w.groupby(['Vorname']).agg({'Anzahl': 'sum'}).reset_index().sort_values(by='Anzahl', ascending=False).head(10)

col3, col4, col5 = st.columns([1, 1, 2])
with col3:
    st.write(f"#### Männliche Vorname - {select_end_jahr}")
    if df_geb_m_top10 is not None and len(df_geb_m_top10) != 0:
        st.dataframe(df_geb_m_top10, hide_index=True, use_container_width=True)
    else:
        if (select_end_jahr < 2008) or (select_end_jahr > 2023):
            st.write("Vornamen sind ab 2008 und bis zum laufenden Datenjahr erfasst.")
        else:
            st.write("Keine Daten vorhanden.")

with col4:
    st.write(f"#### Weibliche Vorname - {select_end_jahr}")
    if df_geb_w_top10 is not None and len(df_geb_w_top10) != 0:
        st.dataframe(df_geb_w_top10, hide_index=True, use_container_width=True)
    else:
        if (select_end_jahr < 2008) or (select_end_jahr > 2023):
            st.write("Vornamen sind ab 2008 und bis zum laufenden Datenjahr erfasst.")
        else:
            st.write("Keine Daten vorhanden.")

df_geb_all = df_geb_all.drop(columns='Vorname')
df_geb_all = df_geb_all.groupby(['Jahr', 'Geschlecht']).agg({'Anzahl': 'sum'}).reset_index()
df_geb_all['Geschlecht'] = df_geb_all['Geschlecht'].map({
    1: 'männlich',
    2: 'weiblich'
})

if (anteil_anzahl == 'Anteil'):
    df_geb_all['DISPLAY'] = df_geb_all['Anzahl'] / df_geb_all.groupby('Jahr')['Anzahl'].transform('sum') * 100
    df_geb_all['DISPLAY_FORMATTED'] = df_geb_all['DISPLAY'].apply(lambda x: handle_comma(str(round(x,1))))
else:
    df_geb_all['DISPLAY'] = df_geb_all['Anzahl']
    df_geb_all['DISPLAY_FORMATTED'] = df_geb_all['Anzahl'].apply(lambda x: add_thousand_dot(str(x)))

geb_stacked_bar_chart = alt.Chart(df_geb_all).mark_bar().encode(
        x=alt.X('Jahr:O', title='Jahr', axis=alt.Axis(labelAngle=45)),  
        y=alt.Y(f'DISPLAY:Q', title=f'{anteil_anzahl}'),
        color=alt.Color('Geschlecht:N', 
                        title='Geschlecht', 
                        #sort='Alter', 
                        scale=alt.Scale(range=['#B9CFDF', '#EAD6D6']),
                        legend=None#alt.Legend(orient='bottom',
                        #                direction='vertical',
                        #                columns=3)
                        ),
        order=alt.Order('Geschlecht:N', 
                        sort='ascending'),
        tooltip=[alt.Tooltip('Jahr:O', title='Jahr'), 
                alt.Tooltip('Geschlecht:N', title='Geschlecht'),
                alt.Tooltip('DISPLAY_FORMATTED:N', title=f'{anteil_anzahl}')],
        ).properties(
                width=800,
                height=600
                ).configure_axis(
                    titleFontWeight='bold'
                ).configure_legend(
                    titleFontWeight='bold'  
                ).properties(
                usermeta={
                    "embedOptions": custom_locale
                }
            )

with col5:
    st.write("### Geburten Zeitreihe")
    if df_geb_all is not None and len(df_geb_all) != 0:
        st.altair_chart(geb_stacked_bar_chart, use_container_width=True)
    else:
        st.write("Keine Daten vorhanden")

# Todesfälle
df_gestorbene = filterJahr(load_data('t_bev4_gestorbene.csv'), select_start_jahr, select_end_jahr)
df_gestorbene['GKZ'] = df_gestorbene['GKZ'].astype(str)
df_gestorbene = df_gestorbene[df_gestorbene['GKZ'].isin(gkz_list)]
df_gestorbene = df_gestorbene.groupby(['Jahr', 'Geschlecht', f'{altersgruppe}']).agg({'Anzahl': 'sum'}).reset_index()
df_gestorbene['age_sort'] = df_gestorbene[f'{altersgruppe}'].map(age_sort_map)

if (anteil_anzahl == 'Anteil'):
    df_gestorbene['DISPLAY'] = df_gestorbene['Anzahl'] / df_gestorbene.groupby(['Jahr', 'Geschlecht'])['Anzahl'].transform('sum') * 100
    df_gestorbene['DISPLAY_FORMATTED'] = df_gestorbene['DISPLAY'].apply(lambda x: handle_comma(str(round(x,1))))
else:
    df_gestorbene['DISPLAY'] = df_gestorbene['Anzahl']
    df_gestorbene['DISPLAY_FORMATTED'] = df_gestorbene['Anzahl'].apply(lambda x: add_thousand_dot(str(x)))

gest_stacked_bar_chart = alt.Chart(df_gestorbene).mark_bar().encode(
        x=alt.X('Jahr:O', title='Jahr', axis=alt.Axis(labelAngle=45)),  
        y=alt.Y(f'DISPLAY:Q', title=f'{anteil_anzahl}'),
        color=alt.Color( f'{altersgruppe}:N', 
                        title='Altersgruppe', 
                        #sort='Alter', 
                        scale=alt.Scale(range=palette),
                        legend=None#alt.Legend(orient='bottom',
                        #                direction='vertical',
                        #                columns=3)
                        ),
        order=alt.Order('age_sort', 
                        sort='ascending'),
        xOffset='Geschlecht:N',
        tooltip=[alt.Tooltip('Jahr:O', title='Jahr'), 
                alt.Tooltip('Geschlecht:N', title='Geschlecht'),
                alt.Tooltip(f'{altersgruppe}:N', title='Altersgruppe'),
                alt.Tooltip('DISPLAY_FORMATTED:N', title=f'{anteil_anzahl}')],
        ).properties(
                width=800,
                height=600
                ).configure_axis(
                    titleFontWeight='bold'
                ).configure_legend(
                    titleFontWeight='bold'  
                ).properties(
                usermeta={
                    "embedOptions": custom_locale
                }
            )
#col6, col7 = st.columns([1, 1])
#with col7:
st.write("### Gestorbene Zeitreihe")
if df_geb_all is not None and len(df_geb_all) != 0:
    st.altair_chart(gest_stacked_bar_chart, use_container_width=True)
else:
    st.write("Keine Daten vorhanden")

### Wanderungen nach Wanderungstyp ###
st.write("#### Wanderungen nach Wanderungstyp")

df = get_data('t_bev3_wanderungen.csv', select_start_jahr, select_end_jahr)
df = filterJahr(df, select_start_jahr, select_end_jahr)
df['ort_je_h'] = df['ort_je_h'].astype(str)
df['ort_je_z'] = df['ort_je_z'].astype(str)
df = df[df['ort_je_h'].isin(gkz_list) | df['ort_je_z'].isin(gkz_list)]

df_done = df[~df['TYPE'].isna()]
df_bearb = df[df['TYPE'].isna()]

df_bearb['TYPE'] = df_bearb.apply(lambda row: 'Umzug' if row['ort_je_h'] in gkz_list and row['ort_je_z'] in gkz_list else
                                  'Abwanderung nach Kärnten' if row['ort_je_h'] in gkz_list else
                                  'Zuwanderung aus Kärnten'if row['ort_je_z'] in gkz_list else '', axis=1)
df_new = pd.concat([df_done, df_bearb])
df_new['Anzahl'] = 1
df_new = df_new.groupby(['Jahr', 'TYPE']).agg({'Anzahl': 'sum'}).reset_index()
abwList = ['Abwanderung nach Kärnten', 'Abwanderung in anderes Bundesland', 'Abwanderung in das Ausland']
df_new.loc[df_new['TYPE'].isin(abwList), 'Anzahl'] = -df_new['Anzahl']

umzug_rows = df_new[df_new['TYPE'] == 'Umzug'].copy()
umzug_rows['Anzahl'] *= -1
umzug_rows['TYPE'] = 'Umzug'
df_new = pd.concat([df_new, umzug_rows], ignore_index=True)
if ohne_umzuege == False:
    df_new = df_new[df_new['TYPE'] != 'Umzug']

#findmax = df.groupby('JAHR').agg({'ANZAHL': 'sum'}).reset_index()
#max_value = max(abs(findmax['ANZAHL'].min()), abs(findmax['ANZAHL'].max()))

df_saldo = df_new.groupby('Jahr', as_index=False)['Anzahl'].sum()

df_new['ANZAHL_FORMATTED'] = df_new['Anzahl'].apply(lambda x: add_thousand_dot(str(x)))
df_saldo['ANZAHL_FORMATTED'] = df_saldo['Anzahl'].apply(lambda x: add_thousand_dot(str(x)))

only_line_chart = alt.Chart(df_saldo).mark_line(size=5).encode(
    x='Jahr:O',
    y='Anzahl:Q',
    color=alt.value(palette[6]), 
    tooltip=[alt.Tooltip('Jahr:O', title='Jahr'), 
             alt.Tooltip('ANZAHL_FORMATTED:N', title='Saldo')]
)
df_new['sort_order'] = df_new['TYPE'].apply(lambda x: 0 if x=='Umzug' else
                                            #1 if x=='Umzug ' else

                                            2 if x=='Abwanderung nach Kärnten' else
                                            3 if x=='Zuwanderung aus Kärnten' else

                                            4 if x=='Abwanderung in anderes Bundesland' else
                                            5 if x=='Zuwanderung aus anderem Bundesland' else

                                            6 if x=='Abwanderung in das Ausland' else
                                            7 if x=='Zuwanderung aus dem Ausland' else '')

df_new['POS_NEG_HUE'] = df_new['Anzahl'].apply(lambda x: 0 if x <= 0 else 1)

if (anteil_anzahl == 'Anteil'):
    df_new['DISPLAY'] = df_new['Anzahl'] / df_new.groupby(['Jahr', 'POS_NEG_HUE'])['Anzahl'].transform('sum') * 100
    df_new['DISPLAY_FORMATTED'] = df_new['DISPLAY'].apply(lambda x: handle_comma(str(round(x,1))))
    df_new.loc[df_new['Anzahl'].astype(str).str.startswith('-'), 'DISPLAY'] *= -1
else:
    df_new['DISPLAY'] = df_new['Anzahl']
    df_new['DISPLAY_FORMATTED'] = df_new['Anzahl'].apply(lambda x: add_thousand_dot(str(x)))
pd.set_option('display.max_rows', None)

stacked_bar_chart = alt.Chart(df_new).mark_bar().encode(
    x=alt.X('Jahr:O', title='Jahr', axis=alt.Axis(labelAngle=45)),  
    y=alt.Y(f'DISPLAY:Q', title=f'{anteil_anzahl}' 
            ), 
    color=alt.Color('TYPE:N', 
                    title='Wanderungstyp', 
                    #sort=group_order, 
                    legend=alt.Legend(orient='bottom',
                    direction='vertical',
                    columns=4), 
                    scale=alt.Scale(domain=['Zuwanderung aus Kärnten', 'Abwanderung nach Kärnten', 'Zuwanderung aus anderem Bundesland', 'Abwanderung in anderes Bundesland', 'Zuwanderung aus dem Ausland', 'Abwanderung in das Ausland', 'Umzug', 'Saldo'], 
                                    range=[palette[1], palette[1], palette[2], palette[2], palette[3], palette[3], palette[0], palette[6]])
                   ),
    order=alt.Order('sort_order', sort='ascending'),
    tooltip=[alt.Tooltip('Jahr:O', title='Jahr'), 
             alt.Tooltip('TYPE:N', title='Wanderungstyp'),
             alt.Tooltip('DISPLAY_FORMATTED:N', title=f'{anteil_anzahl}')],
    ).properties(
    width=800,
    height=600
)

white_line = alt.Chart(pd.DataFrame({'y': [0]})).mark_rule(color='white').encode(
    y='y'
)

hover_points = alt.Chart(df_saldo).mark_circle(size=2, opacity=0.5).encode(
    x='Jahr:O',
    y='Anzahl:Q',
    tooltip=[alt.Tooltip('Jahr:O', title='Jahr'), alt.Tooltip('ANZAHL_FORMATTED:N', title='Saldo')] 
)

combined_chart = alt.layer(stacked_bar_chart, only_line_chart, white_line, hover_points).configure_axis(
            titleFontWeight='bold'  
        ).configure_legend(
            titleFontWeight='bold'  
        )

if not df_new.empty:
    if anteil_anzahl == 'Anteil':
        st.altair_chart(stacked_bar_chart+white_line, use_container_width=True)
    else:
        st.altair_chart(combined_chart, use_container_width=True)
else:
    st.write("")
