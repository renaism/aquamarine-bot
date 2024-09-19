import discord
from discord.ext import commands

class SocialGame(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data = bot.data
    
    @commands.command()
    async def start(self, ctx):
        vc = None
        voice_state = ctx.author.voice

        if voice_state: 
            vc = voice_state.channel

        if vc == None:
            await ctx.send("You're not in any voice channel. Join a voice channel where the meeting will be held.")
            return
        else:
            if vc.guild.id in self.data["SocialGame"]:
                await ctx.send("A session is already running on this server. End session with `=end` command.")
                return
            
            self.data["SocialGame"][vc.guild.id] = {"vc": vc, "dead_members": []}

            await ctx.send(f"Starting game session in channel `{vc.name}`. Everyone will be muted and deafened.")
            await self.silence_all_vc_members(vc, self.data["SocialGame"][ctx.guild.id])
    
    @commands.command()
    async def unmute(self, ctx):
        if ctx.guild.id not in self.data["SocialGame"]:
            return
        
        vc = self.data["SocialGame"][ctx.guild.id]["vc"]
        await ctx.send(f"Starting emergency meeting. Everyone will be unmuted and undeafened.")
        await self.unsilence_all_vc_members(vc, self.data["SocialGame"][ctx.guild.id])
    
    @commands.command()
    async def mute(self, ctx):
        if ctx.guild.id not in self.data["SocialGame"]:
            return
            
        vc = self.data["SocialGame"][ctx.guild.id]["vc"]
        await ctx.send(f"Resuming activity. Everyone will be muted and deafened.")
        await self.silence_all_vc_members(vc, self.data["SocialGame"][ctx.guild.id])

    @commands.command()
    async def dead(self, ctx, *, member: discord.Member = None):
        if ctx.guild.id not in self.data["SocialGame"] or member == None:
            return
        
        self.data["SocialGame"][ctx.guild.id]["dead_members"].append(member)
        await member.edit(mute=True, deafen=False)
        await ctx.send(f"{member.display_name} is now dead.")
    
    @commands.command()
    async def end(self, ctx):
        if ctx.guild.id not in self.data["SocialGame"]:
            await ctx.send("No game session currently running in this server.")
            return
        
        self.data["SocialGame"][ctx.guild.id]["dead_members"] = []
        vc = self.data["SocialGame"][ctx.guild.id]["vc"]
        await self.unsilence_all_vc_members(vc, self.data["SocialGame"][ctx.guild.id])
        self.data["SocialGame"].pop(ctx.guild.id)
        await ctx.send("Game session in this server is now ended.")
    
    async def silence_all_vc_members(self, vc, guild_data):
        for member in vc.members:
            if member not in guild_data["dead_members"]:
                await member.edit(mute=True, deafen=True)
    
    async def unsilence_all_vc_members(self, vc, guild_data):
        for member in vc.members:
            if member not in guild_data["dead_members"]:
                await member.edit(mute=False, deafen=False)