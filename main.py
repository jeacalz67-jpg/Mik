import discord
from discord.ext import commands
import sqlite3

# ================= DATABASE =================
conn = sqlite3.connect("bot.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS warnings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    guild_id TEXT,
    user_id TEXT,
    moderator_id TEXT,
    reason TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")
conn.commit()

# ================= BOT =================
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=["!", "."], intents=intents)

# ================= IDS =================
GENDER_ID = 1486370771638030357
PRONOUN_ID = 1486370774414655488
AGE_ID = 1486370776247701553
GAME_ID = 1486370778130809002
CONTINENT_ID = 1486370780341342209
PING_ID = 1486370783025565841

FEMALE_ID = 1486349082778800178
MALE_ID = 1486349133219368991
NB_ID = 1486349376086606025

SHE_ID = 1486349711987445860
HE_ID = 1486349771571593377
THEY_ID = 1486349819327811594

AGE1_ID = 1486350014597824685
AGE2_ID = 1486350058491482235
AGE3_ID = 1486350098853007391

GENSHIN_ID = 1486350269272035399
MLBB_ID = 1486350320799056003
HSR_ID = 1486350359784849518
MINECRAFT_ID = 1486350672541519983
ROBLOX_ID = 1486350403476914399
VALO_ID = 1486350463707254795

ASIA_ID = 1486362791613960293
EUROPE_ID = 1486362839802449961
NA_ID = 1486362905829052577
SA_ID = 1486363026775998605
AFRICA_ID = 1486363218870931507
OCEANIA_ID = 1486363311435022436
ANTARCTICA_ID = 1486363672526848070

CHAT_ID = 1486350776111730720
ANNOUNCE_ID = 1486350723049324584
GIVE_ID = 1486350832315273290

# ================= HELPERS =================
async def set_one_role(guild, member, role_ids, new_role_id):
    for rid in role_ids:
        role = guild.get_role(rid)
        if role and role in member.roles:
            await member.remove_roles(role)

    role = guild.get_role(new_role_id)
    if role:
        await member.add_roles(role)

# ================= EVENTS =================
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.event
async def on_raw_reaction_add(payload):
    if payload.user_id == bot.user.id:
        return

    guild = bot.get_guild(payload.guild_id)
    if not guild:
        return

    member = guild.get_member(payload.user_id)
    if not member:
        return

    emoji = str(payload.emoji)
    msg = payload.message_id

    # GENDER
    if msg == GENDER_ID:
        if emoji == "🌸":
            await set_one_role(guild, member, [FEMALE_ID, MALE_ID, NB_ID], FEMALE_ID)
        elif emoji == "💙":
            await set_one_role(guild, member, [FEMALE_ID, MALE_ID, NB_ID], MALE_ID)
        elif emoji == "🤍":
            await set_one_role(guild, member, [FEMALE_ID, MALE_ID, NB_ID], NB_ID)

    # PRONOUNS
    elif msg == PRONOUN_ID:
        if emoji == "🌸":
            await set_one_role(guild, member, [SHE_ID, HE_ID, THEY_ID], SHE_ID)
        elif emoji == "🌿":
            await set_one_role(guild, member, [SHE_ID, HE_ID, THEY_ID], HE_ID)
        elif emoji == "✨":
            await set_one_role(guild, member, [SHE_ID, HE_ID, THEY_ID], THEY_ID)

    # AGE
    elif msg == AGE_ID:
        if emoji == "🧁":
            await set_one_role(guild, member, [AGE1_ID, AGE2_ID, AGE3_ID], AGE1_ID)
        elif emoji == "🍰":
            await set_one_role(guild, member, [AGE1_ID, AGE2_ID, AGE3_ID], AGE2_ID)
        elif emoji == "🎂":
            await set_one_role(guild, member, [AGE1_ID, AGE2_ID, AGE3_ID], AGE3_ID)

    # CONTINENT
    elif msg == CONTINENT_ID:
        all_roles = [ASIA_ID, EUROPE_ID, NA_ID, SA_ID, AFRICA_ID, OCEANIA_ID, ANTARCTICA_ID]

        if emoji == "🌏":
            await set_one_role(guild, member, all_roles, ASIA_ID)
        elif emoji == "🌍":
            await set_one_role(guild, member, all_roles, EUROPE_ID)
        elif emoji == "🌎":
            await set_one_role(guild, member, all_roles, NA_ID)
        elif emoji == "🌴":
            await set_one_role(guild, member, all_roles, SA_ID)
        elif emoji == "🌊":
            await set_one_role(guild, member, all_roles, OCEANIA_ID)
        elif emoji == "❄️":
            await set_one_role(guild, member, all_roles, ANTARCTICA_ID)

    # GAMES
    elif msg == GAME_ID:
        game_map = {
            "🌸": GENSHIN_ID,
            "🔥": MLBB_ID,
            "✨": HSR_ID,
            "⛏": MINECRAFT_ID,
            "🎮": ROBLOX_ID,
            "🔫": VALO_ID
        }
        role_id = game_map.get(emoji)
        if role_id:
            role = guild.get_role(role_id)
            if role:
                await member.add_roles(role)

    # PINGS
    elif msg == PING_ID:
        ping_map = {
            "💬": CHAT_ID,
            "📢": ANNOUNCE_ID,
            "🎁": GIVE_ID
        }
        role_id = ping_map.get(emoji)
        if role_id:
            role = guild.get_role(role_id)
            if role:
                await member.add_roles(role)

# ================= COMMANDS =================
@bot.command()
async def test(ctx):
    await ctx.send("IT WORKS 💖")

# ================= RUN =================
import os

token = os.getenv("TOKEN")
bot.run(token)
