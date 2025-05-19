from config import RANKING_PARTICIPANTS_COLUMNS
from utils import load_util_df
import pandas as pd
import streamlit as st
from datetime import datetime

RANKING_COLUMNS = ["DISTANCE", "SEXE"]

st.set_page_config(
    page_title="Arrivée",
    page_icon="🏃‍♀️🏃",
)

df_arrivals = load_util_df('arrivals', force_load=True)
df_participants = load_util_df('participants')
df_participants = df_participants[RANKING_PARTICIPANTS_COLUMNS.keys()]


st.title('Moutiers-au-Trail classement')

df =(
    df_participants
    .merge(df_arrivals, how='right', on='DOSSARD', validate='1:1')
)

df["SCRATCH"] = df.groupby(["DISTANCE"])["ARRIVEE"].rank()
df["CATEGORIE"] = df.groupby(RANKING_COLUMNS)["ARRIVEE"].rank()
df = df.sort_values(["DISTANCE", "SCRATCH"])
df = df.drop(columns=["ARRIVEE", "START"])

st.subheader("Classement SCRATCH")
for (key, _df) in df.groupby("DISTANCE"):
    st.text(key)
    st.dataframe(_df, hide_index=True)

st.subheader("Classement par CATEGORIE")
for (key, _df) in df.groupby(RANKING_COLUMNS):
    st.text(" /// ".join(key))
    st.dataframe(_df, hide_index=True)