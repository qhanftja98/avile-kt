import streamlit as st
import pandas as pd
import pydeck as pdk
import folium
import pickle
import datetime
from branca.element import Figure
from streamlit_folium import folium_static
import requests
import polyline

def get_route(origin_lon, origin_lat, dest_lon, dest_lat):
    """출발지, 도착지 좌표를 입력해서 Route 정보 Return"""
    loc = "{},{};{},{}".format(origin_lon, origin_lat, dest_lon, dest_lat)
    url = "http://router.project-osrm.org/route/v1/car/"
    r = requests.get(url + loc) 
    if r.status_code!= 200:
        return {}
    res = r.json()   
    routes = polyline.decode(res['routes'][0]['geometry'])
    start_point = [res['waypoints'][0]['location'][1], res['waypoints'][0]['location'][0]]
    end_point = [res['waypoints'][1]['location'][1], res['waypoints'][1]['location'][0]]
    distance = res['routes'][0]['distance']
    route = {'route':routes,
           'start_point':start_point,
           'end_point':end_point,
           'distance':distance
          }
    return route


# 피클피클불러오기
with open('route1.pkl','rb') as f:
    route1 = pickle.load(f)
    
with open('route2.pkl','rb') as f:
    route2 = pickle.load(f)

with open('route3.pkl','rb') as f:
    route3 = pickle.load(f)
    
distance = []
    
#사이드바   
st.sidebar.header('충전 서비스 기능')

#사이드바 날짜 선택
time_input = st.sidebar.date_input('날짜 선택', datetime.datetime.now())

#사이드바 시간 선택
name = st.sidebar.selectbox('시간 선택', ['👈모아보기','🕗8시-13시', '🕐13시-18시', '🕕18시-23시'])


