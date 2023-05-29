# coding:utf-8
import discord
from discord.ext import commands
import asyncio
import keep_alive
import requests
import json
import re
import random
import math
from PIL import Image, ImageEnhance, ImageFont, ImageDraw, ImageOps, ImageFilter
from io import BytesIO
import os
import string
import demoji
from datetime import datetime
import pytz
import logging

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(
    filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter(
    '%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

tw = pytz.timezone('Asia/Taipei')
twtime = datetime.now(tw)
cutime = twtime.strftime("%F %H:%M:%S")

intents = discord.Intents.all()
intents.message_content = True
bot = commands.Bot(command_prefix=['dy8 ', 'D'], intents=intents)


i = 0


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="dy help"))


@bot.event
async def on_raw_reaction_add(payload):
    global pvpemo1  # 身分驗證
    global pvpemo2  # 是否點選表情
    global pvpemo3  # 回傳點選表情
    global helpemo1
    global helpemo2
    global helpemo3
    if payload.guild_id is None:
        return  # Reaction is on a private message
    channel = bot.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    user = bot.get_user(payload.user_id)
    if str(payload.emoji) == "\U0001F621":
        await message.add_reaction("<:angry:1104806970785018039>")
    print(str(payload.emoji))
    if str(payload.emoji) == "✴️":
        print("123")
        await message.delete()
    if str(payload.emoji) == "\U0001F6D0":
        await message.remove_reaction("\U0001F6D0", user)
        await message.add_reaction("<:lao1:1102149331101954058>")
        await message.add_reaction("<:lao2:1102149279746891786>")
        await message.add_reaction("<:dalaoooo:1070885764608573532>")

    if str(payload.emoji) == "\U000026D4":
        for r in message.reactions:
            async for user in r.users():
                if user.bot == True:
                    await message.remove_reaction(r.emoji, user)
        await message.remove_reaction("\U000026D4", user)

    if str(payload.emoji.name) == "EZ_dy" and user == pvpemo1:
        await message.clear_reaction(emo("ex"))
        await message.clear_reaction(emo("hd"))
        pvpemo1 = "0"
        pvpemo2 = 1
        pvpemo3 = "easy"
    elif str(payload.emoji.name) == "HD_dy" and user == pvpemo1:
        await message.clear_reaction(emo("ex"))
        await message.clear_reaction(emo("ez"))
        pvpemo1 = "0"
        pvpemo2 = 1
        pvpemo3 = "hard"
    elif str(payload.emoji.name) == "EX_dy" and user == pvpemo1:
        await message.clear_reaction(emo("ez"))
        await message.clear_reaction(emo("hd"))
        pvpemo1 = "0"
        pvpemo2 = 1
        pvpemo3 = "extreme"

    if str(payload.emoji.name) == "ZH_dy" and user == helpemo1:
        await message.clear_reaction(emo("en"))
        helpemo1 = "0"
        helpemo2 = 1
        helpemo3 = 1
    elif str(payload.emoji.name) == "EN_dy" and user == helpemo1:
        await message.clear_reaction(emo("zh"))
        helpemo1 = "0"
        helpemo2 = 1
        helpemo3 = 2


