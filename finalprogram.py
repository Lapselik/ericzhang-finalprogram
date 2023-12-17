"""
Name:       Eric Zhang
CS230:      Section 6
Data:       Building_and_Property_Violations
URL:        Link to your web application on Streamlit Cloud (if posted)

Description:
The program includes 3 charts and a map about the buildings and property violations
"""

import streamlit as st
import pydeck as pdk
import pandas as pd
import matplotlib.pyplot as plt


st.set_option('deprecation.showPyplotGlobalUse', False)

df_violation = pd.read_csv('Building_and_Property_Violations.csv')
df_violation.drop(["code", "value", "violation_sthigh", "contact_city", "contact_state", "contact_zip", "sam_id", "ward", "contact_addr1", "contact_addr2"], axis=1, inplace= True)
select_chart = st.sidebar.radio("Please select the type of virtualization", ["Welcome!!", "Pie Chart", "Bar Chart", "Map View"])



def unique_value_list(filelist):
    empty_list = []
    for i in filelist:
        if i not in empty_list:
            empty_list.append(i)

    return empty_list


# city
city_list = unique_value_list(df_violation["violation_city"])


# store amount of violation buildings in each city
city_dict = {key: None for key in city_list}
amount_list = []
for cityname in city_list:
    df_city_amount = df_violation[df_violation["violation_city"] == cityname]
    amount = len(df_city_amount)
    amount_list.append(amount)
for i, key in enumerate(city_dict):
    city_dict[key] = amount_list[i]


# Bar chart
if select_chart == "Bar Chart":
    st.title("Building and Property Violations in Boston")
    st.title("Bar Chart")
    colors = ['blue', 'green', 'red', 'purple', 'orange', 'cyan', 'magenta', 'yellow', 'black', 'brown', 'pink',
              'gray', 'olive', 'teal', 'skyblue', 'lime']

    city_data = {'City Name': city_list, 'Amount': amount_list}
    df_citydata = pd.DataFrame(city_data)  # df for all cities
    df_citydata = df_citydata.set_index(pd.Index(city_list))
    select_city = st.multiselect(f"Please select a city", city_list)
    df_city = df_violation[(df_violation.violation_city.isin(select_city))]

    if len(select_city) > 0:
        df_selected_city = df_citydata.loc[select_city]
        df_selected_city.plot(kind="bar", x="City Name", y="Amount", color=colors)
        plt.title("Bar Chart for city you select")
        plt.xticks(rotation=45, ha='right')
        st.pyplot()
        st.write(f"{len(df_city)} violation buildings and property are found")
    else:
        st.write("Please select at least one city")


elif select_chart == "Pie Chart":
    st.title("Building and Property Violations in Boston")
    st.title("Pie Chart")
    city_data = {'City Name': city_list, 'Amount': amount_list}
    df_citydata = pd.DataFrame(city_data)  # df for all cities
    df_citydata = df_citydata.set_index(pd.Index(city_list))
    df_citydata.plot(kind='pie', y='Amount')
    plt.legend().set_visible(False)
    plt.title('Pie Chart for Violation in each City')
    st.pyplot()


elif select_chart == "Welcome!!":
    st.markdown(
        "<h1 style='text-align: center; color: pink; font-family: Verdana, sans-serif;'>Welcome to my web!!</h1>",
        unsafe_allow_html=True
    )
    st.markdown(
        "<h1 style='text-align: center; color: pink; font-family: Verdana, sans-serif;'>This program is about building and property violations in Boston</h1>",
        unsafe_allow_html=True
    )

elif select_chart == "Map View":
    st.header('Map')
    df_violation.rename(columns={"latitude":"lat", "longitude": "lon"}, inplace=True)

    selected_city = st.multiselect("Select the city", city_list)
    status_list = unique_value_list(df_violation["status"])
    select_status = st.selectbox(f"Please select the status", status_list)
    df_city_scatter = df_violation[(df_violation.violation_city.isin(selected_city))]
    df_city_scatter1 = df_city_status = df_violation[
        (df_violation.violation_city.isin(selected_city)) & (df_violation.status == select_status)]


    view_state = pdk.ViewState(
        latitude=df_violation["lat"].mean(),
        longitude=df_violation["lon"].mean(),
        zoom=12,
        pitch=0
    )

    layer1 = pdk.Layer(type = 'ScatterplotLayer',
                      data=df_city_scatter1,
                      get_position='[lon, lat]',
                      get_radius=30,
                      get_color=[0,200,0],
                      pickable=True
                      )

    layer2 = pdk.Layer('ScatterplotLayer',
                      data=df_city_scatter1,
                      get_position='[lon, lat]',
                      get_radius=20,
                      get_color=[0,0,255],
                      pickable=True
                      )


    tool_tip = {
        "html": "<b>Case Number:</b> <b>{case_no}</b></br><b>{description}</b>",
        "style": {
            "backgroundColor": "steelblue",
            "color": "white"
        }
    }

    map = pdk.Deck(
        map_style='mapbox://styles/mapbox/outdoors-v11',
        initial_view_state=view_state,
        layers=[layer1, layer2],
        tooltip=tool_tip
                )

    st.pydeck_chart(map)

    st.write(df_city_scatter1)







