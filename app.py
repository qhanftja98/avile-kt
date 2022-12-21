import streamlit as st
import pandas as pd
import pydeck as pdk
import folium
import pickle
import datetime
from branca.element import Figure
from streamlit_folium import folium_static


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
if (name == '🕗8시-13시') and (time_input == datetime.date(2022,12,20)) :
    st.title('충전 서비스 예측 위치 및 경로')

    input = st.text_input(label="자동차 대수", value="5", max_chars=10, help='input message < 20')
    
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
    
    fig=Figure(height=1000,width=1000)
    route_map = folium.Map(location=[(route1['start_point'][0][0] + route1['end_point'][0][0])/2,
                                    (route1['start_point'][0][1] + route1['end_point'][0][1])/2],
                        zoom_start=10)
    for t in range(int(input)) :
        d = 0
        if t % 2 == 0 :
            for i in range(5) :
                f1=folium.FeatureGroup("Vehicle 1")
                line=folium.vector_layers.PolyLine(route1.iloc[i + 9 * t, :]['route'],popup='<b>Path of Vehicle_1</b>',tooltip=t,color='blue',weight=10).add_to(route_map)
                f1.add_to(route_map)
                d = d + route1.iloc[i + 9 * t, :]['distance']
            distance.append(d)
        else :
            for i in range(5) :
                f1=folium.FeatureGroup("Vehicle 1")
                line=folium.vector_layers.PolyLine(route1.iloc[i + 9 * t, :]['route'],popup='<b>Path of Vehicle_1</b>',tooltip=t,color='red',weight=10).add_to(route_map)
                f1.add_to(route_map)
                d = d + route1.iloc[i + 9 * t, :]['distance']
            distance.append(d)
    folium_static(route_map)
    
    
    
    if st.checkbox('클러스터별 상세 정보 보기'):
        number = []
        for i in range(1,int(input)+1):
            number.append(i)
        choice = st.selectbox('클러스터 지역 선택', number)
        
        
        if choice == number[0]:
            st.write('클러스터',1, '구역의 최적 운영 거리🛣️ ', float("{:.5f}".format(distance[0]/1000)), 'km')
            st.write('클러스터',1, '구역의 예상 충전량⚡ ', float("{:.5f}".format(df_opt_FS['이용률8시_13시'][0])))
        elif choice  == number[1]:
            st.write('클러스터',2, '구역의 최적 운영 거리🛣️ ', float("{:.5f}".format(distance[1]/1000)), 'km')
            st.write('클러스터',2, '구역의 예상 충전량⚡ ', float("{:.5f}".format(df_opt_FS['이용률8시_13시'][1])))
        elif choice  == number[2]:
            st.write('클러스터',3, '구역의 최적 운영 거리🛣️ ', float("{:.5f}".format(distance[2]/1000)), 'km')
            st.write('클러스터',3, '구역의 예상 충전량⚡ ', float("{:.5f}".format(df_opt_FS['이용률8시_13시'][2])))
        elif choice  == number[3]:
            st.write('클러스터',4, '구역의 최적 운영 거리🛣️ ', float("{:.5f}".format(distance[3]/1000)), 'km')
            st.write('클러스터',4, '구역의 예상 충전량⚡ ', float("{:.5f}".format(df_opt_FS['이용률8시_13시'][3])))   
        elif choice  == number[4]:
            st.write('클러스터',5, '구역의 최적 운영 거리🛣️ ', float("{:.5f}".format(distance[4]/1000)), 'km')
            st.write('클러스터',5, '구역의 예상 충전량⚡ ', float("{:.5f}".format(df_opt_FS['이용률8시_13시'][4])))
        elif choice  == number[5]:
            st.write('클러스터',6, '구역의 최적 운영 거리🛣️ ', float("{:.5f}".format(distance[5]/1000)), 'km')
            st.write('클러스터',6, '구역의 예상 충전량⚡ ', float("{:.5f}".format(df_opt_FS['이용률8시_13시'][5])))   
        elif choice  == number[6]:
            st.write('클러스터',7, '구역의 최적 운영 거리🛣️ ', float("{:.5f}".format(distance[6]/1000)), 'km')
            st.write('클러스터',7, '구역의 예상 충전량⚡ ', float("{:.5f}".format(df_opt_FS['이용률8시_13시'][6])))
        elif choice  == number[7]:
            st.write('클러스터',8, '구역의 최적 운영 거리🛣️ ', float("{:.5f}".format(distance[7]/1000)), 'km')
            st.write('클러스터',8, '구역의 예상 충전량⚡ ', float("{:.5f}".format(df_opt_FS['이용률8시_13시'][7])))  
        elif choice  == number[8]:
            st.write('클러스터',9, '구역의 최적 운영 거리🛣️ ', float("{:.5f}".format(distance[8]/1000)), 'km')
            st.write('클러스터',9, '구역의 예상 충전량⚡ ', float("{:.5f}".format(df_opt_FS['이용률8시_13시'][8]))) 
        elif choice  == number[9]:
            st.write('클러스터',10, '구역의 최적 운영 거리🛣️ ', float("{:.5f}".format(distance[9]/1000)), 'km')
            st.write('클러스터',10, '구역의 예상 충전량⚡ ', float("{:.5f}".format(df_opt_FS['이용률8시_13시'][9])))   
        elif choice  == number[10]:
            st.write('클러스터',11, '구역의 최적 운영 거리🛣️ ', float("{:.5f}".format(distance[10]/1000)), 'km')
            st.write('클러스터',11, '구역의 예상 충전량⚡ ', float("{:.5f}".format(df_opt_FS['이용률8시_13시'][10])))
        elif choice  == number[11]:
            st.write('클러스터',12, '구역의 최적 운영 거리🛣️ ', float("{:.5f}".format(distance[11]/1000)), 'km')
            st.write('클러스터',12, '구역의 예상 충전량⚡ ', float("{:.5f}".format(df_opt_FS['이용률8시_13시'][11])))   
        elif choice  == number[12]:
            st.write('클러스터',13, '구역의 최적 운영 거리🛣️ ', float("{:.5f}".format(distance[12]/1000)), 'km')
            st.write('클러스터',13, '구역의 예상 충전량⚡ ', float("{:.5f}".format(df_opt_FS['이용률8시_13시'][12])))
        elif choice  == number[13]:
            st.write('클러스터',14, '구역의 최적 운영 거리🛣️ ', float("{:.5f}".format(distance[13]/1000)), 'km')
            st.write('클러스터',14, '구역의 예상 충전량⚡ ', float("{:.5f}".format(df_opt_FS['이용률8시_13시'][13])))   
        elif choice  == number[14]:
            st.write('클러스터',15, '구역의 최적 운영 거리🛣️ ', float("{:.5f}".format(distance[14]/1000)), 'km')
            st.write('클러스터',15, '구역의 예상 충전량⚡ ', float("{:.5f}".format(df_opt_FS['이용률8시_13시'][14])))
        elif choice  == number[15]:
            st.write('클러스터',16, '구역의 최적 운영 거리🛣️ ', float("{:.5f}".format(distance[15]/1000)), 'km')
            st.write('클러스터',16, '구역의 예상 충전량⚡ ', float("{:.5f}".format(df_opt_FS['이용률8시_13시'][15])))   
        elif choice  == number[16]:
            st.write('클러스터',17, '구역의 최적 운영 거리🛣️ ', float("{:.5f}".format(distance[16]/1000)), 'km')
            st.write('클러스터',17, '구역의 예상 충전량⚡ ', float("{:.5f}".format(df_opt_FS['이용률8시_13시'][16])))   
        elif choice  == number[17]:
            st.write('클러스터',18, '구역의 최적 운영 거리🛣️ ', float("{:.5f}".format(distance[17]/1000)), 'km')
            st.write('클러스터',18, '구역의 예상 충전량⚡ ', float("{:.5f}".format(df_opt_FS['이용률8시_13시'][17])))   
        elif choice  == number[18]:
            st.write('클러스터',19, '구역의 최적 운영 거리🛣️ ', float("{:.5f}".format(distance[18]/1000)), 'km')
            st.write('클러스터',19, '구역의 예상 충전량⚡ ', float("{:.5f}".format(df_opt_FS['이용률8시_13시'][18])))
        elif choice  == number[19]:
            st.write('클러스터',20, '구역의 최적 운영 거리🛣️ ', float("{:.5f}".format(distance[19]/1000)), 'km')
            st.write('클러스터',20, '구역의 예상 충전량⚡ ', float("{:.5f}".format(df_opt_FS['이용률8시_13시'][19])))
        
        fig=Figure(height=1000,width=1000)
        route_map = folium.Map(location=[(route1['start_point'][0][0] + route1['end_point'][0][0])/2,
                                        (route1['start_point'][0][1] + route1['end_point'][0][1])/2],
                            zoom_start=10)
        t = choice
        for i in range(5) :
            f1=folium.FeatureGroup("Vehicle 1")
            folium.Marker(location=[route1['start_point'][i + 9 * t][0],route1['start_point'][i + 9 * t][1]],popup='Custom Marker 2',tooltip='<strong>Click here to see Popup</strong>',icon=folium.Icon(color='green',prefix='glyphicon',icon='off')).add_to(route_map)
            line=folium.vector_layers.PolyLine(route1.iloc[i + 9 * t, :]['route'],popup='<b>Path of Vehicle_1</b>',tooltip=t,color='blue',weight=10).add_to(route_map)
            f1.add_to(route_map)
            d = d + route1.iloc[i + 9 * t, :]['distance']
        distance.append(d)
        folium_static(route_map)
    
    
    else:
        st.text('클러스터별로 상세 운영 정보 보기가 가능합니다.')
 

    