# 시간 선택 기능 구현(8시-13시 선택시)
if (name == '🕗8시-13시') and (time_input == datetime.date(2023,1,3)) :
    st.title('충전 서비스 예측 위치 및 경로')
    
    st.header('1. 차량 대수에 따른 클러스터')

    input = st.text_input(label="자동차 대수", value="5")
    
    df_result = pd.read_csv('데이터', index_col = 0)
    
    df_opt_FSS = pd.read_csv('df_opt_FSS', index_col = 0)
    df_opt_FS = df_opt_FSS[0 : int(input)]

    
    center = [126.5, 33.5]
    
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
                data=df_opt_FS,
                opacity = 0.2,
                get_position='[lon, lat]',
                get_fill_color='[255, 255, 153]',
                get_radius=10000,
                pickable=True,
                auto_highlight=True
         
            )
        ],
        
         tooltip={
            "html": "<b>우선순위:</b> {index}"
            "<br/> <b>위도:</b> {lon}"
            "<br/> <b>경도:</b> {lat} "
            "<br/> <b>충전소수:</b> {충전소수}"
            "<br/> <b>관광지수:</b> {관광지수}"
            "<br/> <b>호텔수:</b> {호텔수}"
            "<br/> <b>음석점수:</b> {음식점수}"
            "<br/> <b>주차장수:</b> {주차장수}"
            "<br/> <b>예상충전량:</b> {이용률8시_13시}",
            "style": {"color": "white"},
        },
    ))
    
    # 경로 표시 (8시-13시)
    
    st.header('2. 클러스터에 따른 최적 경로')
    fig=Figure(height=1000,width=1000)
    route_map = folium.Map(location=[33.5,
                                    126.5],
                        zoom_start=10)
    for t in range(int(input)) :
        d = 0
        for i in range(5) :
            f1=folium.FeatureGroup("Vehicle 1")
            line=folium.vector_layers.PolyLine(route1.iloc[i + 9 * t, :]['route'],popup='<b>Path of Vehicle_1</b>',tooltip=t,color='blue',weight=6).add_to(route_map)
            f1.add_to(route_map)
            d = d + route1.iloc[i + 9 * t, :]['distance']
        distance.append(d)
    folium_static(route_map)
    
    
    
    st.header('3. 클러스터별 상세 정보 보기')
    number = []
    for i in range(1,int(input)+1):
        number.append(i)
    choice = st.selectbox('클러스터 지역 선택', number)
    
    fig=Figure(height=1000,width=1000)
    route_map = folium.Map(location=[33.5,
                                126.5],
                    zoom_start=10)
    t = choice
    for i in range(5) :
        f1=folium.FeatureGroup("Vehicle 1")
        line=folium.vector_layers.PolyLine(route1.iloc[i + 9 * t, :]['route'],popup='<b>Path of Vehicle_1</b>',tooltip=t,color='blue',weight=6).add_to(route_map)
        folium.Marker(location=[route1['start_point'][i + 9 * t][0],route1['start_point'][i + 9 * t][1]],popup='Custom Marker 2',tooltip='<strong>Click here to see Popup</strong>',icon=folium.Icon(color='green',prefix='glyphicon',icon='off')).add_to(route_map)
        folium.Marker(location=[route1['start_point'][5 + 9 * t][0],route1['start_point'][5 + 9 * t][1]],popup='Custom Marker 2',tooltip='<strong>Click here to see Popup</strong>',icon=folium.Icon(color='green',prefix='glyphicon',icon='off')).add_to(route_map)
        f1.add_to(route_map)
    folium_static(route_map)
    
    if choice == number[0]:
        col1, col2 = st.columns(2)
        col1.metric('클러스터 1구역의 최적 운영 거리🛣️ ', float("{:.5f}".format(distance[0]/1000)))
        col2.metric('클러스터 1구역의 예상 충전량⚡ ', float("{:.5f}".format(df_opt_FS['이용률8시_13시'][0])))
    elif choice  == number[1]:
        col1, col2 = st.columns(2)
        col1.metric('클러스터 2구역의 최적 운영 거리🛣️ ', float("{:.5f}".format(distance[1]/1000)))
        col2.metric('클러스터 2구역의 예상 충전량⚡ ', float("{:.5f}".format(df_opt_FS['이용률8시_13시'][1])))
    elif choice  == number[2]:
        col1, col2 = st.columns(2)
        col1.metric('클러스터 3구역의 최적 운영 거리🛣️ ', float("{:.5f}".format(distance[2]/1000)))
        col2.metric('클러스터 3구역의 예상 충전량⚡ ', float("{:.5f}".format(df_opt_FS['이용률8시_13시'][2])))
    elif choice  == number[3]:
        col1, col2 = st.columns(2)
        col1.metric('클러스터 4구역의 최적 운영 거리🛣️ ', float("{:.5f}".format(distance[3]/1000)))
        col2.metric('클러스터 4구역의 예상 충전량⚡ ', float("{:.5f}".format(df_opt_FS['이용률8시_13시'][3])))
    elif choice  == number[4]:
        col1, col2 = st.columns(2)
        col1.metric('클러스터 5구역의 최적 운영 거리🛣️ ', float("{:.5f}".format(distance[4]/1000)))
        col2.metric('클러스터 5구역의 예상 충전량⚡ ', float("{:.5f}".format(df_opt_FS['이용률8시_13시'][4])))
    elif choice  == number[5]:
        col1, col2 = st.columns(2)
        col1.metric('클러스터 6구역의 최적 운영 거리🛣️ ', float("{:.5f}".format(distance[5]/1000)))
        col2.metric('클러스터 6구역의 예상 충전량⚡ ', float("{:.5f}".format(df_opt_FS['이용률8시_13시'][5])))
    elif choice  == number[6]:
        col1, col2 = st.columns(2)
        col1.metric('클러스터 7구역의 최적 운영 거리🛣️ ', float("{:.5f}".format(distance[6]/1000)))
        col2.metric('클러스터 7구역의 예상 충전량⚡ ', float("{:.5f}".format(df_opt_FS['이용률8시_13시'][6])))
    elif choice  == number[7]:
        col1, col2 = st.columns(2)
        col1.metric('클러스터 8구역의 최적 운영 거리🛣️ ', float("{:.5f}".format(distance[7]/1000)))
        col2.metric('클러스터 8구역의 예상 충전량⚡ ', float("{:.5f}".format(df_opt_FS['이용률8시_13시'][7])))
    elif choice  == number[8]:
        col1, col2 = st.columns(2)
        col1.metric('클러스터 9구역의 최적 운영 거리🛣️ ', float("{:.5f}".format(distance[8]/1000)))
        col2.metric('클러스터 9구역의 예상 충전량⚡ ', float("{:.5f}".format(df_opt_FS['이용률8시_13시'][8])))
    elif choice  == number[9]:
        col1, col2 = st.columns(2)
        col1.metric('클러스터 10구역의 최적 운영 거리🛣️ ', float("{:.5f}".format(distance[9]/1000)))
        col2.metric('클러스터 10구역의 예상 충전량⚡ ', float("{:.5f}".format(df_opt_FS['이용률8시_13시'][9])))
    elif choice  == number[10]:
        col1, col2 = st.columns(2)
        col1.metric('클러스터 11구역의 최적 운영 거리🛣️ ', float("{:.5f}".format(distance[10]/1000)))
        col2.metric('클러스터 11구역의 예상 충전량⚡ ', float("{:.5f}".format(df_opt_FS['이용률8시_13시'][10])))
    elif choice  == number[11]:
        col1, col2 = st.columns(2)
        col1.metric('클러스터 12구역의 최적 운영 거리🛣️ ', float("{:.5f}".format(distance[11]/1000)))
        col2.metric('클러스터 12구역의 예상 충전량⚡ ', float("{:.5f}".format(df_opt_FS['이용률8시_13시'][11])))
    elif choice  == number[12]:
        col1, col2 = st.columns(2)
        col1.metric('클러스터 13구역의 최적 운영 거리🛣️ ', float("{:.5f}".format(distance[12]/1000)))
        col2.metric('클러스터 13구역의 예상 충전량⚡ ', float("{:.5f}".format(df_opt_FS['이용률8시_13시'][12])))
    elif choice  == number[13]:
        col1, col2 = st.columns(2)
        col1.metric('클러스터 14구역의 최적 운영 거리🛣️ ', float("{:.5f}".format(distance[13]/1000)))
        col2.metric('클러스터 14구역의 예상 충전량⚡ ', float("{:.5f}".format(df_opt_FS['이용률8시_13시'][13])))
    elif choice  == number[14]:
        col1, col2 = st.columns(2)
        col1.metric('클러스터 15구역의 최적 운영 거리🛣️ ', float("{:.5f}".format(distance[14]/1000)))
        col2.metric('클러스터 15구역의 예상 충전량⚡ ', float("{:.5f}".format(df_opt_FS['이용률8시_13시'][14])))
    elif choice  == number[15]:
        col1, col2 = st.columns(2)
        col1.metric('클러스터 16구역의 최적 운영 거리🛣️ ', float("{:.5f}".format(distance[15]/1000)))
        col2.metric('클러스터 16구역의 예상 충전량⚡ ', float("{:.5f}".format(df_opt_FS['이용률8시_13시'][15])))
    elif choice  == number[16]:
        col1, col2 = st.columns(2)
        col1.metric('클러스터 17구역의 최적 운영 거리🛣️ ', float("{:.5f}".format(distance[16]/1000)))
        col2.metric('클러스터 17구역의 예상 충전량⚡ ', float("{:.5f}".format(df_opt_FS['이용률8시_13시'][16])))
    elif choice  == number[17]:
        col1, col2 = st.columns(2)
        col1.metric('클러스터 18구역의 최적 운영 거리🛣️ ', float("{:.5f}".format(distance[17]/1000)))
        col2.metric('클러스터 18구역의 예상 충전량⚡ ', float("{:.5f}".format(df_opt_FS['이용률8시_13시'][17])))
    elif choice  == number[18]:
        col1, col2 = st.columns(2)
        col1.metric('클러스터 19구역의 최적 운영 거리🛣️ ', float("{:.5f}".format(distance[18]/1000)))
        col2.metric('클러스터 19구역의 예상 충전량⚡ ', float("{:.5f}".format(df_opt_FS['이용률8시_13시'][18])))
    elif choice  == number[19]:
        col1, col2 = st.columns(2)
        col1.metric('클러스터 20구역의 최적 운영 거리🛣️ ', float("{:.5f}".format(distance[19]/1000)))
        col2.metric('클러스터 20구역의 예상 충전량⚡ ', float("{:.5f}".format(df_opt_FS['이용률8시_13시'][19])))
    
    st.header('4. 실시간 예약 현황을 통한 최적 경로 수정')
    r1 = []
    r2 = []
    for i in range(0, 5) :
        r = get_route(route1['start_point'][i + 9 * t][1], route1['start_point'][i + 9 * t][0], route1['start_point'][6 + 9 * t][1], route1['start_point'][6 + 9 * t][0])
        r1.append(r['distance'])
        r2.append(r)
    fig=Figure(height=1000,width=1000)
    route_map = folium.Map(location=[33.5,
                                126.5],
                    zoom_start=10)
    t = choice
    f1=folium.FeatureGroup("Vehicle 1")
    line=folium.vector_layers.PolyLine(r2[r1.index(min(r1))]['route'],popup='<b>Path of Vehicle_1</b>',tooltip=t,color='red',weight=6).add_to(route_map)
    folium.Marker(location=[r2[r1.index(min(r1))]['start_point'][0],r2[r1.index(min(r1))]['start_point'][1]],popup='Custom Marker 2',tooltip='<strong>Click here to see Popup</strong>',icon=folium.Icon(color='red',prefix='glyphicon',icon='off')).add_to(route_map)
    folium.Marker(location=[route1['start_point'][6 + 9 * t][0],route1['start_point'][6 + 9 * t][1]],popup='Custom Marker 2',tooltip='<strong>Click here to see Popup</strong>',icon=folium.Icon(color='red',prefix='glyphicon',icon='off')).add_to(route_map)
    f1.add_to(route_map)
    for i in range(4) :
        f1=folium.FeatureGroup("Vehicle 1")
        line=folium.vector_layers.PolyLine(route1.iloc[i + 9 * t, :]['route'],popup='<b>Path of Vehicle_1</b>',tooltip=t,color='blue',weight=6).add_to(route_map)
        folium.Marker(location=[route1['start_point'][i + 9 * t][0],route1['start_point'][i + 9 * t][1]],popup='Custom Marker 2',tooltip='<strong>Click here to see Popup</strong>',icon=folium.Icon(color='green',prefix='glyphicon',icon='off')).add_to(route_map)
        folium.Marker(location=[route1['start_point'][4 + 9 * t][0],route1['start_point'][4 + 9 * t][1]],popup='Custom Marker 2',tooltip='<strong>Click here to see Popup</strong>',icon=folium.Icon(color='green',prefix='glyphicon',icon='off')).add_to(route_map)
        f1.add_to(route_map)
    folium_static(route_map)
    col1, col2 = st.columns(2)
    col1.metric('최적 경로 거점에서 이동 거리(km)🛣️ ', float("{:.5f}".format(min(r1)/1000)))
    col2.metric('최적 경로 거점에서 이동 시간(분)🛣️ ', float("{:.5f}".format(min(r1)/1000/40*60)))
    
    r2 = get_route(126.5014788, 33.50895004, route1['start_point'][6 + 9 * t][1], route1['start_point'][6 + 9 * t][0])
    fig=Figure(height=1000,width=1000)
    route_map = folium.Map(location=[33.5,
                                126.5],
                    zoom_start=10)
    t = choice
    r2 = get_route(126.5014788, 33.50895004, route1['start_point'][6 + 9 * t][1], route1['start_point'][6 + 9 * t][0])
    f1=folium.FeatureGroup("Vehicle 1")
    line=folium.vector_layers.PolyLine(r2['route'],popup='<b>Path of Vehicle_1</b>',tooltip=t,color='red',weight=6).add_to(route_map)
    folium.Marker(location=[r2['start_point'][0],r2['start_point'][1]],popup='Custom Marker 2',tooltip='<strong>Click here to see Popup</strong>',icon=folium.Icon(color='red',prefix='glyphicon',icon='off')).add_to(route_map)
    folium.Marker(location=[route1['start_point'][6 + 9 * t][0],route1['start_point'][6 + 9 * t][1]],popup='Custom Marker 2',tooltip='<strong>Click here to see Popup</strong>',icon=folium.Icon(color='red',prefix='glyphicon',icon='off')).add_to(route_map)
    folium_static(route_map)
    
    col1, col2 = st.columns(2)
    col1.metric('롯데 렌탈에서 이동 거리(km)🛣️ ', float("{:.5f}".format(r2['distance']/1000)))
    col2.metric('롯데 렌탈에서 이동 시간(분)🛣️ ', float("{:.5f}".format(r2['distance']/1000/40*60)))
 

    
