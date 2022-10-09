import os
import discord
from discord.ext import commands
import fastf1 as ff1
from fastf1 import plotting
from fastf1.api import track_status_data
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.colors import ListedColormap
from matplotlib.collections import LineCollection
import asyncio
from keep_alive import keep_alive


prefix = "#fuan "
client = commands.Bot(command_prefix=prefix, intents=discord.Intents.all())
ff1.Cache.enable_cache('cache')
ff1.plotting.setup_mpl()

@client.event
async def on_ready():
  print(f"I am ready to go - {client.user.name}")
  await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"Drive to Survive"))

@client.event
async def on_command_error(ctx, error):
    await ctx.send(f"An error occured: {str(error)}")  

@client.command(name="ping")
async def _ping(ctx):
  await ctx.send(f"Ping: {client.latency}")

@client.command(name="telemetry")
async def _command(ctx,arg1,arg2,arg3,arg4,arg5):
  year=arg1
  track=arg2
  session_time=arg3
  driver_1=arg4
  driver_2=arg5
  await ctx.send("{},{},{},{},{}".format(year,track,session_time,driver_1,driver_2))
  session = ff1.get_session(int(arg1), str(arg2), str(arg3))
  session.load()
  laps_driver_1 = session.laps.pick_driver(str(arg4))
  laps_driver_2 = session.laps.pick_driver(str(arg5))

  fastest_driver_1 = laps_driver_1.pick_fastest()
  fastest_driver_2 = laps_driver_2.pick_fastest()

  telemetry_driver_1 = fastest_driver_1.get_telemetry()
  telemetry_driver_2 = fastest_driver_2.get_telemetry()
  delta_time, ref_tel, compare_tel = ff1.utils.delta_time(fastest_driver_1, fastest_driver_2)
  team_driver_1 = laps_driver_1['Team'].iloc[0]
  team_driver_2 = laps_driver_2['Team'].iloc[0]
  color_1 = ff1.plotting.team_color(team_driver_1)
  color_2 = ff1.plotting.team_color(team_driver_2)
  # Set the size of the plot
  plt.rcParams['figure.figsize'] = [20, 15]

  # Our plot will consist of 7 "subplots":
  #     - Delta
  #     - Speed
  #     - Throttle
  #     - Braking
  #     - Gear
  #     - RPM
  #     - DRS
  fig, ax = plt.subplots(7, gridspec_kw={'height_ratios': [1, 3, 2, 1, 1, 2, 1]})

  # Set the title of the plot
  ax[0].title.set_text(f"Telemetry comparison {driver_1} vs. {driver_2}")

  # Subplot 1: The delta
  ax[0].plot(ref_tel['Distance'], delta_time, color=color_1)
  ax[0].axhline(0)
  ax[0].set(ylabel=f"Gap to {driver_2} (s)")

  # Subplot 2: Distance
  ax[1].plot(telemetry_driver_1['Distance'], telemetry_driver_1['Speed'], label=driver_1, color=color_1)
  ax[1].plot(telemetry_driver_2['Distance'], telemetry_driver_2['Speed'], label=driver_2, color=color_2)
  ax[1].set(ylabel='Speed')
  ax[1].legend(loc="lower right")

  # Subplot 3: Throttle
  ax[2].plot(telemetry_driver_1['Distance'], telemetry_driver_1['Throttle'], label=driver_1, color=color_1)
  ax[2].plot(telemetry_driver_2['Distance'], telemetry_driver_2['Throttle'], label=driver_2, color=color_2)
  ax[2].set(ylabel='Throttle')

  # Subplot 4: Brake
  ax[3].plot(telemetry_driver_1['Distance'], telemetry_driver_1['Brake'], label=driver_1, color=color_1)
  ax[3].plot(telemetry_driver_2['Distance'], telemetry_driver_2['Brake'], label=driver_2, color=color_2)
  ax[3].set(ylabel='Brake')

  # Subplot 5: Gear
  ax[4].plot(telemetry_driver_1['Distance'], telemetry_driver_1['nGear'], label=driver_1, color=color_1)
  ax[4].plot(telemetry_driver_2['Distance'], telemetry_driver_2['nGear'], label=driver_2, color=color_2)
  ax[4].set(ylabel='Gear')

  # Subplot 6: RPM
  ax[5].plot(telemetry_driver_1['Distance'], telemetry_driver_1['RPM'], label=driver_1, color=color_1)
  ax[5].plot(telemetry_driver_2['Distance'], telemetry_driver_2['RPM'], label=driver_2, color=color_2)
  ax[5].set(ylabel='RPM')

  # Subplot 7: DRS
  ax[6].plot(telemetry_driver_1['Distance'], telemetry_driver_1['DRS'], label=driver_1, color=color_1)
  ax[6].plot(telemetry_driver_2['Distance'], telemetry_driver_2['DRS'], label=driver_2, color=color_2)
  ax[6].set(ylabel='DRS')
  ax[6].set(xlabel='Lap distance (meters)')

  # Hide x labels and tick labels for top plots and y ticks for right plots.
  for a in ax.flat:
      a.label_outer()
  fig.savefig("telemetry.png")
  with open('telemetry.png', 'rb') as f:
    picture = discord.File(f)
    await ctx.send(file=picture)
  
  ff1.Cache.clear_cache('cache')   

 
keep_alive()
my_secret = os.environ['TOKEN']
client.run(my_secret)   
##token = os.environ.get('BOT_TOKEN')
##client.run("")  


  

