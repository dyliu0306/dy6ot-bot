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
import time
import pytz
import numpy as np
import sys
import traceback
import matplotlib.pyplot as plt


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
    plt.savefig("cache1.png")
    font_path = "./font/MPLUSRounded1c-Regular.ttf"
    font_path3 = "./font/ARIALN.TTF"
    font_path4 = "./font/NotoSansSC-Medium.otf"
    font_path5 = "./font/NotoSans-Regular.ttf"
    level_path = requests.get(url)
    ctrcc = Image.open(BytesIO(level_path.content)).convert("RGBA")
    ctrimg = img_circle(ctrcc, 52)
    result_image = Image.new('RGB', (500, 270))
    chart_img = Image.open("cache1.png").convert("RGBA")
    result_image.paste(chart_img, box=(5, -28), mask=chart_img)
    result_image.paste(ctrimg, box=(15, 10), mask=ctrimg)
    drawtext = ImageDraw.Draw(result_image)
    if "ja" in judge_language(title01) or "zh" in judge_language(title01):
        f1 = ImageFont.truetype(os.path.abspath(font_path4), 27)
    else:
        f1 = ImageFont.truetype(os.path.abspath(font_path5), 30)
    f2 = ImageFont.truetype(os.path.abspath(font_path), 14)
    
    title = demoji.replace(title01, "")
    title = title if len(title)<15 else str(title[:12] + "...")
    drawtext.text((77, 6), title, "#ffffff", font=f1)
    drawtext.text((79, 42), author, "#ffffff", font=f2)
    result_image.save("cache1.png")


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
    plt.savefig("cache1.png")
    font_path3 = "./font/ARIALN.TTF"
    font_path4 = "./font/NotoSansSC-Medium.otf"
    font_path5 = "./font/NotoSans-Regular.ttf"
    level_path = requests.get(url)
    ctrcc = Image.open(BytesIO(level_path.content)).convert("RGBA")
    ctrimg = img_circle(ctrcc, 48)
    result_image = Image.new('RGB', (478, 250))
    chart_img = Image.open("cache1.png").convert("RGBA")
    result_image.paste(chart_img, box=(13, 40), mask=chart_img)
    result_image.paste(ctrimg, box=(12, 5), mask=ctrimg)
    drawtext = ImageDraw.Draw(result_image)
    if "ja" in judge_language(title01) or "zh" in judge_language(title01):
        f1 = ImageFont.truetype(os.path.abspath(font_path4), 20)
    else:
        f1 = ImageFont.truetype(os.path.abspath(font_path5), 24)
    title = demoji.replace(title01, "")
    drawtext.text((72, 2), title, "#ffffff", font=f1)
    result_image.save("cache1.png")

def getChartInfoEmbed(chart_data):
    cha1 = 0
    dif1 = ""
    while cha1 < len(chart_data["charts"]):
        dif1 = f'{dif1} {chart_data["charts"][cha1]["type"]} {chart_data["charts"][cha1]["difficulty"]} /'
        cha1 += 1
    dif1 = re.sub("/$", "", dif1)
    dif1 = re.sub("^ ", "", dif1)
    embed = discord.Embed(
        title=chart_data["uid"],
        description=
        f'**Title**\n{chart_data["title"]}\n\n**Difficulty**\n{dif1}\n\n**Length**\n{stmtime(chart_data["duration"])}',
        color=0xFFFF28,
        url=f'https://next.cytoid.io/levels/{chart_data["uid"]}',
    )
    embed.set_thumbnail(url=chart_data["cover"]["cover"])
    embed.set_footer(text="Search level-id in Cytoid to download it")
    embed.set_author(
        name=chart_data["owner"]["uid"],
        icon_url=chart_data["owner"]["avatar"]["small"],
    )
    return embed


