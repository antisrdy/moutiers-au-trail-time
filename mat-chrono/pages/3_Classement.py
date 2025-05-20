import streamlit as st
from config import RANKING_COLUMNS, RANKING_PARTICIPANTS_COLUMNS
from utils import get_df, save_df

st.set_page_config(
    page_title="Arrivée",
    page_icon="🏃‍♀️🏃",
)

df_arrivals = get_df("arrivals", force_reload=True)
df_participants = get_df("participants")
df_participants = df_participants[RANKING_PARTICIPANTS_COLUMNS.keys()]

st.title("Classement 🥇🥈🥉")

df = df_participants.merge(df_arrivals, how="right", on="DOSSARD", validate="1:1")

df["SCRATCH"] = df.groupby(["DISTANCE"])["ARRIVEE"].rank()
df["CATEGORIE"] = df.groupby(list(RANKING_COLUMNS.keys()))["ARRIVEE"].rank()
df = df.sort_values(["DISTANCE", "SCRATCH"])
df = df.drop(columns=["ARRIVEE", "START"])

save_df(df, key="ranking")

st.subheader("Classement SCRATCH")
for key, _df in df.groupby("DISTANCE"):
    st.text(key)
    st.dataframe(_df, hide_index=True)

st.subheader("Classement par CATEGORIE")
for key, _df in df.groupby(list(RANKING_COLUMNS.keys())):
    st.text(" /// ".join(key))
    st.dataframe(_df, hide_index=True)
