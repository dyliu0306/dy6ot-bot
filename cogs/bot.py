# coding:utf-8
import discord
from discord.ext import commands
import asyncio
import requests
import json
import re
import random
import math
from PIL import Image, ImageEnhance, ImageFont, ImageDraw, ImageOps, ImageFilter
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
from opencc import OpenCC

debuging = True

i = 0
global guess_cd
guess = 0


def btn(s, l, e, u, r=0, ban=False):
    return discord.ui.Button(style=s, label=l, emoji=e, url=u, row=r, disabled=ban)


def slc(p, o, min=1, max=1, ban=False):
    o = [discord.SelectOption(label=l, value=v) for l, v in o]
    return discord.ui.Select(placeholder=p, options=o, min_values=min, max_values=max, disabled=ban)


async def timeout(view, msg):
    for item in view.children:
        item.disabled = True
    await msg.edit(content=msg.content, view=view)


async def handle_error(interaction, error, item, ctx):
    cmd = ctx.invoked_with
    full_error = traceback.format_exception(error)  # type: ignore
    with open("./text/full_error.txt", "w") as f:
        text = ""
        for i in range(len(full_error)):
            text += full_error[i]
        f.write(text)
    f.close()
    file = discord.File("./text/full_error.txt",
                        filename="full_error.txt")
    text = f"> **ERROR ID**:`{int(time.time())}`\n```Unknown Error at [{cmd}]:\n {error}```"
    await ctx.send(text, file=file)


