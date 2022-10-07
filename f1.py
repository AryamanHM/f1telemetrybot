#!/usr/bin/env python
# coding: utf-8

# In[1]:


pip install fastf1


# In[2]:


import fastf1 as ff1


# In[4]:


#enable the cache
ff1.Cache.enable_cache('cache')


# In[5]:


#Specify the session (no data downloaded yet)
session=ff1.get_session(2022,'Zandvoort','Q')
#download the data
session.load()


# In[6]:


session.laps


# In[7]:


#Get all laps from Latifi
session.laps.pick_driver('LAT')


# In[8]:


session.laps.pick_driver('LAT').pick_fastest()


# Intro to F1 Data Analysis with Python
# Jupyter notebooks have shortcuts
# -N convert cell to markdown
# -A insert cell above
# -DD deletes cell
# -b INSERT CELL Below
# Shift+Enter will run a cell and move on to the next one

# 0.Setting Everything up

# In[10]:


import fastf1 as ff1
from fastf1 import plotting
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.colors import ListedColormap
from matplotlib.collections import LineCollection


# How to install fastf1

# In[9]:


get_ipython().run_line_magic('pip', 'install fastf1')


# In[11]:


#Enable the cache
ff1.Cache.enable_cache('cache') #argument is the name of the folder


# In[12]:


#Enable the plotting settings
ff1.plotting.setup_mpl()


# In[13]:


session=ff1.get_session(2022,'Zandvoort','Q')


# In[14]:


session


# In[15]:


session.load()


# 1.eXPLORE THE DATA

# In[16]:


session.laps


# In[17]:


laps_alb=session.laps.pick_driver('ALB')
laps_alb


# In[18]:


laps_alb.pick_fastest()


# In[21]:


573/73


# In[22]:


laps_alb.pick_fastest().get_telemetry()


# LETS BUILD SOME PLOTS

# In[23]:


driver_1,driver_2='VET','NOR'


# In[24]:


laps_driver_1=session.laps.pick_driver(driver_1)
laps_driver_2=session.laps.pick_driver(driver_2)


# In[25]:


fastest_driver_1=laps_driver_1.pick_fastest()
fastest_driver_2=laps_driver_2.pick_fastest()


# In[26]:


telemetry_driver_1=fastest_driver_1.get_telemetry()
telemetry_driver_2=fastest_driver_2.get_telemetry()


# In[29]:


delta_time, ref_tel, compare_tel = ff1.utils.delta_time(fastest_driver_1, fastest_driver_2)


# In[34]:


#Identify team color
#laps_driver_1
team_driver_1=laps_driver_1['Team'].iloc[0]
team_driver_2=laps_driver_2['Team'].iloc[0]

color_1=ff1.plotting.team_color(team_driver_1)
color_2=ff1.plotting.team_color(team_driver_2)


# In[32]:


team_driver_1


# In[35]:


color_1


# 2.1 Telemtry Bot

# In[41]:


#Set the size of the plot
plt.rcParams['figure.figsize']=[20,15]

#7 plots
#- Delta
#Speed
#Throttle
#Breaking
#Gear
#RPM
#DRS
fig, ax = plt.subplots(7, gridspec_kw={'height_ratios': [1, 3, 2, 1, 1, 2, 1]})

#set the title of the plot
ax[0].title.set_text(f"Telemtry Comparison {driver_1} vs. {driver_2}")

#Subplot 1:The delta
ax[0].plot(ref_tel['Distance'],delta_time,color=color_1)
ax[0].axhline(0)
ax[0].set(ylabel=f"Gap to {driver_2}(s)")

#Subplot 2,Speed
ax[1].plot(telemetry_driver_1['Distance'],telemetry_driver_1['Speed'],label=driver_1,color=color_1)
ax[1].plot(telemetry_driver_2['Distance'],telemetry_driver_2['Speed'],label=driver_1,color=color_2)
ax[1].set(ylabel="Speed")
ax[1].legend(loc="lower right")

"""ax[1].plot(telemetry_driver_1['Distance'], telemetry_driver_1['Speed'], label=driver_1, color=color_1)
ax[1].plot(telemetry_driver_2['Distance'], telemetry_driver_2['Speed'], label=driver_2, color=color_2)
ax[1].set(ylabel="Speed")
ax[1].legend(loc="lower right")
"""
# Subplot 3: Throttle
ax[2].plot(telemetry_driver_1['Distance'], telemetry_driver_1['Throttle'], label=driver_1, color=color_1)
ax[2].plot(telemetry_driver_2['Distance'], telemetry_driver_2['Throttle'], label=driver_2, color=color_2)
ax[2].set(ylabel="Throttle")

#Subplot 4:Breaking
ax[3].plot(telemetry_driver_1['Distance'], telemetry_driver_1['Brake'], label=driver_1, color=color_1)
ax[3].plot(telemetry_driver_2['Distance'], telemetry_driver_2['Brake'], label=driver_2, color=color_2)
ax[3].set(ylabel="Breaking")

