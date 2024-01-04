# coding:utf-8
import discord
from discord.ext import commands
import asyncio
import requests
import json
import re
import random
import math
from io import BytesIO
import os
import demoji
import core1.func as func
from core1.classes import Cog_Extension
from urllib import request
import core1.CytoidData as CytoidData
import core1.MainTask as MainTask
import core1.Storyboard as sb
import core1.MostRecentPlay as MostRecentPlay
import core1.coin as coin
import core1.mail as mail
import time
import traceback
from typing import Optional
from discord.app_commands import Choice
from collections import defaultdict
from datetime import datetime, timedelta
from discord.ext.commands.errors import BadArgument
from discord.ext.commands.errors import MissingRequiredArgument
from discord.ext.commands.errors import MissingPermissions
from cogs.coin import Coin

debuging = True

i = 0
global guess_cd
guess = 0


class Ctd(Cog_Extension):
    @commands.command()
    async def bind(self, ctx, category, id):
        if ("ctd" or "cytoid") in category:
            checkA = CytoidData.checkId(id, 1)
            if "nofindctd" == checkA:
                await ctx.send(f"{func.ebt(checkA)}")
                return
            UserCtd = coin.getUserAttrib(ctx.author.id, "bind", "ctd",name=ctx.author.name)
            if UserCtd:
                await ctx.send(f"已經綁定了，你的Cytoid ID：{UserCtd} (already bound)")
                return
            elif UserCtd is False:
                coin.addUser(ctx.author.id, name=ctx.author.name, ctd=id)
                await Coin(self.bot).firstuse(ctx)
            else:
                coin.changeUserAttrib(ctx.author.id,"bind","ctd",id)
            await ctx.send("綁定成功！ (Success!)")
        else:
            await ctx.send(f"{func.ebt('mra')}\n{func.ebt('bind')}")

    @commands.command()
    async def unbind(self, ctx, category):
        if "ctd" in category:
            UserCtd = coin.getUserAttrib(ctx.author.id, "bind", "ctd")
            if not UserCtd:
                await ctx.send(f"你沒有綁定過帳號 (You havn't bound)")
            else:
                coin.changeUserAttrib(ctx.author.id, "bind", "ctd", None, "o")
                await ctx.send(f"刪除成功！ (Success!)")
        else:
            await ctx.send(f"{func.ebt('mra')}\n{func.ebt('unbind')}")

    @commands.command()
    async def info(self, ctx, levelId):
        async with ctx.typing():
            checkC = CytoidData.checkLevelID(levelId)
            if "nofindctdlevel" in checkC:
                await ctx.send(f"{func.ebt(checkC)}")
                return
            raw_data = CytoidData.getLevelData(levelId)
            embed = func.getChartInfoEmbed(raw_data)
            await ctx.send(embed=embed)

    @commands.command()
    async def rate(self, ctx, level_id):
        async with ctx.typing():
            if not CytoidData.isValidLevelId(level_id):
                await ctx.send("level id輸入錯誤 (keyword error)")
                return 0

            rating_data = CytoidData.getRateDistribution(level_id)
            level_data = CytoidData.getLevelData(level_id)
            if rating_data["total"] - 1 < 0:
                await ctx.send("譜面無人評分或id輸入不正確 (id wrong or no one rate)")
                return 0
            down, play = CytoidData.getPlay(level_id)
            title = level_data["title"]
            if (re.sub("^([^<>]*?)(?=<)|>([^<>]+)<|>([^<>]+)|", "",
                       level_data["title"]) != level_data["title"]):
                matches = re.findall(r"^([^<>]*?)(?=<)|>([^<>]+)<|>([^<>]+)|",
                                     level_data["title"])
                title = "".join("".join(match).strip() for match in matches
                                if any(match))
            func.plot_line_chart(
                rating_data["distribution"],
                level_data["owner"]["avatar"]["original"],
                title,
                down,
                play,
            )
            file = discord.File("./photo/cache1.png",
                                filename="RatingChart.png")
        await ctx.send(file=file)

    @commands.command()
    async def best(self, ctx, levelid, playerAid="me"):
        async with ctx.typing():
            checkA = CytoidData.checkCytoidID(
                playerAid, ctx.author, getID=True)
            checkC = CytoidData.checkLevelID(levelid)
            if set(("nobindctd", "nofindctd", "nofindctdlevel")) & set(
                    (checkA, checkC)):
                await ctx.send(f"{func.ebt(checkA)}{func.ebt(checkC)}")
                return
            type_ = {"E": "extreme", "H": "hard", "Z": "easy"}
            type_1 = {"E": "ex", "H": "hd", "Z": "ez"}
            difflist = CytoidData.getLevelDiff(levelid)
            if len(difflist) != 1:
                chs_diff_msg = await ctx.send("> 請選擇難度 (select diff type)")
                for d in difflist:
                    await chs_diff_msg.add_reaction(func.emo(type_1[d]))

                def check(reaction, user):
                    return (reaction.message == chs_diff_msg
                            and user == ctx.author
                            and "_dy" in str(reaction.emoji))
                type = ""
                try:
                    chs_diff, z1 = await self.bot.wait_for("reaction_add",
                                                           timeout=20,
                                                           check=check)
                    if "EZ" in str(chs_diff.emoji):
                        await chs_diff_msg.edit(
                            content="你選擇的是 **easy** (Your select is easy)")
                        type = type_["Z"]
                    elif "HD" in str(chs_diff.emoji):
                        await chs_diff_msg.edit(
                            content="你選擇的是 **hard** (Your select is hard)")
                        type = type_["H"]
                    elif "EX" in str(chs_diff.emoji):
                        await chs_diff_msg.edit(
                            content="你選擇的是 **extreme** (Your select is extreme)"
                        )
                        type = type_["E"]
                except asyncio.TimeoutError:
                    await chs_diff_msg.edit(content="超時未選擇 (Time out)")
                    return
            else:
                type = type_[difflist[0]]
            playerAid = checkA
            str1 = requests.get(
                f"https://services.cytoid.io/levels/{levelid}/charts/{type}/records?limit=20000"
            )
            user1 = json.loads(str1.content.decode("utf-8"))
            if "statusCode" in user1:
                await ctx.send("關卡讀取失敗 (Load chart failed)")
                return
            key = 0
            for i in range(len(user1)):
                if playerAid == user1[i]["owner"]["uid"]:
                    score1 = user1[i]["score"]
                    date1 = f'{func.ctdtime(user1[i]["date"])}'
                    acc1 = format(
                        int(user1[i]["accuracy"] * 100000) / 100000, ".3%")
                    perfect1 = user1[i]["details"]["perfect"]
                    great1 = user1[i]["details"]["great"]
                    good1 = user1[i]["details"]["good"]
                    bad1 = user1[i]["details"]["bad"]
                    miss1 = user1[i]["details"]["miss"]
                    avt1 = user1[i]["owner"]["avatar"]["small"]
                    rank1 = i + 1
                    leveldata = CytoidData.getLevelData(levelid)
                    embed = discord.Embed(
                        title=leveldata["title"],
                        description=f"**Score (Acc)**\n{score1}⠀⠀({acc1})\n\n**Notes Judgement**\n{perfect1}p / {great1}gr / {good1}g / {bad1}b / {miss1}m\n\n**RANK**\n#{rank1}\n\n**Date**\n{date1}",
                        color=0x27FF27,
                        url=f"https://cytoid.io/levels/{levelid}"
                    )
                    embed.set_footer(text=levelid)
                    embed.set_author(name=playerAid, icon_url=avt1)
                    await ctx.send(embed=embed)
                    return
            await ctx.send("沒有遊玩記錄 (no record)")
            return

    @commands.command()
    async def ran(self, ctx, diff="QAZWSX"):
        async with ctx.typing():
            url = "https://services.cytoid.io/search/levels?&sort=creation_date"
            page = 15
            if diff == "QAZWSX":
                diff = "&limit=24"
                page = 400
                diff_num = ""
            else:
                diff = re.sub("[^0-9]+", "", diff)
                if diff == "":
                    await ctx.send("請輸入正確的難度\nPlease enter correct difficulty")
                    return
                diff_num = int(diff)
                if int(diff_num) > 16:
                    url = "https://services.cytoid.io/search/levels?sort=difficulty&order=desc&category=all&limit=24"
                    diff = ""
                    page = 5
                elif int(diff_num) >= 13:
                    page = 20
                elif int(diff_num) >= 10:
                    page = 12
                else:
                    page = 5
                diff_num = str(diff_num)
                diff = "&difficulty=" + diff_num + "&limit=24"
            page = func.custom_randint(0, int(page))
            url += diff + "&page=" + str(page)
            if diff_num == "0":
                page = random.randint(0, 22)
                url = (
                    "https://services.cytoid.io/search/levels?sort=difficulty&order=asc&category=all&limit=24&page="
                    + str(page))
            jsonstr2 = CytoidData.getRandomChart(url, exclude_black_list=True)
            if jsonstr2:
                embed = func.getChartInfoEmbed(jsonstr2)
                await ctx.send(embed=embed)
            else:
                await ctx.send("請輸入正確的參數\nPlease type corret arg")

    @commands.command()
    async def random(self, ctx, diff="QAZWSX"):
        async with ctx.typing():
            url = "https://services.cytoid.io/search/levels?&sort=creation_date"
            page = 15
            if diff == "QAZWSX":
                diff = "&limit=24"
                page = 400
                diff_num = ""
            else:
                diff = re.sub("[^0-9]+", "", diff)
                if diff == "":
                    await ctx.send("請輸入正確的難度\nPlease enter correct difficulty")
                    return
                diff_num = int(diff)
                if int(diff_num) > 16:
                    url = "https://services.cytoid.io/search/levels?sort=difficulty&order=desc&category=all&limit=24"
                    diff = ""
                    page = 5
                elif int(diff_num) >= 13:
                    page = 20
                elif int(diff_num) >= 10:
                    page = 12
                else:
                    page = 5
                diff_num = str(diff_num)
                diff = "&difficulty=" + diff_num + "&limit=24"
            page = func.custom_randint(0, int(page))
            print(page)
            url += diff + "&page=" + str(page)
            if diff_num == "0":
                page = random.randint(0, 22)
                url = (
                    "https://services.cytoid.io/search/levels?sort=difficulty&order=asc&category=all&limit=24&page="
                    + str(page))
            jsonstr2 = CytoidData.getRandomChart(url)
            if jsonstr2:
                embed = func.getChartInfoEmbed(jsonstr2)
                await ctx.send(embed=embed)
            else:
                await ctx.send("請輸入正確的參數\nPlease type corret arg")

    @commands.command()
    async def ctd(self, ctx, playerAid="me"):
        async with ctx.typing():
            # if playerAid != "me" and ctx.guild is None:
            # return
            checkA = CytoidData.checkCytoidID(playerAid,
                                              ctx.author,
                                              getID=True)
            if checkA in ["nobindctd", "nofindctd"]:
                await ctx.send(func.ebt(checkA))
                return
            elif checkA == "norecord":
                await ctx.send("此玩家未玩過任何關卡\nThis player has no record")
                return
            loading_message = await ctx.send("Loading...")
            img_file, file_name, level_id, date_object_of_record = MainTask.generateRecentPlayPic(
                checkA)
            if not level_id:
                await ctx.send(func.ebt("norecord"))
                return
            await loading_message.delete()
            UserGmt = 8
            day_of_record = func.getCurrentDay(UserGmt, date_object_of_record)
            today = func.getCurrentDay(UserGmt)
            if int(today) == int(day_of_record) and playerAid == "me":
                if not coin.getUserCooldown().played(ctx.author.id):
                    coin.changeUserCooldown().played(ctx.author.id)
                    UserCoin, FirstUse = coin.getUserData(
                        ctx.author.id, "coin")
                    if FirstUse:
                        await Coin(self.bot).firstuse(ctx)
                    UserCoin += 500
                    UserLang = coin.getUserAttrib(
                        ctx.author.id, "setting", "lang")
                    coin.changeUserData(
                        ctx.author.id, "coin", UserCoin, 500, "played cytoid")
                    embed_text = coin.text("played", UserLang)
                    embed = discord.Embed(
                        title=embed_text[0],
                        description=f"💵 `+500`\n\n**{ctx.author.display_name}{embed_text[1]}**:  `{UserCoin}`",
                        color=0x27FF27
                    )
                    await ctx.send(embed=embed)
            embed = discord.Embed(
                title=level_id,
                color=0x27FF27,
                url=f"https://dyliu0306.github.io/run-cytoid?&levels={level_id}",
            )
            await ctx.send(embed=embed)
            await ctx.send(file=img_file)
            os.remove(file_name)
            return

    @commands.command()
    async def pvp(self, ctx, playerAid, playerBid, levelid, ch123="-1"):
        async with ctx.typing():
            if ch123 != "-1":
                return
            checkA = CytoidData.checkCytoidID(playerAid, ctx.author)
            checkB = CytoidData.checkCytoidID(playerBid, ctx.author)
            checkC = CytoidData.checkLevelID(levelid)
            if ("nobindctd" or "nofindctd"
                    or "nofindctdlevel") == (checkA or checkB or checkC):
                await ctx.send(
                    f"{func.ebt(checkA)}{func.ebt(checkB)}{func.ebt(checkC)}")
                return
            leveldata = CytoidData.getLevelData(levelid)
            difflist = CytoidData.getLevelDiff(levelid)
            diff_index = 0
            type_1 = {"E": "ex", "H": "hd", "Z": "ez"}
            if len(difflist) != 1:
                chs_diff_msg = await ctx.send("> 請選擇難度 (select diff type)")
                for d in difflist:
                    await chs_diff_msg.add_reaction(func.emo(type_1[d]))

                def check(reaction, user):
                    return (reaction.message == chs_diff_msg
                            and user == ctx.author
                            and "_dy" in str(reaction.emoji))

                try:
                    chs_diff, z1 = await self.bot.wait_for("reaction_add",
                                                           timeout=20,
                                                           check=check)
                    if "EZ" in str(chs_diff.emoji):
                        await chs_diff_msg.edit(
                            content="你選擇的是 **easy** (Your select is easy)")
                        diff_index = int(difflist.find("Z"))
                    elif "HD" in str(chs_diff.emoji):
                        await chs_diff_msg.edit(
                            content="你選擇的是 **hard** (Your select is hard)")
                        diff_index = int(difflist.find("H"))
                    elif "EX" in str(chs_diff.emoji):
                        await chs_diff_msg.edit(
                            content="你選擇的是 **extreme** (Your select is extreme)"
                        )
                        diff_index = int(difflist.find("E"))
                except asyncio.TimeoutError:
                    await chs_diff_msg.edit(content="超時未選擇 (Time out)")
                    return
            playerAid = CytoidData.checkCytoidID(playerAid,
                                                 ctx.author,
                                                 getID=True)
            playerBid = CytoidData.checkCytoidID(playerBid,
                                                 ctx.author,
                                                 getID=True)
            if CytoidData.getPvpImg(leveldata, diff_index, playerAid,
                                    playerBid, levelid):
                file = discord.File("./photo/pvp.png", filename="pvp.png")
                await ctx.send(file=file)
                return
            await ctx.send("遊玩關卡不正確 (wrong chart playing)")

    @commands.command()
    async def drop1(self, ctx, bpm, default_ticks, arg, filelink, sb1="0"):
        file = sb.getChart(filelink, int(arg), int(bpm), int(default_ticks),
                           sb1)
        await ctx.send(file=file)

    @discord.app_commands.command(
        name="drop",
        description='upload sb.json and reply this msg with "dy getlink" and paste link in filelink',
    )
    @discord.app_commands.describe(
        bpm="bpm during default_ticks",
        default_ticks="Usually is 960",
        arg="Do you use Argument(引數)?",
        filelink='upload sb.json  reply this msg with "dy getlink" to get link',
    )
    @discord.app_commands.choices(
        arg=[Choice(name="Yes", value=0),
             Choice(name="No", value=1)])
    async def drop(
        self,
        interaction: discord.Interaction,
        bpm: float,
        default_ticks: int,
        arg: Choice[int],
        filelink: str,
    ):
        try:
            file = sb.getChart(filelink, arg.value, bpm, default_ticks)
            await interaction.response.send_message(file=file)
        except:
            await interaction.response.send_message(
                "File loads Failed\n請上傳含有 `chartBackup` 項的Storyboard檔")


async def setup(bot):
    await bot.add_cog(Ctd(bot))