def plot_line_chart(rates_list, url, title01):
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
    plt.savefig("cache1.png")
    font_path3 = "./font/ARIALN.TTF"
    font_path4 = "./font/NotoSansSC-Medium.otf"
    font_path5 = "./font/NotoSans-Regular.ttf"
    level_path = requests.get(url)
    ctrcc = Image.open(BytesIO(level_path.content)).convert("RGB")
    ctrimg = img_circle(ctrcc, 37)
    pvpimg = Image.open("cache1.png")
    pvpimg = pvpimg.convert("RGB")
    pvpimg.paste(ctrimg, box=(12, 3), mask=ctrimg)
    drawtext = ImageDraw.Draw(pvpimg)
    if "ja" in judge_language(title01) or "zh" in judge_language(title01):
        f1 = ImageFont.truetype(os.path.abspath(font_path4), 15)
    elif "en" in judge_language(title01):
        f1 = ImageFont.truetype(os.path.abspath(font_path5), 15)
    else:
        f1 = ImageFont.truetype(os.path.abspath(font_path5), 15)
    title = demoji.replace(title01, "")
    drawtext.text((65, 0), title, "#ffffff", font=f1)
    pvpimg.save("cache1.png")


def filter_str(sentence):
    remove_nota = "[’·°–!\"#$%&'()*+,-.\/:;<=>?@，。?★、…【】（）《》？“”‘’！\[\\\]^_`{|}~]+"
    remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)
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
    
    with open("./hack.txt", "rb") as hack_histroy_file:
        hack_histroy = hack_histroy_file.read().decode("utf-8")
        if id in hack_histroy:
           return False

    with open("./hack.txt", "a") as hack_histroy_file:
        hack_histroy_file.write("," + id)

    return True


def isValidLevelId(mystr):
    for c in mystr:
        if c not in "abcdefghijklmnopqrstuvwxyz._-0123456789":
            return False
    return True


def plot_line_chart(rates_list, url, title01):
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
    plt.savefig("cache1.png")
    font_path3 = "./font/ARIALN.TTF"
    font_path4 = "./font/NotoSansSC-Medium.otf"
    font_path5 = "./font/NotoSans-Regular.ttf"
    level_path = requests.get(url)
    ctrcc = Image.open(BytesIO(level_path.content)).convert("RGB")
    ctrimg = img_circle(ctrcc, 37)
    pvpimg = Image.open("cache1.png")
    pvpimg = pvpimg.convert("RGB")
    pvpimg.paste(ctrimg, box=(12, 3), mask=ctrimg)
    drawtext = ImageDraw.Draw(pvpimg)
    if "ja" in judge_language(title01) or "zh" in judge_language(title01):
        f1 = ImageFont.truetype(os.path.abspath(font_path4), 15)
    elif "en" in judge_language(title01):
        f1 = ImageFont.truetype(os.path.abspath(font_path5), 15)
    else:
        f1 = ImageFont.truetype(os.path.abspath(font_path5), 15)
    title = demoji.replace(title01, "")
    drawtext.text((65, 0), title, "#ffffff", font=f1)
    pvpimg.save("cache1.png")


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


def get_memberid(text):
    plist = re.findall(r"<[@!&]+[0-9]+>", text)
    for a1 in plist:
        id_ = re.match("[0-9]+", plist[a1])
        plist[a1] = re.replace("<[@!&]+[0-9]+>", id_, plist[a1])
    return plist


def mentionReplacement(author,
                       txt,
                       isRecording=False,
                       isBold=False,
                       isPrefixName=False,
                       isDisplayed=False):
    
    if txt == "me":
        return str(author)
    
    guild = author.guild
    all_mentions = re.findall(r"<[@!&]+[0-9]+>", txt)
    for mention in all_mentions:
        memberNum = int(mention[2:-1])
        member = guild.get_member(memberNum)
        if isDisplayed:
            member_name = member.display_name
        else:
            member_name = str(member)
        if isPrefixName:
            member_name = member_name.split("#")[0]
        if isRecording:
            member_name = f"@{member_name}"
        if isBold:
            member_name = f"**{member_name}**"
        txt = txt.replace(mention, member_name)
    return txt

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
    with open(f"./guess_song.txt", "r") as b:
        f = b.read()
        song_list = json.loads(f)
        x=len(song_list)
        b.close()
    return x

def get_song(id):
    with open(f"./guess_song.txt", "r") as b:
        f = b.read()
        song_list = json.loads(f)
        x=len(song_list)
        output1=[]
        i=0
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
                i+=1
        b.close()
    return output1

def get_cd(name,channelid):
    with open(f"./{name}_cd.txt", "r") as b:
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
         write_cd(name,channelid)
         return True

