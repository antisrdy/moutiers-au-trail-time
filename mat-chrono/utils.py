from config import FILES, COLUMNS, STARTING_TIMES
import pandas as pd
import streamlit as st

def load_df(key: str) -> pd.DataFrame:
    if key == 'participants':
        df = pd.read_excel(FILES[key], dtype=COLUMNS[key])
        df = df.merge(STARTING_TIMES, on='DISTANCE', how='left', validate='m:1')
    else:
        df = pd.read_csv(FILES[key], dtype=COLUMNS[key])
    return df

def load_util_df(key: str, force_load: bool = False) -> pd.DataFrame:
    if force_load or (key not in st.session_state):
        df = load_df(key)
    else:
        df = st.session_state[key]
    return df