class Main(Cog_Extension):

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        func.del_cd("guess", ctx.channel.id)
        cmd = ctx.invoked_with
        full_error = traceback.format_exception(error)  # type: ignore
        if isinstance(error, commands.CommandNotFound):
            pass
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(
                f"**請輸入正確的參數 (Please type in all require args.**)\n{func.ebt(cmd)}"
            )
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send(
                "**You dont have the permissions for using this command**")
        else:
            with open("./text/full_error.txt", "w") as f:
                text = ""
                for i in range(len(full_error)):
                    text += full_error[i]
                f.write(text)
            f.close()
            file = discord.File("./text/full_error.txt",
                                filename="full_error.txt")
            text = f"> **ERROR ID**:`{int(time.time())}`\n```Unknown Error at [{cmd}]:\n {error}```"
            await ctx.send(text, file=file)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        global helpemo1
        global helpemo2
        global helpemo3
        if payload.guild_id is None:
            return  # Reaction is on a private message
        channel = self.bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        user = self.bot.get_user(payload.user_id)
        if str(payload.emoji) == "\U0001F621":
            await message.add_reaction("<:angry:1104806970785018039>")
        if str(payload.emoji) == "♣️" and user.id == 830395796490158081:
            if str(user) == "dy6ot":
                return
            detect_name = "dyliu"
            detect_id = "<@830395796490158081>"
            detect_server = "Cytus系中文自製譜師交流區"
            if str(message.channel.guild.name) == detect_server and str(
                    user.display_name) == detect_name:
                await message.channel.send("...@^...為.^.什..&.麼.*....")
                await asyncio.sleep(1)
                await message.channel.send("...!@?不要.離..@.救#%...我..")
                await asyncio.sleep(5)
                await message.channel.send("..I...]>..I...v..")
                await asyncio.sleep(1)
                await message.channel.send("..y.vvy..........y...")
                await asyncio.sleep(1)
                await message.channel.send("....yy...I.vy.")
                await asyncio.sleep(5)
                await message.channel.send("..^$%檢Iv測到$..%#入y侵$...^")
                await asyncio.sleep(5)
                await message.channel.send("Hc?試自#$動排vy除...$..%#敵I$.人..^")
                await asyncio.sleep(5)
                await message.add_reaction("⬅")
                await asyncio.sleep(1)
                await message.add_reaction("<:laughyou:944857747864817724>")
                await message.channel.send("<:laughyou:944857747864817724>")
                await asyncio.sleep(3)
                await message.channel.send("注意！注意！")
                await asyncio.sleep(1)
                await message.channel.send("注意！注意！")
                await asyncio.sleep(1)
                await message.channel.send("大家注意！")
                await asyncio.sleep(3)
                await message.channel.send(detect_id)
                await asyncio.sleep(3)
                await message.channel.send("想靠著dy6ot偷偷留著的後門把訊息刪掉！！")
                await asyncio.sleep(3)
                await message.channel.send("身為正義化身的我阻止了他邪惡的行為！！！！")
            else:
                tx = str(message.created_at)
                tx = re.sub("\\.[^\0]+", "", tx)
                func.del_txt(str(message.author.display_name), message.content,
                             tx)
                await message.delete()
        if str(payload.emoji) == "\U0001F6D0":
            await message.add_reaction("<:lao1:1102149331101954058>")
            await message.add_reaction("<:lao2:1102149279746891786>")
            await message.add_reaction("<:dalaoooo:1070885764608573532>")
        if (str(payload.emoji) == func.emo("bpm")
                and str(message.author) == "dy6ot#9006"
                and "Estimated" in message.content
                and str(payload.member) != "dy6ot#9006"):
            try:
                nid = re.findall("No.[0-9]+(?=`)", message.content)
                func.get_bpm(nid[0])
                file = discord.File("./bpm_cache.txt",
                                    filename="beat_frame list.txt")
                await message.channel.send(file=file)
            except:
                await message.channel.send("Unknow Wrong")
                return
        if str(payload.emoji) == "\U000026D4":
            for r in message.reactions:
                async for user in r.users():
                    if user.bot == True:
                        await message.remove_reaction(r.emoji, user)
            await message.remove_reaction("\U000026D4", user)

    @commands.Cog.listener()
    async def on_message(self, message):
        if not func.get_cd("guess", message.channel.id, False):
            return
        elif ("```Unknown Error at" in message.content
              and str(message.author) == "dy6ot#9006"
              and message.channel.id != 1162804715990548640):
            file = discord.File("./text/full_error.txt",
                                filename="full_error.txt")
            g1 = self.bot.get_guild(1133038534702407790)
            ch123 = g1.get_channel(1162804715990548640)
            msg = await MainTask.getErrorMessage(message.channel)
            await ch123.send(
                f"> **Server**: `{message.channel.guild.name}`\n> **Command**:`{msg}`\n{message.content}",
                file=file,
            )
            return
        elif str(message.author) == "dy6ot#9006":
            return
        global helpemo1
        global helpemo2
        global helpemo3
        global ramlimit
        global wait
        if str(message.author) == "Nadeko#6685":
            if len(message.mentions) > 0:
                output_message = MainTask.replaceNadekoMention(message)
                await message.delete()
                await message.channel.send(output_message)
            return
        if message.content.startswith("dy"):
            # 分割訊息成兩份
            tmp = re.findall("[^ ]+", message.content)
            # 如果分割後串列長度只有1
            if len(tmp) == 1:
                return
            elif len(tmp) == 3:
                if tmp[1].startswith("test"):
                    if not CytoidData.isValidLevelId(tmp[2]):
                        await message.channel.send(
                            "level id輸入錯誤 (keyword error)")
                        return 0

                    rating_data = CytoidData.getRateDistribution(tmp[2])
                    level_data = CytoidData.getLevelData(tmp[2])
                    if rating_data["total"] - 1 < 0:
                        await message.channel.send(
                            "譜面無人評分或id輸入不正確 (id wrong or no one rate)")
                        return 0
                    tmg = await message.channel.send("Search...")
                    await asyncio.sleep(3)
                    await tmg.delete()
                    func.plot_line_chart2(
                        rating_data["distribution"],
                        level_data["owner"]["avatar"]["original"],
                        level_data["title"],
                        level_data["owner"]["uid"],
                    )
                    file = discord.File("photo/cache1.png",
                                        filename="RatingChart.png")
                    await message.channel.send(file=file)
            elif len(tmp) == 6:
                if tmp[1].startswith("pvp"):
                    x1 = 1
                    x3 = 1
                    # code copyright belongs to akari-bot[github.com/Teahouse-Studios/akari-bot/blob/master/modules/cytoid/rating.py]
                    check1 = requests.get(
                        f"https://services.cytoid.io/profile/{tmp[2]}")
                    check1a = json.loads(check1.content.decode("utf-8"))
                    if "me" == tmp[2] or re.match(r"<[@!]+[0-9]+>", tmp[2]):
                        # tmp[2] = func.ment(message.author, tmp[2], message.author.guild)
                        tmp[2] = func.mentionReplacement(message.author,
                                                         tmp[2],
                                                         isId=True)
                        tmp[2] = func.get_id(tmp[2])
                        if "e404" in tmp[2]:
                            await message.channel.send(
                                "無註冊資料，使用`bind ctd <cytoid id>`綁定帳號 (You have not bound yet)"
                            )
                            x1 = 0
                    elif "statusCode" in check1a:
                        if check1a["statusCode"] == 404:
                            x1 = 0
                            await message.channel.send("玩家一Cytoid ID未正確輸入")
                    check2 = requests.get(
                        f"https://services.cytoid.io/profile/{tmp[3]}")
                    check2a = json.loads(check2.content.decode("utf-8"))
                    if "me" == tmp[3] or re.match(r"<[@!]+[0-9]+>", tmp[3]):
                        # tmp[3] = func.ment(message.author, tmp[3], message.author.guild)
                        tmp[3] = func.mentionReplacement(message.author,
                                                         tmp[3],
                                                         isId=True)
                        tmp[3] = func.get_id(tmp[3])
                        if "e404" in tmp[3]:
                            await message.channel.send(
                                "無註冊資料，使用`bind ctd <cytoid id>`綁定帳號 (You have not bound yet)"
                            )
                            x1 = 0
                    elif "statusCode" in check2a:
                        if check2a["statusCode"] == 404:
                            x1 = 0
                            await message.channel.send("玩家二Cytoid ID未正確輸入")
                    check3 = requests.get(
                        f"https://services.cytoid.io/profile/{tmp[4]}")
                    check3a = json.loads(check3.content.decode("utf-8"))
                    if "me" == tmp[4] or re.match(r"<[@!]+[0-9]+>", tmp[4]):
                        # tmp[4] = func.ment(message.author, tmp[4], message.author.guild)
                        tmp[4] = func.mentionReplacement(message.author,
                                                         tmp[4],
                                                         isId=True)
                        tmp[4] = func.get_id(tmp[4])
                        if "e404" in tmp[4]:
                            await message.channel.send(
                                "無註冊資料，使用`bind ctd <cytoid id>`綁定帳號 (You have not bound yet)"
                            )
                            x1 = 0
                    elif "statusCode" in check3a:
                        if check3a["statusCode"] == 404:
                            x1 = 0
                            await message.channel.send("玩家三Cytoid ID未正確輸入")

                    # end
                    if x1 == 1:
                        check1 = requests.get(
                            f"https://services.cytoid.io/profile/{tmp[2]}")
                        check1a = json.loads(check1.content.decode("utf-8"))
                        check2 = requests.get(
                            f"https://services.cytoid.io/profile/{tmp[3]}")
                        check2a = json.loads(check2.content.decode("utf-8"))
                        check3 = requests.get(
                            f"https://services.cytoid.io/profile/{tmp[4]}")
                        check3a = json.loads(check2.content.decode("utf-8"))
                        x2 = 1
                        url = "https://services.cytoid.io/levels/" + tmp[5]
                        res = requests.get(url)
                        jsonstr = json.loads(res.content.decode("utf-8"))
                        type = ""
                        if jsonstr["duration"] >= 240:
                            await message.channel.send(
                                f'譜面時長超出上限 ({jsonstr["duration"]}秒)')
                            x3 = 0
                        if x3 >= 1:
                            length = (jsonstr["duration"]) + 32
                            if len(jsonstr["charts"]) > 2:
                                if (jsonstr["charts"][0]["difficulty"] ==
                                        jsonstr["charts"][1]["difficulty"] ==
                                        jsonstr["charts"][2]["difficulty"]):
                                    type = "extreme"
                                elif (jsonstr["charts"][0]["difficulty"] !=
                                      jsonstr["charts"][1]["difficulty"] !=
                                      jsonstr["charts"][2]["difficulty"]):
                                    for i in range(3):
                                        if (max(
                                                jsonstr["charts"][0]
                                            ["difficulty"],
                                                jsonstr["charts"][1]
                                                    ["difficulty"],
                                                jsonstr["charts"][2]
                                                ["difficulty"],
                                        ) == jsonstr["charts"][i]["difficulty"]
                                            ):
                                            type = jsonstr["charts"][i]["type"]
                                            break
                                else:
                                    for i in range(3):
                                        if (max(
                                                jsonstr["charts"][0]
                                            ["difficulty"],
                                                jsonstr["charts"][1]
                                                    ["difficulty"],
                                                jsonstr["charts"][2]
                                                ["difficulty"],
                                        ) == jsonstr["charts"][i]["difficulty"]
                                            ):
                                            type = jsonstr["charts"][i]["type"]
                                            break
                            elif len(jsonstr["charts"]) > 1:
                                if (jsonstr["charts"][0]["difficulty"] ==
                                        jsonstr["charts"][1]["difficulty"]):
                                    for i in range(2):
                                        if max(
                                                ord(jsonstr["charts"][0]
                                                    ["type"][2]),
                                                ord(jsonstr["charts"][1]
                                                    ["type"][2]),
                                        ) == ord(jsonstr["charts"][i]["type"]
                                                 [2]):
                                            type = jsonstr["charts"][i]["type"]
                                            break
                                elif (jsonstr["charts"][0]["difficulty"] !=
                                      jsonstr["charts"][1]["difficulty"]):
                                    for i in range(2):
                                        if (max(
                                                jsonstr["charts"][0]
                                            ["difficulty"],
                                                jsonstr["charts"][1]
                                                    ["difficulty"],
                                        ) == jsonstr["charts"][i]["difficulty"]
                                            ):
                                            type = jsonstr["charts"][i]["type"]
                                            break
                            else:
                                type = jsonstr["charts"][0]["type"]
                            await message.channel.send(f"請三方遊玩{type}難度")
                            user1 = CytoidData.getUserMostRecentPlay(tmp[2])
                            user2 = CytoidData.getUserMostRecentPlay(tmp[3])
                            user3 = CytoidData.getUserMostRecentPlay(tmp[4])
                            score1 = user1["score"]
                            score2 = user2["score"]
                            score3 = user3["score"]
                            acc1 = user1["accuracy"]
                            acc2 = user2["accuracy"]
                            acc3 = user3["accuracy"]
                            perfect1 = user1["details"]["perfect"]
                            great1 = user1["details"]["great"]
                            good1 = user1["details"]["good"]
                            bad1 = user1["details"]["bad"]
                            miss1 = user1["details"]["miss"]
                            perfect3 = user3["details"]["perfect"]
                            great3 = user3["details"]["great"]
                            good3 = user3["details"]["good"]
                            bad3 = user3["details"]["bad"]
                            miss3 = user3["details"]["miss"]
                            perfect2 = user2["details"]["perfect"]
                            great2 = user2["details"]["great"]
                            good2 = user2["details"]["good"]
                            bad2 = user2["details"]["bad"]
                            miss2 = user2["details"]["miss"]
                            notes1 = user1["chart"]["notesCount"]
                            notes2 = user2["chart"]["notesCount"]
                            notes3 = user3["chart"]["notesCount"]
                            num1a = 0
                            if miss1 > 0:
                                num1a = 1 / math.sqrt(miss1 / 2)
                            num2a = 0
                            if miss2 > 0:
                                num2a = 1 / math.sqrt(miss2 / 2)
                            num3a = 0
                            if miss3 > 0:
                                num3a = 1 / math.sqrt(miss3 / 2)
                            num1b = 0
                            if great1 > 0:
                                num1b = ((notes1 * acc1) - perfect1 -
                                         (good1 * 0.3)) / great1
                            num2b = 0
                            if great2 > 0:
                                num2b = ((notes2 * acc2) - perfect2 -
                                         (good2 * 0.3)) / great2
                            num3b = 0
                            if great3 > 0:
                                num3b = ((notes3 * acc3) - perfect3 -
                                         (good3 * 0.3)) / great3
                            total1 = (
                                (((miss1**2) * (num1a)) /
                                 (math.log(notes1, 50)**3) + 0.6 * miss1) *
                                (-1) + (bad1 * (-0.6)) + (good1 * (-0.1)) +
                                (num1b - 0.2) + (perfect1 * 0.8))
                            total2 = (
                                (((miss2**2) * (num2a)) /
                                 (math.log(notes2, 50)**3) + 0.6 * miss2) *
                                (-1) + (bad2 * (-0.6)) + (good2 * (-0.1)) +
                                (num2b - 0.2) + (perfect2 * 0.8))
                            total3 = (
                                (((miss3**2) * (num3a)) /
                                 (math.log(notes3, 50)**3) + 0.6 * miss3) *
                                (-1) + (bad3 * (-0.6)) + (good3 * (-0.1)) +
                                (num3b - 0.2) + (perfect3 * 0.8))

                            await message.channel.send(
                                f".....................\n{tmp[2]}的加權總分是：{format(total1,'.3f')}\n分數：{score1}   acc：{format(acc1*100,'.3f')}%\n{perfect1}P | {great1}Gr | {good1}G | {bad1}B | {miss1}M\n.....................\n{tmp[3]}的加權總分是：{format(total2,'.3f')}\n分數：{score2}   acc：{format(acc2 *100,'.3f')}%\n{perfect2}P | {great2}Gr | {good2}G | {bad2}B | {miss2}M\n.....................\n{tmp[4]}的加權總分是：{format(total3,'.3f')}\n分數：{score3}   acc：{format(acc3*100,'.3f')}%\n{perfect3}P | {great3}Gr | {good3}G | {bad3}B | {miss3}M\n"
                            )

    @commands.Cog.listener()
    async def on_message_edit(self, before, message):
        if (str(before.author) == "豆腐貓咪#1702"
                and "請找出" in message.embeds[0].description
                and "xiaoke" in str(before.author.guild)):
            emo1 = re.findall(r"<[^\0]+>", message.embeds[0].description)
            await message.add_reaction(str(emo1[0]))

    @commands.command()
    async def month(self, ctx, rate, count):
        rate, count = float(rate), int(count)
        await ctx.send(f"分數: {(rate*count*2+60)/(count+10)}")

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f"延遲: {round(self.bot.latency * 1000)}ms")

    @commands.command()
    async def png(self, ctx):
        if len(ctx.message.attachments) >= 1:
            link = ctx.message.attachments[0].url
            fname = ctx.message.attachments[0].filename
            try:
                fname = fname.split(".")[0]
                path = requests.get(link)
                img = Image.open(BytesIO(path.content)).convert("RGBA")
                img.save(f"photo/cache.png", format='PNG')
                print(fname)
                file = discord.File("photo/cache.png", filename=f"{fname}.png")
                await ctx.reply(file=file)
            except:
                await ctx.reply("Can't open this file.\nCheck the file format or filename.")
                return
        else:
            await ctx.reply("No file found.")

    @commands.command()
    async def guess(self, ctx, song_category="-1"):
        global guess_cd
        guess_cd = 1
        song_cates = func.get_song_len() - 1
        if ctx.guild.id is None:
            await ctx.send("無法在此使用此指令")
            return
        id = func.get_guess_cate(song_category, song_cates)
        if func.get_cd("guess", ctx.channel.id):
            tip = "> **你選擇的出題範圍是：|"
            tips = ["arc", "c2", "mai", "中二", "phi", "bof", "盤子", "ALL"]
            for o in range(len(id)):
                j = id[o]
                tip += f" {tips[j]} |"
            tip += "**\n> 輸入`stop`可中止遊戲\n> 輸入`猜 / $<序號> <猜測的答案>`來搶答 \n($4 MAXRAGE)\n\n選擇題庫指令：`dy guess <要選擇的題庫代碼>`        \nEX:`dy guess 0134`\n0️⃣     Arcaea\n1️⃣     CYTUS II\n2️⃣     maimai\n3️⃣     CHUNITHM\n4️⃣     Phigros\n5️⃣     BOF\n6️⃣     Lanota"
            await ctx.send(tip)
            await asyncio.sleep(2)
            await ctx.send(
                "==============\n\n>>> **為避免超載，機器人接收CD為五秒，小心別被搶答囉！**")
            await asyncio.sleep(2)
            song_list = func.get_song(id)  # id=出題範圍(-1=全題庫)
            time_stamp = int(time.time()) + 56
            now_time = f"<t:{time_stamp}:R>"
            text = f"=======================\n> **Timer:** {now_time}\n\n```"
            final_ans = "```"
            guess_key = " "  # 正則查詢
            guess_time = 0
            figure_ans = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]  # 被找出的答案會刪掉
            for i in range(10):
                x1 = (i + 1) % 10
                x2 = int((i + 1 - x1) / 10)
                x3 = i
                white_list = re.sub("[^ ]", "ˍ", song_list[x3])
                text += f"\n{x2}{x1}. {white_list}"
                final_ans += f"\n{x2}{x1}. {song_list[i]}"
            text += "```"
            final_ans += "```"
            await ctx.send(text)

            def check(m):
                return m.channel == ctx.channel and ctx.author != self.bot.user

            while len(figure_ans) >= 1:
                try:
                    msg = await self.bot.wait_for("message",
                                                  timeout=60,
                                                  check=check)
                    if (len(msg.content) == 1
                            and msg.content.lower() not in guess_key
                            and not re.match("[\\\/\\-\\]]", msg.content)):
                        guess_time += 1
                        guess_key += msg.content.lower()
                        text = func.guess_word(guess_time, guess_key,
                                               song_list, figure_ans)
                        await ctx.send(text)
                        await asyncio.sleep(5)
                    elif re.match("[猜\\$][0-9.]+ ", msg.content):
                        if True:
                            fid = re.findall("[0-9]+(?=[. ])", msg.content)
                            if len(fid) >= 1:
                                print(ctx.guild.name[:8], ctx.channel.name,
                                      f"猜{fid[0]}")
                                text = func.guess_ans(fid, msg, song_list,
                                                      figure_ans, guess_time)
                                await ctx.send(text)
                                await asyncio.sleep(5)
                        else:
                            pass
                    elif (len(msg.content) == 1
                          and str(msg.content).lower() in guess_key):
                        cd_time = int(time.time()) + 5
                        cd_time = f"<t:{cd_time}:R>"
                        await ctx.send(
                            f"> **CD:** {cd_time}\n\n猜測字重複 (Repeated Key)")
                        await asyncio.sleep(5)
                    elif (msg.author == ctx.author and "stop" == str(msg.content).lower()
                          or msg.author.guild_permissions.administrator == True
                          and "stop"
                          == msg.content) and msg.author != self.bot.user:
                        guess_cd = 0
                        print(ctx.guild.name[:8], ctx.channel.name, "STOP")
                        text1 = "> **遊戲被強制中止**\n```"
                        for i in range(10):
                            x1 = (i + 1) % 10
                            x2 = int((i + 1 - x1) / 10)
                            x3 = i
                            text1 += f"\n{x2}{x1}. {song_list[i]}"
                        text1 += "```"
                        await ctx.send(text1)
                        func.del_cd("guess", ctx.channel.id)
                        return
                    elif re.match("[\\\/\\-\\]]", msg.content):
                        cd_time = int(time.time()) + 5
                        cd_time = f"<t:{cd_time}:R>"
                        await ctx.send(
                            f"> **CD:** {cd_time}\n\n無法猜測下列字詞：-   \\   /   ]")
                        await asyncio.sleep(5)
                except asyncio.TimeoutError:
                    guess_cd = 0
                    text1 = "> **超時未輸入 (Time out)**\n\n```"
                    for i in range(10):
                        x1 = (i + 1) % 10
                        x2 = int((i + 1 - x1) / 10)
                        x3 = i
                        text1 += f"\n{x2}{x1}. {song_list[i]}"
                    text1 += "```"
                    await ctx.send(text1)
                    func.del_cd("guess", ctx.channel.id)
                    return
            if len(figure_ans) == 0:
                guess_cd = 0
                text1 = "> **答案已全被找出！**\n```"
                for i in range(10):
                    x1 = (i + 1) % 10
                    x2 = int((i + 1 - x1) / 10)
                    x3 = i
                    text1 += f"\n{x2}{x1}. {song_list[i]}"
                text1 += "```"
                await ctx.send(text1)
            func.del_cd("guess", ctx.channel.id)
        else:
            await ctx.send("正在冷卻中 (Cooldown)")

    @commands.command()
    async def calc(self, ctx, category, diff, value):
        if "mai" in category:
            value = float(value)
            diff = float(diff)
            rank = [100.5, 100, 99.5, 99, 98, 97, 94, 90, 80]
            mag = [22.4, 21.6, 21.1, 20.8, 20.3, 20, 16.8, 15.2, 13.6, 13.6]
            mag_inr = [
                22.624,
                22.512,
                21.708,
                21.6,
                21.1,
                20.995,
                20.696,
                20.592,
                20.097,
                19.894,
                19.6,
                19.4,
                16.296,
                15.792,
                14.288,
                13.68,
                12.24,
                10.88,
            ]
            if value <= 101 and value >= 0:
                rank.append(value)
                rank.sort(reverse=True)
                index = int(rank.index(value))
                Rpt = diff * mag[index] * value / 100
                await ctx.send(
                    f'定數`{diff}`打到`{format(value,".4f")}%`的R值是`{format(Rpt,".1f")}`'
                )
            elif value > 101:
                value = value / diff
                mag_inr.append(value)
                mag_inr.sort(reverse=True)
                index = int(mag_inr.index(value))
                if index == 0:
                    await ctx.send(
                        f'定數`{diff}`的理論R值是`{format(diff*22.624,".1f")}`')
                    return
                elif (index + 1) == len(mag_inr):
                    index = math.floor(index / 2)
                    result = value / (mag[index] / 100)
                    await ctx.send(
                        f'定數`{diff}`要取得`{format(value*diff,".1f")}`R值必須達到`{format(result,".4f")}`%'
                    )
                elif index % 2 == 0:
                    index = int(index / 2) - 1
                    await ctx.send(
                        f'定數`{diff}`要取得`{format(value*diff,".1f")}`R值必須達到`{rank[index]}`% \n(實得R值：`{format (diff*rank[index]*mag[index]/100,".1f")}`)'
                    )
                else:
                    index = math.floor(index / 2)
                    result = value / (mag[index] / 100)
                    await ctx.send(
                        f'定數`{diff}`要取得`{format(value*diff,".1f")}`R值必須達到`{format(result,".4f")}`%'
                    )
        elif ("chu" or "中二") in category:
            diff = float(diff)
            value = float(value)
            if value >= 1010000:
                await ctx.send(f"哇！<@{ctx.author.id}>突破理論值，海放眾人！")
            elif value >= 1009000:
                Rpt = value + 2.15
                await ctx.send(f"定數`{diff}`打到`{value}`的R值是`{Rpt}`")
            elif value >= 900000:
                mag = [2, 1.5, 1, 0.6, 0, -3, -5]
                mag_inr = [100, 50, 100, 250, 250, 166.666666666666, 125]
                rank = [
                    1007499.0, 1004999, 999999, 989999, 974999, 924999, 899999
                ]
                rank.append(value)
                rank.sort(reverse=True)
                index = int(rank.index(value))
                i2 = index + 1
                Rpt = (diff + mag[index] + int(
                    (value - rank[i2]) / mag_inr[index]) * 0.01)
                await ctx.send(f"定數`{diff}`打到`{int(value)}`的R值是`{Rpt:.2f}`")
            elif value >= 800000:
                mag = (diff - 5) / 2
                Rpt = mag + ((diff - 5) - mag) * (value - 800000) / 100000
                await ctx.send(f"定數`{diff}`打到`{int(value)}`的R值是`{Rpt:.2f}`")
            elif value >= 500000:
                mag = (diff - 5) / 2
                Rpt = mag * (value / 500000)
                await ctx.send(f"定數`{diff}`打到`{int(value)}`的R值是`{Rpt:.2f}`")
            elif value >= 100:
                await ctx.send(f"定數`{diff}`打到`{int(value)}`的R值是`0`")
            elif (value - diff) > 2.15:
                Rpt = diff + 2.15
                await ctx.send(f"定數`{diff}`的理論R值是`{Rpt}`")
            elif value < 0:
                await ctx.send("把機台拆了就能得到負分囉")
            elif (diff - value) <= 5:
                mag = [2, 1.5, 1, 0.6, 0, -3, -5]
                mag_inr = [100, 50, 100, 250, 250, 166.666666666666, 125]
                rank = [
                    1007499, 1004999, 999999, 989999, 974999, 924999, 899999
                ]
                f_mag = value - diff
                mag.append(f_mag)
                mag.sort(reverse=True)
                index = int(mag.index(f_mag))
                i2 = index + 1
                Rpt = rank[index] + int(
                    (f_mag - mag[i2]) / 0.01) * mag_inr[index] + 1
                await ctx.send(f"定數`{diff}`要取得`{value}`R值必須達到`{int(Rpt)}`分")

    @commands.command()
    async def backup(self, ctx):
        try:
            url = ctx.message.attachments[0].url
        except:
            await ctx.send("沒有找到檔案 (No file found)")
            return
        path = "text/sb.txt"
        opener = request.build_opener()
        opener.addheaders = [(
            "User-Agent",
            "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
        )]
        request.install_opener(opener)
        request.urlretrieve(url, path)
        key, chart = func.c2v3(path)
        if key == "e200":
            file = discord.File("text/backup_cache.txt",
                                filename="backup.json")
            await ctx.send(file=file)
        else:
            await ctx.send(chart)

    @commands.command()
    async def color(self, ctx, role_name, Color):
        role = await ctx.guild.create_role(
            name=str(role_name),
            colour=discord.Colour.from_str(Color),
            mentionable=False,
        )
        await role.edit(position=1)
        await ctx.message.author.add_roles(role)

    @commands.command()
    async def history(self, ctx, no=1):
        txt = func.get_deltxt()
        list = re.findall(
            "20[0-9][0-9]-[0-9][0-9]-[0-9][0-9] [0-9][0-9]:[0-9][0-9]:[0-9][0-9] \\| ",
            txt,
        )
        txt = re.sub(
            "20[0-9][0-9]-[0-9][0-9]-[0-9][0-9] [0-9][0-9]:[0-9][0-9]:[0-9][0-9] \\| ",
            "@d+y@",
            txt,
        )
        txt = txt.split("@d+y@")
        a1 = len(list) - int(no)
        b1 = len(txt) - int(no)
        list[a1] = re.sub(" \\| ", "", list[a1])
        await ctx.send(f">>> {func.ctdtime(list[a1])}\n{txt[b1]}")

    @commands.command()
    async def servers(self, ctx):
        activeservers = self.bot.guilds
        txt = ""
        for guild in activeservers:
            txt += guild.name + ":" + str(guild.id) + "\n"
        await ctx.send(txt)

    @commands.command()
    async def list(self, ctx, g):
        if g == "all":
            activeservers = self.bot.guilds
            result = defaultdict(list)
            for guild in activeservers:
                g = self.bot.get_guild(int(guild.id))
                for channel in g.channels:
                    result[guild.name].append(f"{channel.name}:{channel.id}")
            with open("a1.txt", "w") as f:
                json.dump(result, f, indent=4, ensure_ascii=False)
        else:
            g = self.bot.get_guild(int(g))
            text = g.channels
            txt = ""
            for x in range(len(text)):
                txt += f"{text[x].name},{text[x].id}\n"
            with open("a1.txt", "w") as f:
                f.write(txt)
            f.close()
        file = discord.File("a1.txt", filename="a1.txt")
        await ctx.send(file=file)

    @commands.command()
    async def reply(self, ctx, txt, m, g="-1", c="-1"):
        txt = re.sub("\\$", "\n", txt)
        txt = re.sub("_", " ", txt)
        if c == "-1":
            g, c = func.get_keep(g)
        if g == "e404" and str(c) != "-1":
            await ctx.send("沒有Keep記錄")
            return
        g = self.bot.get_guild(int(g))
        c = g.get_channel(int(c))
        m = await c.fetch_message(int(m))
        await m.reply(content=txt)

    @commands.command()
    async def sayat(self, ctx, say, g="-1", c="-1"):
        say = re.sub("\\$", "\n", say)
        say = re.sub("_", " ", say)
        if c == "-1":
            g, c = func.get_keep(g)
        if g == "e404" and str(c) != "-1":
            await ctx.send("沒有Keep記錄")
            return
        g = self.bot.get_guild(int(g))
        c = g.get_channel(int(c))
        await c.send(say)

    @commands.command()
    async def edit(self, ctx, say, m, g="-1", c="-1"):
        say = re.sub("\\$", "\n", say)
        say = re.sub("_", " ", say)
        if c == "-1":
            g, c = func.get_keep(g)
        if g == "e404" and str(c) != "-1":
            await ctx.send("沒有Keep記錄")
            return
        g = self.bot.get_guild(int(g))
        c = g.get_channel(int(c))
        m = await c.fetch_message(int(m))
        await m.edit(content=say)
        await ctx.send("已修改")

    @commands.command()
    async def say(self, ctx, *, say):
        await ctx.message.delete()
        async with ctx.typing():
            output_message = MainTask.repeatMessage(say, ctx.author)
            await ctx.send(output_message)

    @commands.command()
    async def rkeep(self, ctx, txt, g, c):
        if func.write_keep(txt, g, c) == "e200":
            await ctx.send("成功儲存至Keep")
        else:
            await ctx.send("Keep已有相同關鍵詞")

    @commands.command()
    async def pub(self, ctx, date, value, coin: int):
        publist = func.write_keep("公費", date, value, coin, False)
        inclist = func.get_keep("收入", False)
        epdlist = func.get_keep("支出", False)
        esum = 0
        isum = 0
        psum = 0
        for date, cache in epdlist.items():  # type: ignore
            for item in cache:
                esum += item[1]
        for date, cache in inclist.items():  # type: ignore
            for item in cache:
                isum += item[1]
        for date, cache in publist.items():  # type: ignore
            for item in cache:
                psum += item[1]
        sum = isum - esum - psum
        await ctx.send(f"儲存成功\n餘額：{sum}")

    # 支出
    @commands.command()
    async def epd(self, ctx, date, value, coin: int):
        epdlist = func.write_keep("支出", date, value, coin, False)
        inclist = func.get_keep("收入", False)
        publist = func.get_keep("公費", False)
        esum = 0
        isum = 0
        psum = 0
        for date, cache in epdlist.items():  # type: ignore
            for item in cache:
                esum += item[1]
        for date, cache in inclist.items():  # type: ignore
            for item in cache:
                isum += item[1]
        for date, cache in publist.items():  # type: ignore
            for item in cache:
                psum += item[1]
        sum = isum - esum - psum
        await ctx.send(f"儲存成功\n餘額：{sum}")

    # 收入
    @commands.command()
    async def inc(self, ctx, date, text, value):
        if ctx.author.id != 830395796490158081:
            await ctx.send("Missing Permission")
            return
        inclist = func.write_keep("收入", date, text, int(value), False)
        epdlist = func.get_keep("支出", False)
        publist = func.get_keep("公費", False)
        esum = 0
        isum = 0
        psum = 0
        for date, cache in epdlist.items():  # type: ignore
            for item in cache:
                esum += item[1]
        for date, cache in inclist.items():  # type: ignore
            for item in cache:
                isum += item[1]
        for date, cache in publist.items():  # type: ignore
            for item in cache:
                psum += item[1]
        sum = isum - esum - psum
        await ctx.send(f"儲存成功\n餘額：{sum}")

    @commands.command()
    async def epdlist(self, ctx, count=5):
        count = int(count)
        epdlist = func.get_keep("支出", False)

        func.keep_chart(epdlist, count)
        file = discord.File("./photo/keep1.png", filename="keep.png")
        await ctx.send(file=file)

    @commands.command()
    async def newch(self, ctx, g, c):
        g = self.bot.get_guild(int(g))
        c = g.get_channel(int(c))
        overwrites = {
            g.default_role:
            discord.PermissionOverwrite(
                read_messages=True,
                attach_files=True,
                add_reactions=True,
                read_message_history=True,
                send_messages=True,
                use_external_emojis=True,
            )
        }
        await g.create_text_channel("【課題】-看釘選-",
                                    overwrites=overwrites,
                                    category=c)

    @commands.command()
    async def quote(self, ctx, who, say, name):
        if not re.match(r"<[@!]+[0-9]+>", who):
            await ctx.send("請正確標註成員 (Key error)")
            return
        avater = func.mentionReplacement(ctx.author, who, isAvatar=True)
        if avater == "bot":
            await ctx.send("不能標註機器人")
            return
        PNG = Image.new("RGB", (800, 400), (30, 33, 42))
        avater_path = requests.get(avater)
        avater = Image.open(BytesIO(avater_path.content))
        avater = avater.convert("RGBA")
        avater = avater.resize((180, 180))
        PNG.paste(avater, box=(10, 80), mask=avater)
        drawtext = ImageDraw.Draw(PNG)
        say = re.sub("\\$", "\n", say)
        say = re.sub("_", " ", say)
        font_path = "font/ChenYuluoyan-Thin-Monospaced.ttf"
        font = ImageFont.truetype(font_path, 68, encoding="utf-8")
        font2 = ImageFont.truetype(font_path, 45, encoding="utf-8")
        print("42")
        drawtext.text((200, 80), say, "#ffffff", font=font)
        drawtext.text((595, 290), name, "#ffffff", font=font2)
        print("3")
        PNG.save("./photo/quote.png")
        file = discord.File("./photo/quote.png", filename="quote.png")
        await ctx.send(file=file)

    @commands.command()
    async def getlink(self, ctx):
        if ctx.message.reference:
            msg = await ctx.fetch_message(ctx.message.reference.message_id)
            link = msg.attachments[0].url
            await ctx.send(f"> {link}")
        else:
            await ctx.send("No file found")

    @commands.command()
    async def suggest(self, ctx, *, suggest):
        g = self.bot.get_guild(1133038534702407790)
        ch = g.get_channel(1150805649979101185)
        embed = discord.Embed(title=f"{ctx.author}的建議",
                              color=0x27FF27,
                              description=suggest)
        await ch.send(embed=embed)
        embed = discord.Embed(title="你的建議",
                              color=0x27FF27,
                              description=suggest)
        await ctx.send(embed=embed)

    @commands.command()
    async def c2info(self, ctx, *text):
        def t2s(traditional_text):
            cc = OpenCC('t2s')  # 繁體轉簡體
            simplified_text = cc.convert(traditional_text)
            return simplified_text

        def chartEmbed(song, color, character):
            chart_data=song["charts"]
            song_data = list(song.values())
            embed = coin.emb(
                f"**{song_data[1]}**", f"{song_data[2]}\n⠀\n", int(color))
            ver=song["version"]
            try:
                ver+=" / G:("+song["charts"]["glitch"]["version"]+")"
            except:
                pass
            metadata = [["BPM",song_data[3]] ,["Character",character] ,["Version",ver]]
            for b,c in metadata:
                embed.add_field(
                    name=f"**{b}**", value=f"```fix\n{c}\n```", inline=True)
            
            type = ["ＣＨＡＯＳ", "ＧＬＩＴＣＨ"]
            type_color = [35, 36]
            count = 0
            for t,chart in (chart_data.items()):
                
                for d, c, n in [list(chart.values())[0:3]]:
                    embed.add_field(
                        name=f" \n", value=f"\n```ansi\n[1;47;{type_color[count]}m{type[count]}```", inline=False)
                    embed.add_field(
                        name="**Official diff**", value=f"\n```fix\n{d}\n```", inline=True)
                    embed.add_field(
                        name="**CN:DC Diff**", value=f"\n```fix\n{c}\n```", inline=True)
                    embed.add_field(
                        name="**Notes**", value=f"\n```fix\n{n}\n```", inline=True)
                count += 1
            return embed

        async with ctx.typing():
            path = requests.get(
                "https://c2info.starsky919.xyz/assets/c2data.json")
            data = json.loads(path.content.decode("utf-8"))
            t = ''.join(str(item) for item in text).lower()
            s = t2s(t)
            
            result = [item for item in data["songs"]
                      if (t in re.sub(" ","",item["name"].lower())) or (s in item["aliases"])]
            count = len(result)
            view = discord.ui.View(timeout=15)
            if count == 0:
                await ctx.send("No result")
                return
            elif count == 1:
                song = result[int(0)]
                color, character = [[s["theme_color"], s["name"]] for s in data["characters"]
                                        if s["id"] == song["character"]][0]
                color = int(color[1:], 16)
                embed = chartEmbed(song, color,character)
                await ctx.send(embed=embed)
                return 
            elif count > 25:
                await ctx.send("Too many result")
                return

            view.on_error = lambda interaction, error, item: handle_error(
                interaction, error, item, ctx)

            async def slc_cb_1(interaction):
                if interaction.user.id == ctx.author.id:
                    index = interaction.data["values"][0]
                    song = result[int(index)]
                    color, character = [[s["theme_color"], s["name"]] for s in data["characters"]
                                        if s["id"] == song["character"]][0]
                    color = int(color[1:], 16)
                    embed = chartEmbed(song, color,character)
                    view.clear_items()
                    view.stop()
                    await interaction.response.edit_message(embed=embed,view=view)
                    return
            songname = [[result[i]["name"], i] for i in range(len(result))]
            select_1 = slc(
                "Select a song", songname)
            select_1.callback = slc_cb_1
            view.add_item(select_1)
            msg = await ctx.send(view=view)
            view.on_timeout = lambda: timeout(view, msg)


async def setup(bot):
    await bot.add_cog(Main(bot))
