import os
import random
from threading import Thread
from flask import Flask
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN")

# 特定のギルドIDを指定
GUILD_ID = 1258077953326190713  # ギルドIDを設定

intents = discord.Intents.default()
intents.message_content = True  # メッセージコンテンツインテントを有効にする

bot = commands.Bot(command_prefix="/", intents=intents)

# FlaskでUptimeRobotのPingを受け付ける
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running!"

def run():
    app.run(host="0.0.0.0", port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    await bot.change_presence(
        activity=discord.Game(name="常海電鉄")
    )
    
    # ギルドIDが一致する場合のみコマンドを同期
    guild = discord.utils.get(bot.guilds, id=GUILD_ID)
    if guild:
        try:
            synced = await bot.tree.sync(guild=guild)  # ギルド指定で同期
            print(f"🔁 Synced {len(synced)} command(s) for guild {guild.name}")
        except Exception as e:
            print(f"❌ Sync error: {e}")

# おみくじコマンド
@bot.tree.command(name="omikuzi", description="おみくじを引きます")
async def omikuzi(interaction: discord.Interaction):
    fortunes = ["大吉", "中吉", "小吉", "末吉", "凶", "大凶"]
    result = random.choice(fortunes)
    await interaction.response.send_message(f"🎴 あなたの運勢は… **{result}**！")

@bot.tree.command(name="luckycolor", description="今日のラッキーカラーを教えます")
async def luckycolor(interaction: discord.Interaction):
    colors = ["赤", "青", "黄色", "緑", "紫", "ピンク", "白", "黒"]
    color = random.choice(colors)
    await interaction.response.send_message(f"🎨 今日のラッキーカラーは **{color}** です！")

@bot.tree.command(name="tsuneumi", description="常海電鉄のロゴを送信します")
async def tsuneumi(interaction: discord.Interaction):
    embed = discord.Embed(
        title="ロゴの画像",
        description="常海のロゴだよ！",
        color=discord.Color.blue()
    )
    embed.set_image(url="https://img.atwiki.jp/rbxjptrain/attach/403/2403/%E5%90%8D%E7%A7%B0%E6%9C%AA%E8%A8%AD%E5%AE%9A%E3%81%AE%E3%83%87%E3%82%B6%E3%82%A4%E3%83%B3%20%284%29.png")

    await interaction.response.send_message(embed=embed)

keep_alive()
bot.run(TOKEN)



