# coding:utf-8
import core1.coin as coin
import core1.CytoidData as CytoidData
import matplotlib.pyplot as plt
import traceback
import sys
import pytz
import time
from datetime import datetime, timedelta
import demoji
import string
import discord
import requests
import json
import re
import random
import math
from PIL import Image, ImageEnhance, ImageFont, ImageDraw, ImageOps, ImageFilter
from io import BytesIO
import os
os.environ['MPLCONFIGDIR'] = os.getcwd() + "/configs/"


def custom_randint(x, y):
    # 檢查 x 和 y 的差值是否大於等於 4
    if y - x >= 4:
        # 計算切割點 cut_num
        cut_num = math.ceil((x + y) / 2)

        # 計算兩個區間的整數數量
        first_interval_count = cut_num - x
        second_interval_count = y - cut_num + 1

        # 計算兩個區間的機率
        first_interval_prob = 0.5 / first_interval_count
        second_interval_prob = 0.5 / second_interval_count

        # 隨機選擇區間並返回結果
        if random.random() < 0.5:
            return random.randint(x, cut_num)
        else:
            return random.randint(cut_num, y)
    else:
        # 差值小於 4 時，使用原始的 randint
        return random.randint(x, y)


def getCurrentDay(gmt, now=None):
    if now is None:
        current_time = datetime.now()
    else:
        current_time = now
    time_with_offset = current_time + timedelta(hours=float(gmt))
    return str(time_with_offset.day)


def keep_chart(data, count):
    if count > len(data):
        count = len(data)
    last_five_dates = list(data.keys())[-count:]
    labels = last_five_dates
    epd_list = []
    for date in last_five_dates:
        total_amount = sum(item[1] for item in data[date])  # 計算金額總和
        epd_list.append(total_amount)  # 加入金額總和到陣列
    heights = epd_list
    sum_epd = sum(epd_list)
    avg_epd = sum_epd / count
    max_rate = max(epd_list)
    clr = 0xFFFFFF
    plt.style.use("dark_background")
    plt.figure(figsize=(5, 3))
    plt.plot(labels, heights, marker="o", color="#{:06X}".format(clr))
    plt.axhline(
        avg_epd,
        color="#{:06X}".format(clr),
        linestyle="dashed",
        linewidth=1,
        label=f"Avg epd: {avg_epd:.2f}",
    )
    plt.xticks(labels, [str(label.split("/")[1])
               for label in labels], fontsize=8)
    plt.plot([], [], " ", label=f"Total epd: {sum_epd}")
    plt.legend(bbox_to_anchor=(0.63, 1.38),
               loc='upper left',
               markerfirst=False,
               alignment="center")
    for label, height in zip(labels, heights):
        if height == max_rate:
            plt.text(
                label,
                height - max_rate * 0.15,
                str(height),
                ha="center",
                va="top",
                fontsize=8,
            )
            continue
        plt.text(
            label,
            height + max_rate * 0.1,
            str(height),
            ha="center",
            va="bottom",
            fontsize=8,
        )
    plt.tight_layout()
    plt.savefig("photo/keep1.png")


def plot_line_chart2(rates_list, url, title01, author):
    labels = [0.5 * i for i in range(1, 11)]
    heights = rates_list
    total_rates = sum(rates_list)
    sum_rate = sum([label * rate for label, rate in zip(labels, rates_list)])
    avg_rate = sum_rate / total_rates
    max_rate = max(rates_list)
    clr = 0xFFFFFF
    score = (60 + sum_rate * 2) / (total_rates + 10)
    if score > 1:
        clr = 0x777777
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
    if total_rates < 1:
        clr = 0xFFFFFF
    plt.style.use("dark_background")
    plt.figure(figsize=(5, 3))
    plt.plot(labels, heights, marker="o", color="#{:06X}".format(clr))
    plt.axvline(
        avg_rate,
        color="#{:06X}".format(clr),
        linestyle="dashed",
        linewidth=1,
        label=f"Avg rate: {avg_rate:.2f}",
    )
    plt.xticks(labels, [str(label) for label in labels], fontsize=8)
    plt.plot([], [], " ", label=f"Total rates: {total_rates}")
    plt.legend(bbox_to_anchor=(0.63, 1.38),
               loc='upper left',
               markerfirst=False,
               alignment="center")
    for label, height in zip(labels, heights):
        if height == max_rate:
            plt.text(
                label,
                height - max_rate * 0.15,
                str(height),
                ha="center",
                va="top",
                fontsize=8,
            )
            continue
        plt.text(
            label,
            height + max_rate * 0.1,
            str(height),
            ha="center",
            va="bottom",
            fontsize=8,
        )
    plt.tight_layout()
    plt.savefig("photo/cache1.png")
    font_path = "font/MPLUSRounded1c-Regular.ttf"
    font_path3 = "font/ARIALN.TTF"
    font_path4 = "font/NotoSansSC-Medium.otf"
    font_path5 = "font/NotoSans-Regular.ttf"
    level_path = requests.get(url)
    ctrcc = Image.open(BytesIO(level_path.content)).convert("RGBA")
    ctrimg = img_circle(ctrcc, 52)
    result_image = Image.new('RGB', (500, 270))
    chart_img = Image.open("./photo/cache1.png").convert("RGBA")
    result_image.paste(chart_img, box=(5, -28), mask=chart_img)
    result_image.paste(ctrimg, box=(15, 10), mask=ctrimg)
    drawtext = ImageDraw.Draw(result_image)
    if "ja" in judge_language(title01) or "zh" in judge_language(title01):
        f1 = ImageFont.truetype(os.path.abspath(font_path4), 27)
    else:
        f1 = ImageFont.truetype(os.path.abspath(font_path5), 30)
    f2 = ImageFont.truetype(os.path.abspath(font_path), 14)

    title = demoji.replace(title01, "")
    title = title if len(title) < 15 else str(title[:12] + "...")
    drawtext.text((77, 6), title, "#ffffff", font=f1)
    drawtext.text((79, 42), author, "#ffffff", font=f2)
    result_image.save("./photo/cache1.png")


