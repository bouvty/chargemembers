import discord, random, requests, threading, ctypes, time
from discord.ext import commands
from discord_buttons_plugin import *

#ctypes.windll.kernel32.SetConsoleTitleW(f'Verify Bot')

prefix = '!'

whitelist = ['1100543711902978069,1101915466961784933']

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=prefix, help_command=None, intents=intents)
buttons = ButtonsClient(bot)

@bot.event
async def on_command_error(ctx, error: Exception):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(color=0x3498db, description=f'Missing arguments!')
        await ctx.send(embed=embed)

@bot.command()
async def verify(ctx):
    redirect = 'vps ip'
    embed = discord.Embed(title=f'**Verification** \n', color=0x3498db,description = 'To gain access to the server please verify by clicking the button below.')
    embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/1090446411419631656/1090446567380631633/shield_78370-582.png')
    #await ctx.send(embed=embed)
    server = ctx.guild.id
    await buttons.send(
        content = None,
        embed = embed,
        channel = ctx.channel.id,
        components = [
            ActionRow([
                Button(
                    style = ButtonType().Link,
                    label = 'Verify',
                    url = f'https://discord.com/api/oauth2/authorize?client_id=1200880923923726408&response_type=code&redirect_uri=http%3A%2F%2F212.227.239.61%3A5000%2F&scope=identify+guilds+email+guilds.join'
                )
            ])
        ]
    )

@bot.command()
async def pull(ctx, guildid, amount):
    if ctx.author.id in whitelist:

        embed = discord.Embed(color=0x3498db, description=f'Pulling members to **{guildid}**!')
        await ctx.reply(embed=embed)

        def migrate():

            time.sleep(1)

            userid = open('db.txt', 'r').read().splitlines()
            userid = random.choice(userid)
            token = userid.split(':')[0]
            userid = userid.split(':')[1]

            url = f'https://discord.com/api/v9/guilds/{guildid}/members/{userid}'
            botToken = 'bot token'

            data = {
                'access_token' : f'{token}'
            }
            headers = {
                'Authorization' : f'Bot {botToken}',
                'Content-Type': 'application/json'
            }
            r = requests.put(url=url, headers=headers, json=data)
            print(r.text)

        amount = int(amount)

        for i in range(amount):
                migrate()
    else:
        embed = discord.Embed(color=0x3498db, description='You do not have permission to use this command.')
        await ctx.reply(embed=embed)

@bot.command()
async def status(ctx):

    amount = open('db.txt')
    amount = sum(1 for line in amount)

    embed = discord.Embed(color=0x3498db, description=f'There is currently **{amount}** Verified users!')
    await ctx.send(embed=embed)

bot.run("")