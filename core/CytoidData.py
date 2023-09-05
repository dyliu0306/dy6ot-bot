import json
import requests
import random
import re
import core.func as func

_isDebug = False
_recentPlay = '{"data":{"recentRecords":[{"date":"2023-07-23T19:45:46.633Z","chart":{"difficulty":12,"level":{"uid":"claris.nisekoi.click.jf"}},"id":18020656,"owner":{"uid":"jujukim","registrationDate":"2023-07-23T17:55:14.761Z"},"score":98119},{"date":"2023-07-23T19:45:25.761Z","chart":{"difficulty":6,"level":{"uid":"lumixanth.partenza"}},"id":18020655,"owner":{"uid":"aizakku_hayati","registrationDate":"2022-04-15T02:59:38.210Z"},"score":151418},{"date":"2023-07-23T19:43:47.188Z","chart":{"difficulty":3,"level":{"uid":"flina.rinne"}},"id":18020651,"owner":{"uid":"jujukim","registrationDate":"2023-07-23T17:55:14.761Z"},"score":518640},{"date":"2023-07-23T19:43:02.213Z","chart":{"difficulty":16,"level":{"uid":"flina.touhou.time_freeze"}},"id":18020649,"owner":{"uid":"jokre","registrationDate":"2023-05-27T09:24:47.639Z"},"score":601263},{"date":"2023-07-23T19:42:46.405Z","chart":{"difficulty":6,"level":{"uid":"lumixanth.partenza"}},"id":18020647,"owner":{"uid":"aizakku_hayati","registrationDate":"2022-04-15T02:59:38.210Z"},"score":329614},{"date":"2023-07-23T19:41:24.921Z","chart":{"difficulty":12,"level":{"uid":"io.cytoid.alternativedestination"}},"id":18020644,"owner":{"uid":"mr_reggie","registrationDate":"2023-05-20T14:19:14.021Z"},"score":737457},{"date":"2023-07-23T19:40:20.985Z","chart":{"difficulty":1,"level":{"uid":"lumixanth.partenza"}},"id":18020640,"owner":{"uid":"aizakku_hayati","registrationDate":"2022-04-15T02:59:38.210Z"},"score":734708},{"date":"2023-07-23T19:39:19.081Z","chart":{"difficulty":14,"level":{"uid":"mdk.kagetora"}},"id":18020637,"owner":{"uid":"jaguar5c","registrationDate":"2020-08-13T05:40:41.851Z"},"score":930269},{"date":"2023-07-23T19:39:08.662Z","chart":{"difficulty":8,"level":{"uid":"rabpet.sos"}},"id":18020636,"owner":{"uid":"ikhwan_8000","registrationDate":"2022-12-19T11:00:15.534Z"},"score":921925},{"date":"2023-07-23T19:39:00.841Z","chart":{"difficulty":16,"level":{"uid":"9sp.daat1stseekersouls"}},"id":18020635,"owner":{"uid":"9223372_sp","registrationDate":"2021-04-15T11:11:09.900Z"},"score":926717},{"date":"2023-07-23T19:38:01.193Z","chart":{"difficulty":1,"level":{"uid":"lumixanth.partenza"}},"id":18020632,"owner":{"uid":"aizakku_hayati","registrationDate":"2022-04-15T02:59:38.210Z"},"score":387353},{"date":"2023-07-23T19:36:36.410Z","chart":{"difficulty":12,"level":{"uid":"io.cytoid.ginevra"}},"id":18020628,"owner":{"uid":"jaguar5c","registrationDate":"2020-08-13T05:40:41.851Z"},"score":959472},{"date":"2023-07-23T19:36:12.979Z","chart":{"difficulty":5,"level":{"uid":"gfsd.damonisch"}},"id":18020627,"owner":{"uid":"rinabina","registrationDate":"2023-07-23T19:20:29.680Z"},"score":980920},{"date":"2023-07-23T19:35:26.406Z","chart":{"difficulty":13,"level":{"uid":"bc.paranoia"}},"id":18020625,"owner":{"uid":"touhoulover1234","registrationDate":"2023-07-23T07:53:47.037Z"},"score":181024},{"date":"2023-07-23T19:34:21.391Z","chart":{"difficulty":14,"level":{"uid":"bombman.c2.bigscaryandpink"}},"id":18020624,"owner":{"uid":"ikhwan_8000","registrationDate":"2022-12-19T11:00:15.534Z"},"score":571640}]}}'
_userRecentPlay = '{"data":{"profile":{"recentRecords":[{"chart":{"difficulty":0,"level":{"uid":"emc.grievouslady","title":"Grievous Lady - nothing is but what is not"}},"score":1000000},{"chart":{"difficulty":0,"level":{"uid":"emc.grievouslady","title":"Grievous Lady - nothing is but what is not"}},"score":0},{"chart":{"difficulty":0,"level":{"uid":"emc.grievouslady","title":"Grievous Lady - nothing is but what is not"}},"score":1000000},{"chart":{"difficulty":15,"level":{"uid":"kima.nuclear","title":"Nuclear 10466211"}},"score":999816},{"chart":{"difficulty":15,"level":{"uid":"kima.nuclear","title":"Nuclear 10466211"}},"score":998575}]}}}'
_randomChart = '{"id":18341,"version":1,"uid":"birb.altostratus","title":"[P/S]Altostratus","metadata":{"title":"[P/S]Altostratus","artist":{"url":"https://youtu.be/uhGhZawkbpQ","name":"Syatten","localized_name":"Syatten"},"charter":{"name":"birb"},"illustrator":{"url":" ","name":" "},"title_localized":"Altostratus"},"duration":125.47171,"size":3736804,"description":"","censored":null,"tags":["Syatten","Tone Sphere","bit192","Altostratus"],"category":[],"ownerId":"d827b3ab-9006-4b7f-bbb7-7a5bc10d856d","creationDate":"2023-07-08T17:46:14.646Z","modificationDate":"2023-07-08T17:47:21.110Z","charts":[{"id":34368,"name":"easy","type":"easy","difficulty":2,"notesCount":151},{"id":34369,"name":"hard","type":"hard","difficulty":6,"notesCount":444}],"owner":{"id":"d827b3ab-9006-4b7f-bbb7-7a5bc10d856d","uid":"ricebirb","name":null,"role":"user","active":true,"avatar":{"original":"https://assets.cytoid.io/avatar/78bg2xS73sRpV7tZrIAuPSSzEEfXjETLAOtetnr99P85VQgHFhjkGdb41IzmV4gITY","small":"https://images.cytoid.io/avatar/78bg2xS73sRpV7tZrIAuPSSzEEfXjETLAOtetnr99P85VQgHFhjkGdb41IzmV4gITY?h=64&w=64","medium":"https://images.cytoid.io/avatar/78bg2xS73sRpV7tZrIAuPSSzEEfXjETLAOtetnr99P85VQgHFhjkGdb41IzmV4gITY?h=128&w=128","large":"https://images.cytoid.io/avatar/78bg2xS73sRpV7tZrIAuPSSzEEfXjETLAOtetnr99P85VQgHFhjkGdb41IzmV4gITY?h=256&w=256"}},"state":"PUBLIC","cover":{"original":"https://assets.cytoid.io/levels/bundles/dN4cAf7uv4htXSEMDEiStlNYM3ljsHk4lj3WN8sNevldMQhfss6ItceqJjWPr9PYFWg/background.png","thumbnail":"https://images.cytoid.io/levels/bundles/dN4cAf7uv4htXSEMDEiStlNYM3ljsHk4lj3WN8sNevldMQhfss6ItceqJjWPr9PYFWg/background.png?h=360&w=576","cover":"https://images.cytoid.io/levels/bundles/dN4cAf7uv4htXSEMDEiStlNYM3ljsHk4lj3WN8sNevldMQhfss6ItceqJjWPr9PYFWg/background.png?h=800&w=1280","stripe":"https://images.cytoid.io/levels/bundles/dN4cAf7uv4htXSEMDEiStlNYM3ljsHk4lj3WN8sNevldMQhfss6ItceqJjWPr9PYFWg/background.png?h=800&w=768"},"music":"https://assets.cytoid.io/levels/bundles/dN4cAf7uv4htXSEMDEiStlNYM3ljsHk4lj3WN8sNevldMQhfss6ItceqJjWPr9PYFWg/music.ogg","musicPreview":"https://assets.cytoid.io/levels/bundles/dN4cAf7uv4htXSEMDEiStlNYM3ljsHk4lj3WN8sNevldMQhfss6ItceqJjWPr9PYFWg/preview.ogg"}'
_userMostRecentPlay = '{"data":{"profile":{"recentRecords":[{"chart":{"difficulty":0,"type":"extreme","name":"Cataclysm","level":{"uid":"emc.grievouslady","title":"Grievous Lady - nothing is but what is not"},"notesCount":2},"date":"2023-07-22T16:31:13.946Z","mods":[],"score":1000000,"accuracy":1,"rating":0,"details":{"perfect":2,"great":0,"good":0,"bad":0,"miss":0,"maxCombo":2}}]}}}'


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

    url = "https://services.cytoid.io/levels/" + levelId
    raw_data = requests.get(url).content.decode("utf-8")
    levelData = json.loads(raw_data)

    return levelData

