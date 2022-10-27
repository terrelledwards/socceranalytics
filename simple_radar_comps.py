 #!/usr/bin/env python3
 # -*- coding: utf-8 -*-
 
"""
 Created on Thu Sep 29 10:00:24 2022

 @author: tedwards
 """

import matplotlib.pyplot as plt 
from mplsoccer import Pitch, VerticalPitch, Radar, FontManager, grid


URL4 = 'https://raw.githubusercontent.com/googlefonts/roboto/main/src/hinted/Roboto-Thin.ttf'
robotto_thin = FontManager(URL4)

pitch = Pitch(half=False, pitch_color=('grass'), 
               goal_linestyle=':', corner_arcs=True, positional=True, shade_middle=True,
               shade_color='grey', goal_type='box', line_alpha=0.5, goal_alpha=0.8)
fig, ax = pitch.draw(figsize= (10,10))

 #Names of Parameters to be evaluated.
params = ["npxG", "Non-Penalty Goals", "xA", "Key Passes", "Through Balls",
           "Progressive Passes", "Shot-Creating Actions", "Goal-Creating Actions",
           "Dribbles Completed", "Pressure Regains", "Touches In Box", "Miscontrol"]

 # The lower and upper boundaries for the statistics
low =  [0.08, 0.0, 0.1, 1, 0.6,  4, 3, 0.3, 0.3, 2.0, 2, 0]
high = [0.37, 0.6, 0.6, 4, 1.2, 10, 8, 1.3, 2.7, 5.5, 10, 5]

 # Add anything to this list where having a lower number is better
 # this flips the statistic
lower_is_better = ['Miscontrol']

 # Instantiate the Radar Class
 # ---------------------------
 # We will instantiate a ``Radar`` object with the above parameters so that we can re-use it
 # several times.

radar = Radar(params, low, high,
               lower_is_better=lower_is_better,
               # whether to round any of the labels to integers instead of decimal places
               round_int=[False]*len(params),
               num_rings=4,  # the number of concentric circles (excluding center circle)
               # if the ring_width is more than the center_circle_radius then
               # the center circle radius will be wider than the width of the concentric circles
               ring_width=1, center_circle_radius=1)

 ##Through Ball stats for JackyG are horribly low
 #JackyG pressured less but was more successful with City indicating their team pressure is better
grealish_england = []
grealish_villa = [.18, .25, .35, 3.41, .6, 6.92, 6.18, .86, 2.51, 4.11, 7.3, 1.89]
grealish_city = [.22, .14, .30, 2.54, .6, 3.86, 5.17, .33, 1.6, 4.93, 9.1, 1.22]

fig, ax = radar.setup_axis()
rings_inner = radar.draw_circles(ax=ax, facecolor='#ffb2b2', edgecolor='#fc5f5f')
radar_output = radar.draw_radar_compare(grealish_villa, grealish_city, ax=ax,
                                         kwargs_radar={'facecolor': '#00f2c1', 'alpha': 0.6},
                                         kwargs_compare={'facecolor': '#d80499', 'alpha': 0.6})
radar_poly, radar_poly2, vertices1, vertices2 = radar_output
range_labels = radar.draw_range_labels(ax=ax, fontsize=15,
                                        fontproperties=robotto_thin.prop)
param_labels = radar.draw_param_labels(ax=ax, fontsize=15,
                                        fontproperties=robotto_thin.prop)
 
 
 #After Grealish, analyze the rightback options for England. 
 
def_params = ["Fouls", "Dribbled Past", "Aerial Wins %", "Dispossesed", "Successful Dribbles",
               "Completed Crosses", "Key Passes", "Pass %", "Adj. Tkls", "Adj. Int"]
 
def_low = [0.1, 0, 0, 0, 0, 0, 0, 25, 0, 0]
def_high = [2.4, 2, 100, 3, 3, 8, 5, 95, 5, 5]
def_lower_is_better = ['Dispossesed', 'Dribbled Past']
 
radar = Radar(def_params, def_low, def_high, lower_is_better=def_lower_is_better,
               round_int=[False]*len(def_params), num_rings=4, ring_width=1, 
               center_circle_radius=1)
trent_stats = [.5, 1.14, 45, .82, .82, 4.01, 2.81, 74.4, .73, 2.4]
trippier_stats =[1.04, 1.25, 70.6, .63, .21, 2.29, 1.46, 68.8, 4.38, 2.29]
reece_stats = [.87, .82, 47.8, 1.16, 1.64, 3.96, 2.27, 86.5, 1.88, 1.01]
walker_stats = [.36, .56, 55.3, .36, .41, 1.44, .67, 88.9, 1.18, 1.28]
 
 
fig, ax = radar.setup_axis()
rings_inner = radar.draw_circles(ax=ax, facecolor='#ffb2b2', edgecolor='#fc5f5f')

radar1, vertices1 = radar.draw_radar_solid(trent_stats, ax=ax,
                                           kwargs={'facecolor': 'red',
                                                   'alpha': 0.6,
                                                   'edgecolor': '#216352',
                                                   'lw': 3})

radar2, vertices2 = radar.draw_radar_solid(trippier_stats, ax=ax,
                                           kwargs={'facecolor': 'grey',
                                                   'alpha': 0.6,
                                                   'edgecolor': '#216352',
                                                   'lw': 3})

radar3, vertices3 = radar.draw_radar_solid(reece_stats, ax=ax,
                                           kwargs={'facecolor': 'blue',
                                                   'alpha': 0.6,
                                                   'edgecolor': '#222b54',
                                                   'lw': 3})
radar4, vertices4 = radar.draw_radar_solid(walker_stats, ax=ax,
                                           kwargs={'facecolor': 'green',
                                                   'alpha': 0.6,
                                                   'edgecolor': '#222b54',
                                                   'lw': 3})

ax.scatter(vertices1[:, 0], vertices1[:, 1],
           c='#aa65b2', edgecolors='#502a54', marker='o', s=150, zorder=2)
ax.scatter(vertices2[:, 0], vertices2[:, 1],
           c='#66d8ba', edgecolors='#216352', marker='o', s=150, zorder=2)
ax.scatter(vertices3[:, 0], vertices3[:, 1],
           c='#697cd4', edgecolors='#222b54', marker='o', s=150, zorder=2)
ax.scatter(vertices4[:, 0], vertices3[:, 1],
           c='#697cd4', edgecolors='#222b54', marker='o', s=150, zorder=2)

range_labels = radar.draw_range_labels(ax=ax, fontsize=25, fontproperties=robotto_thin.prop)
param_labels = radar.draw_param_labels(ax=ax, fontsize=25, fontproperties=robotto_thin.prop)


 
 