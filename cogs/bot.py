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
import core.func as func
from core.classes import Cog_Extension
import librosa
from urllib import request
import core.CytoidData as CytoidData
import core.MainTask as MainTask
import time
import difflib
import traceback
debuging = True

i = 0


class Main(Cog_Extension):
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        func.del_cd("guess", ctx.channel.id)
        cmd = ctx.invoked_with
        full_error = traceback.format_exception(error)
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(
                f'**請輸入正確的參數 (Please type in all require args.**)\n{func.ebt(cmd)}\n```ERROR: {error}```'
            )
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send(
                f"**You dont have the permissions for using this command**\n`{error}`"
            )
        elif isinstance(error, commands.CommandNotFound):
            pass
        else:
            with open ("full_error.txt","w") as f:
                text=""
                for i in range(len(full_error)):
                    text+=full_error[i]
                f.write(text)
            f.close()
            file = discord.File("full_error.txt",
                                    filename="full_error.txt")
            await ctx.send(f"Unknown Error at **{cmd}**: {error}",file=file)
            
            
  
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        global pvpemo1  # 身分驗證
        global pvpemo2  # 是否點選表情
        global pvpemo3  # 回傳點選表情
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
        try:
            if str(payload.emoji.name) == "EZ_dy" and user == pvpemo1:
                await message.clear_reaction(func.emo("ex"))
                await message.clear_reaction(func.emo("hd"))
                pvpemo1 = "0"
                pvpemo2 = 1
                pvpemo3 = "easy"
            elif str(payload.emoji.name) == "HD_dy" and user == pvpemo1:
                await message.clear_reaction(func.emo("ex"))
                await message.clear_reaction(func.emo("ez"))
                pvpemo1 = "0"
                pvpemo2 = 1
                pvpemo3 = "hard"
            elif str(payload.emoji.name) == "EX_dy" and user == pvpemo1:
                await message.clear_reaction(func.emo("ez"))
                await message.clear_reaction(func.emo("hd"))
                pvpemo1 = "0"
                pvpemo2 = 1
                pvpemo3 = "extreme"
        except:
            return
        try:
            if str(payload.emoji.name) == "ZH_dy" and user == helpemo1:
                await message.clear_reaction(func.emo("en"))
                helpemo1 = "0"
                helpemo2 = 1
                helpemo3 = 1
            elif str(payload.emoji.name) == "EN_dy" and user == helpemo1:
                await message.clear_reaction(func.emo("zh"))
                helpemo1 = "0"
                helpemo2 = 1
                helpemo3 = 2
            if str(payload.emoji) == "\U0001F22F":
                print("1")
                text = func.ztf(message.content)
                if "e200" not in text:
                    await message.channel.send(text)
                else:
                    return
        except:
            return

    global wait

    @commands.Cog.listener()
    async def on_message(self, message):
        if str(message.author) == "dy6ot#9006":
            return
        global pvpemo1  # 身分驗證
        global pvpemo2  # 是否點選表情 N/Y = 0/1
        global pvpemo3  # 回傳點選表情
        global helpemo1
        global helpemo2
        global helpemo3
        global ramlimit
        global wait
        is_guess = func.get_cd_notkeep("guess", message.channel.id)
        tx3 = 0  # 關鍵字判定
        if str(message.author) == "Nadeko#6685":
            if len(message.mentions) > 0:
                output_message = MainTask.replaceNadekoMention(message)
                await message.delete()
                await message.channel.send(output_message)
            return

        if message.content.startswith("說，") or message.content.startswith(
                "say,"):
            # 因為有bug，以後再修
            if not is_guess:
                await message.channel.send("指令冷卻中 (Cooldown)")
                return
            message_content = message.content
            if message_content.startswith("說，"):
                message_content = message_content[2:]
            else:
                message_content = message_content[4:]
            output_message = MainTask.repeatMessage(message_content,
                                                    message.author)
            await message.delete()
            await message.channel.send(output_message)
            return

        if message.content.startswith("dy"):
            # 分割訊息成兩份
            tmp = re.findall("[^ ]+", message.content)
            # 如果分割後串列長度只有1
            if len(tmp) == 1:
                return
            if len(tmp) == 2:
                if tmp[1].startswith("ran") and "random" not in tmp[1]:
                    jsonstr2 = CytoidData.getRandomChart(
                        exclude_black_list=True)
                    embed = func.getChartInfoEmbed(jsonstr2)
                    await message.channel.send(embed=embed)
                if tmp[1].startswith("random"):
                    jsonstr2 = CytoidData.getRandomChart()
                    embed = func.getChartInfoEmbed(jsonstr2)
                    await message.channel.send(embed=embed)
                if tmp[1].startswith("hack"):
                    output_message, embed_list = MainTask.checkHack(0)
                    if output_message == None:
                        await message.channel.send("No one cheated")
                        return
                    else:
                        await message.channel.send(output_message)
                        for embed in embed_list:
                            await message.channel.send(embed=embed)
                if tmp[1].startswith("bpm"):
                    w1 = await message.channel.send("Working...")
                    try:
                        url = message.attachments[0].url
                        img_nmae = f"{str(random.randrange(1,10000))}{str(random.randrange(1,10000))}.mp3"
                        path_str = "./audio/"
                        path = path_str + img_nmae
                        opener = request.build_opener()
                        opener.addheaders = [(
                            "User-Agent",
                            "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
                        )]
                        request.install_opener(opener)
                        request.urlretrieve(url, path)
                        audio_file = librosa.load(path)
                    except:
                        await w1.delete()
                        await message.channel.send("Get File Failed")
                        ramlimit -= 1
                        return
                    y, sr = audio_file
                    print(librosa.core.get_duration(y=y, sr=sr))
                    if librosa.core.get_duration(y=y, sr=sr) > 265:
                        await w1.delete()
                        await message.channel.send(
                            "BREAKDOWN: RAM overload, Audio duration is too long"
                        )
                        ramlimit -= 1
                        return
                    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
                    beat_times = librosa.frames_to_time(beat_frames, sr=sr)
                    BPM = func.bpm(beat_times)
                    await w1.delete()
                    tmg = await message.channel.send(BPM)
                    await tmg.add_reaction(func.emo("bpm"))
                    os.remove(path)
                    ramlimit -= 1
            if len(tmp) == 3:
                if tmp[1].startswith("test"):
                    if not func.isValidLevelId(tmp[2]):
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
                    file = discord.File("cache1.png",
                                        filename="RatingChart.png")
                    await message.channel.send(file=file)
                if tmp[1].startswith("rate"):
                    if not func.isValidLevelId(tmp[2]):
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
                    func.plot_line_chart(
                        rating_data["distribution"],
                        level_data["owner"]["avatar"]["original"],
                        level_data["title"],
                    )
                    file = discord.File("cache1.png",
                                        filename="RatingChart.png")
                    await message.channel.send(file=file)
                if tmp[1].startswith("plays"):
                    if not func.isValidLevelId(tmp[2]):
                        await message.channel.send(
                            "level id輸入錯誤 (keyword error)")
                        return 0
                    url = ("https://next.cytoid.io/levels?owner=" + tmp[2] +
                           "&page=1&sort=plays&order=desc&category=all")
                    res = requests.get(url)
                    res = res.content.decode()
                    str1 = res.split("<script>", 2)
                    str2 = str1[1].split("</script>", 2)
                    str3 = str2[0].split('layout:"default",data:[', 2)
                    str4 = str3[1].split("],fetch:", 2)
                    if "levels:[]" in str4[0]:
                        await message.channel.send(
                            "使用者id輸入不正確或此人無上傳譜面 (id wrong or no result)")
                        return 0
                    tmg = await message.channel.send("Search...")
                    await asyncio.sleep(3)
                    await tmg.delete()
                    play = re.findall("plays:([0-9]*)", str4[0])
                    down = re.findall("downloads:([0-9]*)", str4[0])
                    raw_uid = re.findall('uid:"([0-9a-z._-]*)"', str4[0])
                    url1 = "https://services.cytoid.io/levels/" + raw_uid[0]
                    res1 = requests.get(url1)
                    js1 = json.loads(res1.content.decode("utf-8"))
                    uid1 = js1["title"]
                    url1 = "https://services.cytoid.io/levels/" + raw_uid[1]
                    res1 = requests.get(url1)
                    js1 = json.loads(res1.content.decode("utf-8"))
                    uid2 = js1["title"]
                    url1 = "https://services.cytoid.io/levels/" + raw_uid[2]
                    res1 = requests.get(url1)
                    js1 = json.loads(res1.content.decode("utf-8"))
                    uid3 = js1["title"]

                    embed = discord.Embed(
                        title=f"{tmp[2]}的譜面遊玩數Top3:",
                        description=
                        f"Top1: {uid1}\n遊玩數： {play[0]}\n下載數： {down[0]}\n\nTop2: {uid2}\n遊玩數： {play[1]}\n下載數： {down[1]}\n\nTop3: {uid3}\n遊玩數： {play[2]}\n下載數： {down[2]}",
                        color=0x00FFFF,
                    )
                    await message.channel.send(embed=embed)
                if tmp[1].startswith("random"):
                    level = tmp[2].replace("5+", "6").replace("?", "0")
                    if level.isdigit():
                        level = int(level)
                    else:
                        await message.channel.send("請輸入正確的數字 (Keyword error)")
                        return

                    jsonstr2 = CytoidData.getRandomChart(
                        level=level, exclude_black_list=True)
                    if jsonstr2 == None:
                        await message.channel.send("查詢出錯 (Please retry)")
                        return

                    embed = func.getChartInfoEmbed(jsonstr2)

                    await message.channel.send(embed=embed)
            if len(tmp) == 4:
                if tmp[1].startswith("best"):
                    x1 = 1
                    x3 = 1
                    # code copyright belongs to akari-bot[github.com/Teahouse-Studios/akari-bot/blob/master/modules/cytoid/rating.py]
                    check1 = requests.get(
                        f"https://services.cytoid.io/profile/{tmp[2]}")
                    check1a = json.loads(check1.content.decode("utf-8"))
                    if "me" == tmp[2] or re.match(r"<[@!]+[0-9]+>", tmp[2]):
                        # u1 = func.ment(message.author, tmp[2], message.author.guild)
                        u1 = func.mentionReplacement(message.author, tmp[2])
                        tmp[2] = func.get_ctdid(u1)
                        if "e404" in tmp[2]:
                            await message.channel.send(
                                "無註冊資料，使用`bind ctd <cytoid id>`綁定帳號 (You have not bound yet)"
                            )
                            x1 = 0
                    elif "statusCode" in check1a:
                        if check1a["statusCode"] == 404:
                            x1 = 0
                            await message.channel.send(
                                "Cytoid ID未正確輸入 (keyword error)")
                    check2 = requests.get(
                        f"https://services.cytoid.io/levels/{tmp[3]}")
                    check2a = json.loads(check2.content.decode("utf-8"))
                    if "statusCode" in check2a:
                        if check2a["statusCode"] == 404:
                            x1 = 0
                            await message.channel.send(
                                "Level ID未正確輸入 (keyword error)")
                    # end
                    url = "https://services.cytoid.io/levels/" + tmp[3]
                    res = requests.get(url)
                    jsonstr = json.loads(res.content.decode("utf-8"))
                    c1 = 1
                    if c1 == 1 and x1 == 1:
                        if len(jsonstr["charts"]) > 2:
                            pvpemo1 = message.author
                            pvpemo2 = 0
                            em1 = await message.channel.send(
                                "> 請選擇難度 (select diff type)")
                            await em1.add_reaction(func.emo("ez"))
                            await em1.add_reaction(func.emo("hd"))
                            await em1.add_reaction(func.emo("ex"))
                            await asyncio.sleep(5)
                            if pvpemo2 == 0:
                                await em1.delete()
                                await message.channel.send("選擇時間超時 (time out)")
                                x1 = 0
                        if len(jsonstr["charts"]) > 2:
                            for i in range(3):
                                if pvpemo3 in jsonstr["charts"][i]["type"]:
                                    type = jsonstr["charts"][i]["type"]
                                    diff = jsonstr["charts"][i]["difficulty"]
                                    break
                        elif len(jsonstr["charts"]) > 1:
                            chpe = ["1", "2"]
                            for i in range(2):
                                chpe[i] = jsonstr["charts"][i]["type"]
                            if "extreme" not in chpe:
                                pvpemo1 = message.author
                                pvpemo2 = 0
                                em1 = await message.channel.send(
                                    "> 請選擇難度 (select diff type)")
                                await em1.add_reaction(func.emo("ez"))
                                await em1.add_reaction(func.emo("hd"))
                                await asyncio.sleep(8)
                                if pvpemo2 == 1:
                                    for i in range(2):
                                        if pvpemo3 in jsonstr["charts"][i][
                                                "type"]:
                                            pvpemo3 = "0"
                                            type = jsonstr["charts"][i]["type"]
                                            diff = jsonstr["charts"][i][
                                                "difficulty"]
                                else:
                                    await em1.delete()
                                    await message.channel.send(
                                        "選擇時間超時 (time out)")
                                    x1 = 0
                            elif "hard" not in chpe:
                                pvpemo1 = message.author
                                pvpemo2 = 0
                                em1 = await message.channel.send(
                                    "> 請選擇難度 (select diff type)")
                                await em1.add_reaction(func.emo("ez"))
                                await em1.add_reaction(func.emo("ex"))
                                await asyncio.sleep(8)
                                if pvpemo2 == 1:
                                    for i in range(2):
                                        if pvpemo3 in jsonstr["charts"][i][
                                                "type"]:
                                            pvpemo3 = "0"
                                            type = jsonstr["charts"][i]["type"]
                                            diff = jsonstr["charts"][i][
                                                "difficulty"]
                                    pvpemo3 = "0"
                                else:
                                    await em1.delete()
                                    await message.channel.send(
                                        "選擇時間超時 (time out)")
                                    x1 = 0
                            elif "easy" not in chpe:
                                pvpemo1 = message.author
                                pvpemo2 = 0
                                em1 = await message.channel.send(
                                    "> 請選擇難度 (select diff type)")
                                await em1.add_reaction(func.emo("hd"))
                                await em1.add_reaction(func.emo("ex"))
                                await asyncio.sleep(8)
                                if pvpemo2 == 1:
                                    for i in range(2):
                                        if pvpemo3 in jsonstr["charts"][i][
                                                "type"]:
                                            pvpemo3 = "0"
                                            type = jsonstr["charts"][i]["type"]
                                            diff = jsonstr["charts"][i][
                                                "difficulty"]
                                    pvpemo3 = "0"
                                else:
                                    await em1.delete()
                                    await message.channel.send(
                                        "選擇時間超時 (time out)")
                                    x1 = 0
                        else:
                            type = jsonstr["charts"][0]["type"]
                            diff = jsonstr["charts"][0]["difficulty"]
                    if x1 == 1:
                        x2 = 1
                        str1 = requests.get(
                            f"https://services.cytoid.io/levels/{tmp[3]}/charts/{type}/records?limit=20000"
                        )
                        user1 = json.loads(str1.content.decode("utf-8"))
                        x3 = 1
                        if "statusCode" in user1:
                            if user1["statusCode"] == 404:
                                x2 = 0
                                x3 = 0
                                await message.channel.send(
                                    "沒有此Diff type，請重新確認 (d-type doesn't exist in level)"
                                )
                        if x3 > 0:
                            for i in range(len(user1)):
                                if tmp[2] == user1[i]["owner"]["uid"]:
                                    score1 = user1[i]["score"]
                                    date1 = f'{func.ctdtime(user1[i]["date"])}'
                                    acc1 = format(user1[i]["accuracy"] * 100,
                                                  ".3f")
                                    perfect1 = user1[i]["details"]["perfect"]
                                    great1 = user1[i]["details"]["great"]
                                    good1 = user1[i]["details"]["good"]
                                    bad1 = user1[i]["details"]["bad"]
                                    miss1 = user1[i]["details"]["miss"]
                                    avt1 = user1[i]["owner"]["avatar"]["small"]
                                    rank1 = i + 1
                                    x2 = 1
                                    break
                                else:
                                    x2 = 2
                            x3 = 1
                        if x2 == 1:
                            embed = discord.Embed(
                                title=check2a["title"],
                                description=
                                f"**Score (Acc)**\n{score1}⠀⠀({acc1}%)\n\n**Notes Judgement**\n{perfect1}p / {great1}gr / {good1}g / {bad1}b / {miss1}m\n\n**RANK**\n#{rank1}\n\n**Date**\n{date1}",
                                color=0x27FF27,
                                url=f"https://next.cytoid.io/levels/{tmp[3]}",
                            )
                            embed.set_footer(text=tmp[3])
                            embed.set_author(name=tmp[2], icon_url=avt1)
                            await message.channel.send(embed=embed)
                        else:
                            await message.channel.send("沒有遊玩記錄 (no record)")
            if len(tmp) == 6:
                if tmp[1].startswith("pvp"):
                    x1 = 1
                    x3 = 1
                    # code copyright belongs to akari-bot[github.com/Teahouse-Studios/akari-bot/blob/master/modules/cytoid/rating.py]
                    check1 = requests.get(
                        f"https://services.cytoid.io/profile/{tmp[2]}")
                    check1a = json.loads(check1.content.decode("utf-8"))
                    if "me" == tmp[2] or re.match(r"<[@!]+[0-9]+>", tmp[2]):
                        # tmp[2] = func.ment(message.author, tmp[2], message.author.guild)
                        tmp[2] = func.mentionReplacement(
                            message.author, tmp[2])
                        tmp[2] = func.get_ctdid(tmp[2])
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
                        tmp[3] = func.mentionReplacement(
                            message.author, tmp[3])
                        tmp[3] = func.get_ctdid(tmp[3])
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
                        tmp[4] = func.mentionReplacement(
                            message.author, tmp[4])
                        tmp[4] = func.get_ctdid(tmp[4])
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
                            await message.channel.send(
                                f'請三方遊玩{type}難度，並在譜面時長({jsonstr["duration"]})+20秒內上傳遊玩分數'
                            )
                            await asyncio.sleep(int(length))

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
                                f".....................\n{tmp[2]}的加權總分是：{format(total1,'.3f')}\n分數：{score1}   acc：{format(acc1*100,'.3f')}%\n....................."
                            )
                            await message.channel.send(
                                f"{tmp[3]}的加權總分是：{format(total2,'.3f')}\n分數：{score2}   acc：{format(acc2 *100,'.3f')}%"
                            )
                            await message.channel.send(
                                f".....................\n{tmp[4]}的加權總分是：{format(total3,'.3f')}\n分數：{score3}   acc：{format(acc3*100,'.3f')}%"
                            )
        #改變dy help
        if message.content.startswith("@dy6ot") or message.content.startswith("<@1046351345352986705>"):
            tmp = re.findall("[^ ]+", message.content)
            if len(tmp) == 2:
                if tmp[1].startswith("help"):
                    helpemo1 = message.author
                    helpemo2 = 0
                    helpemo3 = 0
                    x3 = 1
                    em1 = await message.channel.send(
                        "> 請選擇語言 (select language)")
                    await em1.add_reaction(func.emo("zh"))
                    await em1.add_reaction(func.emo("en"))
                    await asyncio.sleep(3)
                    if helpemo2 == 1:
                        if helpemo3 == 1:
                            embed = discord.Embed(
                                title="指令列表：",
                                description=
                                "**[說，<要機器人說的內容>]**\n\n**[dy rate <譜面id>]**：查看譜面評分詳情\n\n**[dy ping]**：延遲間隔\n\n**[dy random (難度)]**：隨機產生Cytoid關卡id\n\n**[dy ctd <cytoid id>]**：近期遊玩記錄\n\n**[dy best <cytoid id> <level id>]**：最佳遊玩記錄\n\n**[dy pvp <cytoid id> <cytoid id> <level id>]**：Cytoid雙人對戰（遊玩同個關卡後再輸送指令）\n\n**[dy guess]**：猜曲名遊戲。輸入[猜<序號> <猜測的答案>]來搶答\n\n\n**[bind ctd <cytoid id>]**：綁定Cytoid帳戶 (使用 'me' 或者 '@someone' 取代 <cytoid id>)\n\n**[unbind ctd]**：解除綁定Cytoid帳戶",
                                color=0xFFFF37,
                            )
                        elif helpemo3 == 2:
                            embed = discord.Embed(
                                title="Commands List：",
                                description=
                                "**[say,<what you want dy6ot to say>]**\n\n**[dy rate <level id>]**：check level's rating composing\n\n**[dy ping]**：return ping\n\n**[dy random]**：Randomly generate Cytoid level id\n\n**[dy ctd <cytoid id>]**：Last play record\n\n**[dy best <cytoid id> <level id>]**：Best play record\n\n**[dy pvp <cytoid id> <cytoid id> <level id>]**：Cytoid pvp function（Played the same level before sending command）\n\n**[bind ctd <cytoid id>]**：Bind your Cytoid account (Use 'me' or '@someone' replace <cytoid id>)\n\n**[unbind ctd]**：unbind your Cytoid account",
                                color=0xFFFF37,
                            )
                        else:
                            await message.channel.send("發生未知錯誤 (unknown error)"
                                                       )
                            x3 = 0
                    else:
                        await em1.delete()
                        await message.channel.send("選擇時間超時 (time out)")
                        x3 = 0
                    if x3 == 1:
                        await message.channel.send(embed=embed)       
        if message.content.startswith("bind"):
            tmp = message.content.split(" ", 5)
            if len(tmp) == 3:
                if tmp[1].startswith("ctd"):
                    x1 = 1
                    check1 = requests.get(
                        f"https://services.cytoid.io/profile/{tmp[2]}")
                    check1a = json.loads(check1.content.decode("utf-8"))
                    if "statusCode" in check1a:
                        if check1a["statusCode"] == 404:
                            x1 = 0
                            await message.channel.send(
                                "Cytoid ID未正確輸入 (keyword error)")
                    if x1 == 1:
                        work = func.write_ctdid(str(message.author), tmp[2])
                        if "e405" in work:
                            id = re.sub("e405：", "", work)
                            await message.channel.send(
                                f"已經綁定了，你的Cytoid ID是{id} (already binded)")
                        elif "e200" in work:
                            await message.channel.send("綁定成功！ (Success!)")
        if message.content.startswith("unbind"):
            tmp = message.content.split(" ", 5)
            if len(tmp) == 2:
                if tmp[1].startswith("ctd"):
                    x1 = 1
                    if x1 == 1:
                        work = func.delete_ctdid(str(message.author))
                        if "e404" in work:
                            await message.channel.send(
                                "無註冊資料，使用`bind ctd <cytoid id>`綁定帳號 (You have not bound yet)"
                            )
                        elif "e200" in work:
                            await message.channel.send("解除綁定成功！ (Success!)")
    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f"延遲: {round(self.bot.latency * 1000)}ms")
 
    @commands.command()
    async def ctd(self, ctx, playerAid="me"):
        if True:
           checkA=CytoidData.checkCytoidID(playerAid,ctx.author,getID=True)
           if "nobind" in checkA:
                await ctx.send(f"{func.ebt(checkA)}")
                return
           elif "nofind" in checkA:
                await ctx.send(f"{func.ebt(checkA)}")
                return
           loading_message = await ctx.send("圖片產生中...")
           img_file, file_name,level_id = MainTask.generateRecentPlayPic(checkA)
           if not level_id:
               await ctx.send(func.ebt("norecord"))
               return
           embed = discord.Embed(title=level_id,color=0x27FF27,url=f"https://next.cytoid.io/levels/{level_id}")
           await loading_message.edit(content="",embed=embed)
           await ctx.send(file=img_file)
           os.remove(file_name)
           return
  
    @commands.command()
    async def pvp(self, ctx, playerAid, playerBid, levelid):
        global pvpemo1  # 身分驗證
        global pvpemo2  # 是否點選表情 N/Y = 0/1
        global pvpemo3  # 回傳點選表情
        pvpemo1 = ctx.author
        pvpemo2 = 0
        checkA=CytoidData.checkCytoidID(playerAid,ctx.author)
        checkB=CytoidData.checkCytoidID(playerBid,ctx.author)
        checkC=CytoidData.checkLevelID(levelid)
        if "nobind" in (checkA or checkB):
            await ctx.send(f"{func.ebt(checkA)}{func.ebt(checkB)}{func.ebt(checkC)}")
            return
        elif "nofind" in (checkA or checkB):
            await ctx.send(f"{func.ebt(checkA)}{func.ebt(checkB)}{func.ebt(checkC)}")
            return
        elif "nofindctdlevel" in checkC:
            await ctx.send(f"{func.ebt(checkC)}")
            return
        leveldata=CytoidData.getLevelData(levelid)
        difflist=CytoidData.getLevelDiff(levelid)
        chs_diff_msg = await ctx.send("> 請選擇難度 (select diff type)")
        if "Z" in difflist:
            await chs_diff_msg.add_reaction(func.emo("ez"))
        if "H" in difflist:
            await chs_diff_msg.add_reaction(func.emo("hd"))
        if "E" in difflist:
            await chs_diff_msg.add_reaction(func.emo("ex"))  
        def check(reaction , user):
            return reaction.message == chs_diff_msg and user == ctx.author and "_dy" in str(reaction.emoji) 
        try:
            chs_diff, z1= await self.bot.wait_for("reaction_add",timeout=10,check=check)
            if "EZ" in str(chs_diff.emoji):
                await chs_diff_msg.edit(content="你選擇的是 **easy** (Your select is easy)")
                diff_index=int(difflist.find("Z"))
            elif "HD" in str(chs_diff.emoji):
                await chs_diff_msg.edit(content="你選擇的是 **hard** (Your select is hard)")
                diff_index=int(difflist.find("H"))
            elif "EX" in str(chs_diff.emoji):
                await chs_diff_msg.edit(content="你選擇的是 **extreme** (Your select is extreme)")
                diff_index=int(difflist.find("E"))
        except asyncio.TimeoutError:
            await chs_diff_msg.edit(content="超時未選擇 (Time out)")
            return
        type = leveldata["charts"][diff_index]["type"]
        diff = leveldata["charts"][diff_index][
            "difficulty"]
        lid = leveldata["charts"][diff_index]["id"]
        font_path2 = "./font/jh.ttf"
        font_path1 = "./font/MPLUSRounded1c-Bold.ttf"
        font_path = "./font/MPLUSRounded1c-Regular.ttf"
        font_path3 = "./font/ARIALN.TTF"
        font_path4 = "./font/NotoSansSC-Medium.otf"
        font_path5 = "./font/NotoSans-Regular.ttf"
        level_path = requests.get(
            leveldata["cover"]["cover"])
        try:
            levelcachepng = Image.open(
                BytesIO(level_path.content))
        except:
            levelcachepng = Image.new(
                "RGB", (1280, 800), (30, 33, 42))
        levelcache1png = levelcachepng.filter(
            ImageFilter.GaussianBlur(7))
        levelcache2png = ImageEnhance.Brightness(
            levelcache1png)
        pvpimg = levelcache2png.enhance(0.23)
        a1 = 0
        while a1 < 1:  # 為了收合
            playerAid = CytoidData.checkCytoidID(playerAid,ctx.author,getID=True)
            check1a=CytoidData.getProfileData(playerAid)
            playerBid = CytoidData.checkCytoidID(playerBid,ctx.author,getID=True)
            print(playerAid,playerBid)
            check2a=CytoidData.getProfileData(playerBid)
            p1_path = requests.get(
                check1a["user"]["avatar"]["original"])
            p1cc = Image.open(BytesIO(p1_path.content))
            p1img = func.img_circle(p1cc, 100)
            p2_path = requests.get(
                check2a["user"]["avatar"]["original"])
            p2cc = Image.open(BytesIO(p2_path.content))
            p2img = func.img_circle(p2cc, 100)
            ctr_path = requests.get(
                leveldata["owner"]["avatar"]["original"])
            ctrcc = Image.open(BytesIO(ctr_path.content))
            ctrimg = func.img_circle(ctrcc, 124)
            pvpimg.paste(ctrimg, box=(12, 30), mask=ctrimg)
            pvpimg.paste(p1img, box=(65, 185), mask=p1img)
            pvpimg.paste(p2img, box=(65, 490), mask=p2img)
            pvpimg = pvpimg.convert("RGB")
            drawtext = ImageDraw.Draw(pvpimg)
            f1 = ImageFont.truetype(
                os.path.abspath(font_path5), 60)
            f2 = ImageFont.truetype(
                os.path.abspath(font_path), 42)
            f2a = ImageFont.truetype(
                os.path.abspath(font_path), 37)
            f2b = ImageFont.truetype(
                os.path.abspath(font_path), 30)
            f2c = ImageFont.truetype(
                os.path.abspath(font_path), 18)
            h1 = 21
            if "ja" in func.judge_language(
                    leveldata["title"]
            ) or "zh" in func.judge_language(
                    leveldata["title"]):
                f1 = ImageFont.truetype(
                    os.path.abspath(font_path4), 67)
                if len(
                        re.findall("[^\0]",
                                   leveldata["title"])) > 13:
                    size = 78 - round(
                        len(
                            re.findall(
                                "[^\0 ('.~a-z0-9A-Z]",
                                leveldata["title"],
                            )) * 1.77 +
                        len(
                            re.findall(
                                "[()'.]", leveldata["title"])
                        ) * 0.2 + len(
                            re.findall(
                                "[ ~a-z0-9]",
                                leveldata["title"])) * 0.75 +
                        len(
                            re.findall(
                                "[A-Z]",
                                leveldata["title"])) * 1.35)
                    h1 = h1 + round((78 - size) / 6)
                    f1 = ImageFont.truetype(
                        os.path.abspath(font_path4), size)
            elif "en" in func.judge_language(
                    leveldata["title"]):
                f1 = ImageFont.truetype(
                    os.path.abspath(font_path3), 80)
                if len(
                        re.findall("[^\0]",
                                   leveldata["title"])) > 24:
                    size = 100 - int(
                        len(
                            re.findall(
                                "[^\0]", leveldata["title"]))
                        * 1.26)
                    f1 = ImageFont.truetype(
                        os.path.abspath(font_path3), size)
                    h1 = h1 + round((102 - size) / 12)
            title = demoji.replace(leveldata["title"], "")
            drawtext.text((150, h1),
                          title,
                          "#ffffff",
                          font=f1)
            drawtext.text((188, 178),
                          playerAid,
                          "#ffffff",
                          font=f2)
            drawtext.text((188, 483),
                          playerBid,
                          "#ffffff",
                          font=f2)
            drawtext.text((150, 101),
                          levelid,
                          "#ffffff",
                          font=f2a)
            drawtext.text(
                (150, 2),
                'Generated by "dy6ot bot" | Based on CytoidAPI',
                "#ffffff",
                font=f2c,
            )
            a1 = 1
        a1 = 0
        while a1 < 1:  # 為了收合
            user1 = CytoidData.getUserMostRecentPlay(playerAid)
            user2 = CytoidData.getUserMostRecentPlay(playerBid)
            date1 = f"{re.findall('[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]T[0-9][0-9]:[0-9][0-9]',user1['date'])[0]}  UTC+0"
            score1 = user1["score"]
            score2 = user2["score"]
            acc1 = user1["accuracy"]
            acc2 = user2["accuracy"]
            mods1 = user1["mods"]
            mods2 = user2["mods"]
            perfect1 = user1["details"]["perfect"]
            great1 = user1["details"]["great"]
            good1 = user1["details"]["good"]
            bad1 = user1["details"]["bad"]
            miss1 = user1["details"]["miss"]
            perfect2 = user2["details"]["perfect"]
            great2 = user2["details"]["great"]
            good2 = user2["details"]["good"]
            bad2 = user2["details"]["bad"]
            miss2 = user2["details"]["miss"]
            notes1 = user1["chart"]["notesCount"]
            notes2 = user2["chart"]["notesCount"]
            uid1 = user1["chart"]["id"]
            uid2 = user2["chart"]["id"]
            a1 = 1
        a1 = 0
        key1 = 1
        if uid1 != lid or uid2 != lid:
            key1 = 0
            await ctx.send(
                "遊玩關卡不正確 (wrong chart playing)")
            return
        if key1 == 1:
            while a1 < 1:  # 為了收合
                if uid1 != lid or uid2 != lid:
                    key1 = 0
                num1a = 0
                if miss1 > 0:
                    num1a = 1 / math.sqrt(miss1 / 2)
                num2a = 0
                if miss2 > 0:
                    num2a = 1 / math.sqrt(miss2 / 2)
                num1b = 0.2
                if great1 > 0:
                    num1b = ((notes1 * acc1) - perfect1 -
                             (good1 * 0.3)) / great1
                num2b = 0.2
                if great2 > 0:
                    num2b = ((notes2 * acc2) - perfect2 -
                             (good2 * 0.3)) / great2
                total1 = (
                    (((miss1**2) * (num1a)) /
                     (math.log(notes1, 50)**3) + 0.6 * miss1) *
                    (-1) + (bad1 * (-0.735)) + (good1 * (-0.2)) +
                    (num1b - 0.2) + (perfect1 * 1.05))
                total2 = (
                    (((miss2**2) * (num2a)) /
                     (math.log(notes2, 50)**3) + 0.6 * miss2) *
                    (-1) + (bad2 * (-0.735)) + (good2 * (-0.2)) +
                    (num2b - 0.2) + (perfect2 * 1.05))
                total1a = math.exp((total1 / (notes1 * 1.05)) -
                                   1)
                total2a = math.exp((total2 / (notes2 * 1.05)) -
                                   1)
                a1 = 1
            a1=0
            if a1 < 1:  # Mods
                loc = 190
                if mods1 != None:
                    for i in range(len(mods1)):
                        path = f"./mod/{mods1[i]}.png"
                        modpng = Image.open(path).convert(
                            "RGBA")
                        modpng1 = modpng.resize(
                            (62, 45), Image.LANCZOS)
                        pvpimg.paste(modpng1,
                                     box=(loc, 240),
                                     mask=modpng1)
                        loc = loc + 80
                loc = 190
                if mods2 != None:
                    for i in range(len(mods2)):
                        path = f"./mod/{mods2[i]}.png"
                        modpng = Image.open(path).convert(
                            "RGBA")
                        modpng2 = modpng.resize(
                            (62, 45), Image.LANCZOS)
                        pvpimg.paste(modpng2,
                                     box=(loc, 545),
                                     mask=modpng2)
                        loc = loc + 80
                a1 = 1
            f3 = ImageFont.truetype(
                os.path.abspath(font_path2), 115)
            f4 = ImageFont.truetype(
                os.path.abspath(font_path1), 84)
            f5 = ImageFont.truetype(
                os.path.abspath(font_path1), 88)
            f6 = ImageFont.truetype(
                os.path.abspath(font_path), 45)
            f7 = ImageFont.truetype(
                os.path.abspath(font_path1), 36)
            f8 = ImageFont.truetype(
                os.path.abspath(font_path1), 117)
            f9 = ImageFont.truetype(
                os.path.abspath(font_path4), 160)
            if diff > 15:
                diff = "15+"
            elif diff < 1:
                diff = "？"
            if type == "extreme":
                color = "#FF2D2D"
            elif type == "hard":
                color = "#B15BFF"
            elif type == "easy":
                color = "#4DFFFF"
            drawtext.text((1055, 11),
                          str(diff),
                          color,
                          font=f8)
            drawtext.text((55, 262),
                          "▢",
                          "#2894FF",
                          font=f9)
            drawtext.text((55, 562),
                          "▢",
                          "#2894FF",
                          font=f9)
            drawtext.text((67, 302),
                          "PT",
                          "#9AFF02",
                          font=f3)
            drawtext.text((67, 602),
                          "PT",
                          "#9AFF02",
                          font=f3)
            drawtext.text(
                (233, 293),
                f"{format(total1a*100,'.2f')}%",
                "#ffffff",
                font=f4,
            )
            drawtext.text(
                (233, 593),
                f"{format(total2a*100,'.2f')}%",
                "#ffffff",
                font=f4,
            )
            drawtext.text(
                (240, 407),
                f"{format(total1,'.2f')}",
                "#ffffff",
                font=f7,
            )
            drawtext.text(
                (240, 707),
                f"{format(total2,'.2f')}",
                "#ffffff",
                font=f7,
            )
            drawtext.text((645, 180),
                          str(score1),
                          "#ffffff",
                          font=f5)
            drawtext.text((645, 485),
                          str(score2),
                          "#ffffff",
                          font=f5)
            drawtext.text(
                (1066, 222),
                f"{format(acc1*100,'.2f')}%",
                "#ffffff",
                font=f6,
            )
            drawtext.text(
                (1066, 527),
                f"{format(acc2*100,'.2f')}%",
                "#ffffff",
                font=f6,
            )
            drawtext.text((630, 110),
                          date1,
                          "#ffffff",
                          font=f2b)
            drawtext.text(
                (645, 340),
                f"{perfect1}p / {great1}gr / {good1}g / {bad1}b / {miss1}m",
                "#ffffff",
                font=f2a,
            )
            drawtext.text(
                (645, 645),
                f"{perfect2}p / {great2}gr / {good2}g / {bad2}b / {miss2}m",
                "#ffffff",
                font=f2a,
            )
            pvpimg.save("pvp.png")
            file = discord.File("pvp.png",
                                filename="pvp.png")
            await ctx.send(file=file)
  
    @commands.command()
    async def guess(self, ctx, song_category="-1"):
        song_cates = func.get_song_len() - 1
        if ctx.guild.id is None:
            await ctx.send("無法在此使用此指令")
            return
        if "-1" == str(song_category) or "ran" in str(song_category):
            id = [-1]
        elif "arc" in str(song_category) or "Arc" in str(song_category):
            id = [0]
        elif ("c2" in str(song_category) or "cy2" in str(song_category)
              or "cytus2" in str(song_category) or "ii" in str(song_category)):
            id = [1]
        elif "mai" in str(song_category) or "dx" in str(song_category):
            id = [2]
        elif ("中二" in str(song_category) or "chu" in str(song_category)
              or "Chu" in str(song_category)):
            id = [3]
        elif ("phi" in str(song_category) or "Phi" in str(song_category)
              or "pgr" in str(song_category)):
            id = [4]
        elif "bms" in str(song_category) or "bof" in str(song_category):
            id = [5]
        elif "盤" in str(song_category) or "anota" in str(song_category):
            id = [6]
        elif re.sub(f"[^0-{str(song_cates)}]", "",
                    song_category) == song_category:
            id = re.sub(f"[^0-{str(song_cates)}]", "", song_category)
            id = re.findall(f"[0-{str(song_cates)}]", id)
            list(set(id))
            id = [int(x) for x in id]
        else:
            id = [-1]
        if func.get_cd("guess", ctx.channel.id):
            tip = "> **你選擇的出題範圍是：|"
            for o in range(len(id)):
                if id[o] == -1:
                    tip += " 全題庫 |"
                elif id[o] == 0:
                    tip += " arc |"
                elif id[o] == 1:
                    tip += " c2 |"
                elif id[o] == 2:
                    tip += " mai |"
                elif id[o] == 3:
                    tip += " 中二 |"
                elif id[o] == 4:
                    tip += " phi |"
                elif id[o] == 5:
                    tip += " bof |"
                elif id[o] == 6:
                    tip += " 盤子 |"
            tip += "**\n> 輸入`stop`可中止遊戲\n> 輸入`猜 / $<序號> <猜測的答案>`來搶答 ($4 MAXRAGE)\n\n選擇題庫指令：`dy guess <要選擇的題庫代碼>`        EX:`dy guess 0134`\n0️⃣     Arcaea\n1️⃣     CYTUS II\n2️⃣     maimai\n3️⃣     CHUNITHM\n4️⃣     Phigros\n5️⃣     BOF\n6️⃣     Lanota"
            await ctx.send(tip)
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
            await asyncio.sleep(2)
            await ctx.send(text)

            def check(m):
                return m.channel == ctx.channel

            while len(figure_ans) >= 1:
                try:
                    msg = await self.bot.wait_for("message",timeout=60,check=check)
                    if (len(msg.content) == 1 and msg.content.lower() not in guess_key and not re.match("[\\\/-]", msg.content)):
                        guess_time += 1
                        guess_key += msg.content.lower()
                        time_stamp = int(time.time()) + 56
                        now_time = f"<t:{time_stamp}:R>"
                        cd_time = int(time.time()) + 1
                        cd_time = f"<t:{cd_time}:R>"
                        text = f"> 機器人復活連結：https://ppt.cc/f9ZO1x\n> **Timer:** {now_time}\n> **CD:** {cd_time}\n\n```"
                        for i in range(10):
                            x1 = (i + 1) % 10
                            x2 = int((i + 1 - x1) / 10)
                            white_list = re.sub(
                                f"[^{guess_key.lower()}{guess_key.upper()}]",
                                "ˍ",
                                song_list[i],
                            )
                            if i + 1 in figure_ans:
                                text += f"\n{x2}{x1}. {white_list}"
                            else:
                                text += f"\n{x2}{x1}. {song_list[i]}"
                        ls = list(guess_key)
                        ls.sort()
                        text += f"\n\nGuess Key:{''.join(ls)}```"
                        await ctx.send(text)
                        await asyncio.sleep(5)
                    elif re.match("[猜\$][0-9]+ ", msg.content):
                        try:
                            guess_time += 1
                            fid = re.findall("[0-9]+(?= )", msg.content)
                            if len(fid) >= 1:
                                x = int(fid[0]) - 1
                                gname=["",""]
                                gname[1] = re.sub(f"[猜\$]{fid[0]} ","",msg.content)
                                user = msg.author.display_name
                                matcher1 = difflib.SequenceMatcher(
                                    None, gname[1].lower(),
                                    song_list[x].lower())
                                matcher2 = difflib.SequenceMatcher(
                                    None, gname[1].upper(),
                                    song_list[x].upper())
                                if (re.sub("[^A-Za-z0-9]", "",
                                           gname[1].lower()) == re.sub(
                                               "[^A-Za-z0-9]", "",
                                               song_list[x].lower())
                                        and matcher1.ratio() >= 0.2
                                        or re.sub("[^A-Za-z0-9]", "",
                                                  gname[1].lower()) == re.sub(
                                                      "[^A-Za-z0-9]", "",
                                                      song_list[x].lower())
                                        and matcher2.ratio() >= 0.6):
                                    figure_ans.remove(int(fid[0]))
                                    x1 = (x + 1) % 10
                                    x2 = int((x + 1 - x1) / 10)
                                    song_list[x] = song_list[x] + f"  ({user})"
                                    time_stamp = int(time.time()) + 56
                                    now_time = f"<t:{time_stamp}:R>"
                                    cd_time = int(time.time()) + 1
                                    cd_time = f"<t:{cd_time}:R>"
                                    text = f"> **Timer:** {now_time}\n> **CD:** {cd_time}\n\n```{x2}{x1}. {song_list[x]}```"
                                    await ctx.send(text)
                                elif int(fid[0]) not in figure_ans:
                                    cd_time = int(time.time()) + 1
                                    cd_time = f"<t:{cd_time}:R>"
                                    await ctx.send(
                                        f"> **CD:** {cd_time}\n\n{user}，猜測條目重複 (Repeated Key)"
                                    )
                                else:
                                    cd_time = int(time.time()) + 1
                                    cd_time = f"<t:{cd_time}:R>"
                                    await ctx.send(
                                        f"> **CD:** {cd_time}\n\n{user}，你猜錯了！ (Incorect)"
                                    )
                                await asyncio.sleep(5)
                        except:
                            pass
                    elif len(msg.content) == 1 and str(msg.content).lower() in guess_key:
                        cd_time = int(time.time()) + 1
                        cd_time = f"<t:{cd_time}:R>"
                        await ctx.send(
                            f"> **CD:** {cd_time}\n\n猜測字重複 (Repeated Key)")
                        await asyncio.sleep(5)
                    elif (msg.author == ctx.author and "stop" == msg.content
                          or msg.author.guild_permissions.administrator == True
                          and "stop" == msg.content):
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
                    elif re.match("[\\\/-]", msg.content):
                        cd_time = int(time.time()) + 1
                        cd_time = f"<t:{cd_time}:R>"
                        await ctx.send(
                            f"> **CD:** {cd_time}\n\n無法猜測下列字詞：-   \   /")
                        await asyncio.sleep(5)
                except asyncio.TimeoutError:
                    await ctx.send(f"超時未輸入 (Time out)\n{final_ans}")
                    func.del_cd("guess", ctx.channel.id)
                    return
            if len(figure_ans) == 0:
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
            value=float(value)
            diff=float(diff)
            rank=[100.5,100,99.5,99,98,97,94,90,80]
            mag=[22.4,21.6,21.1,20.8,20.3,20,16.8,15.2,13.6,13.6]
            mag_inr=[22.624,22.512,21.708,21.6,21.1,20.995,20.696,20.592,20.097,19.894,19.6,19.4,16.296,15.792,14.288,13.68,12.24,10.88]
            if value<=101 and value>=0:
                rank.append(value)
                rank.sort(reverse = True)
                index=int(rank.index(value))
                Rpt=diff*mag[index]*value/100
                await ctx.send(f'定數`{diff}`打到`{format(value,".4f")}%`的R值是`{format(Rpt,".1f")}`')
            elif value>101:
                value=value/diff
                mag_inr.append(value)
                mag_inr.sort(reverse = True)
                index=int(mag_inr.index(value))
                if index==0:
                    await ctx.send(f'定數`{diff}`的理論R值是`{format(diff*22.624,".1f")}`')
                    return
                elif (index+1)==len(mag_inr):
                    index=math.floor(index/2)
                    result=value/(mag[index]/100)
                    await ctx.send(f'定數`{diff}`要取得`{format(value*diff,".1f")}`R值必須達到`{format(result,".4f")}`%')
                elif index%2==0:
                    index=int(index/2)-1
                    await ctx.send(f'定數`{diff}`要取得`{format(value*diff,".1f")}`R值必須達到`{rank[index]}`% \n(實得R值：`{format (diff*rank[index]*mag[index]/100,".1f")}`)')
                else:
                    index=math.floor(index/2)
                    result=value/(mag[index]/100)
                    await ctx.send(f'定數`{diff}`要取得`{format(value*diff,".1f")}`R值必須達到`{format(result,".4f")}`%')

    @commands.command()
    async def color(self,ctx,role_name,Color):
        role =  await ctx.guild.create_role(name=str(role_name), colour=discord.Colour.from_str(Color),mentionable=False)
        lv = func.write_role(role.id)
        await role.edit(position=lv)
        await ctx.message.author.add_roles(role)
        
    @commands.command()
    async def reply(self,ctx,g,c,m,txt):
        g = self.bot.get_guild(int(g))
        c = g.get_channel(int(c))
        m = await c.fetch_message(int(m))
        await m.reply(content=txt)
      
async def setup(bot):
    await bot.add_cog(Main(bot))
