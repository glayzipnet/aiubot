import discord
import os

TOKEN = os.getenv("TOKEN")

TARGET_USER_ID = 815488939191697430
CHANNEL_ID = 1562321769262616648
MENTION_ID = 724056894297210940

intents = discord.Intents.default()
intents.members = True
intents.presences = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"✅ ログイン: {client.user}")

@client.event
async def on_presence_update(before, after):
    if after.id != TARGET_USER_ID:
        return

    channel = client.get_channel(CHANNEL_ID)
    mention = f"<@{MENTION_ID}>"

    # オンライン
    if before.status == discord.Status.offline and after.status != discord.Status.offline:
        await channel.send(
            f"🟢 {mention}\nオンラインになりました"
        )

    # オフライン
    elif before.status != discord.Status.offline and after.status == discord.Status.offline:
        await channel.send(
            f"🔴 {mention}\nオフラインになりました"
        )

    # 離席中
    elif before.status != discord.Status.idle and after.status == discord.Status.idle:
        await channel.send(
            f"🟡 {mention}\n離席中になりました"
        )

    # 取り込み中
    elif before.status != discord.Status.dnd and after.status == discord.Status.dnd:
        await channel.send(
            f"⛔ {mention}\n取り込み中になりました"
        )

    # ゲーム開始判定
    before_games = {
        a.name for a in before.activities
        if hasattr(a, "name")
    }

    after_games = {
        a.name for a in after.activities
        if hasattr(a, "name")
    }

    started_games = after_games - before_games

    for game in started_games:
        await channel.send(
            f"🎮 {mention}\n『{game}』を始めました"
        )

    # ゲーム終了判定
    ended_games = before_games - after_games

    for game in ended_games:
        await channel.send(
            f"🏁 {mention}\n『{game}』を終わりました"
        )

client.run(TOKEN)