#Z H E = EZ HD EX
def getLevelDiff(levelId):
    url = "https://services.cytoid.io/levels/" + levelId
    raw_data = requests.get(url).content.decode("utf-8")
    levelData = json.loads(raw_data)
    difflist=""
    for i in range(len(levelData["charts"])):
        if "extreme" in levelData["charts"][i]["type"]:
            difflist+="E"
        if "hard" in levelData["charts"][i]["type"]:
            difflist+="H"
        if "easy" in levelData["charts"][i]["type"]:
            difflist+="Z"
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


def getRandomChart(level=-1, exclude_black_list=False):
    if _isDebug:
        raw_data = _randomChart
        levelData = json.loads(raw_data)
        return levelData

    if level > 16:
        level = 16

    count_down = 13

    page_low_bound = 1
    page_upper_bound = 1010
    if level >= 14:
        page_upper_bound = 520
    elif level > 0:
        page_low_bound = 510

    blackList = ["cy7"]
    if not exclude_black_list:
        blackList = []
    time_limit = 600

    while count_down > 0:
        if abs(page_low_bound - page_upper_bound) <= 3:
            return None

        page_random = random.randrange(page_low_bound, page_upper_bound)
        url = (
            "https://services.cytoid.io/levels?&sort=difficulty&order=desc&category=all&page="
            + str(page_random))
        raw_data = requests.get(url).content.decode("utf-8")
        random_page_data = json.loads(raw_data)
        r = random.randrange(0, 9)

        max = -1
        for chart in random_page_data[r]["charts"]:
            chart_level = chart["difficulty"]
            if chart_level > 16:
                chart_level = 16
            elif chart_level < 0:
                chart_level = 0

            if chart_level == level or level == -1:
                # 只有這裡是成功的部分
                levelData = getLevelData(random_page_data[r]["uid"])
                author = levelData["owner"]["uid"]
                duration = levelData["duration"]
                if author in blackList or duration >= time_limit:
                    continue
                return levelData

            elif chart_level > max:
                max = chart_level

        if max < level:
            page_upper_bound = page_random - 1
        elif max > level:
            page_low_bound = page_random + 1

        count_down -= 1

    return None


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

