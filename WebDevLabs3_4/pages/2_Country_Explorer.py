# Lab 3: API data page
# TODO: Rename this file to fit your page. Keep the number at the front, since it sets the
#       page's order in the sidebar (for example, 2_Pokedex.py).
#
# This page shows data from your API, processed with your own Python code. No AI on this page.
# It should have:
#   - at least 2 meaningful user inputs (for example st.selectbox, st.text_input, st.slider)
#   - at least 2 dynamic visuals that change based on the user's input: charts, displays of
#     images, or other visualizations (see the example website for examples!)

import requests
import streamlit as st
import pandas as pd
st.title("🌎🌎Country Explorer🌎🌎 ")
st.write(
    "Welcome to Country Explorer! Select two countries "
    "to compare their population, land area, languages, "
    "currencies, and other information."
)
url = "https://countries.dev/countries?fields=name,alpha2Code&sort=name"
try:
    response = requests.get(url, timeout=10)
except requests.exceptions.RequestException:
    st.error("Unable to connect to the country database. Please try again.")
    st.stop()
if response.status_code == 200:
    countryList = response.json()
    countryNames = []
    countryCodes = {}
    for country in countryList:
        countryNames.append(country["name"])
        countryCodes[country["name"]] = country["alpha2Code"]
    countryOne = st.selectbox("Select your home country:", countryNames)
    countryTwo = st.selectbox("select a country to compare:", countryNames, index=1)
    codeOne = countryCodes[countryOne]
    codeTwo = countryCodes[countryTwo]
    urlOne = f"https://countries.dev/alpha/{codeOne}"
    urlTwo = f"https://countries.dev/alpha/{codeTwo}"
    try:
        responseOne = requests.get(urlOne, timeout=10)
        responseTwo = requests.get(urlTwo, timeout=10)
    except requests.exceptions.RequestException:
        st.error("Unable to connect to the country database. Please try again.")
        st.stop()
    if responseOne.status_code == 200 and responseTwo.status_code == 200:
        dataOne = responseOne.json()
        dataTwo = responseTwo.json()
        col1, col2 = st.columns(2)
        with col1:
            st.subheader(dataOne["name"])
            st.image(dataOne["flags"]["png"], width = 150)
            st.write("Capital:", dataOne["capital"])
            st.write("Region:", dataOne["region"])
            st.write("Population:", f'{dataOne["population"]:,}')
            st.write("Land Area:", f'{dataOne["area"]:,} km²' if dataOne["area"] is not None else "N/A")
            st.write("Subregion:", dataOne.get("subregion") or "N/A")
            st.write("Languages:", ", ".join(
                language["name"] for language in dataOne.get("languages", [])
            ) or "N/A")
            st.write("Currencies:", ", ".join(
                currency["name"] for currency in dataOne.get("currencies", [])
            ) or "N/A")
            st.write("UTC Offsets:", ", ".join(dataOne.get("timezones", [])) or "N/A")
        with col2:
            st.subheader(dataTwo["name"])
            st.image(dataTwo["flags"]["png"], width = 150)
            st.write("Capital:", dataTwo["capital"])
            st.write("Region:", dataTwo["region"])
            st.write("Population:", f'{dataTwo["population"]:,}')
            st.write("Land Area:", f'{dataTwo["area"]:,} km²' if dataTwo["area"] is not None else "N/A")
            st.write("Subregion:", dataTwo.get("subregion") or "N/A")
            st.write("Languages:", ", ".join(
                language["name"] for language in dataTwo.get("languages", [])
            ) or "N/A")
            st.write("Currencies:", ", ".join(
                currency["name"] for currency in dataTwo.get("currencies", [])
            ) or "N/A")
            st.write("UTC Offsets:", ", ".join(dataTwo.get("timezones", [])) or "N/A")
        chartData = pd.DataFrame({
            "Country": [dataOne["name"], dataTwo["name"]],
            "Population": [dataOne["population"], dataTwo["population"]],
            "Land Area (km²)": [dataOne["area"], dataTwo["area"]]
        })
        st.subheader("Population Comparison")
        st.bar_chart(chartData, x="Country", y="Population")
        st.subheader("Land Area Comparison")
        st.bar_chart(chartData, x="Country", y="Land Area (km²)")
    else:
        st.error("Unable to retrieve information for the selected countries.")
else:
    st.error("Unable to retrieve the country list.")
