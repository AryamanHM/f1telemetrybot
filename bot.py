import os
import discord
from discord.ext import commands
import fastf1 as ff1
from fastf1 import plotting
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.colors import ListedColormap
from matplotlib.collections import LineCollection


prefix = "#fuan "
client = commands.Bot(command_prefix=prefix, intents=discord.Intents.all())





@client.event
async def on_ready():
  print(f"I am ready to go - {client.user.name}")
  await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"Drive to Survive"))

@client.command(name="ping")
async def _ping(ctx):
  global times_used
  await ctx.send(f"Ping: {client.latency}")
  times_used = times_used + 1

@client.command(name="time")
async def _time(ctx):
  global times_used
  from datetime import date, datetime

  now = datetime.now()

  if (now.strftime("%H") <= "12"):
    am_pm = "AM"
  else:
    am_pm = "PM"

  datetime = now.strftime("%m/%d/%Y, %I:%M")

  await ctx.send("Current Time:" + ' '  + datetime + ' ' + am_pm)
  times_used = times_used + 1

@client.command(name="telemetry")
async def _command(ctx):
    def telemetry(year,track,session_race,driver_1,driver_2):
        ff1.Cache.enable_cache('cache')
        ff1.plotting.setup_mpl()
        #session = ff1.get_session(2022, 'Zandvoort', 'Q')
        session = ff1.get_session(year,track,session_race)
        session.load()
        ctx.send(session.laps)
        laps_driver_1 = session.laps.pick_driver(driver_1)
        laps_driver_2 = session.laps.pick_driver(driver_2)

        fastest_driver_1 = laps_driver_1.pick_fastest()
        fastest_driver_2 = laps_driver_2.pick_fastest()

        telemetry_driver_1 = fastest_driver_1.get_telemetry()
        telemetry_driver_2 = fastest_driver_2.get_telemetry() 
        # Get the gap (delta time) between driver 1 and driver 2
        delta_time, ref_tel, compare_tel = ff1.utils.delta_time(fastest_driver_1, fastest_driver_2)
        # Identify team colors
        team_driver_1 = laps_driver_1['Team'].iloc[0]
        team_driver_2 = laps_driver_2['Team'].iloc[0]

        # Fastf1 has a built-in function for the team colors!
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

        return ax    
     
    global times_used
    await ctx.send(f"Enter year,track,session_race,driver_1,driver_2 one by one.")

    # This will make sure that the response will only be registered if the following
    # conditions are met:
    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel 

    year = await client.wait_for("message", check=check)
    track = await client.wait_for("message", check=check)
    session_race = await client.wait_for("message", check=check)
    driver_1 = await client.wait_for("message", check=check)
    driver_2 = await client.wait_for("message", check=check)
    ax=telemetry(year,track,session_race,driver_1,driver_2)
    ax.plot()
    plt.show()


    times_used = times_used + 1  

#my_secret = os.environ['TOKEN']
#client.run(my_secret)   
client.run("MTAyNDkyNTYxMzM3NjY4MDAwNw.Gk4Rmu.LweosvTxAlFSh_LwzsognkczgSUQp9Xpj-jyYM")  


  