# 시간 선택 기능 구현(13시-18시 선택시)
elif name == '🕐13시-18시'and (time_input == datetime.date(2023,1,3)):
    
    st.title('충전 서비스 예측 위치 및 경로')
    
    st.header('1. 차량 대수에 따른 클러스터')
    
    input = st.text_input(label="자동차 대수", value="5", max_chars=10, help='input message < 20')
    
    center = [126.5, 33.5]
       
    df_opt_SSS = pd.read_csv('df_opt_SSS', index_col = 0)
    df_opt_SS = df_opt_SSS[0 : int(input)]

    
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
                data=df_opt_SS,
                opacity = 0.2,
                get_position='[lon, lat]',
                get_fill_color='[153, 255, 204]',
                get_radius=10000,
                pickable=True,
                auto_highlight=True
            )
        ],
         tooltip={
            "html": "<b>우선순위:</b> {index}"
            "<br/> <b>위도:</b> {lon}"
            "<br/> <b>경도:</b> {lat} "
            "<br/> <b>충전소수:</b> {충전소수}"
            "<br/> <b>관광지수:</b> {관광지수}"
            "<br/> <b>호텔수:</b> {호텔수}"
            "<br/> <b>음석점수:</b> {음식점수}"
            "<br/> <b>주차장수:</b> {주차장수}"
            "<br/> <b>예상충전량:</b> {이용률13시_18시}",
            "style": {"color": "white"},
        },
    ))
    
    st.header('2. 클러스터에 따른 최적 경로')
    fig=Figure(height=1000,width=1000)
    route_map = folium.Map(location=[33.5,
                                    126.5],
                        zoom_start=10)
    for t in range(int(input)) :
        d = 0
        for i in range(5) :
            f1=folium.FeatureGroup("Vehicle 1")
            line=folium.vector_layers.PolyLine(route2.iloc[i + 9 * t, :]['route'],popup='<b>Path of Vehicle_1</b>',tooltip=t,color='blue',weight=6).add_to(route_map)
            f1.add_to(route_map)
            d = d + route2.iloc[i + 9 * t, :]['distance']
        distance.append(d)
    folium_static(route_map)
    
    
    # 클러스터별 상세 정보 보기
    
    st.header('3. 클러스터별 상세 정보 보기')
    number = []
    for i in range(1,int(input)+1):
        number.append(i)
    choice = st.selectbox('클러스터 지역 선택', number)
    
    fig=Figure(height=1000,width=1000)
    route_map = folium.Map(location=[33.5,
                                    126.5],
                        zoom_start=10)
    t = choice
    for i in range(5) :
        f1=folium.FeatureGroup("Vehicle 1")
        line=folium.vector_layers.PolyLine(route2.iloc[i + 9 * t, :]['route'],popup='<b>Path of Vehicle_1</b>',tooltip=t,color='blue',weight=6).add_to(route_map)
        folium.Marker(location=[route2['start_point'][i + 9 * t][0],route2['start_point'][i + 9 * t][1]],popup='Custom Marker 2',tooltip='<strong>Click here to see Popup</strong>',icon=folium.Icon(color='green',prefix='glyphicon',icon='off')).add_to(route_map)
        folium.Marker(location=[route2['start_point'][5 + 9 * t][0],route2['start_point'][5 + 9 * t][1]],popup='Custom Marker 2',tooltip='<strong>Click here to see Popup</strong>',icon=folium.Icon(color='green',prefix='glyphicon',icon='off')).add_to(route_map)
        f1.add_to(route_map)
    folium_static(route_map)
        
        
    if choice == number[0]:
        col1, col2 = st.columns(2)
        col1.metric('클러스터 1구역의 최적 운영 거리🛣️ ', float("{:.5f}".format(distance[0]/1000)))
        col2.metric('클러스터 1구역의 예상 충전량⚡ ', float("{:.5f}".format(df_opt_SS['이용률13시_18시'][0])))
    elif choice  == number[1]:
        col1, col2 = st.columns(2)
        col1.metric('클러스터 2구역의 최적 운영 거리🛣️ ', float("{:.5f}".format(distance[1]/1000)))
        col2.metric('클러스터 2구역의 예상 충전량⚡ ', float("{:.5f}".format(df_opt_SS['이용률13시_18시'][1])))
    elif choice  == number[2]:
        col1, col2 = st.columns(2)
        col1.metric('클러스터 3구역의 최적 운영 거리🛣️ ', float("{:.5f}".format(distance[2]/1000)))
        col2.metric('클러스터 3구역의 예상 충전량⚡ ', float("{:.5f}".format(df_opt_SS['이용률13시_18시'][2])))
    elif choice  == number[3]:
        col1, col2 = st.columns(2)
        col1.metric('클러스터 4구역의 최적 운영 거리🛣️ ', float("{:.5f}".format(distance[3]/1000)))
        col2.metric('클러스터 4구역의 예상 충전량⚡ ', float("{:.5f}".format(df_opt_SS['이용률13시_18시'][3])))
    elif choice  == number[4]:
        col1, col2 = st.columns(2)
        col1.metric('클러스터 5구역의 최적 운영 거리🛣️ ', float("{:.5f}".format(distance[4]/1000)))
        col2.metric('클러스터 5구역의 예상 충전량⚡ ', float("{:.5f}".format(df_opt_SS['이용률13시_18시'][4])))
    elif choice  == number[5]:
        col1, col2 = st.columns(2)
        col1.metric('클러스터 6구역의 최적 운영 거리🛣️ ', float("{:.5f}".format(distance[5]/1000)))
        col2.metric('클러스터 6구역의 예상 충전량⚡ ', float("{:.5f}".format(df_opt_SS['이용률13시_18시'][5])))
    elif choice  == number[6]:
        col1, col2 = st.columns(2)
        col1.metric('클러스터 7구역의 최적 운영 거리🛣️ ', float("{:.5f}".format(distance[6]/1000)))
        col2.metric('클러스터 7구역의 예상 충전량⚡ ', float("{:.5f}".format(df_opt_SS['이용률13시_18시'][6])))
    elif choice  == number[7]:
        col1, col2 = st.columns(2)
        col1.metric('클러스터 8구역의 최적 운영 거리🛣️ ', float("{:.5f}".format(distance[7]/1000)))
        col2.metric('클러스터 8구역의 예상 충전량⚡ ', float("{:.5f}".format(df_opt_SS['이용률13시_18시'][7])))
    elif choice  == number[8]:
        col1, col2 = st.columns(2)
        col1.metric('클러스터 9구역의 최적 운영 거리🛣️ ', float("{:.5f}".format(distance[8]/1000)))
        col2.metric('클러스터 9구역의 예상 충전량⚡ ', float("{:.5f}".format(df_opt_SS['이용률13시_18시'][8])))
    elif choice  == number[9]:
        col1, col2 = st.columns(2)
        col1.metric('클러스터 10구역의 최적 운영 거리🛣️ ', float("{:.5f}".format(distance[9]/1000)))
        col2.metric('클러스터 10구역의 예상 충전량⚡ ', float("{:.5f}".format(df_opt_SS['이용률13시_18시'][9])))
    elif choice  == number[10]:
        col1, col2 = st.columns(2)
        col1.metric('클러스터 11구역의 최적 운영 거리🛣️ ', float("{:.5f}".format(distance[10]/1000)))
        col2.metric('클러스터 11구역의 예상 충전량⚡ ', float("{:.5f}".format(df_opt_SS['이용률13시_18시'][10])))
    elif choice  == number[11]:
        col1, col2 = st.columns(2)
        col1.metric('클러스터 12구역의 최적 운영 거리🛣️ ', float("{:.5f}".format(distance[11]/1000)))
        col2.metric('클러스터 12구역의 예상 충전량⚡ ', float("{:.5f}".format(df_opt_SS['이용률13시_18시'][11])))
    elif choice  == number[12]:
        col1, col2 = st.columns(2)
        col1.metric('클러스터 13구역의 최적 운영 거리🛣️ ', float("{:.5f}".format(distance[12]/1000)))
        col2.metric('클러스터 13구역의 예상 충전량⚡ ', float("{:.5f}".format(df_opt_SS['이용률13시_18시'][12])))
    elif choice  == number[13]:
        col1, col2 = st.columns(2)
        col1.metric('클러스터 14구역의 최적 운영 거리🛣️ ', float("{:.5f}".format(distance[13]/1000)))
        col2.metric('클러스터 14구역의 예상 충전량⚡ ', float("{:.5f}".format(df_opt_SS['이용률13시_18시'][13])))
    elif choice  == number[14]:
        col1, col2 = st.columns(2)
        col1.metric('클러스터 15구역의 최적 운영 거리🛣️ ', float("{:.5f}".format(distance[14]/1000)))
        col2.metric('클러스터 15구역의 예상 충전량⚡ ', float("{:.5f}".format(df_opt_SS['이용률13시_18시'][14])))
    elif choice  == number[15]:
        col1, col2 = st.columns(2)
        col1.metric('클러스터 16구역의 최적 운영 거리🛣️ ', float("{:.5f}".format(distance[15]/1000)))
        col2.metric('클러스터 16구역의 예상 충전량⚡ ', float("{:.5f}".format(df_opt_SS['이용률13시_18시'][15])))
    elif choice  == number[16]:
        col1, col2 = st.columns(2)
        col1.metric('클러스터 17구역의 최적 운영 거리🛣️ ', float("{:.5f}".format(distance[16]/1000)))
        col2.metric('클러스터 17구역의 예상 충전량⚡ ', float("{:.5f}".format(df_opt_SS['이용률13시_18시'][16])))
    elif choice  == number[17]:
        col1, col2 = st.columns(2)
        col1.metric('클러스터 18구역의 최적 운영 거리🛣️ ', float("{:.5f}".format(distance[17]/1000)))
        col2.metric('클러스터 18구역의 예상 충전량⚡ ', float("{:.5f}".format(df_opt_SS['이용률13시_18시'][17])))
    elif choice  == number[18]:
        col1, col2 = st.columns(2)
        col1.metric('클러스터 19구역의 최적 운영 거리🛣️ ', float("{:.5f}".format(distance[18]/1000)))
        col2.metric('클러스터 19구역의 예상 충전량⚡ ', float("{:.5f}".format(df_opt_SS['이용률13시_18시'][18])))
    elif choice  == number[19]:
        col1, col2 = st.columns(2)
        col1.metric('클러스터 20구역의 최적 운영 거리🛣️ ', float("{:.5f}".format(distance[19]/1000)))
        col2.metric('클러스터 20구역의 예상 충전량⚡ ', float("{:.5f}".format(df_opt_SS['이용률13시_18시'][19])))
        
        
    st.header('4. 실시간 예약 현황을 통한 최적 경로 수정')
    r1 = []
    r2 = []
    for i in range(0, 5) :
        r = get_route(route2['start_point'][i + 9 * t][1], route2['start_point'][i + 9 * t][0], route2['start_point'][6 + 9 * t][1], route2['start_point'][6 + 9 * t][0])
        r1.append(r['distance'])
        r2.append(r)
    fig=Figure(height=1000,width=1000)
    route_map = folium.Map(location=[33.5,
                                126.5],
                    zoom_start=10)
    t = choice
    f1=folium.FeatureGroup("Vehicle 1")
    line=folium.vector_layers.PolyLine(r2[r1.index(min(r1))]['route'],popup='<b>Path of Vehicle_1</b>',tooltip=t,color='red',weight=6).add_to(route_map)
    folium.Marker(location=[r2[r1.index(min(r1))]['start_point'][0],r2[r1.index(min(r1))]['start_point'][1]],popup='Custom Marker 2',tooltip='<strong>Click here to see Popup</strong>',icon=folium.Icon(color='red',prefix='glyphicon',icon='off')).add_to(route_map)
    folium.Marker(location=[route2['start_point'][6 + 9 * t][0],route2['start_point'][6 + 9 * t][1]],popup='Custom Marker 2',tooltip='<strong>Click here to see Popup</strong>',icon=folium.Icon(color='red',prefix='glyphicon',icon='off')).add_to(route_map)
    f1.add_to(route_map)
    for i in range(4) :
        f1=folium.FeatureGroup("Vehicle 1")
        line=folium.vector_layers.PolyLine(route2.iloc[i + 9 * t, :]['route'],popup='<b>Path of Vehicle_1</b>',tooltip=t,color='blue',weight=6).add_to(route_map)
        folium.Marker(location=[route2['start_point'][i + 9 * t][0],route2['start_point'][i + 9 * t][1]],popup='Custom Marker 2',tooltip='<strong>Click here to see Popup</strong>',icon=folium.Icon(color='green',prefix='glyphicon',icon='off')).add_to(route_map)
        folium.Marker(location=[route2['start_point'][4 + 9 * t][0],route2['start_point'][4 + 9 * t][1]],popup='Custom Marker 2',tooltip='<strong>Click here to see Popup</strong>',icon=folium.Icon(color='green',prefix='glyphicon',icon='off')).add_to(route_map)
        f1.add_to(route_map)
    folium_static(route_map)
    col1, col2 = st.columns(2)
    col1.metric('최적 경로 거점에서 이동 거리(km)🛣️ ', float("{:.5f}".format(min(r1)/1000)))
    col2.metric('최적 경로 거점에서 이동 시간(분)🛣️ ', float("{:.5f}".format(min(r1)/1000/40*60)))
    
    r2 = get_route(126.5014788, 33.50895004, route2['start_point'][6 + 9 * t][1], route2['start_point'][6 + 9 * t][0])
    fig=Figure(height=1000,width=1000)
    route_map = folium.Map(location=[33.5,
                                126.5],
                    zoom_start=10)
    t = choice
    r2 = get_route(126.5014788, 33.50895004, route2['start_point'][6 + 9 * t][1], route2['start_point'][6 + 9 * t][0])
    f1=folium.FeatureGroup("Vehicle 1")
    line=folium.vector_layers.PolyLine(r2['route'],popup='<b>Path of Vehicle_1</b>',tooltip=t,color='red',weight=6).add_to(route_map)
    folium.Marker(location=[r2['start_point'][0],r2['start_point'][1]],popup='Custom Marker 2',tooltip='<strong>Click here to see Popup</strong>',icon=folium.Icon(color='red',prefix='glyphicon',icon='off')).add_to(route_map)
    folium.Marker(location=[route2['start_point'][6 + 9 * t][0],route2['start_point'][6 + 9 * t][1]],popup='Custom Marker 2',tooltip='<strong>Click here to see Popup</strong>',icon=folium.Icon(color='red',prefix='glyphicon',icon='off')).add_to(route_map)
    folium_static(route_map)
    
    col1, col2 = st.columns(2)
    col1.metric('롯데 렌탈에서 이동 거리(km)🛣️ ', float("{:.5f}".format(r2['distance']/1000)))
    col2.metric('롯데 렌탈에서 이동 시간(분)🛣️ ', float("{:.5f}".format(r2['distance']/1000/40*60)))
    
    r1 = []
    r2 = []
    for i in range(0, 5) :
        r = get_route(route2['start_point'][i + 9 * t][1], route2['start_point'][i + 9 * t][0], route2['start_point'][6 + 9 * t][1], route2['start_point'][6 + 9 * t][0])
        r1.append(r['distance'])
        r2.append(r)
    fig=Figure(height=1000,width=1000)
    route_map = folium.Map(location=[33.5,
                                126.5],
                    zoom_start=10)
    t = choice
    f1=folium.FeatureGroup("Vehicle 1")
    line=folium.vector_layers.PolyLine(r2[r1.index(min(r1))]['route'],popup='<b>Path of Vehicle_1</b>',tooltip=t,color='red',weight=6).add_to(route_map)
    folium.Marker(location=[r2[r1.index(min(r1))]['start_point'][0],r2[r1.index(min(r1))]['start_point'][1]],popup='Custom Marker 2',tooltip='<strong>Click here to see Popup</strong>',icon=folium.Icon(color='red',prefix='glyphicon',icon='off')).add_to(route_map)
    folium.Marker(location=[route2['start_point'][6 + 9 * t][0],route2['start_point'][6 + 9 * t][1]],popup='Custom Marker 2',tooltip='<strong>Click here to see Popup</strong>',icon=folium.Icon(color='red',prefix='glyphicon',icon='off')).add_to(route_map)
    f1.add_to(route_map)
    for i in range(4) :
        f1=folium.FeatureGroup("Vehicle 1")
        line=folium.vector_layers.PolyLine(route2.iloc[i + 9 * t, :]['route'],popup='<b>Path of Vehicle_1</b>',tooltip=t,color='blue',weight=6).add_to(route_map)
        folium.Marker(location=[route2['start_point'][i + 9 * t][0],route2['start_point'][i + 9 * t][1]],popup='Custom Marker 2',tooltip='<strong>Click here to see Popup</strong>',icon=folium.Icon(color='green',prefix='glyphicon',icon='off')).add_to(route_map)
        folium.Marker(location=[route2['start_point'][4 + 9 * t][0],route2['start_point'][4 + 9 * t][1]],popup='Custom Marker 2',tooltip='<strong>Click here to see Popup</strong>',icon=folium.Icon(color='green',prefix='glyphicon',icon='off')).add_to(route_map)
        f1.add_to(route_map)
    folium_static(route_map)
    col1, col2 = st.columns(2)
    col1.metric('최적 경로 거점에서 이동 거리(km)🛣️ ', float("{:.5f}".format(min(r1)/1000)))
    col2.metric('최적 경로 거점에서 이동 시간(분)🛣️ ', float("{:.5f}".format(min(r1)/1000/40*60)))
    
    