def plot_line_chart3(rates_list, url, title01):
    labels = [0.5 * i for i in range(1, 11)]
    heights = rates_list
    total_rates = sum(rates_list)
    sum_rate = sum([label * rate for label, rate in zip(labels, rates_list)])
    avg_rate = sum_rate / total_rates
    max_rate = max(rates_list)
    clr = 0xFFFFFF
    score = (60 + sum_rate * 2) / (total_rates + 10)
    if score > 1:
        clr = 0x777777
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
    if total_rates < 1:
        clr = 0xFFFFFF
    plt.style.use("dark_background")
    plt.figure(figsize=(5, 2))
    plt.plot(labels, heights, marker="o", color="#{:06X}".format(clr))
    plt.axvline(
        avg_rate,
        color="#{:06X}".format(clr),
        linestyle="dashed",
        linewidth=1,
        label=f"Avg rate: {avg_rate:.2f}",
    )
    plt.xticks(labels, [str(label) for label in labels], fontsize=8)
    plt.plot([], [], " ", label=f"Total rates: {total_rates}")
    plt.legend(markerfirst=False, alignment="left")
    for label, height in zip(labels, heights):
        if height == max_rate:
            plt.text(
                label,
                height - max_rate * 0.15,
                str(height),
                ha="center",
                va="top",
                fontsize=8,
            )
            continue
        plt.text(
            label,
            height + max_rate * 0.1,
            str(height),
            ha="center",
            va="bottom",
            fontsize=8,
        )
    plt.savefig("./photo/cache1.png")
    font_path3 = "font/ARIALN.TTF"
    font_path4 = "font/NotoSansSC-Medium.otf"
    font_path5 = "font/NotoSans-Regular.ttf"
    level_path = requests.get(url)
    ctrcc = Image.open(BytesIO(level_path.content)).convert("RGBA")
    ctrimg = img_circle(ctrcc, 48)
    result_image = Image.new('RGB', (478, 250))
    chart_img = Image.open("./photo/cache1.png").convert("RGBA")
    result_image.paste(chart_img, box=(13, 40), mask=chart_img)
    result_image.paste(ctrimg, box=(12, 5), mask=ctrimg)
    drawtext = ImageDraw.Draw(result_image)
    if "ja" in judge_language(title01) or "zh" in judge_language(title01):
        f1 = ImageFont.truetype(os.path.abspath(font_path4), 20)
    else:
        f1 = ImageFont.truetype(os.path.abspath(font_path5), 24)
    title = demoji.replace(title01, "")
    drawtext.text((72, 2), title, "#ffffff", font=f1)
    result_image.save("./photo/cache1.png")


