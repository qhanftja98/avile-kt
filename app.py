import streamlit as st
import pandas as pd
import geopandas as gpd
import pydeck as pdk

input = st.text_input(label="자동차 대수", value="5", max_chars=10, help='input message < 20')

selected_item = st.radio("운행 시간", ("8시 - 13시", "13시 - 18시", "18시 - 23시"))

df_opt_FS = pd.read_csv('df_opt_FS', index_col = 0)
df_opt_SS = pd.read_csv('df_opt_SS', index_col = 0)
df_opt_LS = pd.read_csv('df_opt_LS', index_col = 0)

df_opt_FSS = df_opt_FS[0 : int(input)]
df_opt_SSS = df_opt_SS[0 : int(input)]
df_opt_LSS = df_opt_LS[0 : int(input)]

center = [126.5, 33.5]
if selected_item == "8시 - 13시":
    st.pydeck_chart(pdk.Deck(
        map_style=None,
        initial_view_state=pdk.ViewState(
            longitude=center[0],
            latitude=center[1],
            zoom=8
        ),
        layers=[
            pdk.Layer(
                'ScatterplotLayer',
                data=df_opt_FSS,
                get_position='[lon, lat]',
                get_fill_color='[255, 255, 153]',
                get_radius=10000,
            )
        ],
    ))
elif selected_item == "13시 - 18시":
    st.pydeck_chart(pdk.Deck(
        map_style=None,
        initial_view_state=pdk.ViewState(
            longitude=center[0],
            latitude=center[1],
            zoom=8
        ),
        layers=[
            pdk.Layer(
                'ScatterplotLayer',
                data=df_opt_SSS,
                get_position='[lon, lat]',
                get_fill_color='[153, 255, 204]',
                get_radius=10000,
            )
        ],
    ))
elif selected_item == "18시 - 23시":
    st.pydeck_chart(pdk.Deck(
        map_style=None,
        initial_view_state=pdk.ViewState(
            longitude=center[0],
            latitude=center[1],
            zoom=8
        ),
        layers=[
            pdk.Layer(
                'ScatterplotLayer',
                data=df_opt_LSS,
                get_position='[lon, lat]',
                get_fill_color='[204, 255, 255]',
                get_radius=10000,
            )
        ],
    ))