# 시간 선택 기능 구현(18시-23시 선택시)
 
elif name == '🕕18시-23시'and (time_input == datetime.date(2023,1,3)) :
    
    st.title('충전 서비스 예측 위치 및 경로')
    
    st.header('1. 차량 대수에 따른 클러스터')
    
    input = st.text_input(label="자동차 대수", value="5", max_chars=10, help='input message < 20')
     
    center = [126.5, 33.5]
    
    df_opt_LSS = pd.read_csv('df_opt_LSS', index_col = 0)
    df_opt_LS = df_opt_LSS[0 : int(input)]

    
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
                data=df_opt_LS,
                opacity = 0.2,
                get_position='[lon, lat]',
                get_fill_color='[204, 255, 255]',
                get_radius=10000,
                pickable=True,
                auto_highlight=True
            )
        ],
        tooltip={
            "html": "<b>우선순위:</b> {index}"
            "<br/> <b>위도:</b> {lon}"
            "<br/> <b>경도:</b> {lat} "
            "<br/> <b>충전소수:</b> {충전소수}"
            "<br/> <b>관광지수:</b> {관광지수}"
            "<br/> <b>호텔수:</b> {호텔수}"
            "<br/> <b>음석점수:</b> {음식점수}"
            "<br/> <b>주차장수:</b> {주차장수}"
            "<br/> <b>예상충전량:</b> {이용률18시_23시}",
            "style": {"color": "white"},
        },
    ))
    
    st.header('2. 클러스터에 따른 최적 경로')
    fig=Figure(height=1000,width=1000)
    route_map = folium.Map(location=[33.5,
                                    126.5],
                        zoom_start=10)
    for t in range(int(input)) :
        d = 0
        for i in range(5) :
            f1=folium.FeatureGroup("Vehicle 1")
            line=folium.vector_layers.PolyLine(route3.iloc[i + 9 * t, :]['route'],popup='<b>Path of Vehicle_1</b>',tooltip=t,color='blue',weight=10).add_to(route_map)
            f1.add_to(route_map)
            d = d + route3.iloc[i + 9 * t, :]['distance']
        distance.append(d)
    folium_static(route_map)

    # 클러스터별 상세 정보 보기
    
    st.header('3. 클러스터별 상세 정보 보기')
    number = []
    for i in range(1,int(input)+1):
        number.append(i)
    choice = st.selectbox('클러스터 지역 선택', number)
    
    fig=Figure(height=1000,width=1000)
    route_map = folium.Map(location=[33.5,
                                    126.5],
                        zoom_start=10)
    t = choice
    for i in range(5) :
        f1=folium.FeatureGroup("Vehicle 1")
        line=folium.vector_layers.PolyLine(route3.iloc[i + 9 * t, :]['route'],popup='<b>Path of Vehicle_1</b>',tooltip=t,color='blue',weight=10).add_to(route_map)
        folium.Marker(location=[route3['start_point'][i + 9 * t][0],route3['start_point'][i + 9 * t][1]],popup='Custom Marker 2',tooltip='<strong>Click here to see Popup</strong>',icon=folium.Icon(color='green',prefix='glyphicon',icon='off')).add_to(route_map)
        folium.Marker(location=[route3['start_point'][5 + 9 * t][0],route3['start_point'][5 + 9 * t][1]],popup='Custom Marker 2',tooltip='<strong>Click here to see Popup</strong>',icon=folium.Icon(color='green',prefix='glyphicon',icon='off')).add_to(route_map)
        f1.add_to(route_map)
    folium_static(route_map)
        
    if choice == number[0]:
        col1, col2 = st.columns(2)
        col1.metric('클러스터 1구역의 최적 운영 거리🛣️ ', float("{:.5f}".format(distance[0]/1000)))
        col2.metric('클러스터 1구역의 예상 충전량⚡ ', float("{:.5f}".format(df_opt_LS['이용률18시_23시'][0])))
    elif choice  == number[1]:
        col1, col2 = st.columns(2)
        col1.metric('클러스터 2구역의 최적 운영 거리🛣️ ', float("{:.5f}".format(distance[1]/1000)))
        col2.metric('클러스터 2구역의 예상 충전량⚡ ', float("{:.5f}".format(df_opt_LS['이용률18시_23시'][1])))
    elif choice  == number[2]:
        col1, col2 = st.columns(2)
        col1.metric('클러스터 3구역의 최적 운영 거리🛣️ ', float("{:.5f}".format(distance[2]/1000)))
        col2.metric('클러스터 3구역의 예상 충전량⚡ ', float("{:.5f}".format(df_opt_LS['이용률18시_23시'][2])))
    elif choice  == number[3]:
        col1, col2 = st.columns(2)
        col1.metric('클러스터 4구역의 최적 운영 거리🛣️ ', float("{:.5f}".format(distance[3]/1000)))
        col2.metric('클러스터 4구역의 예상 충전량⚡ ', float("{:.5f}".format(df_opt_LS['이용률18시_23시'][3])))
    elif choice  == number[4]:
        col1, col2 = st.columns(2)
        col1.metric('클러스터 5구역의 최적 운영 거리🛣️ ', float("{:.5f}".format(distance[4]/1000)))
        col2.metric('클러스터 5구역의 예상 충전량⚡ ', float("{:.5f}".format(df_opt_LS['이용률18시_23시'][4])))
    elif choice  == number[5]:
        col1, col2 = st.columns(2)
        col1.metric('클러스터 6구역의 최적 운영 거리🛣️ ', float("{:.5f}".format(distance[5]/1000)))
        col2.metric('클러스터 6구역의 예상 충전량⚡ ', float("{:.5f}".format(df_opt_LS['이용률18시_23시'][5])))
    elif choice  == number[6]:
        col1, col2 = st.columns(2)
        col1.metric('클러스터 7구역의 최적 운영 거리🛣️ ', float("{:.5f}".format(distance[6]/1000)))
        col2.metric('클러스터 7구역의 예상 충전량⚡ ', float("{:.5f}".format(df_opt_LS['이용률18시_23시'][6])))
    elif choice  == number[7]:
        col1, col2 = st.columns(2)
        col1.metric('클러스터 8구역의 최적 운영 거리🛣️ ', float("{:.5f}".format(distance[7]/1000)))
        col2.metric('클러스터 8구역의 예상 충전량⚡ ', float("{:.5f}".format(df_opt_LS['이용률18시_23시'][7])))
    elif choice  == number[8]:
        col1, col2 = st.columns(2)
        col1.metric('클러스터 9구역의 최적 운영 거리🛣️ ', float("{:.5f}".format(distance[8]/1000)))
        col2.metric('클러스터 9구역의 예상 충전량⚡ ', float("{:.5f}".format(df_opt_LS['이용률18시_23시'][8])))
    elif choice  == number[9]:
        col1, col2 = st.columns(2)
        col1.metric('클러스터 10구역의 최적 운영 거리🛣️ ', float("{:.5f}".format(distance[9]/1000)))
        col2.metric('클러스터 10구역의 예상 충전량⚡ ', float("{:.5f}".format(df_opt_LS['이용률18시_23시'][9])))
    elif choice  == number[10]:
        col1, col2 = st.columns(2)
        col1.metric('클러스터 11구역의 최적 운영 거리🛣️ ', float("{:.5f}".format(distance[10]/1000)))
        col2.metric('클러스터 11구역의 예상 충전량⚡ ', float("{:.5f}".format(df_opt_LS['이용률18시_23시'][10])))
    elif choice  == number[11]:
        col1, col2 = st.columns(2)
        col1.metric('클러스터 12구역의 최적 운영 거리🛣️ ', float("{:.5f}".format(distance[11]/1000)))
        col2.metric('클러스터 12구역의 예상 충전량⚡ ', float("{:.5f}".format(df_opt_LS['이용률18시_23시'][11])))
    elif choice  == number[12]:
        col1, col2 = st.columns(2)
        col1.metric('클러스터 13구역의 최적 운영 거리🛣️ ', float("{:.5f}".format(distance[12]/1000)))
        col2.metric('클러스터 13구역의 예상 충전량⚡ ', float("{:.5f}".format(df_opt_LS['이용률18시_23시'][12])))
    elif choice  == number[13]:
        col1, col2 = st.columns(2)
        col1.metric('클러스터 14구역의 최적 운영 거리🛣️ ', float("{:.5f}".format(distance[13]/1000)))
        col2.metric('클러스터 14구역의 예상 충전량⚡ ', float("{:.5f}".format(df_opt_LS['이용률18시_23시'][13])))
    elif choice  == number[14]:
        col1, col2 = st.columns(2)
        col1.metric('클러스터 15구역의 최적 운영 거리🛣️ ', float("{:.5f}".format(distance[14]/1000)))
        col2.metric('클러스터 15구역의 예상 충전량⚡ ', float("{:.5f}".format(df_opt_LS['이용률18시_23시'][14])))
    elif choice  == number[15]:
        col1, col2 = st.columns(2)
        col1.metric('클러스터 16구역의 최적 운영 거리🛣️ ', float("{:.5f}".format(distance[15]/1000)))
        col2.metric('클러스터 16구역의 예상 충전량⚡ ', float("{:.5f}".format(df_opt_LS['이용률18시_23시'][15])))
    elif choice  == number[16]:
        col1, col2 = st.columns(2)
        col1.metric('클러스터 17구역의 최적 운영 거리🛣️ ', float("{:.5f}".format(distance[16]/1000)))
        col2.metric('클러스터 17구역의 예상 충전량⚡ ', float("{:.5f}".format(df_opt_LS['이용률18시_23시'][16])))
    elif choice  == number[17]:
        col1, col2 = st.columns(2)
        col1.metric('클러스터 18구역의 최적 운영 거리🛣️ ', float("{:.5f}".format(distance[17]/1000)))
        col2.metric('클러스터 18구역의 예상 충전량⚡ ', float("{:.5f}".format(df_opt_LS['이용률18시_23시'][17])))
    elif choice  == number[18]:
        col1, col2 = st.columns(2)
        col1.metric('클러스터 19구역의 최적 운영 거리🛣️ ', float("{:.5f}".format(distance[18]/1000)))
        col2.metric('클러스터 19구역의 예상 충전량⚡ ', float("{:.5f}".format(df_opt_LS['이용률18시_23시'][18])))
    elif choice  == number[19]:
        col1, col2 = st.columns(2)
        col1.metric('클러스터 20구역의 최적 운영 거리🛣️ ', float("{:.5f}".format(distance[19]/1000)))
        col2.metric('클러스터 20구역의 예상 충전량⚡ ', float("{:.5f}".format(df_opt_LS['이용률18시_23시'][19])))
        
    
        
    st.header('4. 실시간 예약 현황을 통한 최적 경로 수정')
    r1 = []
    r2 = []
    for i in range(0, 5) :
        r = get_route(route3['start_point'][i + 9 * t][1], route3['start_point'][i + 9 * t][0], route3['start_point'][6 + 9 * t][1], route3['start_point'][6 + 9 * t][0])
        r1.append(r['distance'])
        r2.append(r)
    fig=Figure(height=1000,width=1000)
    route_map = folium.Map(location=[33.5,
                                126.5],
                    zoom_start=10)
    t = choice
    f1=folium.FeatureGroup("Vehicle 1")
    line=folium.vector_layers.PolyLine(r2[r1.index(min(r1))]['route'],popup='<b>Path of Vehicle_1</b>',tooltip=t,color='red',weight=6).add_to(route_map)
    folium.Marker(location=[r2[r1.index(min(r1))]['start_point'][0],r2[r1.index(min(r1))]['start_point'][1]],popup='Custom Marker 2',tooltip='<strong>Click here to see Popup</strong>',icon=folium.Icon(color='red',prefix='glyphicon',icon='off')).add_to(route_map)
    folium.Marker(location=[route3['start_point'][6 + 9 * t][0],route3['start_point'][6 + 9 * t][1]],popup='Custom Marker 2',tooltip='<strong>Click here to see Popup</strong>',icon=folium.Icon(color='red',prefix='glyphicon',icon='off')).add_to(route_map)
    f1.add_to(route_map)
    for i in range(4) :
        f1=folium.FeatureGroup("Vehicle 1")
        line=folium.vector_layers.PolyLine(route3.iloc[i + 9 * t, :]['route'],popup='<b>Path of Vehicle_1</b>',tooltip=t,color='blue',weight=6).add_to(route_map)
        folium.Marker(location=[route3['start_point'][i + 9 * t][0],route3['start_point'][i + 9 * t][1]],popup='Custom Marker 2',tooltip='<strong>Click here to see Popup</strong>',icon=folium.Icon(color='green',prefix='glyphicon',icon='off')).add_to(route_map)
        folium.Marker(location=[route3['start_point'][4 + 9 * t][0],route3['start_point'][4 + 9 * t][1]],popup='Custom Marker 2',tooltip='<strong>Click here to see Popup</strong>',icon=folium.Icon(color='green',prefix='glyphicon',icon='off')).add_to(route_map)
        f1.add_to(route_map)
    folium_static(route_map)
    col1, col2 = st.columns(2)
    col1.metric('최적 경로 거점에서 이동 거리(km)🛣️ ', float("{:.5f}".format(min(r1)/1000)))
    col2.metric('최적 경로 거점에서 이동 시간(분)🛣️ ', float("{:.5f}".format(min(r1)/1000/40*60)))
    
    r2 = get_route(126.5014788, 33.50895004, route3['start_point'][6 + 9 * t][1], route3['start_point'][6 + 9 * t][0])
    fig=Figure(height=1000,width=1000)
    route_map = folium.Map(location=[33.5,
                                126.5],
                    zoom_start=10)
    t = choice
    r2 = get_route(126.5014788, 33.50895004, route3['start_point'][6 + 9 * t][1], route3['start_point'][6 + 9 * t][0])
    f1=folium.FeatureGroup("Vehicle 1")
    line=folium.vector_layers.PolyLine(r2['route'],popup='<b>Path of Vehicle_1</b>',tooltip=t,color='red',weight=6).add_to(route_map)
    folium.Marker(location=[r2['start_point'][0],r2['start_point'][1]],popup='Custom Marker 2',tooltip='<strong>Click here to see Popup</strong>',icon=folium.Icon(color='red',prefix='glyphicon',icon='off')).add_to(route_map)
    folium.Marker(location=[route3['start_point'][6 + 9 * t][0],route3['start_point'][6 + 9 * t][1]],popup='Custom Marker 2',tooltip='<strong>Click here to see Popup</strong>',icon=folium.Icon(color='red',prefix='glyphicon',icon='off')).add_to(route_map)
    folium_static(route_map)
    
    col1, col2 = st.columns(2)
    col1.metric('롯데 렌탈에서 이동 거리(km)🛣️ ', float("{:.5f}".format(r2['distance']/1000)))
    col2.metric('롯데 렌탈에서 이동 시간(분)🛣️ ', float("{:.5f}".format(r2['distance']/1000/40*60)))
    
    
