#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  5 10:43:53 2022

@author: tedwards
"""

import matplotlib.pyplot as plt
from mplsoccer import Pitch, Sbopen, VerticalPitch
import pandas as pd

parser = Sbopen()
df_matches=parser.match(55, 43)

#Here we specify the team so we can easily change it to observe other teams
team = "England"
team_matches = df_matches.loc[(df_matches["home_team_name"] == team) | (df_matches["away_team_name"] == team)]["match_id"].tolist()
num_games = len(team_matches)

#Here, we use the mplsoccer data to identify all danger passes by 'team' in the specified competition
#Danger passes are defined as passes which occur at most 15 seconds before a goal
danger_passes = pd.DataFrame()
for i in team_matches:
    df_single_match = parser.event(i)[0]
    for period in [1,2]:
        #Here we want to exclude inaccurate passes and dead ball passes from our tracking
        #We do this by creating valid_passes which are passes which match general conditions then keeping the location, timestamp and player name from the pass
        valid_passes = (df_single_match.team_name == team) & (df_single_match.type_name == "Pass") & (df_single_match.outcome_name.isnull()) & (df_single_match.period == period) & (df_single_match.sub_type_name.isnull())
        passes = df_single_match.loc[valid_passes, ["x", "y", "end_x", "end_y", "minute", "second", "player_name"]]
        
        #Here we want to store all the shot data by the team we are tracking. We are not tracking which shots led to goals just the timestamp of them.
        valid_shots = (df_single_match.team_name == team) & (df_single_match.type_name == "Shot") & (df_single_match.period == period)
        shots = df_single_match.loc[valid_shots, ["minute", "second"]]
        shot_times = shots['minute']*60 + shots['second']
        shot_window = 15
        shot_start = shot_times-shot_window
        shot_start = shot_start.apply(lambda x: x if x>0 else (period-1)*45)
        
        pass_times = passes['minute']*60 + passes['second']
        pass_to_shot = pass_times.apply(lambda y: True in ((shot_start < y) & (y < shot_times)).unique())
        
        danger_passes_period = passes.loc[pass_to_shot]
        danger_passes = pd.concat([danger_passes, danger_passes_period])
    
#Now we will plot the danger passes using mplsoccers Pitch
pitch = Pitch(line_color = 'black')
fig, ax = pitch.grid(grid_height=0.9, title_height=0.06, axis=False, endnote_height=0.04, title_space=0, endnote_space=0)
pitch.scatter(danger_passes.x, danger_passes.y, s=100, color='blue', edgecolors='grey', linewidth=1, alpha=0.2, ax=ax["pitch"])
pitch.arrows(danger_passes.x, danger_passes.y, danger_passes.end_x, danger_passes.end_y, color="blue", ax=ax['pitch'])
fig.suptitle('Location of Danger Passes by ' +team, fontsize=30)


#Now we will make a heat map of the danger passes using the 'bin_statistic' from Pitch from mplsoccer
#The bin_statistic will group passes based on location into a bin using the passes starting location
pitch = Pitch(line_color = 'black')
fig, ax = pitch.grid(grid_height=0.9, title_height=0.06, axis=False, endnote_height=0.04, title_space=0, endnote_space=0)
bin_statistic=pitch.bin_statistic(danger_passes.x, danger_passes.y, statistic ='count', bins=(6,5), normalize=False)
bin_statistic["statistic"] = bin_statistic["statistic"]/num_games 
#This creates the actual heatmap
pcm = pitch.heatmap(bin_statistic, cmap='Reds', edgecolor='grey', ax=ax['pitch'])
ax_cbar = fig.add_axes((1, 0.093, 0.03, 0.786))
cbar = plt.colorbar(pcm, cax=ax_cbar)
fig.suptitle('Danger passes by ' + team + " per game", fontsize = 30)

#Now we will make a heatmap of where the danger passes end up using the 'bin_statistic' from Pitch from mplsoccer
pitch = Pitch(line_color = 'black')
fig, ax = pitch.grid(grid_height=0.9, title_height=0.06, axis=False, endnote_height=0.04, title_space=0, endnote_space=0)
bin_statistic=pitch.bin_statistic(danger_passes.end_x, danger_passes.end_y, statistic ='count', bins=(6,5), normalize=False)
bin_statistic["statistic"] = bin_statistic["statistic"]/num_games 
#This creates the actual heatmap
pcm = pitch.heatmap(bin_statistic, cmap='Reds', edgecolor='grey', ax=ax['pitch'])
ax_cbar = fig.add_axes((1, 0.093, 0.03, 0.786))
cbar = plt.colorbar(pcm, cax=ax_cbar)
fig.suptitle('Where danger passes end up ' + team + " per game", fontsize = 30)

#Specifying players in heatmap
#This grabs the last name of the players rather than their full name
danger_passes["player_name"] = danger_passes["player_name"].apply(lambda x: str(x).split()[-1])
pass_count = danger_passes.groupby(["player_name"]).x.count()/num_games
new_ax = pass_count.plot.barh(rot=0)

#grp=pass_count.plot.bar(pass_count)
#grp.set_xlabel("")
#grp.set_ylabel("Number of Danger passes per game")
#plt.show(grp)



   

