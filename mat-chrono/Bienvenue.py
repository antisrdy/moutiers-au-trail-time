import streamlit as st
from config import DF_STARTING_TIMES
from utils import get_df

st.set_page_config(
    page_title="Moutiers-au-Trail",
    page_icon="🏃‍♀️🏃",
)

df_participants = get_df("participants")

st.title("Welcome to Moutiers-au-Trail! 👋")

st.write("Programme de la journée :")
st.dataframe(DF_STARTING_TIMES, hide_index=True)

st.write("Liste initiale des participants :")
st.dataframe(df_participants)