# 시간 선택 기능 구현(모아보기)
elif name == '👈모아보기' :
    col1,col2,col3 = st.columns(3)
    
    # 왼쪽배치
    with col1:
        st.header('8시-13시')
       
        input = st.text_input(label="8시-13시 자동차 대수", value="5", max_chars=10, help='input message < 20')
    
        df_result = pd.read_csv('데이터', index_col = 0)
    
        df_opt_FSS = pd.read_csv('df_opt_FSS', index_col = 0)
        df_opt_FS = df_opt_FSS[0 : int(input)]

        center = [126.5, 33.5]

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
                    data=df_opt_FS,
                    opacity = 0.2,
                    get_position='[lon, lat]',
                    get_fill_color='[255, 255, 153]',
                    get_radius=10000,
                )
            ],
        ))
        
    # 가운데 배치
    with col2:
        st.header('13시-18시')
        input = st.text_input(label="13시-18시 자동차 대수", value="5", max_chars=10, help='input message < 20')
        center = [126.5, 33.5]

            
        df_opt_SSS = pd.read_csv('df_opt_SSS', index_col = 0)
        df_opt_SS = df_opt_SSS[0 : int(input)]

    
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
                    data=df_opt_SS,
                    opacity = 0.2,
                    get_position='[lon, lat]',
                    get_fill_color='[153, 255, 204]',
                    get_radius=10000,
                )
            ],
        ))
        
    # 오른쪽 배치    
    with col3:
        st.header('18시-23시')
        
        input = st.text_input(label="18-23시 자동차 대수", value="5", max_chars=10, help='input message < 20')
     
        center = [126.5, 33.5]

        df_opt_LSS = pd.read_csv('df_opt_LSS', index_col = 0)
        df_opt_LS = df_opt_LSS[0 : int(input)]

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
                    data=df_opt_LS,
                    opacity = 0.2,
                    get_position='[lon, lat]',
                    get_fill_color='[204, 255, 255]',
                    get_radius=10000,
                )
            ],
        ))