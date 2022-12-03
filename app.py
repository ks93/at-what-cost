import datetime
import json

from io import StringIO
import streamlit as st
import pandas as pd
import plotly.express as px
import importlib
import requests
if importlib.util.find_spec("pyodide") is not None:
    import pyodide

st.set_page_config(page_title="At what cost?", page_icon="⚡️", layout="centered", initial_sidebar_state="auto", menu_items=None)
st.title("At what cost?")

price_regions = {
    "NO1": "NO1 - Oslo / Øst-Norge", 
    "NO2": "NO2 - Kristiansand / Sør-Norge",
    "NO3": "NO3 - Trondheim / Midt-Norge",
    "NO4": "NO4 - Tromsø / Nord-Norge",
    "NO5": "NO5 - Bergen / Vest-Norge"
}

@st.cache(show_spinner=False)
def read_url_json(url:str, **kwargs):
    """Read the content from a URL"""

    # If pyodide is available
    if importlib.util.find_spec("pyodide") is not None:
        url_contents = pyodide.http.open_url(url)
    else:
        r = requests.get(url)
        url_contents = StringIO(r.text)
    return json.load(url_contents)



def run():
    """Primary entrypoint."""
    date = datetime.datetime.now()
    st.text(date.strftime("%d/%m/%Y"))

    data = read_url_json(f"https://www.hvakosterstrommen.no/api/v1/prices/{date.year:04}/{date.month:02}-{date.day:02}_{region}.json")
    df = pd.DataFrame(data)
    df.drop(["EUR_per_kWh", "EXR", "time_end"], axis=1, inplace=True)
    df["time_start"] = pd.to_datetime(df["time_start"])
    df["time_start"] = pd.to_datetime(df["time_start"])

    fig = px.line(df, x="time_start", y="NOK_per_kWh")
    fig.add_vline(x=date, line_color="red")

    st.plotly_chart(fig)
    

def footer():
    st.markdown('''<p><a href="https://www.hvakosterstrommen.no"><img src="https://ik.imagekit.io/ajdfkwyt/hva-koster-strommen/strompriser-levert-av-hvakosterstrommen_oTtWvqeiB.png" alt="Strømpriser levert av Hva koster strømmen.no" width="200" height="45"></a></p>''',
    unsafe_allow_html=True)


if __name__ == "__main__":

    with st.sidebar:
        region = st.selectbox("Prisområde", options=price_regions.keys(), format_func=lambda k: price_regions[k])
        #date = st.date_input("Dato", current_date, max_value=current_date, min_value=datetime.date(2021,12,1))

    run()

    footer()