@bot.event
async def on_message(message):
    global pvpemo1  # 身分驗證
    global pvpemo2  # 是否點選表情 N/Y = 0/1
    global pvpemo3  # 回傳點選表情
    global helpemo1
    global helpemo2
    global helpemo3  # 中文=1 英文=2
    Help = ["電", "佬", "強", "神", "830395796490158081"]
    tx2 = ["dyliu"]
    tx3 = 0  # 關鍵字判定
    if message.author == bot.user:
        return
    if message.content.startswith('zz'):
        tmp = message.content.split(" ", 2)
        usname = ment(message.author, tmp[1], message.author.guild)
        await message.channel.send(usname)

    if message.content.startswith('說'):
        # 分割訊息成兩份
        tmp = message.content.split("，", 2)
        # 如果分割後串列長度只有1
        if len(tmp) == 1:
            tmg = await message.channel.send("你要我說什麼啦？")
            await asyncio.sleep(3)
            await tmg.delete()
            return
        else:
            for num in tx2:
                for words in Help:
                    if message.content.find(words) >= 0 and message.content.find(num) >= 0 and tx3 < 1:
                        await message.delete()
                        tx3 = 2
            if tx3 > 1:
                nmg = await message.channel.send(f"{message.author.mention}自認是神<:bowdown:889333644202754058><:bowdown:889333644202754058><:bowdown:889333644202754058>")
                await nmg.add_reaction("<:bowdown:889333644202754058>")
            if tx3 < 1:
                await message.delete()
                await message.channel.send(tmp[1])
                te = ment2(message.author, tmp[1], message.author.guild)
                print(te)
                say_txt(message.author, str(te))

                return
    if message.content.startswith('dy'):
        # 分割訊息成兩份
        tmp = re.findall("[^ ]+", message.content)
        # 如果分割後串列長度只有1
        if len(tmp) == 1:
            return
        if len(tmp) == 2:
            if tmp[1].startswith('help'):
                helpemo1 = message.author
                helpemo2 = 0
                helpemo3 = 0
                x3 = 1
                em1 = await message.channel.send('> 請選擇語言 (select language)')
                await em1.add_reaction(emo('zh'))
                await em1.add_reaction(emo('en'))
                await asyncio.sleep(5)
                if helpemo2 == 1:
                    if helpemo3 == 1:
                        embed = discord.Embed(title="指令列表：",
                                              description='**[說，<要機器人說的內容>]**\n\n**[dy rate <譜面id>]**：查看譜面評分詳情\n\n**[dy ping]**：延遲間隔\n\n**[dy ctd <cytoid id>]**：近期遊玩記錄', color=0xffff37)
                    elif helpemo3 == 2:
                        embed = discord.Embed(title="指令列表：",
                                              description="**[say,<what you want dy6ot to say>]**\n\n**[dy rate <level id>]**：check level's rating composing\n\n**[dy ping]**：return ping", color=0xffff37)
                    else:
                        await message.channel.send("發生未知錯誤 (unknown error)")
                        x3 = 0
                else:
                    await em1.delete()
                    await message.channel.send('選擇時間超時 (time out)')
                    x3 = 0
                if x3 == 1:
                    await message.channel.send(embed=embed)
            if tmp[1].startswith('ping'):
                await message.channel.send(f'Ping: {round(bot.latency * 1000)}ms')
            if tmp[1].startswith('random'):
                x2 = 1
                while x2 >= 1:
                    x2 = x2-1
                    url = 'https://services.cytoid.io/levels?sort=creation_date&order=desc&category=all&page=' + \
                        str(random.randrange(1, 201)) + ''
                    res = requests.get(url)
                    jsonstr = json.loads(res.content.decode('utf-8'))
                    leveluid = jsonstr[random.randrange(0, 9)]["uid"]
                    url2 = 'https://services.cytoid.io/levels/' + leveluid + ''
                    res2 = requests.get(url2)
                    jsonstr2 = json.loads(res2.content.decode('utf-8'))
                    if jsonstr2["duration"] >= 200 or "cy7" in leveluid:
                        x2 = x2+1
                cha1 = 0
                dif1 = ""
                while cha1 < len(jsonstr2["charts"]):
                    dif1 = f'{dif1} {jsonstr2["charts"][cha1]["type"]} {jsonstr2["charts"][cha1]["difficulty"]} /'
                    cha1 += 1
                dif1 = re.sub('/$', " ", dif1)
                await message.channel.send(f'{leveluid}\n{dif1}')
        if len(tmp) == 3:
            if tmp[1].startswith('rate'):
                x1 = 1
                if '/' in tmp[2]:
                    x1 = 0
                if '%' in tmp[2]:
                    x1 = 0
                if '#' in tmp[2]:
                    x1 = 0
                if '?' in tmp[2]:
                    x1 = 0
                if '~' in tmp[2]:
                    x1 = 0
                if '\\' in tmp[2]:
                    x1 = 0
                if tmp[2].isupper() == True:
                    x1 = 0
                if x1 == 0:
                    await message.channel.send('不要亂輸入:rage:')
                if x1 == 1:
                    url = 'https://services.cytoid.io/levels/' + \
                        tmp[2]+'/ratings'
                    res = requests.get(url)
                    jsonstr = json.loads(res.content.decode('utf-8'))
                    avg = jsonstr["average"]
                    if jsonstr["total"]-1 < 0:
                        avg = 0
                        await message.channel.send('譜面無人評分或id輸入不正確')
                        return 0
                    tmg = await message.channel.send('正在查詢...')
                    await asyncio.sleep(3)
                    await tmg.delete()
                    clr = 0xFFFFFF
                    score = (60 + avg*jsonstr["total"])/(jsonstr["total"]+10)
                    if score > 1:
                        clr = 0x000000
                    if score > 4.59:
                        clr = 0xFF2D2D
                    if score > 6.95:
                        clr = 0xFF8040
                    if score > 7.39:
                        clr = 0xFFFF37
                    if score > 8.4:
                        clr = 0x53FF53
                    if score > 9.3:
                        clr = 0x4DFFFF
                    if jsonstr["total"]-1 < 0:
                        clr = 0xFFFFFF
                    embed = discord.Embed(title="譜面評分詳情",
                                          description=f'總評分數： {jsonstr["total"]}\n平均分數： {round(avg/2,3)}\n分數構成： {jsonstr["distribution"]}', color=clr)
                    await message.channel.send(embed=embed)
            if tmp[1].startswith('plays'):
                x1 = 1
                if '/' in tmp[2]:
                    x1 = 0
                if '%' in tmp[2]:
                    x1 = 0
                if '#' in tmp[2]:
                    x1 = 0
                if '?' in tmp[2]:
                    x1 = 0
                if '~' in tmp[2]:
                    x1 = 0
                if '\\' in tmp[2]:
                    x1 = 0
                if tmp[2].isupper() == True:
                    x1 = 0
                if x1 == 0:
                    await message.channel.send('不要亂輸入:rage:')
                if x1 == 1:
                    url = 'https://cytoid.io/levels?owner=' + \
                        tmp[2]+'&page=1&sort=plays&order=desc&category=all'
                    res = requests.get(url)
                    res = res.content.decode()

                    str1 = res.split("<script>", 2)
                    str2 = str1[1].split("</script>", 2)
                    str3 = str2[0].split("layout:\"default\",data:[", 2)
                    str4 = str3[1].split("],fetch:", 2)

                    if "levels:[]" in str4[0]:
                        await message.channel.send('使用者id輸入不正確或此人無上傳譜面')
                        return 0

                    tmg = await message.channel.send('正在查詢...')
                    await asyncio.sleep(3)
                    await tmg.delete()

                    play = re.findall('plays:([0-9]*)', str4[0])
                    down = re.findall('downloads:([0-9]*)', str4[0])
                    raw_uid = re.findall('uid:"([0-9a-z._-]*)"', str4[0])
                    url1 = 'https://services.cytoid.io/levels/'+raw_uid[0]
                    res1 = requests.get(url1)
                    js1 = json.loads(res1.content.decode('utf-8'))
                    uid1 = js1["title"]
                    url1 = 'https://services.cytoid.io/levels/'+raw_uid[1]
                    res1 = requests.get(url1)
                    js1 = json.loads(res1.content.decode('utf-8'))
                    uid2 = js1["title"]
                    url1 = 'https://services.cytoid.io/levels/'+raw_uid[2]
                    res1 = requests.get(url1)
                    js1 = json.loads(res1.content.decode('utf-8'))
                    uid3 = js1["title"]

                    embed = discord.Embed(
                        title=f"{tmp[2]}的譜面遊玩數Top3:", description=f'Top1: {uid1}\n遊玩數： {play[0]}\n下載數： {down[0]}\n\nTop2: {uid2}\n遊玩數： {play[1]}\n下載數： {down[1]}\n\nTop3: {uid3}\n遊玩數： {play[2]}\n下載數： {down[2]}', color=0x00ffff)
                    await message.channel.send(embed=embed)
            if tmp[1].startswith('ctd'):
                x1 = 1
                x3 = 1
                # code copyright belongs to akari-bot[github.com/Teahouse-Studios/akari-bot/blob/master/modules/cytoid/rating.py]
                check1 = requests.get(
                    f'https://services.cytoid.io/profile/{tmp[2]}')
                check1a = json.loads(check1.content.decode('utf-8'))
                if 'me' in tmp[2] or re.match(r'<[@!]+[0-9]+>', tmp[2]):
                    tmp[2] = ment(message.author, tmp[2], message.author.guild)
                    tmp[2] = get_ctdid(tmp[2])
                    if 'e404' in tmp[2]:
                        await message.channel.send("無註冊資料，使用`bind ctd <cytoid id>`綁定帳號 (You have not bound yet)")
                        x1 = 0
                elif 'statusCode' in check1a:
                    if check1a['statusCode'] == 404:
                        x1 = 0
                        await message.channel.send('Cytoid ID未正確輸入')
                # end
                if x1 > 0:
                    p1 = requests.get('https://services.cytoid.io/graphql', params={"query": f"""query StudioAnalytics($uid: String = "{tmp[2]}") {{
  profile(uid: $uid) {{
    recentRecords(limit: 1) {{
      ...RecordFragment
    }}
  }}
}}
fragment RecordFragment on UserRecord{{
  chart {{
        difficulty
        type
        name
        level {{
          uid
          title
        }}
        notesCount
      }}
      mods
      score
      accuracy
      rating
      details {{
        perfect
        great
        good
        bad
        miss
        maxCombo
      }}
}}"""})
                    user1 = json.loads(p1.content.decode('utf-8'))
                    score1 = user1["data"]["profile"]["recentRecords"][0]["score"]
                    acc1 = format(
                        user1["data"]["profile"]["recentRecords"][0]["accuracy"]*100, '.3f')
                    rating1 = format(
                        user1["data"]["profile"]["recentRecords"][0]["rating"], '.5f')
                    perfect1 = user1["data"]["profile"]["recentRecords"][0]["details"]["perfect"]
                    great1 = user1["data"]["profile"]["recentRecords"][0]["details"]["great"]
                    good1 = user1["data"]["profile"]["recentRecords"][0]["details"]["good"]
                    bad1 = user1["data"]["profile"]["recentRecords"][0]["details"]["bad"]
                    miss1 = user1["data"]["profile"]["recentRecords"][0]["details"]["miss"]
                    title1 = user1["data"]["profile"]["recentRecords"][0]["chart"]["level"]["title"]
                    uid1 = user1["data"]["profile"]["recentRecords"][0]["chart"]["level"]["uid"]
                    name1 = user1["data"]["profile"]["recentRecords"][0]["chart"]["name"]
                    diff1 = user1["data"]["profile"]["recentRecords"][0]["chart"]["difficulty"]
                    if name1 == None:
                        name1 = title1
                    embed = discord.Embed(
                        title=f"{tmp[2]}'s recent play", description=f'**Song Title**\n{title1}⠀⠀({uid1})\n\n**Type (diff)**\n{name1} ⠀(Lv. {diff1})\n\n**Score (Acc)**\n{score1}⠀⠀({acc1}%)\n\n**Rating**\n{rating1}\n\n**Notes Judgement**\n{perfect1}p / {great1}gr / {good1}g / {bad1}b / {miss1}m', color=0x00ffff)
                    await message.channel.send(embed=embed)
        if len(tmp) == 5:
            if tmp[1].startswith('pvp'):
                x1 = 1
                x3 = 1
                # code copyright belongs to akari-bot[github.com/Teahouse-Studios/akari-bot/blob/master/modules/cytoid/rating.py]
                check1 = requests.get(
                    f'https://services.cytoid.io/profile/{tmp[2]}')
                check1a = json.loads(check1.content.decode('utf-8'))
                if 'me' in tmp[2] or re.match(r'<[@!]+[0-9]+>', tmp[2]):
                    tmp[2] = ment(message.author, tmp[2], message.author.guild)
                    tmp[2] = get_ctdid(tmp[2])
                    if 'e404' in tmp[2]:
                        await message.channel.send("無註冊資料，使用`bind ctd <cytoid id>`綁定帳號 (You have not bound yet)")
                        x1 = 0
                elif 'statusCode' in check1a:
                    if check1a['statusCode'] == 404:
                        x1 = 0
                        await message.channel.send('玩家一Cytoid ID未正確輸入')
                check2 = requests.get(
                    f'https://services.cytoid.io/profile/{tmp[3]}')
                check2a = json.loads(check2.content.decode('utf-8'))
                if 'me' in tmp[3] or re.match(r'<[@!]+[0-9]+>', tmp[3]):
                    tmp[3] = ment(message.author, tmp[3], message.author.guild)
                    tmp[3] = get_ctdid(tmp[3])
                    if 'e404' in tmp[3]:
                        await message.channel.send("無註冊資料，使用`bind ctd <cytoid id>`綁定帳號 (You have not bound yet)")
                        x1 = 0
                elif 'statusCode' in check2a:
                    if check2a['statusCode'] == 404:
                        x1 = 0
                        await message.channel.send('玩家二Cytoid ID未正確輸入')
                # end
                if x1 == 1:
                    check1 = requests.get(
                        f'https://services.cytoid.io/profile/{tmp[2]}')
                    check1a = json.loads(check1.content.decode('utf-8'))
                    check2 = requests.get(
                        f'https://services.cytoid.io/profile/{tmp[3]}')
                    check2a = json.loads(check2.content.decode('utf-8'))
                    x2 = 1
                    url = 'https://services.cytoid.io/levels/' + tmp[4]
                    res = requests.get(url)
                    jsonstr = json.loads(res.content.decode('utf-8'))
                    if jsonstr["duration"] >= 600:
                        await message.channel.send(f'譜面時長超出上限 ({jsonstr["duration"]}秒)')
                        x3 = 0

                    print(len(jsonstr["charts"]))
                    if len(jsonstr["charts"]) > 2:
                        pvpemo1 = message.author
                        pvpemo2 = 0
                        em1 = await message.channel.send('> 請選擇難度 (select diff type)')
                        await em1.add_reaction(emo('ez'))
                        await em1.add_reaction(emo('hd'))
                        await em1.add_reaction(emo('ex'))
                        await asyncio.sleep(5)
                        if pvpemo2 == 1:
                            await message.channel.send(f'請雙方開始遊玩 **{pvpemo3}** 難度 (start game)')

                        else:
                            await em1.delete()
                            await message.channel.send('選擇時間超時 (time out)')
                            x3 = 0

                    if len(jsonstr["charts"]) > 2:
                        for i in range(3):
                            if pvpemo3 in jsonstr["charts"][i]["type"]:
                                type = jsonstr["charts"][i]["type"]
                                diff = jsonstr["charts"][i]["difficulty"]
                                lid = jsonstr["charts"][i]["id"]
                                break
                    elif len(jsonstr["charts"]) > 1:
                        chpe = ["1", "2"]
                        for i in range(2):
                            chpe[i] = jsonstr["charts"][i]["type"]
                        if 'extreme' not in chpe:
                            pvpemo1 = message.author
                            pvpemo2 = 0
                            em1 = await message.channel.send('> 請選擇難度 (select diff type)')
                            await em1.add_reaction(emo('ez'))
                            await em1.add_reaction(emo('hd'))
                            await asyncio.sleep(8)
                            if pvpemo2 == 1:
                                await message.channel.send(f'請雙方開始遊玩 **{pvpemo3}** 難度 (start game)')
                                for i in range(2):
                                    if pvpemo3 in jsonstr["charts"][i]["type"]:
                                        pvpemo3 = "0"
                                        type = jsonstr["charts"][i]["type"]
                                        diff = jsonstr["charts"][i]["difficulty"]
                                        lid = jsonstr["charts"][i]["id"]
                            else:
                                await em1.delete()
                                await message.channel.send('選擇時間超時 (time out)')
                                x3 = 0
                        elif 'hard' not in chpe:
                            pvpemo1 = message.author
                            pvpemo2 = 0
                            em1 = await message.channel.send('> 請選擇難度 (select diff type)')
                            await em1.add_reaction(emo('ez'))
                            await em1.add_reaction(emo('ex'))
                            await asyncio.sleep(8)
                            if pvpemo2 == 1:
                                await message.channel.send(f'請雙方開始遊玩 **{pvpemo3}** 難度 (start game)')
                                for i in range(2):
                                    if pvpemo3 in jsonstr["charts"][i]["type"]:
                                        pvpemo3 = "0"
                                        type = jsonstr["charts"][i]["type"]
                                        diff = jsonstr["charts"][i]["difficulty"]
                                        lid = jsonstr["charts"][i]["id"]
                                pvpemo3 = "0"
                            else:
                                await em1.delete()
                                await message.channel.send('選擇時間超時 (time out)')
                                x3 = 0
                        elif 'easy' not in chpe:
                            pvpemo1 = message.author
                            pvpemo2 = 0
                            em1 = await message.channel.send('> 請選擇難度 (select diff type)')
                            await em1.add_reaction(emo('hd'))
                            await em1.add_reaction(emo('ex'))
                            await asyncio.sleep(8)
                            if pvpemo2 == 1:
                                await message.channel.send(f'請雙方開始遊玩 **{pvpemo3}** 難度 (start game)')
                                for i in range(2):
                                    if pvpemo3 in jsonstr["charts"][i]["type"]:
                                        pvpemo3 = "0"
                                        type = jsonstr["charts"][i]["type"]
                                        diff = jsonstr["charts"][i]["difficulty"]
                                        lid = jsonstr["charts"][i]["id"]
                                pvpemo3 = "0"
                            else:
                                await em1.delete()
                                await message.channel.send('選擇時間超時 (time out)')
                                x3 = 0
                    else:
                        type = jsonstr["charts"][0]["type"]
                        diff = jsonstr["charts"][0]["difficulty"]
                        lid = jsonstr["charts"][0]["id"]
                        await message.channel.send(f'請雙方開始遊玩** {type} **難度 (start game)')
                    if x3 >= 1:
                        length = jsonstr["duration"] + 2-jsonstr["duration"]

                        font_path2 = './jh.ttf'
                        font_path1 = './MPLUSRounded1c-Bold.ttf'
                        font_path = './MPLUSRounded1c-Regular.ttf'
                        font_path3 = './ARIALN.TTF'
                        font_path4 = './NotoSansSC-Medium.otf'
                        font_path5 = './NotoSans-Regular.ttf'

                        level_path = requests.get(jsonstr["cover"]["cover"])
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
                            p1_path = requests.get(
                                check1a["user"]["avatar"]["large"])
                            p1cc = Image.open(BytesIO(p1_path.content))
                            p1img = img_circle(p1cc, 100)
                            p2_path = requests.get(
                                check2a["user"]["avatar"]["large"])
                            p2cc = Image.open(BytesIO(p2_path.content))
                            p2img = img_circle(p2cc, 100)
                            ctr_path = requests.get(
                                jsonstr["owner"]["avatar"]["large"])
                            ctrcc = Image.open(BytesIO(ctr_path.content))
                            ctrimg = img_circle(ctrcc, 124)
                            pvpimg.paste(ctrimg, box=(12, 30), mask=ctrimg)
                            pvpimg.paste(p1img, box=(65, 185), mask=p1img)
                            pvpimg.paste(p2img, box=(65, 490), mask=p2img)
                            pvpimg = pvpimg.convert('RGB')
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
                                os.path.abspath(font_path), 52)
                            h1 = 21
                            print(judge_language(jsonstr["title"]))
                            if 'ja' in judge_language(jsonstr["title"]) or 'zh' in judge_language(jsonstr["title"]):
                                f1 = ImageFont.truetype(
                                    os.path.abspath(font_path4), 67)
                                if len(re.findall('[^\0]', jsonstr["title"])) > 13:
                                    size = 78-round(len(re.findall('[^\0 (\'.~a-z0-9A-Z]', jsonstr["title"]))*1.77+len(re.findall('[()\'.]', jsonstr["title"]))*0.2+len(
                                        re.findall('[ ~a-z0-9]', jsonstr["title"]))*0.75+len(re.findall('[A-Z]', jsonstr["title"]))*1.35)
                                    h1 = h1+round((78-size)/6)
                                    f1 = ImageFont.truetype(
                                        os.path.abspath(font_path4), size)
                            elif 'en' in judge_language(jsonstr["title"]):
                                f1 = ImageFont.truetype(
                                    os.path.abspath(font_path3), 80)
                                if len(re.findall('[^\0]', jsonstr["title"])) > 24:
                                    size = 102 - \
                                        int(len(re.findall(
                                            '[^\0]', jsonstr["title"]))*1.165)
                                    f1 = ImageFont.truetype(
                                        os.path.abspath(font_path3), size)
                                    h1 = h1+round((102-size)/12)
                            title = demoji.replace(jsonstr["title"], "")
                            drawtext.text((150, h1), title, '#ffffff', font=f1)
                            drawtext.text(
                                (188, 178), tmp[2], '#ffffff', font=f2)
                            drawtext.text(
                                (188, 483), tmp[3], '#ffffff', font=f2)
                            drawtext.text(
                                (150, 101), tmp[4], '#ffffff', font=f2a)
                            drawtext.text(
                                (78, 6), 'Generated by "dy6ot bot" | Based on CytoidAPI', '#ffffff', font=f2a)
                            a1 = 1
                        await asyncio.sleep(int(length))
                        p1 = requests.get('https://services.cytoid.io/graphql', params={"query": f"""query StudioAnalytics($uid: String = "{tmp[2]}") {{
  profile(uid: $uid) {{
    recentRecords(limit: 1) {{
      ...RecordFragment
    }}
  }}
}}
fragment RecordFragment on UserRecord{{
  chart {{
        difficulty
        type
        id
        level {{
          uid
          title
        }}
        notesCount
      }}
      mods
      score
      accuracy
      date
      details {{
        perfect
        great
        good
        bad
        miss
        maxCombo
      }}
}}"""})
                        p2 = requests.get('https://services.cytoid.io/graphql', params={"query": f"""query StudioAnalytics($uid: String = "{tmp[3]}") {{
  profile(uid: $uid) {{
    recentRecords(limit: 1) {{
      ...RecordFragment
    }}
  }}
}}
fragment RecordFragment on UserRecord{{
  chart {{
        difficulty
        type
        id
        level {{
          uid
          title
        }}
        notesCount
      }}
      mods
      score
      date
      accuracy
      details {{
        perfect
        great
        good
        bad
        miss
        maxCombo
      }}
}}"""})
                        user1 = json.loads(p1.content.decode('utf-8'))
                        user2 = json.loads(p2.content.decode('utf-8'))
                        date1 = f"{re.findall('[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]T[0-9][0-9]:[0-9][0-9]',user1['data']['profile']['recentRecords'][0]['date'])[0]}  UTC+0"
                        score1 = user1["data"]["profile"]["recentRecords"][0]["score"]
                        score2 = user2["data"]["profile"]["recentRecords"][0]["score"]
                        acc1 = user1["data"]["profile"]["recentRecords"][0]["accuracy"]
                        acc2 = user2["data"]["profile"]["recentRecords"][0]["accuracy"]
                        mods1 = user1["data"]["profile"]["recentRecords"][0]["mods"]
                        mods2 = user2["data"]["profile"]["recentRecords"][0]["mods"]
                        perfect1 = user1["data"]["profile"]["recentRecords"][0]["details"]["perfect"]
                        great1 = user1["data"]["profile"]["recentRecords"][0]["details"]["great"]
                        good1 = user1["data"]["profile"]["recentRecords"][0]["details"]["good"]
                        bad1 = user1["data"]["profile"]["recentRecords"][0]["details"]["bad"]
                        miss1 = user1["data"]["profile"]["recentRecords"][0]["details"]["miss"]
                        perfect2 = user2["data"]["profile"]["recentRecords"][0]["details"]["perfect"]
                        great2 = user2["data"]["profile"]["recentRecords"][0]["details"]["great"]
                        good2 = user2["data"]["profile"]["recentRecords"][0]["details"]["good"]
                        bad2 = user2["data"]["profile"]["recentRecords"][0]["details"]["bad"]
                        miss2 = user2["data"]["profile"]["recentRecords"][0]["details"]["miss"]
                        notes1 = user1["data"]["profile"]["recentRecords"][0]["chart"]["notesCount"]
                        notes2 = user2["data"]["profile"]["recentRecords"][0]["chart"]["notesCount"]
                        uid1 = user1["data"]["profile"]["recentRecords"][0]["chart"]["id"]
                        uid2 = user2["data"]["profile"]["recentRecords"][0]["chart"]["id"]
                        key1 = 1
                        if uid1 != lid or uid2 != lid:
                            key1 = 0
                            await message.channel.send("遊玩關卡不正確 (wrong chart playing)")
                        if key1 == 1:
                            if uid1 != lid or uid2 != lid:
                                key1 = 0
                            num1a = 0
                            if miss1 > 0:
                                num1a = 1/math.sqrt(miss1/2)
                            num2a = 0
                            if miss2 > 0:
                                num2a = 1/math.sqrt(miss2/2)
                            num1b = 0.2
                            if great1 > 0:
                                num1b = (
                                    ((notes1*acc1)-perfect1-(good1*0.3))/great1)
                            num2b = 0.2
                            if great2 > 0:
                                num2b = (
                                    ((notes2*acc2)-perfect2-(good2*0.3))/great2)
                            total1 = (((miss1**2)*(num1a))/(math.log(notes1, 50)**3)+0.6*miss1) * \
                                (-1)+(bad1*(-0.6))+(good1*(-0.1)) + \
                                (num1b-0.2)+(perfect1*0.8)
                            total2 = (((miss2**2)*(num2a))/(math.log(notes2, 50)**3)+0.6*miss2) * \
                                (-1)+(bad2*(-0.6))+(good2*(-0.1)) + \
                                (num2b-0.2)+(perfect2*0.8)
                            total1a = math.exp((total1/(notes1*0.8))-1)
                            total2a = math.exp((total2/(notes2*0.8))-1)
                            a1 = 0
                            if a1 < 1:  # Mods
                                loc = 190
                                if mods1 != None:
                                    for i in range(len(mods1)):
                                        path = f"./mod/{mods1[i]}.png"
                                        modpng = Image.open(
                                            path).convert("RGBA")
                                        modpng1 = modpng.resize(
                                            (62, 45), Image.LANCZOS)
                                        pvpimg.paste(modpng1, box=(
                                            loc, 240), mask=modpng1)
                                        loc = loc+80
                                loc = 190
                                if mods2 != None:
                                    for i in range(len(mods2)):
                                        path = f"./mod/{mods2[i]}.png"
                                        modpng = Image.open(
                                            path).convert("RGBA")
                                        modpng2 = modpng.resize(
                                            (62, 45), Image.LANCZOS)
                                        pvpimg.paste(modpng2, box=(
                                            loc, 545), mask=modpng2)
                                        loc = loc+80
                                a1 = 1

                            f3 = ImageFont.truetype(
                                os.path.abspath(font_path2), 115)
                            f4 = ImageFont.truetype(
                                os.path.abspath(font_path1), 90)
                            f5 = ImageFont.truetype(
                                os.path.abspath(font_path1), 88)
                            f6 = ImageFont.truetype(
                                os.path.abspath(font_path), 45)
                            f7 = ImageFont.truetype(
                                os.path.abspath(font_path1), 36)
                            f8 = ImageFont.truetype(
                                os.path.abspath(font_path1), 122)
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
                            drawtext.text((1033, 11), str(
                                diff), color, font=f8)
                            drawtext.text((55, 262), "▢", '#2894FF', font=f9)
                            drawtext.text((55, 562), "▢", '#2894FF', font=f9)
                            drawtext.text((67, 302), "PT", '#9AFF02', font=f3)
                            drawtext.text((67, 602), "PT", '#9AFF02', font=f3)
                            drawtext.text(
                                (236, 293), f"{format(total1a*100,'.2f')}%", '#ffffff', font=f4)
                            drawtext.text(
                                (236, 593), f"{format(total2a*100,'.2f')}%", '#ffffff', font=f4)
                            drawtext.text(
                                (240, 407), f"{format(total1,'.2f')}", '#ffffff', font=f7)
                            drawtext.text(
                                (240, 707), f"{format(total2,'.2f')}", '#ffffff', font=f7)
                            drawtext.text((655, 180), str(
                                score1), '#ffffff', font=f5)
                            drawtext.text((655, 485), str(
                                score2), '#ffffff', font=f5)
                            drawtext.text(
                                (1066, 222), f"{format(acc1*100,'.2f')}%", '#ffffff', font=f6)
                            drawtext.text(
                                (1066, 527), f"{format(acc2*100,'.2f')}%", '#ffffff', font=f6)
                            drawtext.text(
                                (630, 110), date1, '#ffffff', font=f2b)
                            drawtext.text(
                                (655, 340), f'{perfect1}p / {great1}gr / {good1}g / {bad1}b / {miss1}m', '#ffffff', font=f2)
                            drawtext.text(
                                (655, 645), f'{perfect2}p / {great2}gr / {good2}g / {bad2}b / {miss2}m', '#ffffff', font=f2)
                            pvpimg.save("pvp.png")
                            file = discord.File("pvp.png", filename="pvp.png")
                            await message.channel.send(file=file)
            if tmp[1].startswith('best'):
                x1 = 1
                x3 = 1
                # code copyright belongs to akari-bot[github.com/Teahouse-Studios/akari-bot/blob/master/modules/cytoid/rating.py]
                check1 = requests.get(
                    f'https://services.cytoid.io/profile/{tmp[2]}')
                check1a = json.loads(check1.content.decode('utf-8'))
                if 'me' in tmp[2] or re.match(r'<[@!]+[0-9]+>', tmp[2]):
                    tmp[2] = ment(message.author, tmp[2], message.author.guild)
                    tmp[2] = get_ctdid(tmp[2])
                    if 'e404' in tmp[2]:
                        await message.channel.send("無註冊資料，使用`bind ctd <cytoid id>`綁定帳號 (You have not bound yet)")
                        x1 = 0
                elif 'statusCode' in check1a:
                    if check1a['statusCode'] == 404:
                        x1 = 0
                        await message.channel.send('Cytoid ID未正確輸入 (keyword error)')
                check2 = requests.get(
                    f'https://services.cytoid.io/levels/{tmp[3]}')
                check2a = json.loads(check2.content.decode('utf-8'))
                if 'statusCode' in check2a:
                    if check2a['statusCode'] == 404:
                        x1 = 0
                        await message.channel.send('Level ID未正確輸入 (keyword error)')
                # end
                if "ex" in tmp[4] or "2" in tmp[4] or "xtreme" in tmp[4]:
                    type = "extreme"
                elif "hd" in tmp[4] or "1" in tmp[4] or "ard" in tmp[4]:
                    type = "hard"
                elif "ez" in tmp[4] or "0" in tmp[4] or "asy" in tmp[4]:
                    type = "easy"
                else:
                    x1 = 0
                    await message.channel.send('Diff type未正確輸入 (keyword error)')
                if x1 == 1:
                    x2 = 1
                    str1 = requests.get(
                        f'https://services.cytoid.io/levels/{tmp[3]}/charts/{type}/records?limit=20000')

                    user1 = json.loads(str1.content.decode('utf-8'))
                    x3 = 1
                    if "statusCode" in user1:
                        if user1['statusCode'] == 404:
                            x2 = 0
                            x3 = 0
                            await message.channel.send("沒有此Diff type，請重新確認 (d-type doesn't exist in level)")
                    if x3 > 0:
                        for i in range(len(user1)):
                            if tmp[2] == user1[i]["owner"]["uid"]:
                                score1 = user1[i]["score"]
                                date1 = f'{user1[i]["date"]}  (UTC+0)'
                                acc1 = format(user1[i]["accuracy"]*100, '.3f')
                                perfect1 = user1[i]["details"]["perfect"]
                                great1 = user1[i]["details"]["great"]
                                good1 = user1[i]["details"]["good"]
                                bad1 = user1[i]["details"]["bad"]
                                miss1 = user1[i]["details"]["miss"]
                                rank1 = i+1
                                x2 = 1
                                break
                            else:
                                x2 = 2

                        x3 = 1
                    if x2 == 1:
                        embed = discord.Embed(
                            title=f"{tmp[2]}'s best score", description=f'**Song Title**\n{check2a["title"]}\n\n**Score (Acc)**\n{score1}⠀⠀({acc1}%)\n\n**Notes Judgement**\n{perfect1}p / {great1}gr / {good1}g / {bad1}b / {miss1}m\n\n**RANK**\n#{rank1}\n⠀⠀', color=0x27ff27)
                        embed.set_footer(text=date1)
                        await message.channel.send(embed=embed)
                    else:
                        await message.channel.send("沒有遊玩記錄")
        if len(tmp) == 6:
            if tmp[1].startswith('pvp'):
                x1 = 1
                x3 = 1
                # code copyright belongs to akari-bot[github.com/Teahouse-Studios/akari-bot/blob/master/modules/cytoid/rating.py]
                check1 = requests.get(
                    f'https://services.cytoid.io/profile/{tmp[2]}')
                check1a = json.loads(check1.content.decode('utf-8'))
                if 'me' in tmp[2] or re.match(r'<[@!]+[0-9]+>', tmp[2]):
                    tmp[2] = ment(message.author, tmp[2], message.author.guild)
                    tmp[2] = get_ctdid(tmp[2])
                    if 'e404' in tmp[2]:
                        await message.channel.send("無註冊資料，使用`bind ctd <cytoid id>`綁定帳號 (You have not bound yet)")
                        x1 = 0
                elif 'statusCode' in check1a:
                    if check1a['statusCode'] == 404:
                        x1 = 0
                        await message.channel.send('玩家一Cytoid ID未正確輸入')
                check2 = requests.get(
                    f'https://services.cytoid.io/profile/{tmp[3]}')
                check2a = json.loads(check2.content.decode('utf-8'))
                if 'me' in tmp[3] or re.match(r'<[@!]+[0-9]+>', tmp[3]):
                    tmp[3] = ment(message.author, tmp[3], message.author.guild)
                    tmp[3] = get_ctdid(tmp[3])
                    if 'e404' in tmp[3]:
                        await message.channel.send("無註冊資料，使用`bind ctd <cytoid id>`綁定帳號 (You have not bound yet)")
                        x1 = 0
                elif 'statusCode' in check2a:
                    if check2a['statusCode'] == 404:
                        x1 = 0
                        await message.channel.send('玩家二Cytoid ID未正確輸入')
                check3 = requests.get(
                    f'https://services.cytoid.io/profile/{tmp[4]}')
                check3a = json.loads(check3.content.decode('utf-8'))
                if 'me' in tmp[4] or re.match(r'<[@!]+[0-9]+>', tmp[4]):
                    tmp[4] = ment(message.author, tmp[4], message.author.guild)
                    tmp[4] = get_ctdid(tmp[4])
                    if 'e404' in tmp[4]:
                        await message.channel.send("無註冊資料，使用`bind ctd <cytoid id>`綁定帳號 (You have not bound yet)")
                        x1 = 0
                elif 'statusCode' in check3a:
                    if check3a['statusCode'] == 404:
                        x1 = 0
                        await message.channel.send('玩家三Cytoid ID未正確輸入')

                # end
                if x1 == 1:
                    check1 = requests.get(
                        f'https://services.cytoid.io/profile/{tmp[2]}')
                    check1a = json.loads(check1.content.decode('utf-8'))
                    check2 = requests.get(
                        f'https://services.cytoid.io/profile/{tmp[3]}')
                    check2a = json.loads(check2.content.decode('utf-8'))
                    check3 = requests.get(
                        f'https://services.cytoid.io/profile/{tmp[4]}')
                    check3a = json.loads(check2.content.decode('utf-8'))
                    x2 = 1
                    url = 'https://services.cytoid.io/levels/' + tmp[5]
                    res = requests.get(url)
                    jsonstr = json.loads(res.content.decode('utf-8'))
                    if jsonstr["duration"] >= 240:
                        await message.channel.send(f'譜面時長超出上限 ({jsonstr["duration"]}秒)')
                        x3 = 0
                    if x3 >= 1:
                        length = (jsonstr["duration"])+32
                        if len(jsonstr["charts"]) > 2:
                            if jsonstr["charts"][0]["difficulty"] == jsonstr["charts"][1]["difficulty"] == jsonstr["charts"][2]["difficulty"]:
                                type = "extreme"
                            elif jsonstr["charts"][0]["difficulty"] != jsonstr["charts"][1]["difficulty"] != jsonstr["charts"][2]["difficulty"]:
                                for i in range(3):
                                    if max(jsonstr["charts"][0]["difficulty"], jsonstr["charts"][1]["difficulty"], jsonstr["charts"][2]["difficulty"]) == jsonstr["charts"][i]["difficulty"]:
                                        type = jsonstr["charts"][i]["type"]
                                        break
                            else:
                                for i in range(3):
                                    if max(jsonstr["charts"][0]["difficulty"], jsonstr["charts"][1]["difficulty"], jsonstr["charts"][2]["difficulty"]) == jsonstr["charts"][i]["difficulty"]:
                                        type = jsonstr["charts"][i]["type"]
                                        break
                        elif len(jsonstr["charts"]) > 1:
                            if jsonstr["charts"][0]["difficulty"] == jsonstr["charts"][1]["difficulty"]:
                                for i in range(2):
                                    if max(ord(jsonstr["charts"][0]["type"][2]), ord(jsonstr["charts"][1]["type"][2])) == ord(jsonstr["charts"][i]["type"][2]):
                                        type = jsonstr["charts"][i]["type"]
                                        break
                            elif jsonstr["charts"][0]["difficulty"] != jsonstr["charts"][1]["difficulty"]:
                                for i in range(2):
                                    if max(jsonstr["charts"][0]["difficulty"], jsonstr["charts"][1]["difficulty"]) == jsonstr["charts"][i]["difficulty"]:
                                        type = jsonstr["charts"][i]["type"]
                                        break
                        else:
                            type = jsonstr["charts"][0]["type"]
                        await message.channel.send(f'請三方遊玩{type}難度，並在譜面時長({jsonstr["duration"]})+20秒內上傳遊玩分數')
                        await asyncio.sleep(int(length))
                        p1 = requests.get('https://services.cytoid.io/graphql', params={"query": f"""query StudioAnalytics($uid: String = "{tmp[2]}") {{
  profile(uid: $uid) {{
    recentRecords(limit: 1) {{
      ...RecordFragment
    }}
  }}
}}
fragment RecordFragment on UserRecord{{
  chart {{
        difficulty
        type
        level {{
          uid
          title
        }}
        notesCount
      }}
      mods
      score
      accuracy
      details {{
        perfect
        great
        good
        bad
        miss
        maxCombo
      }}
}}"""})
                        p2 = requests.get('https://services.cytoid.io/graphql', params={"query": f"""query StudioAnalytics($uid: String = "{tmp[3]}") {{
  profile(uid: $uid) {{
    recentRecords(limit: 1) {{
      ...RecordFragment
    }}
  }}
}}
fragment RecordFragment on UserRecord{{
  chart {{
        difficulty
        type
        level {{
          uid
          title
        }}
        notesCount
      }}
      mods
      score
      accuracy
      details {{
        perfect
        great
        good
        bad
        miss
        maxCombo
      }}
}}"""})
                        p3 = requests.get('https://services.cytoid.io/graphql', params={"query": f"""query StudioAnalytics($uid: String = "{tmp[4]}") {{
  profile(uid: $uid) {{
    recentRecords(limit: 1) {{
      ...RecordFragment
    }}
  }}
}}
fragment RecordFragment on UserRecord{{
  chart {{
        difficulty
        type
        level {{
          uid
          title
        }}
        notesCount
      }}
      mods
      score
      accuracy
      details {{
        perfect
        great
        good
        bad
        miss
        maxCombo
      }}
}}"""})
                        user1 = json.loads(p1.content.decode('utf-8'))
                        user2 = json.loads(p2.content.decode('utf-8'))
                        user3 = json.loads(p3.content.decode('utf-8'))
                        score1 = user1["data"]["profile"]["recentRecords"][0]["score"]
                        score2 = user2["data"]["profile"]["recentRecords"][0]["score"]
                        score3 = user3["data"]["profile"]["recentRecords"][0]["score"]
                        acc1 = user1["data"]["profile"]["recentRecords"][0]["accuracy"]
                        acc2 = user2["data"]["profile"]["recentRecords"][0]["accuracy"]
                        acc3 = user3["data"]["profile"]["recentRecords"][0]["accuracy"]
                        perfect1 = user1["data"]["profile"]["recentRecords"][0]["details"]["perfect"]
                        great1 = user1["data"]["profile"]["recentRecords"][0]["details"]["great"]
                        good1 = user1["data"]["profile"]["recentRecords"][0]["details"]["good"]
                        bad1 = user1["data"]["profile"]["recentRecords"][0]["details"]["bad"]
                        miss1 = user1["data"]["profile"]["recentRecords"][0]["details"]["miss"]
                        perfect3 = user3["data"]["profile"]["recentRecords"][0]["details"]["perfect"]
                        great3 = user3["data"]["profile"]["recentRecords"][0]["details"]["great"]
                        good3 = user3["data"]["profile"]["recentRecords"][0]["details"]["good"]
                        bad3 = user3["data"]["profile"]["recentRecords"][0]["details"]["bad"]
                        miss3 = user3["data"]["profile"]["recentRecords"][0]["details"]["miss"]
                        perfect2 = user2["data"]["profile"]["recentRecords"][0]["details"]["perfect"]
                        great2 = user2["data"]["profile"]["recentRecords"][0]["details"]["great"]
                        good2 = user2["data"]["profile"]["recentRecords"][0]["details"]["good"]
                        bad2 = user2["data"]["profile"]["recentRecords"][0]["details"]["bad"]
                        miss2 = user2["data"]["profile"]["recentRecords"][0]["details"]["miss"]
                        notes1 = user1["data"]["profile"]["recentRecords"][0]["chart"]["notesCount"]
                        notes2 = user2["data"]["profile"]["recentRecords"][0]["chart"]["notesCount"]
                        notes3 = user3["data"]["profile"]["recentRecords"][0]["chart"]["notesCount"]
                        num1a = 0
                        if miss1 > 0:
                            num1a = 1/math.sqrt(miss1/2)
                        num2a = 0
                        if miss2 > 0:
                            num2a = 1/math.sqrt(miss2/2)
                        num3a = 0
                        if miss3 > 0:
                            num3a = 1/math.sqrt(miss3/2)
                        num1b = 0
                        if great1 > 0:
                            num1b = (
                                ((notes1*acc1)-perfect1-(good1*0.3))/great1)
                        num2b = 0
                        if great2 > 0:
                            num2b = (
                                ((notes2*acc2)-perfect2-(good2*0.3))/great2)
                        num3b = 0
                        if great3 > 0:
                            num3b = (
                                ((notes3*acc3)-perfect3-(good3*0.3))/great3)
                        total1 = (((miss1**2)*(num1a))/(math.log(notes1, 50)**3)+0.6*miss1) * \
                            (-1)+(bad1*(-0.6))+(good1*(-0.1)) + \
                            (num1b-0.2)+(perfect1*0.8)
                        total2 = (((miss2**2)*(num2a))/(math.log(notes2, 50)**3)+0.6*miss2) * \
                            (-1)+(bad2*(-0.6))+(good2*(-0.1)) + \
                            (num2b-0.2)+(perfect2*0.8)
                        total3 = (((miss3**2)*(num3a))/(math.log(notes3, 50)**3)+0.6*miss3) * \
                            (-1)+(bad3*(-0.6))+(good3*(-0.1)) + \
                            (num3b-0.2)+(perfect3*0.8)

                        await message.channel.send(f".....................\n{tmp[2]}的加權總分是：{format(total1,'.3f')}\n分數：{score1}   acc：{format(acc1*100,'.3f')}%\n.....................")
                        await message.channel.send(f"{tmp[3]}的加權總分是：{format(total2,'.3f')}\n分數：{score2}   acc：{format(acc2 *100,'.3f')}%")
                        await message.channel.send(f".....................\n{tmp[4]}的加權總分是：{format(total3,'.3f')}\n分數：{score3}   acc：{format(acc3*100,'.3f')}%")

    if message.content.startswith('bind'):
        tmp = message.content.split(" ", 5)
        if len(tmp) == 3:
            if tmp[1].startswith('ctd'):
                x1 = 1
                check1 = requests.get(
                    f'https://services.cytoid.io/profile/{tmp[2]}')
                check1a = json.loads(check1.content.decode('utf-8'))
                if 'statusCode' in check1a:
                    if check1a['statusCode'] == 404:
                        x1 = 0
                        await message.channel.send('Cytoid ID未正確輸入 (keyword error)')
                if x1 == 1:
                    work = write_ctdid(str(message.author), tmp[2])
                    if 'e405' in work:
                        id = re.sub('e405：', "", work)
                        await message.channel.send(f'已經綁定了，你的Cytoid ID是{id} (already binded)')
                    elif 'e200' in work:
                        await message.channel.send('綁定成功！ (Success!)')

    if message.content.startswith('unbind'):
        tmp = message.content.split(" ", 5)
        if len(tmp) == 2:
            if tmp[1].startswith('ctd'):
                x1 = 1
                if x1 == 1:
                    work = delete_ctdid(str(message.author))
                    if 'e404' in work:
                        await message.channel.send("無註冊資料，使用`bind ctd <cytoid id>`綁定帳號 (You have not bound yet)")
                    elif 'e200' in work:
                        await message.channel.send('解除綁定成功！ (Success!)')

