import math
import json
import requests
import random
import re
import core1.func as func
import core1.MostRecentPlay as MostRecentPlay
from PIL import Image, ImageEnhance, ImageFont, ImageDraw, ImageOps, ImageFilter
from io import BytesIO
import os
import demoji
import core1.coin as coin

_isDebug = False
_recentPlay = '{"data":{"recentRecords":[{"date":"2023-07-23T19:45:46.633Z","chart":{"difficulty":12,"level":{"uid":"claris.nisekoi.click.jf"}},"id":18020656,"owner":{"uid":"jujukim","registrationDate":"2023-07-23T17:55:14.761Z"},"score":98119},{"date":"2023-07-23T19:45:25.761Z","chart":{"difficulty":6,"level":{"uid":"lumixanth.partenza"}},"id":18020655,"owner":{"uid":"aizakku_hayati","registrationDate":"2022-04-15T02:59:38.210Z"},"score":151418},{"date":"2023-07-23T19:43:47.188Z","chart":{"difficulty":3,"level":{"uid":"flina.rinne"}},"id":18020651,"owner":{"uid":"jujukim","registrationDate":"2023-07-23T17:55:14.761Z"},"score":518640},{"date":"2023-07-23T19:43:02.213Z","chart":{"difficulty":16,"level":{"uid":"flina.touhou.time_freeze"}},"id":18020649,"owner":{"uid":"jokre","registrationDate":"2023-05-27T09:24:47.639Z"},"score":601263},{"date":"2023-07-23T19:42:46.405Z","chart":{"difficulty":6,"level":{"uid":"lumixanth.partenza"}},"id":18020647,"owner":{"uid":"aizakku_hayati","registrationDate":"2022-04-15T02:59:38.210Z"},"score":329614},{"date":"2023-07-23T19:41:24.921Z","chart":{"difficulty":12,"level":{"uid":"io.cytoid.alternativedestination"}},"id":18020644,"owner":{"uid":"mr_reggie","registrationDate":"2023-05-20T14:19:14.021Z"},"score":737457},{"date":"2023-07-23T19:40:20.985Z","chart":{"difficulty":1,"level":{"uid":"lumixanth.partenza"}},"id":18020640,"owner":{"uid":"aizakku_hayati","registrationDate":"2022-04-15T02:59:38.210Z"},"score":734708},{"date":"2023-07-23T19:39:19.081Z","chart":{"difficulty":14,"level":{"uid":"mdk.kagetora"}},"id":18020637,"owner":{"uid":"jaguar5c","registrationDate":"2020-08-13T05:40:41.851Z"},"score":930269},{"date":"2023-07-23T19:39:08.662Z","chart":{"difficulty":8,"level":{"uid":"rabpet.sos"}},"id":18020636,"owner":{"uid":"ikhwan_8000","registrationDate":"2022-12-19T11:00:15.534Z"},"score":921925},{"date":"2023-07-23T19:39:00.841Z","chart":{"difficulty":16,"level":{"uid":"9sp.daat1stseekersouls"}},"id":18020635,"owner":{"uid":"9223372_sp","registrationDate":"2021-04-15T11:11:09.900Z"},"score":926717},{"date":"2023-07-23T19:38:01.193Z","chart":{"difficulty":1,"level":{"uid":"lumixanth.partenza"}},"id":18020632,"owner":{"uid":"aizakku_hayati","registrationDate":"2022-04-15T02:59:38.210Z"},"score":387353},{"date":"2023-07-23T19:36:36.410Z","chart":{"difficulty":12,"level":{"uid":"io.cytoid.ginevra"}},"id":18020628,"owner":{"uid":"jaguar5c","registrationDate":"2020-08-13T05:40:41.851Z"},"score":959472},{"date":"2023-07-23T19:36:12.979Z","chart":{"difficulty":5,"level":{"uid":"gfsd.damonisch"}},"id":18020627,"owner":{"uid":"rinabina","registrationDate":"2023-07-23T19:20:29.680Z"},"score":980920},{"date":"2023-07-23T19:35:26.406Z","chart":{"difficulty":13,"level":{"uid":"bc.paranoia"}},"id":18020625,"owner":{"uid":"touhoulover1234","registrationDate":"2023-07-23T07:53:47.037Z"},"score":181024},{"date":"2023-07-23T19:34:21.391Z","chart":{"difficulty":14,"level":{"uid":"bombman.c2.bigscaryandpink"}},"id":18020624,"owner":{"uid":"ikhwan_8000","registrationDate":"2022-12-19T11:00:15.534Z"},"score":571640}]}}'
_userRecentPlay = '{"data":{"profile":{"recentRecords":[{"chart":{"difficulty":0,"level":{"uid":"emc.grievouslady","title":"Grievous Lady - nothing is but what is not"}},"score":1000000},{"chart":{"difficulty":0,"level":{"uid":"emc.grievouslady","title":"Grievous Lady - nothing is but what is not"}},"score":0},{"chart":{"difficulty":0,"level":{"uid":"emc.grievouslady","title":"Grievous Lady - nothing is but what is not"}},"score":1000000},{"chart":{"difficulty":15,"level":{"uid":"kima.nuclear","title":"Nuclear 10466211"}},"score":999816},{"chart":{"difficulty":15,"level":{"uid":"kima.nuclear","title":"Nuclear 10466211"}},"score":998575}]}}}'
_randomChart = '{"id":18341,"version":1,"uid":"birb.altostratus","title":"[P/S]Altostratus","metadata":{"title":"[P/S]Altostratus","artist":{"url":"https://youtu.be/uhGhZawkbpQ","name":"Syatten","localized_name":"Syatten"},"charter":{"name":"birb"},"illustrator":{"url":" ","name":" "},"title_localized":"Altostratus"},"duration":125.47171,"size":3736804,"description":"","censored":null,"tags":["Syatten","Tone Sphere","bit192","Altostratus"],"category":[],"ownerId":"d827b3ab-9006-4b7f-bbb7-7a5bc10d856d","creationDate":"2023-07-08T17:46:14.646Z","modificationDate":"2023-07-08T17:47:21.110Z","charts":[{"id":34368,"name":"easy","type":"easy","difficulty":2,"notesCount":151},{"id":34369,"name":"hard","type":"hard","difficulty":6,"notesCount":444}],"owner":{"id":"d827b3ab-9006-4b7f-bbb7-7a5bc10d856d","uid":"ricebirb","name":null,"role":"user","active":true,"avatar":{"original":"https://assets.cytoid.io/avatar/78bg2xS73sRpV7tZrIAuPSSzEEfXjETLAOtetnr99P85VQgHFhjkGdb41IzmV4gITY","small":"https://images.cytoid.io/avatar/78bg2xS73sRpV7tZrIAuPSSzEEfXjETLAOtetnr99P85VQgHFhjkGdb41IzmV4gITY?h=64&w=64","medium":"https://images.cytoid.io/avatar/78bg2xS73sRpV7tZrIAuPSSzEEfXjETLAOtetnr99P85VQgHFhjkGdb41IzmV4gITY?h=128&w=128","large":"https://images.cytoid.io/avatar/78bg2xS73sRpV7tZrIAuPSSzEEfXjETLAOtetnr99P85VQgHFhjkGdb41IzmV4gITY?h=256&w=256"}},"state":"PUBLIC","cover":{"original":"https://assets.cytoid.io/levels/bundles/dN4cAf7uv4htXSEMDEiStlNYM3ljsHk4lj3WN8sNevldMQhfss6ItceqJjWPr9PYFWg/background.png","thumbnail":"https://images.cytoid.io/levels/bundles/dN4cAf7uv4htXSEMDEiStlNYM3ljsHk4lj3WN8sNevldMQhfss6ItceqJjWPr9PYFWg/background.png?h=360&w=576","cover":"https://images.cytoid.io/levels/bundles/dN4cAf7uv4htXSEMDEiStlNYM3ljsHk4lj3WN8sNevldMQhfss6ItceqJjWPr9PYFWg/background.png?h=800&w=1280","stripe":"https://images.cytoid.io/levels/bundles/dN4cAf7uv4htXSEMDEiStlNYM3ljsHk4lj3WN8sNevldMQhfss6ItceqJjWPr9PYFWg/background.png?h=800&w=768"},"music":"https://assets.cytoid.io/levels/bundles/dN4cAf7uv4htXSEMDEiStlNYM3ljsHk4lj3WN8sNevldMQhfss6ItceqJjWPr9PYFWg/music.ogg","musicPreview":"https://assets.cytoid.io/levels/bundles/dN4cAf7uv4htXSEMDEiStlNYM3ljsHk4lj3WN8sNevldMQhfss6ItceqJjWPr9PYFWg/preview.ogg"}'
_userMostRecentPlay = '{"data":{"profile":{"recentRecords":[{"chart":{"difficulty":0,"type":"extreme","name":"Cataclysm","level":{"uid":"emc.grievouslady","title":"Grievous Lady - nothing is but what is not"},"notesCount":2},"date":"2023-07-22T16:31:13.946Z","mods":[],"score":1000000,"accuracy":1,"rating":0,"details":{"perfect":2,"great":0,"good":0,"bad":0,"miss":0,"maxCombo":2}}]}}}'