#Subplot 5:Gears
ax[4].plot(telemetry_driver_1['Distance'], telemetry_driver_1['nGear'], label=driver_1, color=color_1)
ax[4].plot(telemetry_driver_2['Distance'], telemetry_driver_2['nGear'], label=driver_2, color=color_2)
ax[4].set(ylabel="Gear")

# Subplot 6: RPM
ax[5].plot(telemetry_driver_1['Distance'], telemetry_driver_1['RPM'], label=driver_1, color=color_1)
ax[5].plot(telemetry_driver_2['Distance'], telemetry_driver_2['RPM'], label=driver_2, color=color_2)
ax[5].set(ylabel="RPM")

# Subplot 7: DRS
ax[6].plot(telemetry_driver_1['Distance'], telemetry_driver_1['DRS'], label=driver_1, color=color_1)
ax[6].plot(telemetry_driver_2['Distance'], telemetry_driver_2['DRS'], label=driver_2, color=color_2)
ax[6].set(ylabel="DRS")




# 2.2 Minisector Comparison

# In[42]:


# Merge the telemetry from both drivers into one dataframe
telemetry_driver_1['Driver'] = driver_1
telemetry_driver_2['Driver'] = driver_2

telemetry = pd.concat([telemetry_driver_1, telemetry_driver_2])


# In[43]:


telemetry


# In[44]:


#calculate the minisectors
num_minisectors=25
total_distance=max(telemetry['Distance'])


# In[46]:


max(telemetry['Distance'])


# In[47]:


# Calculate the minisectors
num_minisectors = 25
total_distance = max(telemetry['Distance'])
minisector_length = total_distance / num_minisectors


# In[49]:


minisectors=[0]


# In[51]:


for i in range(0,(num_minisectors-1)):
    #print(i)
    minisectors.append(minisector_length*(i+1))


# In[52]:


minisectors


# In[ ]:


"""
for i in range(0, (num_minisectors - 1)):
    minisectors.append(minisector_length * (i + 1))

"""


# In[54]:


# Assign a minisector number to every row in the telemetry dataframe
telemetry


# In[55]:


minisectors


# In[56]:


# Assign a minisector number to every row in the telemetry dataframe
telemetry['Minisector'] = telemetry['Distance'].apply(
    lambda dist: (
        int((dist // minisector_length) + 1)
    )
)


# In[57]:


telemetry


# In[58]:


#Calculate minisector speeds per driver
average_speed = telemetry.groupby(['Minisector', 'Driver'])['Speed'].mean().reset_index()
average_speed


# In[59]:


# Per minisector, find the fastest driver
fastest_driver = average_speed.loc[average_speed.groupby(['Minisector'])['Speed'].idxmax()]
fastest_driver = fastest_driver[['Minisector', 'Driver']].rename(columns={'Driver': 'Fastest_driver'})


# In[60]:


fastest_driver


# In[61]:


# Merge the fastest_driver dataframe to the telemetry dataframe on minisector
telemetry = telemetry.merge(fastest_driver, on=['Minisector'])
telemetry = telemetry.sort_values(by=['Distance'])
telemetry


# In[62]:


# Since our plot can only work with integers, we need to convert the driver abbreviations to integers (1 or 2)
telemetry.loc[telemetry['Fastest_driver'] == driver_1, 'Fastest_driver_int'] = 1
telemetry.loc[telemetry['Fastest_driver'] == driver_2, 'Fastest_driver_int'] = 2
telemetry


# In[63]:


# Get the x and y coordinates 
x = np.array(telemetry['X'].values)
y = np.array(telemetry['Y'].values)


# In[64]:


x


# In[65]:


y


# In[66]:


# Convert the coordinates to points, and then concat them into segments
points = np.array([x, y]).T.reshape(-1, 1, 2)

segments = np.concatenate([points[:-1], points[1:]], axis=1)
fastest_driver_array = telemetry['Fastest_driver_int'].to_numpy().astype(float)


# In[67]:


segments


# In[68]:


# The segments we just created can now be colored according to the fastest driver in a minisector
cmap = ListedColormap([color_1, color_2])
lc_comp = LineCollection(segments, norm=plt.Normalize(1, cmap.N+1), cmap=cmap)
lc_comp.set_array(fastest_driver_array)
lc_comp.set_linewidth(5)


# In[69]:


# Create the plot
plt.rcParams['figure.figsize'] = [18, 10]

plt.gca().add_collection(lc_comp)
plt.axis('equal')
plt.box(False)
plt.tick_params(labelleft=False, left=False, labelbottom=False, bottom=False)

# Add a colorbar for as legend
cbar = plt.colorbar(mappable=lc_comp, boundaries=np.arange(1,4))
cbar.set_ticks(np.arange(1.5, 9.5))
cbar.set_ticklabels([driver_1, driver_2])


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




