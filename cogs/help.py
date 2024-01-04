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
import core1.ui as ui
import random
from datetime import datetime, timedelta
import re
import time
from cogs.coin import Coin

debuging = False


def btn(s, l, e, u, r=0, ban=False):
    return discord.ui.Button(style=s, label=l, emoji=e, url=u, row=r, disabled=ban)


def slc(p, o, min=1, max=1, ban=False):
    o = [discord.SelectOption(label=l, value=v) for l, v in o]
    return discord.ui.Select(placeholder=p, options=o, min_values=min, max_values=max, disabled=ban)


async def timeout(view, msg):
    for item in view.children:
        item.disabled = True
    await msg.edit(content=msg.content, view=view)


class Help(Cog_Extension):

    @commands.command()
    async def help(self, ctx, cate=None):
        view = discord.ui.View(timeout=10)
        btn_style = discord.ButtonStyle
        cmd = ['bind', 'ctd', 'best', 'random', 'mission', 'pvp', 'rate', 'info', 'sign', 'lottery',
               'coupon', 'guess', 'say', 'setting', 'ping', 'calc', 'png', 'c2info', 'getlink', 'suggest']
        if cate:
            cate = None if cate not in cmd else cate
        button = btn(btn_style.link, f"Open **{cate if cate else ''}** help page",
                     None, f"https://hackmd.io/@dyliu0306/dy6ot/edit?view#{cate if cate else ''}", 1)
        view.add_item(button)
        msg = await ctx.send(view=view)
        view.on_timeout = lambda: timeout(view, msg)


async def setup(bot):
    await bot.add_cog(Help(bot))
