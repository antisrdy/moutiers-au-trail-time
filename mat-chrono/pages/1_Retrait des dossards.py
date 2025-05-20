import os

import streamlit as st
from config import BIBS_COLUMNS, BIBS_PARTICIPANTS_COLUMNS
from utils import apply_filter_on_page, get_df, save_df

st.set_page_config(page_title="Retrait des dossards", page_icon="🏃‍♀️🏃")

st.title("Retrait des dossards 👕")
st.header("Pointage")
st.write("🚨 **Attention à ce que le dossier soit complet.**")
st.write("🚨 Ne pas cliquer sur les noms de colonne pour réordonner.")
st.write("🚨 Penser à sauvegarder souvent.")

df_participants = get_df("participants")
df_participants = apply_filter_on_page(df_participants, page="bibs", key="participants")

if "bibs.csv" in os.listdir("data"):
    df_bibs = get_df("bibs", force_reload=True)
else:
    df_bibs = df_participants[["DOSSARD"]].assign(PRESENT=0)
st.session_state["bibs"] = df_bibs

df_edited = df_participants.merge(df_bibs, how="left", on="DOSSARD", validate="1:1").sort_values(["NOM", "PRENOM"])
df_edited = st.data_editor(
    df_edited,
    disabled=BIBS_PARTICIPANTS_COLUMNS.keys(),
    column_config={"PRESENT": st.column_config.CheckboxColumn()},
    hide_index=True,
)

st.button(
    "Sauvegarder",
    on_click=save_df,
    args=(
        df_edited[BIBS_COLUMNS.keys()],
        "bibs",
    ),
)

st.header("Status")

n_present = df_edited.loc[lambda x: x["PRESENT"] == True].shape[0]
df_no_show = df_edited.loc[lambda x: x["PRESENT"] == False]
pct = int(n_present / df_edited.shape[0] * 100)
st.write(f"Nombre de présents : {n_present} / {df_edited.shape[0]} ({pct}%)")

st.write("Participants absents :")
st.dataframe(df_no_show, hide_index=True)