def img_circle(fpath, img_width):
    x = img_width
    r = int(x/2)

    # turn src image to square with x width
    img_src = fpath.convert("RGBA")
    img_src = img_src.resize((x, x), Image.LANCZOS)

    # create a new pinture which is used for return value
    img_return = Image.new('RGBA', (x, x), (255, 255, 255, 0))

    # create a white picture,alpha tunnuel is 100% transparent
    img_white = Image.new('RGBA', (x, x), (255, 255, 255, 0))

    # create the objects link to the pixel matrix of img
    p_src = img_src.load()
    p_return = img_return.load()
    p_white = img_white.load()

    # set the pixels of the return picture
    for i in range(x):
        for j in range(x):
            lx = abs(i-r)
            ly = abs(j-r)
            l = (pow(lx, 2) + pow(ly, 2)) ** 0.5

            if l < r:
                p_return[i, j] = p_src[i, j]
            if l > r:
                p_return[i, j] = p_white[i, j]
    return img_return


remove_nota = u'[’·°–!\"#$%&\'()*+,-.\/:;<=>?@，。?★、…【】（）《》？“”‘’！\[\\\]^_`{|}~]+'
remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)


def filter_str(sentence):
    sentence = re.sub(remove_nota, '', sentence)
    sentence = sentence.translate(remove_punctuation_map)
    return sentence.strip()

