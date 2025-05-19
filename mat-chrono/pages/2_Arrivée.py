from config import ARRIVALS_COLUMNS, ARRIVALS_FILE, ARRIVALS_PARTICIPANTS_COLUMNS
from utils import load_util_df

import streamlit as st
from datetime import datetime
import os
import pandas as pd
import re

def is_string_in_range(variable: str) -> bool:
    pattern = re.compile(r'^(?:[1-9][0-9]?|[12][0-9]{2}|30[0-9]|310)$')
    out = bool(pattern.match(variable))
    if not out:
        st.error("Merci d'ajouter un numéro de dossard valide")
    return out

st.set_page_config(
    page_title='Arrivée',
    page_icon='🏃‍♀️🏃',
)

# Initialize an empty DataFrame to store the results
if 'arrivees.csv' in os.listdir('data'):
    st.session_state['arrivals'] = pd.read_csv(ARRIVALS_FILE).astype(ARRIVALS_COLUMNS)
else:
    st.session_state['arrivals'] = pd.DataFrame(columns=ARRIVALS_COLUMNS.keys()).astype(ARRIVALS_COLUMNS)
df_arrivals = st.session_state['arrivals']

df_participants = load_util_df('participants')
df_participants = df_participants[ARRIVALS_PARTICIPANTS_COLUMNS.keys()].astype(ARRIVALS_PARTICIPANTS_COLUMNS)
df_bibs = load_util_df('bibs', force_load=True)

st.title('Finish line 🏁')

st.header('Arrivées')

bib_number = st.text_input('Entrer le numéro de dossard')

if st.button('✅ Valider arrivée'):
    if is_string_in_range(bib_number):
        bib_number = int(bib_number)
        if bib_number in df_arrivals['DOSSARD'].unique():
            st.error(f'Dossard {bib_number} déjà arrivé.')
        else:
            arrival_time = pd.to_datetime(datetime.now())
            start_time = df_participants.loc[lambda x: x['DOSSARD'] == bib_number]['START'].values[0]
            time = arrival_time - start_time
            time = f"{time.components.hours:02}:{time.components.minutes:02}:{time.components.seconds:02}"
            arrival_df = pd.DataFrame([[bib_number, arrival_time.strftime('%H:%M:%S'), time]], columns=ARRIVALS_COLUMNS.keys()).astype(ARRIVALS_COLUMNS)
            # Sorted descending order by design
            df_arrivals = pd.concat([arrival_df, df_arrivals]).reset_index(drop=True)
            df_arrivals.to_csv(ARRIVALS_FILE, index=None)
            st.success(f"Dossard {bib_number} arrivé à {arrival_time.strftime('%H:%M:%S')}. Parcours en {time}.")        

st.text("En cas d'erreur de dossard, merci d'éditer ci-dessous :")

cols = st.columns([2/3, 0.05, 1/3])
with cols[0]:
    st.subheader('Substitution')
    subcols = st.columns([1, 1])
    with subcols[0]:
        bib_change_old = st.text_input('Dossard à modifier')
    with subcols[-1]:
        bib_change_new = st.text_input('Nouveau dossard')
    if st.button('🔄 Valider substitution'):
        if is_string_in_range(bib_change_old) and is_string_in_range(bib_change_new):
            bib_change_old = int(bib_change_old)
            bib_change_new = int(bib_change_new)
            tmp = df_arrivals[df_arrivals['DOSSARD'] == bib_change_old]
            if tmp.shape[0] == 0:
                st.error(f"Le dossard {bib_change_old} n'est pas encore arrivé. Merci d'ajuster.")
            else:
                tmp = df_arrivals[df_arrivals['DOSSARD'] == bib_change_new]
                if tmp.shape[0] > 0:
                    st.error(f"Le dossard {bib_change_new} est déjà arrivé (voir ci-dessous). Merci de corriger.")
                    st.dataframe(
                        tmp
                        .merge(df_participants, how='left', on='DOSSARD', validate='m:1'),
                        hide_index=True
                        )
                else:
                    df_arrivals.loc[df_arrivals['DOSSARD'] == bib_change_old, 'DOSSARD'] = bib_change_new
                    df_arrivals.to_csv(ARRIVALS_FILE, index=None)
                    st.success(f"Dossard {bib_change_old} modifié pour {bib_change_new}")

with cols[1]:
    st.markdown(
        """<div style='height: 100%; border-left: 1px solid white;'></div>""",
        unsafe_allow_html=True
        )

with cols[-1]:
    st.subheader('Suppression')
    bib_to_remove = st.text_input('Dossard à supprimer')
    if st.button('❌ Valider suppression'):
        if is_string_in_range(bib_to_remove):
            bib_to_remove = int(bib_to_remove)
            tmp = df_arrivals[df_arrivals['DOSSARD'] == bib_to_remove]
            if tmp.shape[0] == 0:
                st.error(f"Le dossard {bib_to_remove} n'est pas encore arrivé. Merci d'ajuster.")
            else:
                df_arrivals = df_arrivals[df_arrivals['DOSSARD'] != bib_to_remove]
                df_arrivals.to_csv(ARRIVALS_FILE, index=None)
                st.success(f"Dossard {bib_to_remove} supprimé")

st.header('Arrivées enregistrées')
st.subheader('Tableau des arrivées')
st.dataframe(
    df_arrivals
    .merge(df_participants, how='left', on='DOSSARD', validate='1:1'),
    hide_index=True
    )

st.subheader('Stats arrivées')

df_stats = (
    df_participants
    .merge(df_bibs, on='DOSSARD', how='left', validate='1:1')
    .loc[lambda x: x['PRESENT'] == True]
    .merge(df_arrivals, on='DOSSARD', how='left', validate='1:1')
)

st.text('Personnes arrivées')

st.dataframe(
    df_stats
    .loc[lambda x: x['ARRIVEE'].notnull()]
    .groupby('DISTANCE', as_index=False)
    .agg({'DOSSARD': 'count'})
    .rename(columns={'DOSSARD': '# arrivés'})
    .merge(
        df_stats
        .groupby('DISTANCE', as_index=False)
        .agg({'DOSSARD': 'count'})
        .rename(columns={'DOSSARD': '# attendus'})
    )
)

st.text('Personnes manquantes')

st.dataframe(
    df_stats
    .loc[lambda x: x['ARRIVEE'].isnull()]
    )