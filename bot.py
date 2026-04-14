import discord
from discord.ext import commands
import os

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

# Limit per user
user_vps = {}

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

# VPS deploy command
@bot.command()
async def deploy(ctx):
    user_id = str(ctx.author.id)

    if user_id in user_vps:
        await ctx.send("❌ Tumhare paas already ek VPS hai!")
        return

    container_name = f"vps_{user_id}"

    os.system(f"docker run -dit --name {container_name} ubuntu")

    user_vps[user_id] = container_name

    await ctx.send(f"✅ VPS created!\nName: `{container_name}`")

# VPS delete
@bot.command()
async def delete(ctx):
    user_id = str(ctx.author.id)

    if user_id not in user_vps:
        await ctx.send("❌ Tumhare paas koi VPS nahi hai!")
        return

    container = user_vps[user_id]

    os.system(f"docker stop {container}")
    os.system(f"docker rm {container}")

    del user_vps[user_id]

    await ctx.send("🗑 VPS deleted!")

# VPS list (admin use)
@bot.command()
async def listvps(ctx):
    if not ctx.author.guild_permissions.administrator:
        await ctx.send("❌ Admin only")
        return

    result = os.popen("docker ps --format '{{.Names}}'").read()

    await ctx.send(f"📦 Running VPS:\n{result}")

bot.run("YOUR_BOT_TOKEN")