def reChangetitlte(html_string):
    html_string = re.sub("\n", "", html_string)
    pattern = r">(.*?)(?=[<]|$)"
    matches = re.findall(pattern, html_string)
    extracted_text = ""
    if matches:
        for i in range(len(matches)):
            extracted_text += matches[i]
        return extracted_text
    else:
        return html_string

def getUserMsnRecord(uid):
    url = "https://services.cytoid.io/graphql"
    params = {
        "query":
        f"""query StudioAnalytics($uid: String = "{uid}"){{
            profile(uid: $uid) {{
                recentRecords(limit: 8) {{
                    ...Recordment
                }}
            }}
        }}
        fragment Recordment on UserRecord{{
            chart {{
                id}}
            date
            accuracy}}
  
   """
    }
    if _isDebug:
        raw_data = _userMostRecentPlay
    else:
        raw_data = requests.get(url, params).content.decode("utf-8")
    plays = json.loads(raw_data)
    return plays["data"]["profile"]["recentRecords"]

def getPlay(uid_to_match):
    url = f"https://services.cytoid.io/search/levels?search={uid_to_match}"
    raw_data = requests.get(url).content.decode("utf-8")
    page_content = json.loads(raw_data)
    for i in range(len(page_content)):
        if page_content[i]["uid"] in uid_to_match:
            plays = int(page_content[i]["plays"])
            downloads = int(page_content[i]["downloads"])
            return downloads, plays
    return -1, -1