# 判断中日韩英


def judge_language(s):
    # s = unicode(s)   # python2需要将字符串转换为unicode编码，python3不需要
    s = filter_str(s)
    result = []
    s = re.sub('[0-9]', '', s).strip()
    # unicode english
    re_words = re.compile(u"[a-zA-Z]")
    res = re.findall(re_words, s)  # 查询出所有的匹配字符串
    res2 = re.sub('^[a-zA-Z ]+$', '', s).strip()
    if len(res2) <= 0:
        return 'en'

    # unicode chinese
    re_words = re.compile(u"[\u4e00-\u9fa5]+")
    res = re.findall(re_words, s)  # 查询出所有的匹配字符串
    res2 = re.sub(u"[\u4e00-\u9fa5]+", '', s).strip()
    if len(res) > 0:
        result.append('zh')
    if len(res2) <= 0:
        return 'zh'

    # unicode korean
    re_words = re.compile(u"[\uac00-\ud7ff]+")
    res = re.findall(re_words, s)  # 查询出所有的匹配字符串
    res2 = re.sub(u"[\uac00-\ud7ff]+", '', s).strip()
    if len(res) > 0:
        result.append('ko')
    if len(res2) <= 0:
        return 'ko'

    # unicode japanese katakana and unicode japanese hiragana
    re_words = re.compile(u"[\u30a0-\u30ff\u3040-\u309f]+")
    res = re.findall(re_words, s)  # 查询出所有的匹配字符串
    res2 = re.sub(u"[\u30a0-\u30ff\u3040-\u309f]+", '', s).strip()
    if len(res) > 0:
        result.append('ja')
    if len(res2) <= 0:
        return 'ja'
    return ','.join(result)


