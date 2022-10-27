#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  3 11:27:18 2022

@author: tedwards
"""

#imports
import matplotlib.pyplot as plt
import numpy as np
from mplsoccer import Pitch, Sbopen
import pandas as pd 

parser = Sbopen()

df_competition = parser.competition()
df_competition.info()


df_match = parser.match(43, 3)
df_match.info()

#England Team ID = 68
#df_match_england = df_match.loc[(df_match['home_team_id'] == 768 |
 #                               df_match['away_team_id'] == 768)]
#Above line is not working. Throwing raise ValueError(

df_lineup = parser.lineup(7570)
df_lineup.info()

df_event = parser.event(7570)[0]
df_event.info()

#England away match numbers: Colombia, Tunisia, Belgium, Croatia, Sweden
#7585, 7537, 8657, 8656, 8651
#England home match numbers: Belgium and Panama
#7570, 7554

#The location data is not available for players for this game 
#df_frame = parser.frame(7585)
#df_frame.info()

#This gathers the pass data for England in their match vs Colombia 
sub = df_event.loc[df_event["type_name"] == "Substitution"].loc[df_event["team_name"] == "England"].iloc[0]["index"]
pass_england = (df_event.type_name == 'Pass') & (df_event.team_name == "England") & (df_event.index < sub) & (df_event.outcome_name.isnull()) & (df_event.sub_type_name != "Throw-in")
df_pass = df_event.loc[pass_england, ['x', 'y', 'end_x', 'end_y', "player_name", "pass_recipient_name"]]
df_pass["player_name"] = df_pass["player_name"].apply(lambda x: str(x).split()[-1])
df_pass["pass_recipient_name"] = df_pass["pass_recipient_name"].apply(lambda x: str(x).split()[-1])

#DataFrame to assist with the calculation of vertices size and location
scatter_df = pd.DataFrame()
for i, name in enumerate(df_pass["player_name"].unique()):
    passx = df_pass.loc[df_pass["player_name"] == name]["x"].to_numpy()
    recx = df_pass.loc[df_pass["pass_recipient_name"] == name]["end_x"].to_numpy()
    passy = df_pass.loc[df_pass["player_name"] == name]["y"].to_numpy()
    recy = df_pass.loc[df_pass["pass_recipient_name"] == name]["end_y"].to_numpy()
    scatter_df.at[i, "player_name"] = name
    
    #x and y location for each player is the average of passes given and received
    scatter_df.at[i, "x"] = np.mean(np.concatenate([passx, recx]))
    scatter_df.at[i, "y"] = np.mean(np.concatenate([passy, recy]))
    #calculate number of passes
    scatter_df.at[i, "num"] = df_pass.loc[df_pass["player_name"] == name].count().iloc[0]

#adjust the size of a circle so that the player who made more passes is larger
scatter_df['marker_size'] = (scatter_df['num'] / scatter_df['num'].max() * 1500)

#counting passes between players
df_pass["pair_key"] = df_pass.apply(lambda x: "_".join(sorted([x["player_name"], x["pass_recipient_name"]])), axis=1)
lines_df = df_pass.groupby(["pair_key"]).x.count().reset_index()
lines_df.rename({'x':'pass_count'}, axis='columns', inplace=True)
#setting a treshold. You can try to investigate how it changes when you change it.
lines_df = lines_df[lines_df['pass_count']>0] 


#Drawing pitch with verticies only
pitch = Pitch(line_color='grey')
fig, ax = pitch.grid(grid_height=0.9, title_height=0.06, axis=False,
                     endnote_height=0.04, title_space=0, endnote_space=0)
#Scatter the location on the pitch
pitch.scatter(scatter_df.x, scatter_df.y, s=scatter_df.marker_size, color='red', edgecolors='grey', linewidth=1, alpha=1, ax=ax["pitch"], zorder = 3)
#annotating player name
for i, row in scatter_df.iterrows():
    pitch.annotate(row.player_name, xy=(row.x, row.y), c='black', va='center', ha='center', weight = "bold", size=16, ax=ax["pitch"], zorder = 4)

fig.suptitle("Nodes Location - England", fontsize = 30)
plt.show()


#Drawing pitch with verticies and lines
pitch_two = Pitch(line_color = 'grey')
fig, ax = pitch_two.grid(grid_height=0.9, title_height=0.06, axis=False, endnote_height=0.04,
                     title_space=0, endnote_space=0)
pitch_two.scatter(scatter_df.x, scatter_df.y, s=scatter_df.marker_size, color='red',
              edgecolors='grey', linewidth=1, alpha=1, ax=ax["pitch"], zorder=3)
for i, row in scatter_df.iterrows():
    pitch_two.annotate(row.player_name, xy=(row.x,row.y), c='black', va='center',
                  ha='center', weight ="bold", size=16, ax=ax["pitch"], zorder=4)

for i, row in lines_df.iterrows():
    player_one = row["pair_key"].split("_")[0]
    player_two = row["pair_key"].split("_")[1]
    
    player_one_x = scatter_df.loc[scatter_df["player_name"] == player_one]['x'].iloc[0]
    player_one_y = scatter_df.loc[scatter_df["player_name"] == player_one]['y'].iloc[0]
    player_two_x = scatter_df.loc[scatter_df["player_name"] == player_two]['x'].iloc[0]
    player_two_y = scatter_df.loc[scatter_df["player_name"] == player_two]['y'].iloc[0]
    num_passes = row["pass_count"]
    
    line_width = (num_passes / lines_df['pass_count'].max() * 10)
    
    pitch_two.lines(player_one_x, player_one_y, player_two_x, player_two_y, alpha = 1, 
                lw = line_width, zorder=2, color="red", ax = ax["pitch"])
fig.suptitle("England Passing Lines", fontsize=30)

    
    
    
    
    
    
    
    
    
    