def getCytoidRecentPlay(checkLimit=1):
    url = "https://services.cytoid.io/graphql"
    params = {
        "query":
        f"""query StudioAnalytics($uid: Int = {checkLimit}){{
            recentRecords(limit: $uid,ranked:true) {{
                ...Recordment
            }}
        }}
        fragment Recordment on Record{{
            date
            chart {{
                difficulty
                level {{
                    uid
                }} 
            }}
            id
            owner{{
                name
                uid
                registrationDate
            }}
            score
        }}"""
    }
    if _isDebug:
        raw_data = _recentPlay
    else:
        raw_data = requests.get(url, params).content.decode("utf-8")
    plays = json.loads(raw_data)
    return plays["data"]["recentRecords"]


def getUserRecentPlay(uid, checkLimit=5):
    url = "https://services.cytoid.io/graphql"
    params = {
        "query":
        f"""query StudioAnalytics($uid: String = "{uid}") {{
            profile(uid: $uid) {{
                recentRecords(limit: {checkLimit}) {{
                    ...Recordment
                }}
            }}
        }}
        fragment Recordment on UserRecord{{
            chart {{
                difficulty
                level {{
                uid
                title
                }}
            }}
            score
        }}"""
    }
    if _isDebug:
        raw_data = _userRecentPlay
    else:
        raw_data = requests.get(url, params).content.decode("utf-8")
    plays = json.loads(raw_data)
    return plays["data"]["profile"]["recentRecords"]


def getUserMostRecentPlay(uid):
    url = "https://services.cytoid.io/graphql"
    params = {
        "query":
        f"""query StudioAnalytics($uid: String = "{uid}") {{
            profile(uid: $uid) {{
                recentRecords(limit: 1) {{
                    ...Recordment
                }}
            }}
        }}
        fragment Recordment on UserRecord{{
            chart {{
                difficulty
                type
                id
                name
                level {{
                    uid
                    title
                }}
                notesCount
            }}
            date
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
        }}"""
    }
    if _isDebug:
        raw_data = _userMostRecentPlay
    else:
        raw_data = requests.get(url, params).content.decode("utf-8")
    plays = json.loads(raw_data)
    return plays["data"]["profile"]["recentRecords"][0]


def getLevelData(levelId):
    if _isDebug:
        raw_data = _randomChart
        levelData = json.loads(raw_data)
        return levelData

    url = f"https://services.cytoid.io/levels/{levelId}"
    raw_data = requests.get(url).content.decode("utf-8")
    levelData = json.loads(raw_data)
    return levelData