def getChartInfoEmbed(chart_data):
    cha1 = 0
    dif1 = ""
    while cha1 < len(chart_data["charts"]):
        dif1 = f'{dif1} {chart_data["charts"][cha1]["type"]} {chart_data["charts"][cha1]["difficulty"]} /'
        cha1 += 1
    dif1 = re.sub("/$", "", dif1)
    dif1 = re.sub("^ ", "", dif1)
    rating_data = CytoidData.getRateDistribution(chart_data["uid"])
    result = "N/A" if rating_data["average"] is None else f'{"{:0.2f}".format(rating_data["average"] / 2, 2)} ({rating_data["total"]})'
    embed = discord.Embed(
        title=chart_data["uid"],
        description=f'**Title**\n{chart_data["title"]}\n\n**Difficulty**\n{dif1}\n\n**Length**\n{stmtime(chart_data["duration"])}\n\n**Rate**\n{result}',
        color=0xFFFF28,
        url=f'https://dyliu0306.github.io/run-cytoid?&levels={chart_data["uid"]}',
    )
    embed.set_thumbnail(url=chart_data["cover"]["cover"])
    embed.set_footer(text="Click link to open Cytoid")
    embed.set_author(
        name=chart_data["owner"]["uid"],
        icon_url=chart_data["owner"]["avatar"]["small"],
    )
    return embed


def plot_line_chart(rates_list, url, title01, download, play):
    labels = [0.5 * i for i in range(1, 11)]
    heights = rates_list
    total_rates = sum(rates_list)
    sum_rate = sum([label * rate for label, rate in zip(labels, rates_list)])
    avg_rate = sum_rate / total_rates
    max_rate = max(rates_list)
    clr = 0xFFFFFF
    score = (60 + sum_rate * 2) / (total_rates + 10)
    if score > 1:
        clr = 0x777777
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
    if total_rates < 1:
        clr = 0xFFFFFF
    plt.style.use("dark_background")
    plt.figure(figsize=(5, 2))
    plt.plot(labels, heights, marker="o", color="#{:06X}".format(clr))
    plt.axvline(
        avg_rate,
        color="#{:06X}".format(clr),
        linestyle="dashed",
        linewidth=1,
        label=f"Avg rate: {avg_rate:.2f}",
    )
    plt.xticks(labels, [str(label) for label in labels], fontsize=8)
    plt.plot([], [], " ", label=f"Total rates: {total_rates}")
    plt.plot([], [], " ", label=f"D-Loads: {download} ")
    plt.plot([], [], " ", label=f"Plays: {play}")
    plt.legend(markerfirst=False, alignment="left", fontsize=8)
    for label, height in zip(labels, heights):
        if height == max_rate:
            plt.text(
                label,
                height - max_rate * 0.15,
                str(height),
                ha="center",
                va="top",
                fontsize=8,
            )
            continue
        plt.text(
            label,
            height + max_rate * 0.1,
            str(height),
            ha="center",
            va="bottom",
            fontsize=8,
        )
    plt.savefig("photo/cache1.png")
    font_path4 = "font/NotoSansSC-Medium.otf"
    font_path5 = "font/NotoSans-Regular.ttf"
    level_path = requests.get(url)
    ctrcc = Image.open(BytesIO(level_path.content)).convert("RGB")
    ctrimg = img_circle(ctrcc, 37)
    pvpimg = Image.open("./photo/cache1.png")
    pvpimg = pvpimg.convert("RGB")
    pvpimg.paste(ctrimg, box=(4, 3), mask=ctrimg)
    drawtext = ImageDraw.Draw(pvpimg)
    if "ja" in judge_language(title01) or "zh" in judge_language(title01):
        f1 = ImageFont.truetype(os.path.abspath(font_path4), 15)
    elif "en" in judge_language(title01):
        f1 = ImageFont.truetype(os.path.abspath(font_path5), 15)
    else:
        f1 = ImageFont.truetype(os.path.abspath(font_path5), 15)
    title = demoji.replace(title01, "")
    drawtext.text((65, 0), title, "#ffffff", font=f1)
    pvpimg.save("./photo/cache1.png")


def filter_str(sentence):
    remove_nota = "[’·°–!\"#$%&'()*+,-.\/:;<=>?@，。?★、…【】（）《》？“”‘’！\[\\\]^_`{|}~]+"
    remove_punctuation_map = dict(
        (ord(char), None) for char in string.punctuation)
    sentence = re.sub(remove_nota, "", sentence)
    sentence = sentence.translate(remove_punctuation_map)
    return sentence.strip()


