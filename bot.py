import discord
from discord.ext import commands
from discord.utils import get
import asyncio

intents = discord.Intents.all()
intents.message_content = True

# Bot
bot = commands.Bot(command_prefix="!", intents=intents)

# Bot Events ----------------------------------------------------

# Role Add for console_roles
@bot.listen()
async def on_raw_reaction_add(payload):
    ourMessageID = 1225299863390916711 # Console Role Message ID

    if ourMessageID == payload.message_id: # Checks that the message sent is by author
        member = payload.member
        guild = member.guild

        emoji = payload.emoji.name
        if emoji == '❌':
            role = get(guild.roles, name="Xbox")
        elif emoji == '🇵':
            role = get(guild.roles, name="Playstation")
        elif emoji == '🖥️':
            role = get(guild.roles, name="PC")
        await member.add_roles(role)

# Role Deletion for console_roles
@bot.listen()
async def on_raw_reaction_remove(payload):
    ourMessageID = 1225299863390916711 # Console Role Message ID

    if ourMessageID == payload.message_id: # Checks that the message sent is by author
        guild = await bot.fetch_guild(payload.guild_id)
        member = await guild.fetch_member(payload.user_id)

        emoji = payload.emoji.name
        if emoji == '❌':
            role = get(guild.roles, name="Xbox")
        elif emoji == '🇵':
            role = get(guild.roles, name="Playstation")
        elif emoji == '🖥️':
            role = get(guild.roles, name="PC")
        await member.remove_roles(role)

# Role Add for genre_roles
@bot.listen()
async def on_raw_reaction_add(payload):
    ourMessageID = 1225299980982419499 # Console Role Message ID

    if ourMessageID == payload.message_id: # Checks that the message sent is by author
        member = payload.member
        guild = member.guild

        emoji = payload.emoji.name
        if emoji == '💥':
            role = get(guild.roles, name="Action")
        elif emoji == '🗺️':
            role = get(guild.roles, name="Adventure")
        elif emoji == '👊':
            role = get(guild.roles, name="Fighting")
        elif emoji == '😱':
            role = get(guild.roles, name="Horror")
        elif emoji == '🧩':
            role = get(guild.roles, name="Puzzle")
        elif emoji == '🥸':
            role = get(guild.roles, name="RPG")
        elif emoji == '🔫':
            role = get(guild.roles, name="Shooter")
        elif emoji == '🏀':
            role = get(guild.roles, name="Sports")
        elif emoji == '♔':
            role = get(guild.roles, name="Strategy")
        elif emoji == '⚒️':
            role = get(guild.roles, name="Survival")
        await member.add_roles(role)

# Role Deletion for genre_roles
@bot.listen()
async def on_raw_reaction_remove(payload):
    ourMessageID = 1225299980982419499 # Console Role Message ID

    if ourMessageID == payload.message_id: # Checks that the message sent is by author
        guild = await bot.fetch_guild(payload.guild_id)
        member = await guild.fetch_member(payload.user_id)

        emoji = payload.emoji.name
        if emoji == '💥':
            role = get(guild.roles, name="Action")
        elif emoji == '🗺️':
            role = get(guild.roles, name="Adventure")
        elif emoji == '👊':
            role = get(guild.roles, name="Fighting")
        elif emoji == '😱':
            role = get(guild.roles, name="Horror")
        elif emoji == '🧩':
            role = get(guild.roles, name="Puzzle")
        elif emoji == '🥸':
            role = get(guild.roles, name="RPG")
        elif emoji == '🔫':
            role = get(guild.roles, name="Shooter")
        elif emoji == '🏀':
            role = get(guild.roles, name="Sports")
        elif emoji == '♔':
            role = get(guild.roles, name="Strategy")
        elif emoji == '⚒️':
            role = get(guild.roles, name="Survival")
        await member.remove_roles(role)

# Voice Channel Deletion
@bot.listen()
async def on_voice_state_update(member, before, after):

    # Checks that its not the Waiting Room
    if before.channel.name == "Waiting Room":
        return
    
    # Checks if the last party is empty
    if len(before.channel.members) == 0: 
        await before.channel.delete()

#----------------------------------------------------------------

# Bot Commands --------------------------------------------------

# Party Creation
# ctx: context 
# *args: Contains voice channel meta info [List]
# Uses a command to make a voice channel given meta data, will also move player
@bot.command()
async def party(ctx, *args):
    
    guild = ctx.guild
    voice_category = guild.categories[2]
    if len(args) == 1:
        new_channel = await guild.create_voice_channel(f"{args[0]}", category=voice_category)
    else:
        new_channel = await guild.create_voice_channel(f"{args[0]}", category=voice_category, user_limit=int(args[1]))

    # Moves member to new party
    member_move = ctx.message.author
    await member_move.move_to(new_channel)

    # Deletes original command message on Discord
    await ctx.message.delete()
    
    
    # Check function for checking capacity of voice channnel
    def check(member, before, after):
        return member == ctx.author and before.channel == new_channel and after.channel is None

    await bot.wait_for("voice_state_update", check=check)
    if len(new_channel.members) == 0:
        await new_channel.delete()
    
# Console Roles   
@bot.command()
async def console_roles(ctx):
    embed = discord.Embed(
        title="Console Role Selections",
        description='''
        Choose your console below!
        ❌ -> Xbox
        🇵 -> Playstation
        🖥️ -> PC'''
    )

    msg = await ctx.send(embed=embed)

    await msg.add_reaction('❌')
    await msg.add_reaction('🇵')
    await msg.add_reaction("🖥️")

# Genre Roles   
@bot.command()
async def genre_roles(ctx):
    embed = discord.Embed(
        title="Genre Role Selections",
        description='''
        Choose your preferred genres below!
        💥 -> Action
        🗺️ -> Adventure
        👊 -> Fighting
        😱 -> Horror
        🧩 -> Puzzle
        🥸 -> RPG
        🔫 -> Shooter
        🏀 -> Sports
        ♔ -> Strategy
        ⚒️ -> Survival
        '''
    )

    msg = await ctx.send(embed=embed)

    await msg.add_reaction("💥")
    await msg.add_reaction("🗺️")
    await msg.add_reaction("👊")
    await msg.add_reaction("😱")
    await msg.add_reaction("🧩")
    await msg.add_reaction("🥸")
    await msg.add_reaction('🔫')
    await msg.add_reaction("🏀")
    await msg.add_reaction("♔")
    await msg.add_reaction("⚒️")
    

#----------------------------------------------------------------

#bot.loop.create_task(delete_empty_channels())
#client = SanctumHelper(intents=intents)
bot.run("MTIyNDkyNjQ2ODY3NzgzMjcwNA.GqmTyI.7EMVqnKNB4FUZMeiwRV2e1ln85i7ul8x_7-uF0")


