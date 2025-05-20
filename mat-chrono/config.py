import os

import pandas as pd
from dotenv import load_dotenv

load_dotenv()

DF_STARTING_TIMES = pd.DataFrame(
    [
        ["Trail 20k / 500m D+", "2025-04-14 17:30"],
        ["Trail 12k / 290m D+", "2025-04-14 17:40"],
        ["Marche 8k / 170m D+", "2025-04-14 17:45"],
        ["Kids 1k", "2025-04-14 17:10"],
    ],
    columns=["DISTANCE", "START"],
)
DF_STARTING_TIMES["START"] = pd.to_datetime(DF_STARTING_TIMES["START"])

# Participants
PARTICIPANTS_COLUMNS = {
    "DISTANCE": "object",
    "NOM": "object",
    "PRENOM": "object",
    "SEXE": "object",
    "DOSSARD": "int",
    "DATE INSCR": "object",
    "NUMERO INSCR": "object",
    "E-MAIL": "object",
    "NE.E LE": "object",
    "DOSSIER": "object",
    "JUSTIFICATIF": "object",
    "TYPE_JUSTIF": "object",
    "DECHARGE": "object",
    "LICENCE": "object",
    "CLUB": "object",
    "GROUPE": "object",
    "TELEPHONE": "object",
    "CP": "object",
    "VILLE": "object",
    "PAYS": "object",
    "SECOURS_NOM": "object",
    "SECOURS_NUM": "object",
}
PARTICIPANTS_FILE = os.getenv("PARTICIPANTS_FILE")

# Bibs
BIBS_COLUMNS = {"DOSSARD": "int", "PRESENT": "int"}
BIBS_FILE = os.getenv("BIBS_FILE")
BIBS_PARTICIPANTS_COLUMNS = {
    "DISTANCE": "object",
    "NOM": "object",
    "PRENOM": "object",
    "DOSSARD": "int",
    "DOSSIER": "object",
}

# Arrivals
ARRIVALS_COLUMNS = {"DOSSARD": "int64", "ARRIVEE": "object", "TEMPS": "object"}
ARRIVALS_FILE = os.getenv("ARRIVALS_FILE")
ARRIVALS_PARTICIPANTS_COLUMNS = {
    "DISTANCE": "object",
    "NOM": "object",
    "PRENOM": "object",
    "DOSSARD": "int",
    "START": "datetime64[ns]",
}

# Ranking
RANKING_COLUMNS = {"DISTANCE": "object", "SEXE": "object"}
RANKING_PARTICIPANTS_COLUMNS = {
    "DISTANCE": "object",
    "NOM": "object",
    "PRENOM": "object",
    "SEXE": "object",
    "DOSSARD": "int",
    "START": "datetime64[ns]",
}
RANKING_FILE = os.getenv("RANKING_FILE")

FILES = {"participants": PARTICIPANTS_FILE, "bibs": BIBS_FILE, "arrivals": ARRIVALS_FILE, "ranking": RANKING_FILE}
COLUMNS = {
    "participants": PARTICIPANTS_COLUMNS,
    "bibs": BIBS_COLUMNS,
    "arrivals": ARRIVALS_COLUMNS,
    "ranking": RANKING_COLUMNS,
}
COLUMNS_IN_PAGE = {
    "arrivals": {"participants": ARRIVALS_PARTICIPANTS_COLUMNS},
    "bibs": {"participants": BIBS_PARTICIPANTS_COLUMNS},
    "ranking": {"participants": RANKING_PARTICIPANTS_COLUMNS},
}