def judge_language(s):
    # s = unicode(s)   # python2需要将字符串转换为unicode编码，python3不需要
    s = filter_str(s)
    result = []
    s = re.sub("[0-9]", "", s).strip()
    # unicode english
    re_words = re.compile("[a-zA-Z]")
    res = re.findall(re_words, s)  # 查询出所有的匹配字符串
    res2 = re.sub("^[a-zA-Z ]+$", "", s).strip()
    if len(res2) <= 0:
        return "en"

    # unicode chinese
    re_words = re.compile("[\u4e00-\u9fa5]+")
    res = re.findall(re_words, s)  # 查询出所有的匹配字符串
    res2 = re.sub("[\u4e00-\u9fa5]+", "", s).strip()
    if len(res) > 0:
        result.append("zh")
    if len(res2) <= 0:
        return "zh"

    # unicode korean
    re_words = re.compile("[\uac00-\ud7ff]+")
    res = re.findall(re_words, s)  # 查询出所有的匹配字符串
    res2 = re.sub("[\uac00-\ud7ff]+", "", s).strip()
    if len(res) > 0:
        result.append("ko")
    if len(res2) <= 0:
        return "ko"

    # unicode japanese katakana and unicode japanese hiragana
    re_words = re.compile("[\u30a0-\u30ff\u3040-\u309f]+")
    res = re.findall(re_words, s)  # 查询出所有的匹配字符串
    res2 = re.sub("[\u30a0-\u30ff\u3040-\u309f]+", "", s).strip()
    if len(res) > 0:
        result.append("ja")
    if len(res2) <= 0:
        return "ja"
    return ",".join(result)


def hack_txt(id):
    id = str(id)

    with open("./text/hack.txt", "rb") as hack_histroy_file:
        hack_histroy = hack_histroy_file.read().decode("utf-8")
        if id in hack_histroy:
            return False

    with open("./text/hack.txt", "a") as hack_histroy_file:
        hack_histroy_file.write("," + id)

    return True


def img_circle(fpath, img_width):
    x = img_width
    r = int(x / 2)

    # turn src image to square with x width
    img_src = fpath.convert("RGBA")
    img_src = img_src.resize((x, x), Image.LANCZOS)

    # create a new pinture which is used for return value
    img_return = Image.new("RGBA", (x, x), (255, 255, 255, 0))

    # create a white picture,alpha tunnuel is 100% transparent
    img_white = Image.new("RGBA", (x, x), (255, 255, 255, 0))

    # create the objects link to the pixel matrix of img
    p_src = img_src.load()
    p_return = img_return.load()
    p_white = img_white.load()

    # set the pixels of the return picture
    for i in range(x):
        for j in range(x):
            lx = abs(i - r)
            ly = abs(j - r)
            l = (pow(lx, 2) + pow(ly, 2))**0.5

            if l < r:
                p_return[i, j] = p_src[i, j]
            if l > r:
                p_return[i, j] = p_white[i, j]
    return img_return


def mentionReplacement(author,
                       txt,
                       isRecording=False,
                       isBold=False,
                       isPrefixName=False,
                       isDisplayed=False,
                       isAvatar=False,
                       isId=False):

    if txt == "me":
        return str(author.id)
    member_name = txt
    guild = author.guild
    all_mentions = re.findall(r"<[@&]+[0-9]+>", txt)
    for mention in all_mentions:
        memberNum = int(re.findall(r"[0-9]+", mention)[0])
        print(memberNum)
        member = guild.get_member(memberNum)
        if member.bot is True:
            return "bot"
        elif isAvatar:
            return member.avatar.url
        elif isDisplayed:
            member_name = member.display_name
        elif isPrefixName:
            member_name = member_name.split("#")[0]
        elif isRecording:
            member_name = f"@{member_name}"
        elif isBold:
            member_name = f"**{member_name}**"
        elif isId:
            member_name = member.id
    return member_name


'''
#將mention轉換成伺服器成員名字 (None則轉換成discord id名)
# mentionReplacement(author, txt, isDisplayed=True)
def ment4(m, user, g):
    if re.match(r"<[@!&]+[0-9]+>", user):
        id1 = re.findall("[0-9]+", user)
        mb1 = g.get_member(int(id1[0]))
        return mb1.display_name


#將字段中的mention轉換成@<成員名字>
# mentionReplacement(author, txt, isDisplayed=True, isRecording=True)
def ment5(m, user, g):
    a1 = 1
    t = user
    if a1 == 1:
        q1 = re.findall(r"<[@!&]+[0-9]+>", user)
        for i in range(len(q1)):
            men = ment4(m, q1[i], g)
            t = re.sub(q1[i], f"@{men}", t)
        return t


#偵測字段(user)中是否含有mention或"me"，有的話返回用戶discord.Member屬性
#(m=message.author , user=message.content , g=messagr.guild)
# mentionReplacement(author, txt)
def ment(m, user, g):
    if re.match(r"<[@!&]+[0-9]+>", user):
        id1 = re.findall("[0-9]+", user)
        return g.get_member(int(id1[0]))
    elif "me" in user:
        return m
    else:
        return user


#將mention轉換成用戶discord id名
# mentionReplacement(author, txt, isRecording=True)
def ment2(m, user, g):
    a1 = 1
    t = user
    if a1 == 1:
        q1 = re.findall(r"<[@!&]+[0-9]+>", user)
        for i in range(len(q1)):
            men = ment(m, q1[i], g)
            t = user.replace(q1[i], f"@{men}")
        return t


# mentionReplacement(author, txt, isBold=True)
def ment3(m, user, g):
    text = user
    if re.findall(r"<@[0-9]+>", user):
        id1 = re.findall("[0-9]+", user)
        for i in range(len(id1)):
            name = str(g.get_member(int(id1[i]))).split("#", 2)
            text = re.sub(f"<@{id1[i]}>", f"**{name[0]}**", user)
            user = text
    return text

'''


