import discord
from discord.ext import commands
import asyncio
import requests
import json
import math
from io import BytesIO
import os
from urllib import request
import core1.func as func
from core1.classes import Cog_Extension
import core1.CytoidData as CytoidData
import core1.MainTask as MainTask
import core1.coin as coin
import random
from datetime import datetime, timedelta
import re
import time
debuging=False
class Hack(Cog_Extension):
    async def detectHack(self):
        g2 = self.bot.get_guild(812156057652035615)
        ch1 = g2.get_channel(1132256270540345365) 
        g1 = self.bot.get_guild(910172705863651350)
        ch2 = g1.get_channel(1132267980890329108)
        for i in range(1):
            print(".")
            message_ch2 = await MainTask.getNoCheaterMessageCount(ch2)
            message_ch1 = await MainTask.getNoCheaterMessageCount(ch1)
            print("..")
            time_stamp = int(time.time())
            now_time = f"<t:{time_stamp}:R>"
            message, embed_list = MainTask.checkHack(4)
            print("...")
            notification_member = (
                "<@671741996766986270> <@830395796490158081> <@133203646983831552>     <@599625808159571986>\n"
            )
            if debuging:
                notification_member = ""
            if message is None:
                print("1")
                if message_ch1:
                    await message_ch1.edit(content=f"No one cheated ({now_time})")
                else:
                    message_ch1 = await ch1.send(f"No one cheated ({now_time})")
                if message_ch2:
                    await message_ch2.edit(content=f"No one cheated ({now_time})")
                else:
                    message_ch2 = await ch2.send(f"No one cheated ({now_time})")
            else:
                print("2")
                await ch1.send(notification_member + message)
                await ch2.send(message)
                if embed_list is None:
                    continue 
                for embed in embed_list:
                    await ch1.send(embed=embed)
                    await ch2.send(embed=embed)
                message_ch1=None
                message_ch2=None
            print("....")
async def setup(bot):
    await bot.add_cog(Hack(bot))