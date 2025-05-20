# Moutiers-au-Trail timing

In-house race timing for a non-profit yearly race: Moutiers-au-Trail.

![Alt text](media/moutiers-au-trail.png)

## In scope
1. Tracking of bib distribution + noshows
2. Manual arrival tracking, with ability to substitue bibs and remove bib
3. Ranking utility

Based on Streamlit

## How to use

### Prerequisite
The main interface lies with a participant list provided by 1dossard.fr, which tracks basic information like name, sex, subscription status, bib number, and running distance. See `mat-chrono/config.py`

### Install
1. Clone the repo
````
git clone https://github.com/antisrdy/moutiers-au-trail-time.git
cd moutiers-au-trail-time
````
2. Install Poetry (optional)
````
curl -sSL https://install.python-poetry.org | python3 -
````
3. Create a virtual environment (if not created already) and install dependencies
````
export PATH="$HOME/.local/bin:$PATH
poetry install
````
4. Activate the virtual environment
````
poetry shell
````
5. Launch the Streamlit app
````
streamlit run mat-chrono/Bienvenue.py
````