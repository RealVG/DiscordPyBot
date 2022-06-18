import discord
from discord.ext import commands

class help_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.help_message = """
```
General commands:
!help - Mostra tutti i comandi disponibili per gli utenti.
!p <Canzone> - Cerca una canzone da youtube e la riproduce nel canale.
!q - Mostra la coda.
!skip - Manda avanti la coda con la canzone successiva.
!clear - Mette in pausa la musica e elimina la coda(admin only).
!leave - Disconnette il bot dal canale connesso.
!pause - Mette in pausa la canzone o, se è gia in pausa, riprende.
!resume - Riprende la canzone messa in pausa.
```
"""
        self.text_channel_list = []

    #some debug info so that we know the bot has started    
    @commands.Cog.listener()
    async def on_ready(self):
        for guild in self.bot.guilds:
            for channel in guild.text_channels:
                self.text_channel_list.append(channel)



    @commands.command(name="help", help="Displays all the available commands")
    async def help(self, ctx):
        await ctx.send(self.help_message)

    async def send_to_all(self, msg):
        for text_channel in self.text_channel_list:
            await text_channel.send(msg)