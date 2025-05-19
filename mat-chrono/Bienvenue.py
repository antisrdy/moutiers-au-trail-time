from utils import load_df

import streamlit as st

st.set_page_config(
    page_title='Moutiers-au-Trail',
    page_icon='🏃‍♀️🏃',
)

st.write('# Welcome to Moutiers-au-Trail! 👋')

df_participants = load_df('participants')
st.session_state['participants'] = df_participants

st.text("Liste initiale des participants :")
st.dataframe(st.session_state['participants'])