def filter_emoji(desstr, restr=""):
    # 过滤表情
    try:
        co = re.compile("[\U00010000-\U0010ffff]")
    except re.error:
        co = re.compile("[\uD800-\uDBFF][\uDC00-\uDFFF]")
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
    if "bpm" in str:
        return "\U0001F4C4"


def get_song_len():
    with open(f"./text/guess_song.json", "r") as b:
        f = b.read()
        song_list = json.loads(f)
        x = len(song_list)
        b.close()
    return x


def get_song(id):
    with open(f"./text/guess_song.json", "r") as b:
        f = b.read()
        song_list = json.loads(f)
        x = len(song_list)
        output1 = []
        i = 0
        while i <= 9:
            if len(id) == 1:
                x4 = id[0]
                if x4 == -1:
                    x4 = random.randrange(0, x)
            else:
                x4 = random.randrange(0, len(id))
                x4 = id[x4]
            x1 = len(song_list[x4])
            y = random.randrange(0, x1)
            if output1.count(song_list[x4][y]) == 0:
                output1.append(song_list[x4][y])
                i += 1
        b.close()
    return output1


def get_cd(name, channelid, write=True):
    with open(f"./text/{name}_cd.txt", "r") as b:
        f = b.read()
        str1 = f.split(",")
        key = 0
        for i in range(len(str1)):
            if str(channelid) == str1[i]:
                key = 1
        b.close()
    if key == 1:
        return False
    elif write:
        write_cd(name, channelid)
        return True
    else:
        return True


def get_cd_notkeep(name, channelid):
    with open(f"./text/{name}_cd.txt", "r") as b:
        f = b.read()
        str1 = f.split(",")
        key = 0
        for i in range(len(str1)):
            if str(channelid) == str1[i]:
                key = 1
        b.close()
    if key == 1:
        return False
    else:
        return True


def write_cd(name, channelid):
    with open(f"./text/{name}_cd.txt", "a") as b1:
        new = "," + str(channelid)
        b1.write(new)
    b1.close()


def reset_cd(name):
    with open(f"./text/{name}_cd.txt", "w") as b1:
        new = "1,2,3"
        b1.write(new)
    b1.close()


def del_cd(name, channelid):
    with open(f"./text/{name}_cd.txt", "r") as b:
        f = b.read()
    b.close()
    with open(f"./text/{name}_cd.txt", "w") as b1:
        new = re.sub(f',{channelid}', '', f)
        b1.write(new)
    b1.close()


def get_id(user, category="cytoid"):
    with open("./text/member.json", "r") as b:
        user = str(user)
        f = b.read()
        memberlist = json.loads(f)
        if str(user) in memberlist.get(category, {}):
            return memberlist[category][user]
        else:
            return "e404"
    b.close()


def write_id(user, id, category="cytoid"):
    with open("./text/member.json", "r") as b:
        user = str(user)
        f = b.read()
        memberlist = json.loads(f)
        if str(user) in memberlist.get(category, {}):
            return memberlist[category][user]
    b.close()
    with open("./text/member.json", "w") as b1:
        memberlist[category][user] = id
        json.dump(memberlist, b1, indent=2, ensure_ascii=False)
        return "e200"
    b1.close()


def del_id(user, category="cytoid"):
    with open("./text/member.json", "r") as b:
        user = str(user)
        f = b.read()
        memberlist = json.loads(f)
        if str(user) not in memberlist.get(category, {}):
            return "e404"
    b.close()
    with open("./text/member.json", "w") as b1:
        del memberlist[category][user]
        json.dump(memberlist, b1, indent=2, ensure_ascii=False)
        return "e200"
    b1.close()


