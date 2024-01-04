import os
import asyncio
import discord
from discord.ext import commands
import keep_alive
import pytz
import time
import core1.func as func
import core1.MainTask as MainTask
import core1.coin as coin
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime
from cogs.coin import Coin
from cogs.hack import Hack

debuging = False
# debuging = True


intents = discord.Intents.all()
bot = commands.Bot(command_prefix=["dy ", "Dy "],
                   intents=intents, help_command=None)

async def ltrmsg():
    await Coin(bot).sendlotterymsg()
    coin.changeUserCooldown().lottery()

async def job1():
    await Hack(bot).detectHack()

# 當機器人完成啟動時
@bot.event
async def on_ready():
    slash = await bot.tree.sync()
    print(f"目前登入身份 --> {bot.user}")
    print(f"載入 {len(slash)} 個斜線指令")
    activity = discord.Game(name="dy help")
    await bot.change_presence(activity=activity)
    func.reset_cd("guess")
    if coin.getUserCooldown().lottery():
        await Coin(bot).sendlotterymsg()
        coin.changeUserCooldown().lottery()
    await Hack(bot).detectHack()
    scheduler = AsyncIOScheduler(timezone="Asia/Taipei")
    scheduler.add_job(ltrmsg, 'cron', day_of_week='0-6', hour=0, minute=0, second=0)
    scheduler.add_job(job1, 'interval', minutes=15)
    scheduler.start()
    # 若半夜斷線，重起就補執行


# 載入指令程式檔案
@bot.command()
async def load(ctx, extension):
    await bot.load_extension(f"cogs.{extension}")
    await ctx.send(f"Loaded {extension} done.")


# 卸載指令檔案


@bot.command()
async def unload(ctx, extension):
    await bot.unload_extension(f"cogs.{extension}")
    await ctx.send(f"UnLoaded {extension} done.")


# 重新載入程式檔案


@bot.command()
async def reload(ctx, extension):
    await bot.reload_extension(f"cogs.{extension}")
    await ctx.send(f"ReLoaded {extension} done.")


# 一開始bot開機需載入全部程式檔案


async def load_extensions():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")


async def main():
    async with bot:
        await load_extensions()
        await bot.start(os.getenv("DISCORD_TOKEN"))


keep_alive.keep_alive()
if __name__ == "__main__":
    asyncio.run(main())