def get_cd_notkeep(name,channelid):
    with open(f"./{name}_cd.txt", "r") as b:
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


def write_cd(name,channelid):
    with open(f"./{name}_cd.txt", "a") as b1:
        new = "," + str(channelid)
        b1.write(new)
    b1.close()

def reset_cd(name):
    with open(f"./{name}_cd.txt", "w") as b1:
        new = "1,2,3"
        b1.write(new)
    b1.close()

def del_cd(name,channelid):
    with open(f"./{name}_cd.txt", "r") as b:
        f = b.read()
    b.close()
    with open(f"./{name}_cd.txt", "w") as b1:
        new = re.sub(f',{channelid}','',f)
        b1.write(new)
    b1.close()



def get_ctdid(user):
    with open("./member.txt", "r") as b:
        f = b.read()
        str1 = f.split(",", 200)
        key = 0
        for i in range(len(str1)):
            name1 = re.findall("[^\0]+#[0-9]+", str1[i])
            if str(user) in name1:
                key = 1
                id_ = str1[i].split(":", 2)
                id = id_[1]
        if key == 1:
            return id
        else:
            return "e404"
    b.close()


def write_ctdid(user, ctdid):
    with open("./member.txt", "r") as b:
        f = b.read()
        str1 = f.split(",", 200)
        key = 0
        for i in range(len(str1)):
            name1 = re.findall("[^\0]+#[0-9]+", str1[i])
            if str(user) in name1:
                key = 1
                id_ = str1[i].split(":", 2)
                id = id_[1]
        if key == 1:
            key2 = 0
        else:
            key2 = 1
    b.close()
    with open("./member.txt", "a") as b1:
        if key2 == 1:
            new = "," + str(user) + ":" + ctdid
            b1.write(new)
            return "e200"
        else:
            return f"e405：{id}"
    b1.close()


def delete_ctdid(user):
    with open("./member.txt", "r") as b:
        f = b.read()
        str1 = f.split(",", 200)
        key = 0
        for i in range(len(str1)):
            name1 = re.findall("[^\0,]+#[0-9]+", str1[i])
            if str(user) in name1:
                key = 1
                n2 = name1
        if key == 1:
            key2 = 1
        else:
            key2 = 0
            return "e404"
    b.close()
    with open("./member.txt", "w") as b1:
        if key2 == 1:
            reg = f",{n2[0]}:[^\0,]+"
            del1 = re.sub(reg, "", f)
            b1.write(del1)
            return "e200"
    b1.close()


def say_txt(ctdid, user):
    tw = pytz.timezone("Asia/Taipei")
    twtime = datetime.now(tw)
    cutime = twtime.strftime("%F %H:%M:%S")
    key2 = 1
    with open("./say.txt", "a") as b1:
        if key2 == 1:
            new = cutime + " | " + str(ctdid) + "說：" + user + "\n"
            b1.write(new)
            return "e200"
    b1.close()


def del_txt(ctdid, user,cutime):
    tw = pytz.timezone("Asia/Taipei")
    twtime = datetime.now(tw)
    if cutime==0:
        cutime = twtime.strftime("%F %H:%M:%S")
    key2=1
    with open("./del.txt", "a") as b1:
        if key2 == 1:
            new = cutime + " | " + str(ctdid) + "說：" + user + "\n"
            b1.write(new)
            return "e200"
    b1.close()

def get_deltxt():
    with open("./del.txt", "r") as b1:
        txt=b1.read()
    b1.close()
    return txt


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