def get_keep(text, say=True):
    with open("./text/keep.json", "r", encoding="utf8") as b:
        f = b.read()
        keep = json.loads(f)
        if text in keep and say == True:
            return keep[text][0], keep[text][1]
        elif say == True:
            return "e404", "e404"
        else:
            return keep[text]
    b.close()


def write_keep(name, guild, channel, coin=-1, say=True):
    with open("./text/keep.json", "r", encoding="utf8") as b:
        f = b.read()
        keep = json.loads(f)
    b.close()
    if name in keep and say == True:
        return "e405"
    elif say:
        keep[name] = [guild, channel]
    else:
        try:
            keep[name][guild].append([channel, coin])
        except:
            keep[name][guild] = ([[channel, coin]])
        with open("./text/keep.json", "w", encoding="utf8") as b1:
            json.dump(keep, b1, indent=2, ensure_ascii=False)
        b1.close()
        return keep[name]
    with open("./text/keep.json", "w", encoding="utf8") as b1:
        json.dump(keep, b1, indent=2, ensure_ascii=False)
    b1.close()
    return "e200"


def delete_keep(text):
    with open("./text/keep.json", "r") as b:
        f = b.read()
        keep = json.loads(f)
    b.close()
    if text in keep and text not in ["收入", '支出']:
        del keep[text]
    else:
        return "e404"
    with open("./text/keep.json", "w") as b1:
        json.dump(keep, b1, indent=2, ensure_ascii=False)
    b1.close()
    return "e200"


def say_txt(ctdid, user):
    tw = pytz.timezone("Asia/Taipei")
    twtime = datetime.now(tw)
    cutime = twtime.strftime("%F %H:%M:%S")
    key2 = 1
    with open("./text/say.txt", "a") as b1:
        if key2 == 1:
            new = cutime + " | " + str(ctdid) + "說：" + user + "\n"
            b1.write(new)
            return "e200"
    b1.close()


def del_txt(ctdid, user, cutime):
    tw = pytz.timezone("Asia/Taipei")
    twtime = datetime.now(tw)
    if cutime == 0:
        cutime = twtime.strftime("%F %H:%M:%S")
    key2 = 1
    with open("./text/del.txt", "a") as b1:
        if key2 == 1:
            new = cutime + " | " + str(ctdid) + "說：" + user + "\n"
            b1.write(new)
            return "e200"
    b1.close()


def get_deltxt():
    with open("./text/del.txt", "r") as b1:
        txt = b1.read()
    b1.close()
    return txt


def c2v3(path):
    try:
        with open(path, "r") as f1:
            f = f1.read()
            chart = json.loads(f)
        f1.close()
    except:
        return "e404", "檔案格式錯誤 (Can't open this file)"
    try:
        backup = chart["chartBackup"]
        with open("./text/backup_cache.txt", "w") as b:
            json.dump(backup, b, indent=2, ensure_ascii=False)
        b.close()
        return "e200", "text/backup_cache.txt"
    except:
        return "e404", "譜面資料解析失敗 (Can't find chart backup)"


def ctdtime(tx):
    tx = re.sub("\.[^\0]+", "", tx)
    tx = re.sub("T", " ", tx)
    struct_time = time.strptime(tx, "%Y-%m-%d %H:%M:%S")
    time_stamp = int(time.mktime(struct_time))
    return f"<t:{time_stamp}:f>"


def stmtime(s):
    seconds = int(s)
    m, s = divmod(seconds, 60)
    return "%02d:%02d" % (m, s)


def ctddiff(n):
    if n > 16:
        n = 16
    a1 = 13
    b1 = 1
    b2 = 994
    if n >= 15:
        b2 = 420
    while a1 > 1:
        if abs(b1 - b2) <= 3:
            c1 = ""
            break
        b0 = random.randrange(b1, b2)
        url = (
            "https://services.cytoid.io/levels?&sort=difficulty&order=desc&category=all&page="
            + str(b0) + "")
        res = requests.get(url)
        js = json.loads(res.content.decode("utf-8"))
        c1 = random.randrange(0, 9)
        max = js[c1]["charts"][0]["difficulty"]
        for i in range(len(js[c1]["charts"])):
            if js[c1]["charts"][i]["difficulty"] == n:
                max = js[c1]["charts"][i]["difficulty"]
                break
            elif js[c1]["charts"][i]["difficulty"] > max:
                max = js[c1]["charts"][i]["difficulty"]
        if max < n:
            b2 = b0
        elif max > n and n < 16:
            b1 = b0
        elif max == n:
            a1 = 0
            break
        a1 -= 1
    try:
        return js[c1]["uid"]
    except:
        return "一"