# Z H E = EZ HD EX
def getLevelDiff(levelId):
    url = "https://services.cytoid.io/levels/" + levelId
    raw_data = requests.get(url).content.decode("utf-8")
    levelData = json.loads(raw_data)
    difflist = ""
    for i in range(len(levelData["charts"])):
        if "extreme" in levelData["charts"][i]["type"]:
            difflist += "E"
        if "hard" in levelData["charts"][i]["type"]:
            difflist += "H"
        if "easy" in levelData["charts"][i]["type"]:
            difflist += "Z"
    return difflist


def getProfileData(playerId):
    if _isDebug:
        raw_data = _randomChart
        levelData = json.loads(raw_data)
        return levelData
    url = "https://services.cytoid.io/profile/" + playerId
    raw_data = requests.get(url).content.decode("utf-8")
    profileData = json.loads(raw_data)

    return profileData


def getRandomChart(url, exclude_black_list=False):
    if _isDebug:
        raw_data = _randomChart
        levelData = json.loads(raw_data)
        return levelData
    blackList = ["cy7", "bentux", "bentuxthecowben"]
    if not exclude_black_list:
        blackList = []
    raw_data = requests.get(url).content.decode("utf-8")
    if "statusCode" in raw_data:
        return None
    levelData = json.loads(raw_data)
    while True:
        r = random.choices(population=[
            0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18,
            19, 20, 21, 22, 23
        ],
            weights=[
            16.5, 7, 7, 7, 3.5, 3.5, 3.5, 3.5, 3.5, 3.5,
            3.5, 3.5, 3.5, 3.5, 3.5, 3.5, 3.5, 3.5, 3.5, 2,
            2, 2, 2, 2
        ])[0]
        print("ran:", r)
        author = levelData[r]["owner"]["uid"]
        if author not in blackList:
            return levelData[r]


def getRateDistribution(levelId):
    url = "https://services.cytoid.io/levels/" + levelId + "/ratings"
    raw_data = requests.get(url).content.decode("utf-8")
    ratings = json.loads(raw_data)
    return ratings


def getRate(levelId):
    rating = getRateDistribution(levelId)["average"]
    if rating == None:
        return -1
    return rating / 2


def getLevelLeaderboard(levelId, diffType):
    url = f"https://services.cytoid.io/levels/{levelId}/charts/{diffType}/records?limit=1000"
    raw_data = requests.get(url).content.decode("utf-8")
    leaderboard = json.loads(raw_data)
    return leaderboard


def checkCytoidID(cytoidID, msgauthor, getID=False):
    if "me" == cytoidID or re.match(r"<[@!]+[0-9]+>", cytoidID):
        # cytoidID = func.ment(message.author, cytoidID, message.author.guild)
        cytoidID = func.mentionReplacement(msgauthor, cytoidID, isId=True)
        cytoidID = coin.getUserAttrib(str(cytoidID), "bind", "ctd")
        if not cytoidID:
            return "nobindctd"
        elif getID == True:
            return cytoidID
    check1 = requests.get(f"https://services.cytoid.io/profile/{cytoidID}")
    check1a = json.loads(check1.content.decode("utf-8"))
    if "statusCode" in check1a:
        return "nofindctd"
    elif check1a["activities"]["totalRankedPlays"] == 0:
        return "norecord"
    elif getID == True:
        return cytoidID
    elif getID == False:
        return "Yes"


def isValidLevelId(mystr):
    for c in mystr:
        if c not in "abcdefghijklmnopqrstuvwxyz._-0123456789":
            return False
    return True


def checkId(ID, category):
    if str(category) in ["level", "0"]:
        if str(ID) != re.sub("[^a-z.\-_0-9]+", "", ID):
            return "nofindctdlevel"
        check1 = requests.get(f"https://services.cytoid.io/levels/{ID}")
        check1a = json.loads(check1.content.decode("utf-8"))
        if "statusCode" in check1a:
            return "nofindctdlevel"
        return "Yes"
    elif str(category) in ["user", "1", "player"]:
        if str(ID) != re.sub("[^a-z.\-_0-9]+", "", ID):
            return "nofindctd"
        check1 = requests.get(f"https://services.cytoid.io/profile/{ID}")
        check1a = json.loads(check1.content.decode("utf-8"))
        if "statusCode" in check1a:
            return "nofindctd"
        return "Yes"