#指考轉分科60分
def ztf(text):
    try:
        a_ = text.split("\n")
        b_ = []
        num_ = 0
        pt_ = 100
        for i in range(101):
            if int(a_[i]) > 0:
                for i1 in range(int(a_[i])):
                    try:
                        b_.append(pt_)
                        num_ += 1
                    except:
                        break
            pt_ -= 1
        t0 = math.ceil((len(b_) / 100))
        L = "{:.5f}".format((sum(b_[0:t0]) / t0) / 60)
        print(L, (59 * float(L)), num_, t0)
        z1 = 20
        x = 0
        z3 = 1
        output1 = ">>> 若錯排請將螢幕轉向\n```"
        for i in range(20):
            z2 = "{:.2f}".format((3 * z1 - x) * float(L)).zfill(5)
            if z3 >= 1:
                z2 = "100.0"
                z3 = 0
            output1 += f'{str(3*z1-x).zfill(2)} | {"{:.2f}".format((3*z1-x-1)*float(L)).zfill(5)}<Ｘ<={z2}  {str(2*z1-x).zfill(2)} | {"{:.2f}".format((2*z1-x-1)*float(L)).zfill(5)}<Ｘ<={"{:.2f}".format((2*z1-x)*float(L)).zfill(5)}  {str(z1-x).zfill(2)} | {"{:.2f}".format((z1-1-x)*float(L)).zfill(5)}<Ｘ<={"{:.2f}".format((z1-x)*float(L)).zfill(5)}\n'
            x += 1
        return f"{output1}```"
    except:
        return "e200"


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

#Embed模板
def ebt(id):
    embed = ""
    if str(id) == "mra":
        embed = "缺少必要的參數\nMissing required arg(s)\n\n"
    elif str(id) == "nobindctd":
        embed = "未找到註冊資料，使用`bind ctd <cytoid id>`綁定帳號\nThis user have not bound yet\n\n"
    elif str(id) == "nofindctd":
        embed = "無效的Cytoid ID，請重新輸入\nThis Cytoid ID can't find out\n\n"
    elif str(id) == "norecord":
        embed = "無遊玩記錄\nThis Player never played\n\n"
    elif str(id) == "nofindctdlevel":
        embed = "無效的Level ID，請重新輸入\nThis Level can't find out\n\n"
    elif str(id) == "pvp":
        embed = "`dy pvp <player_A_id(@menber|me)> <player_B_id(@menber|me)> <level_id>`"
    elif str(id) == "expt":
        embed = "發生未知錯誤\nUnknown error"
    return embed


def write_role(role_):
    with open("./role.txt", 'r') as b0:
        f=b0.read()
        text=re.findall('[0-9]+(?=,)',f)
        per=int(text[0])+1
    b0.close()
    with open("./role.txt", 'w') as b:
        new0=re.sub(text[0],per,f)
        new1=new0+','+role_
        b.write(new1)
    b.close()
    return per


