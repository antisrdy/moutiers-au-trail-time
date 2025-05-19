from config import BIBS_COLUMNS, BIBS_FILE, BIBS_PARTICIPANTS_COLUMNS
from utils import load_df, load_util_df
import os
import pandas as pd
import streamlit as st

def save_bib_retrieval(df: pd.DataFrame) -> None:
    df.to_csv(BIBS_FILE, index=False)

st.set_page_config(
    page_title='Retrait des dossards',
    page_icon='🏃‍♀️🏃',
)

st.title('Retrait des dossards 👕')
st.header('Pointage')
st.write("Cocher la colonne PRESENT lorsqu'un participant se présente. **Attention à ce que le dossier soit complet.**")
st.write('🚨 Ne pas cliquer sur les noms de colonne pour réordonner.')

df_participants = load_util_df('participants')
df_participants = df_participants[BIBS_PARTICIPANTS_COLUMNS.keys()].astype(BIBS_PARTICIPANTS_COLUMNS)

if 'dossards.csv' in os.listdir('data'):
    st.session_state['bibs'] = pd.read_csv(BIBS_FILE)
else:
    st.session_state['bibs'] = df_participants[['DOSSARD']].assign(PRESENT=0)
df_bibs = st.session_state['bibs']

df_edited = df_participants.merge(df_bibs, how='left', on='DOSSARD', validate='1:1').sort_values(['NOM', 'PRENOM'])
df_edited = st.data_editor(
    df_edited,
    disabled=BIBS_PARTICIPANTS_COLUMNS.keys(),
    column_config={'PRESENT': st.column_config.CheckboxColumn()},
    hide_index=True
    )

st.button('Sauvegarder', on_click=save_bib_retrieval, args=(df_edited[BIBS_COLUMNS.keys()], ))

st.header('Status')
n_present = df_edited.loc[lambda x: x["PRESENT"] == True].shape[0]
df_no_show = df_edited.loc[lambda x: x["PRESENT"] == False]

st.write(f"Nombre de présents : {n_present} / {df_edited.shape[0]} ({int(n_present/df_edited.shape[0]*100)}%)")


st.write("Participants absents :")
st.dataframe(df_no_show, hide_index=True)