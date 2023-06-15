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
    elif 'me' in user:
        return m
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
            name1 = re.findall('[^\0,]+#[0-9][0-9][0-9][0-9]', str1[i])
            if str(user) in name1:
                key = 1
                n2=name1
        if key == 1:
            key2 = 1
        else:
            key2 = 0
            return 'e404'
    b.close()
    with open("./member.txt", 'w') as b1:
        if key2 == 1:
            reg=f',{n2[0]}:[^\0,]+'
            del1 = re.sub(reg, "", f)
            b1.write(del1)
            return 'e200'
    b1.close()


def say_txt(ctdid, user):
    tw = pytz.timezone('Asia/Taipei')
    twtime = datetime.now(tw)
    cutime = twtime.strftime("%F %H:%M:%S")
    key2 = 1
    with open("./say.txt", 'a') as b1:
        if key2 == 1:
            new = cutime+" | " + str(ctdid)+"說："+user+"\n"
            b1.write(new)
            return 'e200'
    b1.close()
