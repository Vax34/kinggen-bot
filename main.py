from dotenv import load_dotenv  # pip install python-dotenv
import os
import discord  # pip install discord
from discord.ext import commands
import httpx  # pip install httpx (no i won't use aiohttp fuck off)
import json
import datetime

load_dotenv()
TOKEN = os.getenv("TOKEN") # make a .env file next to this main.py file, edit it and fill in: TOKEN=YourDiscordBotTokenWithoutThisCharacter"
KEY = os.getenv("KEY")

params = {
    "key": KEY
}


bot = commands.Bot(command_prefix="!")
bot.remove_command('help')


@bot.command(name="help")
async def helpmenu(ctx):
    desc = "!generate (amount) - Generates a number of accounts using your api key (default amount: 1)\n!history (optional: date, format: mm/dd)"
    embed = discord.Embed(title="Help Menu", description=desc)
    await ctx.send(embed=embed)


async def writetofile(alt):
    date = str(datetime.datetime.now().strftime("%m/%d"))
    print(date)
    contents = json.loads(open("savedalts.json").read())
    try:
        with open("savedalts.json", 'r+') as file:
            alts = contents[str(date)]
            alts.append(alt)
            file.seek(0)
            json.dump(contents, file, indent=4)
            print("this date is saved in the alt list")
    except:
        print("this date is not in the saved alt list")
        with open("savedalts.json", 'r+') as file:
            toadd = {date: [alt]}
            contents.update(toadd)
            json.dump(contents, file, indent=4)


@bot.command(name="history")
async def send_history(ctx, date=datetime.datetime.now().strftime("%m/%d")):
    contents = json.loads(open("savedalts.json").read())
    if date in contents:
        altlist = contents[date]
        altlistj = '\n'.join(altlist)
        embed = discord.Embed(title=f"Alt history for {date}", description=altlistj)
        await ctx.send(embed=embed)
    else:
        await ctx.send("Invalid date")


@bot.command(name='generate')
async def generate(ctx, amount=1):  # please dont activate this command twice at the same time or it might break thx
    altlist = []
    for alt in range(amount):
        response = httpx.get("https://kinggen.wtf/api/v2/alt", params=params)
        contents = json.loads(str(response.text))
        if response.status_code != 200:
            embed = discord.Embed(title="An error occured", description=contents['message'])
            await ctx.send(embed=embed)
        else:
            email = contents['email']
            password = contents['password']
            altstring = f"{email}:{password}"
            altlist.append(altstring)
            await writetofile(alt=altstring)
    print(altlist)
    if len(altlist) == 0:
        await ctx.send("No alts were generated due to an error")
    else:
        alts = '\n'.join(altlist)
        embed = discord.Embed(title="Generated alts:", description=alts)
        await ctx.send(embed=embed)


bot.run(TOKEN)
