# %% [markdown]
# Esercizio 1 – L'Italia a Euro 2024 vista dai dati (StatsBomb open data)
# Obiettivo: capire quanto e da dove ha tirato l'Italia, e quanto valevano quei tiri (xG).
# Setup (una volta sola, da terminale):  pip install statsbombpy mplsoccer pandas matplotlib
# In VS Code ogni blocco "# %%" si esegue come una cella (Shift+Enter).

# %% 1. Partite dell'Italia
import warnings
warnings.filterwarnings("ignore")
import pandas as pd
import matplotlib.pyplot as plt
from statsbombpy import sb
from mplsoccer import VerticalPitch

TEAM = "Italy"
matches = sb.matches(competition_id=55, season_id=282)  # Euro 2024
partite = matches[(matches.home_team == TEAM) | (matches.away_team == TEAM)]
partite = partite.sort_values("match_date")
print(partite[["match_id", "match_date", "home_team", "away_team", "home_score", "away_score"]])

# %% 2. Tutti i tiri dell'Italia
tiri = []
for _, p in partite.iterrows():
    ev = sb.events(match_id=p.match_id)
    s = ev[(ev.type == "Shot") & (ev.team == TEAM)].copy()
    s["avversario"] = p.away_team if p.home_team == TEAM else p.home_team
    tiri.append(s)
tiri = pd.concat(tiri)
tiri["x"] = tiri.location.str[0]
tiri["y"] = tiri.location.str[1]
tiri["gol"] = tiri.shot_outcome == "Goal"
print(f"Tiri totali: {len(tiri)}")

# %% 3. Tabella riassuntiva per partita (stile pivot di Power BI)
riepilogo = tiri.groupby("avversario").agg(
    tiri=("id", "count"),
    xG=("shot_statsbomb_xg", "sum"),
    gol=("gol", "sum"),
).round(2)
riepilogo["xG_per_tiro"] = (riepilogo.xG / riepilogo.tiri).round(3)
print(riepilogo)

# %% 4. Shot map: dimensione = xG, colore = gol
pitch = VerticalPitch(pitch_type="statsbomb", half=True, pitch_color="#22312b", line_color="#c7d5cc")
fig, ax = pitch.draw(figsize=(8, 7))
no_gol = tiri[~tiri.gol]
si_gol = tiri[tiri.gol]
pitch.scatter(no_gol.x, no_gol.y, s=no_gol.shot_statsbomb_xg * 900 + 30,
              c="#ffffff", alpha=0.5, edgecolors="black", ax=ax, label="Tiro")
pitch.scatter(si_gol.x, si_gol.y, s=si_gol.shot_statsbomb_xg * 900 + 30,
              c="#2e8bff", edgecolors="white", ax=ax, label="Gol")
ax.set_title(f"Italia – Euro 2024 | {len(tiri)} tiri, xG {tiri.shot_statsbomb_xg.sum():.2f}, "
             f"gol {int(tiri.gol.sum())}", color="white", fontsize=12)
fig.set_facecolor("#22312b")
ax.legend(loc="lower left", facecolor="#22312b", labelcolor="white")
plt.savefig("shotmap_italia_euro2024.png", dpi=150, bbox_inches="tight")
plt.show()

# %% [markdown]
# SFIDE PER TE (qui inizia il vero esercizio)
# 1. Chi ha tirato di più? Raggruppa per "player" e ordina per xG.
# 2. Quanti tiri sono arrivati da fuori area (x < 102)? Che xG medio avevano?
# 3. Ripeti tutto per la Spagna (vincitrice) e confronta xG per tiro: cosa noti?
# 4. Scrivi 3 righe di conclusioni e pubblica grafico + commento su LinkedIn.

# %% Sfida 1 – chi ha tirato di più
tiratori = tiri.groupby("player").agg(
    tiri=("id", "count"),
    xG=("shot_statsbomb_xg", "sum"),
    gol=("gol", "sum"),
).round(2).sort_values("xG", ascending=False)

print(tiratori)

# %%