def dcsh(m1):
    if m1 == "你好":
        return [
            "歡迎遊玩解謎遊戲\n以下將說明遊戲規則：\n\n• 傳送訊息後若無反應即回答有誤。\n• 有些題目有提示，以數字表示提示數量。提示有漸進順序，以英文字母排列，字母越後面，提示就更容易解題。\n• 若想查看提示，請回答「<題號><英文字母>」\n• 查看提示範例：\n——————————\n題目50：\n題目內容。\n提示數量：2\n——————————\n輸入「50a」將回覆題目50的第一個提示\n輸入「50b」將回覆題目50的第二個提示\n輸入「50c」將不回覆任何內容\n\n• 無法成功解題可輸入「pass<題號>」，將說明謎底並進入下一題\n\n那麼，讓我們開始遊戲，請輸入「開始遊玩」"
        ]
    if m1 == "提示":
        return ["**若想查看提示，請輸入「<題號><英文字母>」**\n"]
    if m1 == "開始遊玩":
        return [
            "**題目1**\n請查看圖片。\n\n提示數量：1\n謎底：一個數字(**以中文回答**)",
            "https://media.discordapp.net/attachments/951022756529602641/1093702058848297011/1680829286485.jpg",
        ]
    if m1 == "1a":
        return ["提示1a: 將選中的圖片連起來吧！"]
    if m1 == "4":
        return ["你是不是沒看清楚題目要求呢？"]
    if m1 == "pass1":
        return [
            "圖片中1、3、4、5（校狗）、6、9格都是大直高中校園場景，連線為「四」",
            "那麼，前往下一題。",
            "**題目2**\n請查看圖片。\n\n提示數量：1\n謎底：四個中文字",
            "https://cdn.discordapp.com/attachments/951022756529602641/1093702058617622538/1680829286475.jpg",
        ]
    if m1 == "四":
        return [
            "答對了！前往下一題。",
            "**題目2**\n請查看圖片。\n\n提示數量：1\n謎底：四個中文字",
            "https://cdn.discordapp.com/attachments/951022756529602641/1093702058617622538/1680829286475.jpg",
        ]
    if m1 == "pass2":
        return [
            "這個亂碼是注音符號忘記切了，答案是大直高中",
            "那麼，前往下一題。",
            ">>> 一輩子一次的高中畢旅\n延期換行程然後停辦\n差那一點點的時間\n時間不會倒流\n================\n提示數量：1\n謎底：四個字，日本茶道用語",
            "-----\n不用擔心，是漢字:D",
            "-----\n好像有個關鍵詞需要自己動手查？",
        ]
    if m1 == "2a":
        return ["提示2a: 這串字有什麼意思嗎？每個注音符號與聲調都被替換成另一個字(含空格)"]
    if m1 == "大直高中":
        return [
            "答對了！前往下一題。",
            "**題目3**\n ",
            ">>> 一輩子一次的高中畢旅\n延期換行程然後停辦\n差那一點點的時間\n時間不會倒流\n================\n提示數量：1\n謎底：四個字，日本茶道用語",
            "-----\n不用擔心，是漢字:D",
            "-----\n好像有個關鍵詞需要自己動手查？",
        ]
    if m1 == "3a":
        return ["提示3a: 這串句子是不是藏著什麼詞？四句又有四個字（觀察句數與字數的關聯吧！）"]
    if m1 == "pass3":
        return [
            "答案是一期一會 (日本用語，原指茶道中的待客精神，後推廣至珍惜一生一次的機會)",
            "那麼，前往下一題。",
            "**題目4**\n```.... /. / .- / .-.. / - / .... / -.-. / . / -. / - / . / .-.```\n============\n提示數量：1\n謎底：學校處室 (**請將答案轉成四個中文**)",
        ]
    if m1 == "一期一會":
        return [
            "答對了！前往下一題。",
            "**題目4**\n```.... /. / .- / .-.. / - / .... / -.-. / . / -. / - / . / .-.```\n============\n提示數量：1\n謎底：學校處室 (**請將答案轉成四個中文**)",
        ]
    if m1 == "4a":
        return [
            "https://telecom.nstm.gov.tw/ckfinder/userfiles/Images/12112(1).jpg"
        ]
    if m1 == "pass4":
        return [
            "這是摩斯密碼,破譯後得出文字healthcenter,健康中心",
            "那麼，前往下一題。",
            "**題目5**: 英文課\n\n你想抄作業，但同學為了搞你而把內容加密\n>>> Fly me to the moon,and let me play among the stars. \nTell me what spring islike on a Jupiter or mars.\nIn other words hold my hand,and in other words darling kiss me…\n\n==============\n提示數量：0\n謎底：英文人名(```_ _ _ _ _     _ _ _ _ _ _ _```)",
            "似乎查一下就能破解了",
        ]
    if m1 == "健保中心":
        return [
            "答對了！前往下一題。",
            "**題目5**: 英文課\n\n你想抄作業，但同學為了搞你而把內容加密\n>>> Fly me to the moon,and let me play among the stars. \nTell me what spring islike on a Jupiter or mars.\nIn other words hold my hand,and in other words darling kiss me…\n\n==============\n提示數量：0\n謎底：英文人名(```_ _ _ _ _     _ _ _ _ _ _ _```)",
            "似乎查一下就能破解了",
        ]
    if m1 == "健康中心":
        return [
            "答對了！前往下一題。",
            "**題目5**: 英文課\n\n你想抄作業，但同學為了搞你而把內容加密\n>>> Fly me to the moon,and let me play among the stars. \nTell me what spring islike on a Jupiter or mars.\nIn other words hold my hand,and in other words darling kiss me…\n\n==============\n提示數量：0\n謎底：英文人名(```_ _ _ _ _     _ _ _ _ _ _ _```)",
            "似乎查一下就能破解了",
        ]
    if m1 == "pass5":
        return ["此題不可跳過"]
    if m1 == "Frank Sinatra":
        return ["恭喜你通過了"]
    if m1 == "frank sinatra":
        return ["恭喜你通過了"]
    if m1 == "Frank sinatra":
        return ["恭喜你通過了"]
    if m1 == "frank Sinatra":
        return ["恭喜你通過了"]


# 123