def checkLevelID(levelID):
    if str(levelID) != re.sub("[^a-z.\-_0-9]+", "", levelID):
        return "nofindctdlevel"
    check1 = requests.get(f"https://services.cytoid.io/levels/{levelID}")
    check1a = json.loads(check1.content.decode("utf-8"))
    if "statusCode" in check1a:
        return "nofindctdlevel"
    return "Yes"


def getPvpDetail(record, cate):
    record_data = record["details"]
    chart = record["chart"]
    if cate == "details":
        return record_data["perfect"], record_data["great"], record_data["good"], record_data["bad"], record_data["miss"]
    return record["score"], record["accuracy"], record["mods"], chart["notesCount"], 0


def getPvpPoint(perfect1, great1, good1, bad1, miss1, notes1, acc1):
    num1a = 0
    if miss1 > 0:
        num1a = 1 / math.sqrt(miss1 / 2)
    num1b = 0.2
    if great1 > 0:
        num1b = ((notes1 * acc1) - perfect1 -
                 (good1 * 0.3)) / great1
    total1 = ((((miss1**2) * (num1a)) / (math.log(notes1, 50)**3) + 0.6 * miss1) *
              (-1) + (bad1 * (-0.735)) + (good1 * (-0.2)) + (num1b - 0.2) + (perfect1 * 1.05))
    total1a = math.exp((total1 / (notes1 * 1.05)) - 1)
    return total1, total1a