# 시간 선택 기능 구현(13시-18시 선택시)
elif name == '🕐13시-18시'and (time_input == datetime.date(2022,12,20)):
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
    
    fig=Figure(height=1000,width=1000)
    route_map = folium.Map(location=[(route2['start_point'][0][0] + route2['end_point'][0][0])/2,
                                    (route2['start_point'][0][1] + route2['end_point'][0][1])/2],
                        zoom_start=10)
    for t in range(int(input)) :
        d = 0
        if t % 2 == 0 :
            for i in range(5) :
                f1=folium.FeatureGroup("Vehicle 1")
                line=folium.vector_layers.PolyLine(route2.iloc[i + 9 * t, :]['route'],popup='<b>Path of Vehicle_1</b>',tooltip=t,color='blue',weight=10).add_to(route_map)
                f1.add_to(route_map)
                d = d + route2.iloc[i + 9 * t, :]['distance']
            distance.append(d)
        else :
            for i in range(5) :
                f1=folium.FeatureGroup("Vehicle 1")
                line=folium.vector_layers.PolyLine(route2.iloc[i + 9 * t, :]['route'],popup='<b>Path of Vehicle_1</b>',tooltip=t,color='red',weight=10).add_to(route_map)
                f1.add_to(route_map)
                d = d + route2.iloc[i + 9 * t, :]['distance']
            distance.append(d)
    folium_static(route_map)
    
    
    # 클러스터별 상세 정보 보기
    
    if st.checkbox('클러스터별 상세 정보 보기'):
        number = []
        for i in range(1,int(input)+1):
            number.append(i)
        choice = st.selectbox('클러스터 지역 선택', number)
        
        
        if choice == number[0]:
            st.write('클러스터',1, '구역의 최적 운영 거리', float("{:.5f}".format(distance[0]/1000)), 'km')
            st.write('클러스터',1, '구역의 예상 충전량', float("{:.5f}".format(df_opt_SS['이용률13시_18시'][0])))
        elif choice  == number[1]:
            st.write('클러스터',2, '구역의 최적 운영 거리', float("{:.5f}".format(distance[1]/1000)), 'km')
            st.write('클러스터',2, '구역의 예상 충전량', float("{:.5f}".format(df_opt_SS['이용률13시_18시'][1])))
        elif choice  == number[2]:
            st.write('클러스터',3, '구역의 최적 운영 거리', float("{:.5f}".format(distance[2]/1000)), 'km')
            st.write('클러스터',3, '구역의 예상 충전량', float("{:.5f}".format(df_opt_SS['이용률13시_18시'][2])))
        elif choice  == number[3]:
            st.write('클러스터',4, '구역의 최적 운영 거리', float("{:.5f}".format(distance[3]/1000)), 'km')
            st.write('클러스터',4, '구역의 예상 충전량', float("{:.5f}".format(df_opt_SS['이용률13시_18시'][3])))   
        elif choice  == number[4]:
            st.write('클러스터',5, '구역의 최적 운영 거리', float("{:.5f}".format(distance[4]/1000)), 'km')
            st.write('클러스터',5, '구역의 예상 충전량', float("{:.5f}".format(df_opt_SS['이용률13시_18시'][4])))
        elif choice  == number[5]:
            st.write('클러스터',6, '구역의 최적 운영 거리', float("{:.5f}".format(distance[5]/1000)), 'km')
            st.write('클러스터',6, '구역의 예상 충전량', float("{:.5f}".format(df_opt_SS['이용률13시_18시'][5])))   
        elif choice  == number[6]:
            st.write('클러스터',7, '구역의 최적 운영 거리', float("{:.5f}".format(distance[6]/1000)), 'km')
            st.write('클러스터',7, '구역의 예상 충전량', float("{:.5f}".format(df_opt_SS['이용률13시_18시'][6])))
        elif choice  == number[7]:
            st.write('클러스터',8, '구역의 최적 운영 거리', float("{:.5f}".format(distance[7]/1000)), 'km')
            st.write('클러스터',8, '구역의 예상 충전량', float("{:.5f}".format(df_opt_SS['이용률13시_18시'][7])))  
        elif choice  == number[8]:
            st.write('클러스터',9, '구역의 최적 운영 거리', float("{:.5f}".format(distance[8]/1000)), 'km')
            st.write('클러스터',9, '구역의 예상 충전량', float("{:.5f}".format(df_opt_SS['이용률13시_18시'][8]))) 
        elif choice  == number[9]:
            st.write('클러스터',10, '구역의 최적 운영 거리', float("{:.5f}".format(distance[9]/1000)), 'km')
            st.write('클러스터',10, '구역의 예상 충전량', float("{:.5f}".format(df_opt_SS['이용률13시_18시'][9])))   
        elif choice  == number[10]:
            st.write('클러스터',11, '구역의 최적 운영 거리', float("{:.5f}".format(distance[10]/1000)), 'km')
            st.write('클러스터',11, '구역의 예상 충전량', float("{:.5f}".format(df_opt_SS['이용률13시_18시'][10])))
        elif choice  == number[11]:
            st.write('클러스터',12, '구역의 최적 운영 거리', float("{:.5f}".format(distance[11]/1000)), 'km')
            st.write('클러스터',12, '구역의 예상 충전량', float("{:.5f}".format(df_opt_SS['이용률13시_18시'][11])))   
        elif choice  == number[12]:
            st.write('클러스터',13, '구역의 최적 운영 거리', float("{:.5f}".format(distance[12]/1000)), 'km')
            st.write('클러스터',13, '구역의 예상 충전량', float("{:.5f}".format(df_opt_SS['이용률13시_18시'][12])))
        elif choice  == number[13]:
            st.write('클러스터',14, '구역의 최적 운영 거리', float("{:.5f}".format(distance[13]/1000)), 'km')
            st.write('클러스터',14, '구역의 예상 충전량', float("{:.5f}".format(df_opt_SS['이용률13시_18시'][13])))   
        elif choice  == number[14]:
            st.write('클러스터',15, '구역의 최적 운영 거리', float("{:.5f}".format(distance[14]/1000)), 'km')
            st.write('클러스터',15, '구역의 예상 충전량', float("{:.5f}".format(df_opt_SS['이용률13시_18시'][14])))
        elif choice  == number[15]:
            st.write('클러스터',16, '구역의 최적 운영 거리', float("{:.5f}".format(distance[15]/1000)), 'km')
            st.write('클러스터',16, '구역의 예상 충전량', float("{:.5f}".format(df_opt_SS['이용률13시_18시'][15])))   
        elif choice  == number[16]:
            st.write('클러스터',17, '구역의 최적 운영 거리', float("{:.5f}".format(distance[16]/1000)), 'km')
            st.write('클러스터',17, '구역의 예상 충전량', float("{:.5f}".format(df_opt_SS['이용률13시_18시'][16])))   
        elif choice  == number[17]:
            st.write('클러스터',18, '구역의 최적 운영 거리', float("{:.5f}".format(distance[17]/1000)), 'km')
            st.write('클러스터',18, '구역의 예상 충전량', float("{:.5f}".format(df_opt_SS['이용률13시_18시'][17])))   
        elif choice  == number[18]:
            st.write('클러스터',19, '구역의 최적 운영 거리', float("{:.5f}".format(distance[18]/1000)), 'km')
            st.write('클러스터',19, '구역의 예상 충전량', float("{:.5f}".format(df_opt_SS['이용률13시_18시'][18])))
        elif choice  == number[19]:
            st.write('클러스터',20, '구역의 최적 운영 거리', float("{:.5f}".format(distance[19]/1000)), 'km')
            st.write('클러스터',20, '구역의 예상 충전량', float("{:.5f}".format(df_opt_SS['이용률13시_18시'][19])))
        
        fig=Figure(height=1000,width=1000)
        route_map = folium.Map(location=[(route2['start_point'][0][0] + route2['end_point'][0][0])/2,
                                        (route2['start_point'][0][1] + route2['end_point'][0][1])/2],
                            zoom_start=10)
        t = choice
        for i in range(5) :
            f1=folium.FeatureGroup("Vehicle 1")
            folium.Marker(location=[route2['start_point'][i + 9 * t][0],route2['start_point'][i + 9 * t][1]],popup='Custom Marker 2',tooltip='<strong>Click here to see Popup</strong>',icon=folium.Icon(color='green',prefix='glyphicon',icon='off')).add_to(route_map)
            line=folium.vector_layers.PolyLine(route2.iloc[i + 9 * t, :]['route'],popup='<b>Path of Vehicle_1</b>',tooltip=t,color='blue',weight=10).add_to(route_map)
            f1.add_to(route_map)
            d = d + route2.iloc[i + 9 * t, :]['distance']
        distance.append(d)
        folium_static(route_map)
    
    
