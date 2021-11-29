'''
This program allows users to easily view telemetry data of specific laps of F1 races. The
data is retrived using the FastF1 library.

race may be entered as a string, or as a number. The number signifies the race number.
For example. in 2021, 1-Bahrain, 2-Imola and so on.

Options for session -  FP1, FP2, FP3, Q, ‘SQ’, ‘R’
'''
year='2021'
race='Mexico'
session='R'

'''
Enter the drivers and corresponding lap numbers for which you wish to view the telemetry.
For example, the current code will display the telemetry for the first laps for Verstappen,
Hamilton and Perez. You may enter the drivers as their 3 letter abbreviation, or their racing number.

The lap number may be entered as a number or a string. If you wish to view the fastest lap,
enter 'fastest' in place of the lap number.
'''
drivers=['VER','HAM','PER']
lapcount=['1','1','1']

'''
Enter the teams in the same order as the drivers. This is to select the color while plotting.
If you wish to use certain custom colors, modify the colors list.

The default is to use team colors for each of the drivers, with solid lines for the first
driver of each team, and dotted lines for the next. To modify this, you may modify the styles list.
'''
teams=['red bull', 'mercedes', 'red bull']

'''
Enter the fields which you wish to view in the telemetry.
You may choose one or more from the following - Speed, Throttle, Brake, RPM, nGear, DRS
'''
fields=['Speed', 'Throttle', 'Brake', 'nGear', 'RPM']

import fastf1 as ff1
from fastf1 import plotting
from matplotlib import pyplot as plt
from matplotlib.pyplot import figure

ff1.Cache.enable_cache('./cache')

plotting.setup_mpl()
if(race.isnumeric()):
	rac=int(race)
r = ff1.get_session(year, race, session)
laps = r.load_laps(with_telemetry=True)

lap_data=[]
telem=[]
colors=[]

for team in teams:
	if(team in plotting.TEAM_COLORS):
		colors.append(plotting.TEAM_COLORS[team])
	else:
		colors.append('#000000')

styles=['-']*len(drivers)
for i in range(1, len(teams)):
	if(teams[i] in teams[:i]):
		styles[i]='--'

for i in range(len(drivers)):
	lap_data.append(laps.pick_driver(drivers[i]))

for i in range(len(lap_data)):
	if(lapcount[i]=='fastest'):
		x=lap_data[i].pick_fastest()
	else:
		lno=int(lapcount[i])
		x=lap_data[i][lap_data[i]['LapNumber']==lno].iloc[0]
	telem.append(x.get_car_data().add_distance())

if(len(fields)==1):
	fig, ax = plt.subplots()
	fig.suptitle(f'{year} {race} {session} Telemetry Comparison')
	for i in range(len(fields)):
		for j in range(len(telem)):
			ax.plot(telem[j]['Distance'], telem[j][fields[i]], label=drivers[j], color=colors[j], linestyle=styles[j])
	ax.set(ylabel=fields[0])
	ax.legend(loc="lower right")

else:
	fig, ax = plt.subplots(len(fields))
	fig.suptitle(f'{year} {race} {session} Telemetry Comparison')
	for i in range(len(fields)):
		for j in range(len(telem)):
			ax[i].plot(telem[j]['Distance'], telem[j][fields[i]], label=drivers[j], color=colors[j], linestyle=styles[j])
		ax[i].set(ylabel=fields[i])
		ax[0].legend(loc="lower right")

	for a in ax.flat:
		a.label_outer()
	
plt.show()