def getPvpImg(leveldata, diff_index, playerAid, playerBid, levelid):
    type = leveldata["charts"][diff_index]["type"]
    diff = leveldata["charts"][diff_index]["difficulty"]
    lid = leveldata["charts"][diff_index]["id"]
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
    check1a = getProfileData(playerAid)
    check2a = getProfileData(playerBid)
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
    font_path = "font/MPLUSRounded1c-Regular.ttf"
    font_path1 = "font/MPLUSRounded1c-Bold.ttf"
    font_path3 = "font/ARIALN.TTF"
    font_path4 = "font/NotoSansSC-Medium.otf"
    font_path5 = "font/NotoSans-Regular.ttf"
    f1 = ImageFont.truetype(font_path5, 60, encoding='utf-8')
    f2 = ImageFont.truetype(font_path, 42, encoding='utf-8')
    f2a = ImageFont.truetype(font_path, 37, encoding='utf-8')
    f2b = ImageFont.truetype(font_path, 30, encoding='utf-8')
    f2c = ImageFont.truetype(font_path, 18, encoding='utf-8')
    h1 = 21
    title = leveldata["title"]
    if func.judge_language(title) in ["ja", "zh"]:
        f1 = ImageFont.truetype(font_path4, 67)
        if len(re.findall("[^\0]", leveldata["title"])) > 13:
            non_alphanumeric_count = len(re.findall(
                r"[^\0 ('.~a-z0-9A-Z]", title))  # 不包括字母和數字的字符數
            punctuation_count = len(
                re.findall(r"[()'.]", title))  # 標點符號字符數
            lower_alphanumeric_count = len(re.findall(
                r"[ ~a-z0-9]", title))  # 小寫字母、數字和空格字符數
            upper_count = len(re.findall(r"[A-Z]", title))  # 大寫字母字符數
            size = 78 - round(non_alphanumeric_count * 1.77 + punctuation_count *
                              0.2 + lower_alphanumeric_count * 0.75 + upper_count * 1.35)
            h1 = h1 + round((78 - size) / 6)
            f1 = ImageFont.truetype(font_path4, size)
    elif func.judge_language(title) == "en":
        f1 = ImageFont.truetype(font_path3, 80, encoding='utf-8')
        if len(re.findall("[^\0]", title)) > 24:
            size = 100 - int(len(re.findall("[^\0]", title)) * 1.26)
            f1 = ImageFont.truetype(font_path3, size, encoding='utf-8')
            h1 = h1 + round((102 - size) / 12)
    title = demoji.replace(leveldata["title"], "")
    drawtext.text((150, h1), title, "#ffffff", font=f1)
    drawtext.text((188, 178), playerAid, "#ffffff", font=f2)
    drawtext.text((188, 483), playerBid, "#ffffff", font=f2)
    drawtext.text((150, 101), levelid, "#ffffff", font=f2a)
    drawtext.text(
        (150, 2), 'Generated by "dy6ot bot" | Based on CytoidAPI', "#ffffff", font=f2c)
    user1 = getUserMostRecentPlay(playerAid)
    user2 = getUserMostRecentPlay(playerBid)
    if (user1["chart"]["id"] or user2["chart"]["id"]) != lid:
        return False
    date1 = MostRecentPlay.getPlayTimeImg(user1["date"], True)
    score1, acc1, mods1, notes1, * \
        _ = getPvpDetail(user1, "chart")
    score2, acc2, mods2, notes2, * \
        _ = getPvpDetail(user2, "chart")
    perfect1, great1, good1, bad1, miss1 = getPvpDetail(
        user1, "details")
    perfect2, great2, good2, bad2, miss2 = getPvpDetail(
        user2, "details")
    total1, total1a = getPvpPoint(
        perfect1, great1, good1, bad1, miss1, notes1, acc1)
    total2, total2a = getPvpPoint(
        perfect2, great2, good2, bad2, miss2, notes2, acc2)
    loc = 190
    if mods1 != None:
        for i in range(len(mods1)):
            path = f"./mod/{mods1[i]}.png"
            modpng = Image.open(path).convert("RGBA")
            modpng1 = modpng.resize((62, 45), Image.LANCZOS)
            pvpimg.paste(modpng1, box=(loc, 240), mask=modpng1)
            loc = loc + 80
    loc = 190
    if mods2 != None:
        for i in range(len(mods2)):
            path = f"./mod/{mods2[i]}.png"
            modpng = Image.open(path).convert("RGBA")
            modpng2 = modpng.resize((62, 45), Image.LANCZOS)
            pvpimg.paste(modpng2, box=(loc, 545), mask=modpng2)
            loc = loc + 80
    f3 = ImageFont.truetype(font_path1, 115, encoding='utf-8')
    f4 = ImageFont.truetype(font_path1, 84, encoding='utf-8')
    f5 = ImageFont.truetype(font_path1, 88, encoding='utf-8')
    f6 = ImageFont.truetype(font_path, 45, encoding='utf-8')
    f7 = ImageFont.truetype(font_path1, 36, encoding='utf-8')
    f8 = ImageFont.truetype(font_path1, 105, encoding='utf-8')
    f9 = ImageFont.truetype(font_path4, 160, encoding='utf-8')
    if diff > 15:
        diff = "15+"
    elif diff < 1:
        diff = "？"
    color = "#FF2D2D"
    if type == "hard":
        color = "#B15BFF"
    elif type == "easy":
        color = "#4DFFFF"
    drawtext.text((1052, -18), str(diff), color, font=f8)
    drawtext.text((55, 262), "▢", "#2894FF", font=f9)
    drawtext.text((55, 562), "▢", "#2894FF", font=f9)
    drawtext.text((67, 302), "PT", "#9AFF02", font=f3)
    drawtext.text((67, 602), "PT", "#9AFF02", font=f3)
    drawtext.text(
        (233, 293), f"{format(total1a*100,'.2f')}%", "#ffffff", font=f4)
    drawtext.text(
        (233, 593), f"{format(total2a*100,'.2f')}%", "#ffffff", font=f4)
    drawtext.text(
        (240, 407), f"{format(total1,'.2f')}", "#ffffff", font=f7)
    drawtext.text(
        (240, 707), f"{format(total2,'.2f')}", "#ffffff", font=f7)
    drawtext.text((645, 180), str(score1), "#ffffff", font=f5)
    drawtext.text((645, 485), str(score2), "#ffffff", font=f5)
    drawtext.text(
        (1066, 222), f"{format(acc1*100,'.2f')}%", "#ffffff", font=f6)
    drawtext.text(
        (1066, 527), f"{format(acc2*100,'.2f')}%", "#ffffff", font=f6,)
    drawtext.text((815, 110), str(date1), "#ffffff", font=f2b)
    drawtext.text((645, 340),
                  f"{perfect1}p / {great1}gr / {good1}g / {bad1}b / {miss1}m",
                  "#ffffff", font=f2a,)
    drawtext.text((645, 645),
                  f"{perfect2}p / {great2}gr / {good2}g / {bad2}b / {miss2}m",
                  "#ffffff", font=f2a,)
    pvpimg.save("./photo/pvp.png")
    return True


if __name__ == "__main__":
    test = "Default debug mesage"
    test = getCytoidRecentPlay(15)
    # test = getUserRecentPlay("cheongsn")
    # test = getRandomChart(2)
    # test = getUserMostRecentPlay("cheongsn")
    print(test)