def ment(m, user, g):
    if re.match(r'<[@!&]+[0-9]+>', user):
        id1 = re.findall('[0-9]+', user)
        return g.get_member(int(id1[0]))
    else:
        return user


def ment2(m, user, g):
    a1 = 1
    t = user
    if a1 == 1:
        q1 = re.findall(r'<[@!&]+[0-9]+>', user)
        for i in range(len(q1)):
            men = ment(m, q1[i], g)
            t = user.replace(q1[i], f'@{men}')
        return t


def filter_emoji(desstr, restr=''):
    # 过滤表情
    try:
        co = re.compile(u'[\U00010000-\U0010ffff]')
    except re.error:
        co = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')
    return co.sub(restr, desstr)


def emo(str):
    if "ez" in str:
        return "<:EZ_dy:1110475152568877066>"
    if "hd" in str:
        return "<:HD_dy:1110471797054390322>"
    if "ex" in str:
        return "<:EX_dy:1110471814490095689>"
    if "zh" in str:
        return "<:ZH_dy:1110841690673123399>"
    if "en" in str:
        return "<:EN_dy:1110841918956511283>"


def get_ctdid(user):
    with open("./member.txt", 'r') as b:
        f = b.read()
        str1 = f.split(",", 200)
        key = 0
        for i in range(len(str1)):
            name1 = re.findall('[^\0]+#[0-9][0-9][0-9][0-9]', str1[i])
            if str(user) in name1:
                key = 1
                id_ = str1[i].split(":", 2)
                id = id_[1]
        if key == 1:
            return id
        else:
            return 'e404'
    b.close()