def bpm(list):
    b = []
    for i in range(len(list) - 1):
        x = i + 1
        b.append(float(list[x]) - float(list[i]))
    b.sort()
    d1 = math.ceil(len(b) / 25) - 1
    d2 = len(b)
    a = b[d1:d2]
    t1 = math.ceil(len(a) / 50 * 2.8)
    t2 = math.ceil(len(a) / 50 * 44)
    t3 = math.ceil(len(a) / 50 * 23.5)
    try:
        if (a[t2] - a[t3]) <= 0.0012 or (a[t3] - a[t1]) <= 0.0012:
            c1 = 0
            c2 = 0
            for i in range(len(a)):
                if (math.ceil(a[t1] * 1000) / 1000 - a[i] < 0.001
                        and math.ceil(a[t1] * 1000) / 1000 - a[i] > 0):
                    c1 += 1
                if (math.ceil(a[t2] * 1000) / 1000 - a[i] < 0.001
                        and math.ceil(a[t2] * 1000) / 1000 - a[i] > 0):
                    c2 += 1
            sum = (a[t1] * c1 + a[t2] * c2) / (c1 + c2)
        else:
            c1 = 0
            c2 = 0
            c3 = 0
            for i in range(len(a)):
                if (math.ceil(a[t1] * 1000) / 1000 - a[i] < 0.001
                        and math.ceil(a[t1] * 1000) / 1000 - a[i] > 0):
                    c1 += 1
                if (math.ceil(a[t2] * 1000) / 1000 - a[i] < 0.001
                        and math.ceil(a[t2] * 1000) / 1000 - a[i] > 0):
                    c2 += 1
                if (math.ceil(a[t3] * 1000) / 1000 - a[i] < 0.001
                        and math.ceil(a[t3] * 1000) / 1000 - a[i] > 0):
                    c3 += 1
            sum = (a[t1] * c1 + a[t2] * c2 + a[t3] * c3) / (c1 + c2 + c3)
        output = 120 / sum
        output2 = output * (3 / 4)
        if output >= 241.25:
            output /= 2
        elif output <= 118.8:
            output *= 2
            output2 *= 2
        id = bpm_txt(a)
        return ("`No." + id + "`\n> Estimated BPM: `" +
                "{:.3f}".format(output) + " (" + "{:.3f}".format(output2) +
                ")`   beat_frame=" + "{:.6f}".format(sum))
    except Exception as e:
        error_class = e.__class__.__name__  # 取得錯誤類型
        detail = e.args[0]  # 取得詳細內容
        cl, exc, tb = sys.exc_info()  # 取得Call Stack
        lastCallStack = traceback.extract_tb(tb)[-1]  # 取得Call Stack的最後一筆資料
        fileName = lastCallStack[0]  # 取得發生的檔案名稱
        lineNum = lastCallStack[1]  # 取得發生的行號
        funcName = lastCallStack[2]  # 取得發生的函數名稱
        errMsg = 'File "{}", line {}, in {}: [{}] {}'.format(
            fileName, lineNum, funcName, error_class, detail)
        outtext = (
            "**Audio analyze failed:**\nCheck if audio's silence for beginning is long enough\n```"
            + errMsg + "```")
        return outtext


def bpm_txt(user):
    tw = pytz.timezone("Asia/Taipei")
    twtime = datetime.now(tw)
    cutime = twtime.strftime("%g%U%u%H%M%S")
    key2 = 1
    with open("./bpm.txt", "a") as b1:
        if key2 == 1:
            new = ";No." + cutime + ":" + json.dumps(user)
            b1.write(new)
            return cutime
    b1.close()


def get_bpm(id):
    with open("./bpm.txt", "r") as b1:
        f = b1.read()
        text = f.split(";")
        x = len(text) - 1
        for i in range(len(text)):
            if id in text[x]:
                str = text[x].split(":")
                break
            x -= 1
    b1.close()
    with open("./bpm_cache.txt", "w") as b2:
        b2.write(str[1])
    b2.close()


def get_guess_cate(song_category, song_cates):
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
    elif re.sub(f"[^0-{str(song_cates)}]", "", song_category) == song_category:
        id = re.sub(f"[^0-{str(song_cates)}]", "", song_category)
        id = re.findall(f"[0-{str(song_cates)}]", id)
        list(set(id))
        id = [int(x) for x in id]
    else:
        id = [-1]
    return id


def guess_word(guess_time, guess_key, song_list, figure_ans):
    time_stamp = int(time.time()) + 56
    now_time = f"<t:{time_stamp}:R>"
    cd_time = int(time.time()) + 4
    cd_time = f"<t:{cd_time}:R>"
    text = f"> 機器人復活連結：https://ppt.cc/f3ZGGx\n> **Timer:** {now_time}\n> **CD:** {cd_time}\n> **Guess Counts:** {guess_time}\n\n```"
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
    return text