def checkCytoidID(cytoidID,msgauthor,getID=False):
    key=0
    if "me" == cytoidID or re.match(r"<[@!]+[0-9]+>", cytoidID):
        # cytoidID = func.ment(message.author, cytoidID, message.author.guild)
        cytoidID = func.mentionReplacement(msgauthor, cytoidID)
        cytoidID = func.get_ctdid(cytoidID)
        if "e404" in cytoidID:
            return "nobindctd" 
        else:
            key=1
    check1 = requests.get(f"https://services.cytoid.io/profile/{cytoidID}")
    check1a = json.loads(check1.content.decode("utf-8"))
    print(cytoidID,key,"statusCode" in check1a,getID)
    if key==1 and getID==True:
        return cytoidID
    elif "statusCode" in check1a:
        return "nofindctd"
    elif getID==True:
        return cytoidID
    elif getID==False:
        return "Yes"
        

def checkLevelID(levelID):
    if str(levelID)!=re.sub("[^a-z.\-_0-9]+","",levelID):
        return "nofindctdlevel"
    check1 = requests.get(f"https://services.cytoid.io/levels/{levelID}")
    check1a = json.loads(check1.content.decode("utf-8"))
    if "statusCode" in check1a:
        return "nofindctdlevel"
    return "Yes"

if __name__ == "__main__":
    test = "Default debug mesage"
    test = getCytoidRecentPlay(15)
    # test = getUserRecentPlay("cheongsn")
    # test = getRandomChart(2)
    # test = getUserMostRecentPlay("cheongsn")
    print(test)