# 시간 선택 기능 구현(18시-23시 선택시)
 
elif name == '🕕18시-23시'and (time_input == datetime.date(2022,12,20)) :
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
    
    fig=Figure(height=1000,width=1000)
    route_map = folium.Map(location=[(route3['start_point'][0][0] + route3['end_point'][0][0])/2,
                                    (route3['start_point'][0][1] + route3['end_point'][0][1])/2],
                        zoom_start=10)
    for t in range(int(input)) :
        d = 0
        if t % 2 == 0 :
            for i in range(5) :
                f1=folium.FeatureGroup("Vehicle 1")
                line=folium.vector_layers.PolyLine(route3.iloc[i + 9 * t, :]['route'],popup='<b>Path of Vehicle_1</b>',tooltip=t,color='blue',weight=10).add_to(route_map)
                f1.add_to(route_map)
                d = d + route3.iloc[i + 9 * t, :]['distance']
            distance.append(d)
        else :
            for i in range(5) :
                f1=folium.FeatureGroup("Vehicle 1")
                line=folium.vector_layers.PolyLine(route3.iloc[i + 9 * t, :]['route'],popup='<b>Path of Vehicle_1</b>',tooltip=t,color='red',weight=10).add_to(route_map)
                f1.add_to(route_map)
                d = d + route3.iloc[i + 9 * t, :]['distance']
            distance.append(d)
    folium_static(route_map)

    # 클러스터별 상세 정보 보기
    
    if st.checkbox('클러스터별 상세 정보 보기'):
        number = []
        for i in range(1,int(input)+1):
            number.append(i)
        choice = st.selectbox('클러스터 지역 선택', number)
        
       
        
        if choice == number[0]:
            st.write('클러스터',1, '구역의 최적 운영 거리', float("{:.5f}".format(distance[0]/1000)), 'km')
            st.write('클러스터',1, '구역의 예상 충전량', float("{:.5f}".format(df_opt_LS['이용률18시_23시'][0])))
        elif choice  == number[1]:
            st.write('클러스터',2, '구역의 최적 운영 거리', float("{:.5f}".format(distance[1]/1000)), 'km')
            st.write('클러스터',2, '구역의 예상 충전량', float("{:.5f}".format(df_opt_LS['이용률18시_23시'][1])))
        elif choice  == number[2]:
            st.write('클러스터',3, '구역의 최적 운영 거리', float("{:.5f}".format(distance[2]/1000)), 'km')
            st.write('클러스터',3, '구역의 예상 충전량', float("{:.5f}".format(df_opt_LS['이용률18시_23시'][2])))
        elif choice  == number[3]:
            st.write('클러스터',4, '구역의 최적 운영 거리', float("{:.5f}".format(distance[3]/1000)), 'km')
            st.write('클러스터',4, '구역의 예상 충전량', float("{:.5f}".format(df_opt_LS['이용률18시_23시'][3])))   
        elif choice  == number[4]:
            st.write('클러스터',5, '구역의 최적 운영 거리', float("{:.5f}".format(distance[4]/1000)), 'km')
            st.write('클러스터',5, '구역의 예상 충전량', float("{:.5f}".format(df_opt_LS['이용률18시_23시'][4])))
        elif choice  == number[5]:
            st.write('클러스터',6, '구역의 최적 운영 거리', float("{:.5f}".format(distance[5]/1000)), 'km')
            st.write('클러스터',6, '구역의 예상 충전량', float("{:.5f}".format(df_opt_LS['이용률18시_23시'][5])))   
        elif choice  == number[6]:
            st.write('클러스터',7, '구역의 최적 운영 거리', float("{:.5f}".format(distance[6]/1000)), 'km')
            st.write('클러스터',7, '구역의 예상 충전량', float("{:.5f}".format(df_opt_LS['이용률18시_23시'][6])))
        elif choice  == number[7]:
            st.write('클러스터',8, '구역의 최적 운영 거리', float("{:.5f}".format(distance[7]/1000)), 'km')
            st.write('클러스터',8, '구역의 예상 충전량', float("{:.5f}".format(df_opt_LS['이용률18시_23시'][7])))  
        elif choice  == number[8]:
            st.write('클러스터',9, '구역의 최적 운영 거리', float("{:.5f}".format(distance[8]/1000)), 'km')
            st.write('클러스터',9, '구역의 예상 충전량', float("{:.5f}".format(df_opt_LS['이용률18시_23시'][8]))) 
        elif choice  == number[9]:
            st.write('클러스터',10, '구역의 최적 운영 거리', float("{:.5f}".format(distance[9]/1000)), 'km')
            st.write('클러스터',10, '구역의 예상 충전량', float("{:.5f}".format(df_opt_LS['이용률18시_23시'][9])))   
        elif choice  == number[10]:
            st.write('클러스터',11, '구역의 최적 운영 거리', float("{:.5f}".format(distance[10]/1000)), 'km')
            st.write('클러스터',11, '구역의 예상 충전량', float("{:.5f}".format(df_opt_LS['이용률18시_23시'][10])))
        elif choice  == number[11]:
            st.write('클러스터',12, '구역의 최적 운영 거리', float("{:.5f}".format(distance[11]/1000)), 'km')
            st.write('클러스터',12, '구역의 예상 충전량', float("{:.5f}".format(df_opt_LS['이용률18시_23시'][11])))   
        elif choice  == number[12]:
            st.write('클러스터',13, '구역의 최적 운영 거리', float("{:.5f}".format(distance[12]/1000)), 'km')
            st.write('클러스터',13, '구역의 예상 충전량', float("{:.5f}".format(df_opt_LS['이용률18시_23시'][12])))
        elif choice  == number[13]:
            st.write('클러스터',14, '구역의 최적 운영 거리', float("{:.5f}".format(distance[13]/1000)), 'km')
            st.write('클러스터',14, '구역의 예상 충전량', float("{:.5f}".format(df_opt_LS['이용률18시_23시'][13])))   
        elif choice  == number[14]:
            st.write('클러스터',15, '구역의 최적 운영 거리', float("{:.5f}".format(distance[14]/1000)), 'km')
            st.write('클러스터',15, '구역의 예상 충전량', float("{:.5f}".format(df_opt_LS['이용률18시_23시'][14])))
        elif choice  == number[15]:
            st.write('클러스터',16, '구역의 최적 운영 거리', float("{:.5f}".format(distance[15]/1000)), 'km')
            st.write('클러스터',16, '구역의 예상 충전량', float("{:.5f}".format(df_opt_LS['이용률18시_23시'][15])))   
        elif choice  == number[16]:
            st.write('클러스터',17, '구역의 최적 운영 거리', float("{:.5f}".format(distance[16]/1000)), 'km')
            st.write('클러스터',17, '구역의 예상 충전량', float("{:.5f}".format(df_opt_LS['이용률18시_23시'][16])))   
        elif choice  == number[17]:
            st.write('클러스터',18, '구역의 최적 운영 거리', float("{:.5f}".format(distance[17]/1000)), 'km')
            st.write('클러스터',18, '구역의 예상 충전량', float("{:.5f}".format(df_opt_LS['이용률18시_23시'][17])))   
        elif choice  == number[18]:
            st.write('클러스터',19, '구역의 최적 운영 거리', float("{:.5f}".format(distance[18]/1000)), 'km')
            st.write('클러스터',19, '구역의 예상 충전량', float("{:.5f}".format(df_opt_LS['이용률18시_23시'][18])))
        elif choice  == number[19]:
            st.write('클러스터',20, '구역의 최적 운영 거리', float("{:.5f}".format(distance[19]/1000)), 'km')
            st.write('클러스터',20, '구역의 예상 충전량', float("{:.5f}".format(df_opt_LS['이용률18시_23시'][19])))
        
        fig=Figure(height=1000,width=1000)
        route_map = folium.Map(location=[(route3['start_point'][0][0] + route3['end_point'][0][0])/2,
                                        (route3['start_point'][0][1] + route3['end_point'][0][1])/2],
                            zoom_start=10)
        t = choice
        for i in range(5) :
            f1=folium.FeatureGroup("Vehicle 1")
            folium.Marker(location=[route3['start_point'][i + 9 * t][0],route3['start_point'][i + 9 * t][1]],popup='Custom Marker 2',tooltip='<strong>Click here to see Popup</strong>',icon=folium.Icon(color='green',prefix='glyphicon',icon='off')).add_to(route_map)
            line=folium.vector_layers.PolyLine(route3.iloc[i + 9 * t, :]['route'],popup='<b>Path of Vehicle_1</b>',tooltip=t,color='blue',weight=10).add_to(route_map)
            f1.add_to(route_map)
            d = d + route3.iloc[i + 9 * t, :]['distance']
        distance.append(d)
        folium_static(route_map)
    
    
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