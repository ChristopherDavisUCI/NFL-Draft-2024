import streamlit as st
import altair as alt
import pandas as pd
import numpy as np

st.set_page_config(layout="wide", page_title="2024 NFL Draft Positions")

st.title('2024 NFL Draft Positions')

df = pd.read_csv("data/draft2024e.csv")
df["date"] = pd.to_datetime(df["date"])

def get_rank(df_mini, player):
    try:
        return list(df_mini["player"]).index(player)+1
    except:
        return None

def make_chart(pos, df):
    dfpos = df[df["position"] == pos].copy()
    players = dfpos.player.unique()
    df_list = []
    for _, df_mini in dfpos.groupby("url", sort=None):
        row = df_mini.iloc[0]
        sample = {}
        for key in ["source", "date", "author", "url", "position", "draft-id"]:
            sample[key] = row[key]
        df_mini["rank"] = df_mini["player"].map(lambda player: get_rank(df_mini, player))
        mini_players = df_mini["player"].unique()
        for player in players:
            if player not in mini_players:
                new_row = sample.copy()
                new_row["player"] = player
                df_mini = pd.concat([df_mini, pd.DataFrame([new_row])])
        df_list.append(df_mini)
    df_rank = pd.concat(df_list, axis=0)
    return alt.Chart(df_rank).mark_line(point=True).encode(
        x=alt.X("draft-id:N", axis=alt.Axis(labelLimit=200), sort=None),
        y=alt.Y("pick:Q", scale=alt.Scale(reverse=True)),
        color=alt.Color(
            "player:N", 
            sort=None, 
            legend=alt.Legend(orient="left"),
            scale=alt.Scale(scheme="tableau20")
        ),
        tooltip = ["player", "pick", "position", "source", "author", "date"],
        href = "url:N"
    ).properties(
        title=pos,
        height=500
    )

# A few positions are missing
positions = [pos for pos in df["position"].unique() if isinstance(pos, str)]
authors = sorted(df["author"].unique())

pos = st.radio("What position?", positions, index = positions.index("QB"))

chosen_authors = st.multiselect(
    "Choose your authors", 
    options = authors, 
    default = ["Dane Brugler", "Matthew Freedman", "Charlie Campbell", "Danny Kelly", "Benjamin Solak",
               "Rob Staton", "Daniel Jeremiah", "Jeff Risdon", "Walter Cherepinsky", "Trevor Sikkema",
               "Shane Hallam"])

st.altair_chart(make_chart(pos, df[df["author"].isin(chosen_authors)]))

