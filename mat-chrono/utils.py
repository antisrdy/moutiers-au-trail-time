import pandas as pd
import streamlit as st
from config import COLUMNS, COLUMNS_IN_PAGE, DF_STARTING_TIMES, FILES


def _load_df(key: str) -> pd.DataFrame:
    if key == "participants":
        df = pd.read_excel(FILES[key], dtype=COLUMNS[key])
        df = df.merge(DF_STARTING_TIMES, on="DISTANCE", how="left", validate="m:1")
    else:
        df = pd.read_csv(FILES[key], dtype=COLUMNS[key])
    return df


def get_df(key: str, force_reload: bool = False) -> pd.DataFrame:
    if force_reload or (key not in st.session_state):
        df = _load_df(key)
    else:
        df = st.session_state[key]
    return df


def save_df(df: pd.DataFrame, key: str) -> None:
    df.to_csv(FILES[key], index=False)


def apply_filter_on_page(df: pd.DataFrame, page: str, key: str) -> pd.DataFrame:
    df = df.copy()
    return df[COLUMNS_IN_PAGE[page][key].keys()].astype(COLUMNS_IN_PAGE[page][key])
