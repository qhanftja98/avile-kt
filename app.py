import streamlit as st
import pandas as pd
import pydeck as pdk
import folium
import pickle
from branca.element import Figure
from streamlit_folium import folium_static

with open('route.pkl','rb') as f:
    route = pickle.load(f)

st.title('제주도 이동형 충전 서비스')
input = st.text_input(label="자동차 대수", value="5", max_chars=10, help='input message < 20')

selected_item = st.radio("운행 시간", ("8시 - 13시", "13시 - 18시", "18시 - 23시"))

df_result = pd.read_csv('데이터', index_col = 0)
df_opt_FS = pd.read_csv('df_opt_FS', index_col = 0)
df_opt_SS = pd.read_csv('df_opt_SS', index_col = 0)
df_opt_LS = pd.read_csv('df_opt_LS', index_col = 0)
df_opt_FSS = pd.read_csv('df_opt_FSS', index_col = 0)
df_opt_SSS = pd.read_csv('df_opt_SSS', index_col = 0)
df_opt_LSS = pd.read_csv('df_opt_LSS', index_col = 0)

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
                opacity = 0.2,
                get_position='[lon, lat]',
                get_fill_color='[255, 255, 153]',
                get_radius=10000,
            )
        ],
    ))
    fig=Figure(height=1000,width=1000)
    route_map = folium.Map(location=[(route['start_point'][0][0] + route['end_point'][0][0])/2,
                                    (route['start_point'][0][1] + route['end_point'][0][1])/2],
                        zoom_start=10)
    for t in range(int(input)) :
        if t % 2 == 0 :
            for i in range(5) :
                f1=folium.FeatureGroup("Vehicle 1")
                line=folium.vector_layers.PolyLine(route.iloc[i + 9 * t, :]['route'],popup='<b>Path of Vehicle_1</b>',tooltip=t,color='blue',weight=10).add_to(route_map)
                f1.add_to(route_map)
        else :
            for i in range(5) :
                f1=folium.FeatureGroup("Vehicle 1")
                line=folium.vector_layers.PolyLine(route.iloc[i + 9 * t, :]['route'],popup='<b>Path of Vehicle_1</b>',tooltip=t,color='red',weight=10).add_to(route_map)
                f1.add_to(route_map)
    folium_static(route_map)
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
                opacity = 0.2,
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
                opacity = 0.2,
                get_position='[lon, lat]',
                get_fill_color='[204, 255, 255]',
                get_radius=10000,
            )
        ],
    ))