def guess_ans(fid, msg, song_list, figure_ans, guess_count):
    x = int(fid[0]) - 1
    gname = ["", ""]
    fid[0] = str(int(fid[0]))
    gname[1] = msg.content.split(' ', 1)[1]
    user = msg.author.display_name
    if int(fid[0]) not in figure_ans:
        cd_time = int(time.time()) + 4
        cd_time = f"<t:{cd_time}:R>"
        text = (f"> **CD:** {cd_time}\n\n{user}，猜測條目重複 (Repeated Key)")
    elif (re.sub("[^A-Za-z0-9]", "",
                 gname[1].lower()) == re.sub("[^A-Za-z0-9]", "",
                                             song_list[x].lower())):
        figure_ans.remove(int(fid[0]))
        print(gname[1], f"剩{len(figure_ans)}")
        x1 = (x + 1) % 10
        x2 = int((x + 1 - x1) / 10)
        song_list[x] = song_list[x] + f"  ({user})"
        time_stamp = int(time.time()) + 56
        now_time = f"<t:{time_stamp}:R>"
        cd_time = int(time.time()) + 4
        cd_time = f"<t:{cd_time}:R>"
        UserCoin, FirstUse = coin.getUserData(msg.author.id, "coin", "zh")
        getCoin = (5-guess_count)*10 if guess_count < 5 else 10
        UserCoin += getCoin
        coin.changeUserData(msg.author.id, "coin", UserCoin,
                            getCoin, "guess correct")
        text = f"> **Timer:** {now_time}\n> **CD:** {cd_time}\n\n```{x2}{x1}. {song_list[x]}```\n💵 :   `+{getCoin} / {UserCoin}`"
    elif int(fid[0]) <= 0 and int(fid[0]) > 10:
        cd_time = int(time.time()) + 4
        cd_time = f"<t:{cd_time}:R>"
        text = (
            f"> **CD:** {cd_time}\n\n{user}，猜測題號未出現 (Guess correct question)")
    else:
        cd_time = int(time.time()) + 4
        cd_time = f"<t:{cd_time}:R>"
        UserCoin, FirstUse = coin.getUserData(msg.author.id, "coin", "zh")
        getCoin = -5
        oldUserCoin = UserCoin
        UserCoin = UserCoin + getCoin if (UserCoin + getCoin) >= 0 else 0
        getCoin = -5 if (UserCoin + getCoin) >= 0 else oldUserCoin*-1
        coin.changeUserData(msg.author.id, "coin", UserCoin,
                            getCoin, "guess incorect")
        text = f"> **CD:** {cd_time}\n\n{user}，你猜錯了！ (Incorect)\n💵 :   `{getCoin} / {UserCoin}`"
    return text


def ebt(id):
    embed = ""
    if str(id) == "mra":
        embed = "缺少必要的參數\nMissing required arg(s)\n\n"
    elif str(id) == "nobindctd":
        embed = "由於discord帳號id改變，請重新使用`dy bind ctd <cytoid id>`綁定帳號\nPlease bind account agian\n\n"
    elif str(id) == "nofindctd":
        embed = "無效的Cytoid ID，請重新輸入\nThis Cytoid ID can't find out\n\n"
    elif str(id) == "norecord":
        embed = "無遊玩記錄\nThis Player never played\n\n"
    elif str(id) == "nofindctdlevel":
        embed = "無效的Level ID，請重新輸入\nThis Level can't find out\n\n"
    elif str(id) == "pvp":
        embed = "`dy pvp <player_A_id(@menber|me)> <player_B_id(@menber|me)> <level_id>`\n"
    elif str(id) == "bind":
        embed = "`dy bind ctd <id>`\n"
    elif str(id) == "unbind":
        embed = "`dy unbind ctd`\n"
    elif str(id) == "best":
        embed = "`dy best <level id> (cytoid id)`\n"
    elif str(id) == "calc":
        embed = "`dy calc <category> <diff> <score | rating>`\n"
    elif str(id) == "expt":
        embed = "發生未知錯誤\nUnknown error\n"
    return embed


def write_role(role_):
    with open("./text/role.txt", 'r') as b0:
        f = b0.read()
        text = re.findall('[0-9]+(?=,)', f)
        per = int(text[0]) + 1
    b0.close()
    with open("./text/role.txt", 'w') as b:
        new0 = re.sub(text[0], per, f)
        new1 = new0 + ',' + role_
        b.write(new1)
    b.close()
    return per