def write_ctdid(user, ctdid):
    with open("./member.txt", 'r') as b:
        f = b.read()
        str1 = f.split(",", 200)
        key = 0
        for i in range(len(str1)):
            name1 = re.findall('[^\0]+#[0-9][0-9][0-9][0-9]', str1[i])
            if str(user) in name1:
                key = 1
                id_ = str1[i].split(":", 2)
                id = id_[1]
        if key == 1:
            key2 = 0
        else:
            key2 = 1
    b.close()
    with open("./member.txt", 'a') as b1:
        if key2 == 1:
            new = ","+str(user)+":"+ctdid
            b1.write(new)
            return 'e200'
        else:
            return f'e405：{id}'
    b1.close()


def delete_ctdid(user):
    with open("./member.txt", 'r') as b:
        f = b.read()
        str1 = f.split(",", 200)
        key = 0
        for i in range(len(str1)):
            name1 = re.findall('[^\0]+#[0-9][0-9][0-9][0-9]', str1[i])
            if str(user) in name1:
                key = 1
        if key == 1:
            key2 = 1
        else:
            key2 = 0
            return 'e404'
    b.close()
    with open("./member.txt", 'a') as b1:
        if key2 == 1:
            reg1 = f',{str(user)}:[^,]+'
            del1 = re.sub(reg1, "", f)
            b1.write(del1)
            return 'e200'
    b1.close()


def say_txt(ctdid, user):
    key2 = 1
    with open("./say.txt", 'a') as b1:
        if key2 == 1:
            new = cutime+" | " + str(ctdid)+"說："+user+"\n"
            b1.write(new)
            return 'e200'
    b1.close()


keep_alive.keep_alive()
bot.run('BOT TOKEN')
