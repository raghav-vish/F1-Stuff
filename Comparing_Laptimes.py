'''
Comparing two drivers laptimes over a race

This program helps to visualize the lap time differences between
any two drivers over a given race.

The data used is from the FastF1 library.



Stuff you need to enter - Year, Race, Number of Laps

Drivers - You may choose any two drivers that took part in that race.
Teams - The teams that these drivers are a part of. This is 
		required only for the plot colors. If you do not want team-specific
		colors or want custom colors, you may edit the colors list below.

fpitlaps - This is a list of the laps during which the first driver pit. The first
		   driver here is the one you have mentioned first in the drivers array.
spitlaps - Similarly, this is a list of the laps during which the second driver pitted.

(One easy way to find out which laps each of the drivers pitted, assuming that they did
not pit at the same lap, is to leave both the pit lists empty, run the program, and 
look for the laps where one drivers is a huge amount, say more than 15-20s faster than
the other. If x is such a huge amount faster than y over a lap, it is likely that y 
pitted that lap.)
'''

year=2021
race='France'
numberlaps=53

drivers=['VER','HAM']
teams=['red bull', 'mercedes']
fpitlaps=[18,32]
spitlaps=[19]

import fastf1 as ff1
from fastf1 import plotting
from matplotlib import pyplot as plt
from matplotlib.pyplot import figure
import pandas as pd

ff1.Cache.enable_cache('./cache')

plotting.setup_mpl()

session='R'
r = ff1.get_session(year, race, session)
laps = r.load_laps(with_telemetry=True)

lap_data=[]
colors=['#000000','#FFFFFF']
for i in range(2):
	teams[i]=teams[i].lower()
	if(teams[i] in plotting.TEAM_COLORS):
		colors[i]=plotting.TEAM_COLORS[teams[i]]

laptimes=[]
for i in range(len(drivers)):
	lap_data.append(laps.pick_driver(drivers[i]))
	laptimes.append([])
	for l in range(1, numberlaps+1):
		t=lap_data[i][lap_data[i]['LapNumber']==l].iloc[0]['LapTime'].value/1000000000
		laptimes[i].append(t)
diff=[]
laps=[]
flaps=[]
ftimes=[]
slaps=[]
stimes=[]

for i in range(len(laptimes[0])):
	if(i+1 in fpitlaps or i+1 in spitlaps):
		continue
	t=laptimes[1][i]-laptimes[0][i]
	diff.append(t)
	laps.append(i+1)
	if(t>0):
		flaps.append(i+1)
		ftimes.append(t)
	else:
		slaps.append(i+1)
		stimes.append(t)

pits=[i for i in range(-15,15)]

fig, ax = plt.subplots()
fig.suptitle(f'{year} {race} {session} {drivers[0]} vs. {drivers[1]} Laptime Comparison')
ax.plot(laps,diff,'--',color='Black')
ax.plot(flaps,ftimes,'o',color=colors[0],label=f'{drivers[0]} faster',markersize=9)
ax.plot(slaps,stimes,'o',color=colors[1],label=f'{drivers[1]} faster',markersize=9)
ax.plot([i for i in range(0,numberlaps+2)],[0]*(numberlaps+2) ,'Black')
for i in range(len(fpitlaps)):
	ax.plot([fpitlaps[i]]*30,pits,'r',label=f'{drivers[0]} pits' if i == 0 else "")
for i in range(len(spitlaps)):
	ax.plot([spitlaps[i]]*30,pits,'--r',label=f'{drivers[1]} pits' if i == 0 else "")
ax.legend(loc='best')
plt.ylim((min(diff)-0.2,max(diff)+0.2))
plt.xlim(0,numberlaps+1)
plt.xlabel('Lap Number')
plt.ylabel(f'<--  {drivers[1]} faster | {drivers[0]} faster  -->')
plt.show()