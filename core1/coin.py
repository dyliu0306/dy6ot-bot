# coding:utf-8
import discord
import requests
import json
import re
import random
import math
from datetime import datetime, timedelta
import core1.func as func
import core1.CytoidData as CytoidData
import core1.MainTask as MainTask
from cogs.coin import Coin
import core1.func as func
import core1.CytoidData as CytoidData
import core1.MainTask as MainTask
from cogs.coin import Coin
import time


def getUserData(id, cate, lang="en", name=None, add=True):
    with open("coin/coin.json", "r") as f:
        txt = f.read()
        database = json.loads(txt)
    f.close()
    # 沒用過就新建
    if str(id) not in database.keys():
        if add:
            addUser(str(id), lang, name=name)
        return 0, True
    else:
        return int(database[str(id)][cate]), False


def getUserAttrib(id, attrib_cate, attrib_item, name=None):
    try:
        with open("coin/coin.json", "r") as f:
            txt = f.read()
            database = json.loads(txt)
        return database[str(id)][attrib_cate][attrib_item]
    except:
        addUser(str(id), name=name)
        return False


def addUser(id, lang="en", name=None, ctd=None):
    with open("coin/coin.json", "r") as f:
        txt = f.read()
        database = json.loads(txt)
        # 創建預設值
        database[str(id)] = {"name": name, "coin": 0, "setting": {
            "lang": f"{lang}", "gmt": 8, "lvrank": [12, 16]}, "bind": {"ctd": ctd}}
    with open("coin/coin.json", "w") as f1:
        json.dump(database, f1, indent=4, ensure_ascii=False)
    # 初使化record資料
    recordEvent(id, "coin", 0, 0, 0, True)


def changeUserData(id, cate, value, change, reason, name=None):
    # value=計算後餘額，change=變化金額
    with open("coin/coin.json", "r") as f:
        txt = f.read()
        database = json.loads(txt)
        database[str(id)][cate] = int(value)
        if name:
            database[str(id)]["name"] = name
    with open("coin/coin.json", "w") as f1:
        json.dump(database, f1, indent=4, ensure_ascii=False)
    recordEvent(id, cate, value, change, reason)


def changeUserAttrib(id, attrib_cate, attrib_item, value, value_type="s"):
    # value=設定值
    with open("coin/coin.json", "r") as f:
        txt = f.read()
        database = json.loads(txt)
        if value_type == "s":
            value = str(value)
        elif value_type == "o":
            pass
        elif value_type == "i":
            value = int(value)
        elif value_type == "f":
            value = float(value)
        else:
            pass
        database[str(id)][attrib_cate][attrib_item] = value
    with open("coin/coin.json", "w") as f1:
        json.dump(database, f1, indent=4, ensure_ascii=False)


def recordEvent(id, cate, value, change, reason, new=False):
    with open("coin/record.json", "r") as f:
        txt = f.read()
        database = json.loads(txt)
        time = datetime.now().timestamp()
        if new:
            database[str(id)] = {"coin": []}
        else:
            database[str(id)][cate].append([time, reason, change, value])
    with open("coin/record.json", "w") as f1:
        json.dump(database, f1, indent=4, ensure_ascii=False)


async def useCoupon(id, code, bot, ctx):
    with open("coin/coupon.json", "r") as f:
        txt = f.read()
        database = json.loads(txt)
        if code not in database.keys():
            return None, 0, 0
        elif int(id) in database[code]["user"]:
            return False, 0, 0
        UserCoin, FirstUse = getUserData(str(id), "coin")
        if FirstUse:
            await Coin(bot).firstuse(ctx)
        UserCoin += database[code]["cash"]
        changeUserData(str(id), "coin", UserCoin,
                       database[code]["cash"], "use coupon")
        database[code]["user"].append(int(id))
    with open("coin/coupon.json", "w") as f1:
        json.dump(database, f1, indent=4, ensure_ascii=False)
    return True, UserCoin, database[code]["cash"]


class getUserCooldown:
    # True=正在CD中，False=沒有CD記錄
    def sign(self, id):
        gmt = 8
        with open("coin/cooldown.json", "r") as f:
            txt = f.read()
            database = json.loads(txt)
            today = func.getCurrentDay(gmt)
            if today not in database["sign"].keys():
                return False
            elif id in database["sign"][today]:
                return True
            return False

    def played(self, id):
        gmt = 8
        with open("coin/cooldown.json", "r") as f:
            txt = f.read()
            database = json.loads(txt)
            today = func.getCurrentDay(gmt)
            if today not in database["played"].keys():
                return False
            elif id in database["played"][today]:
                return True
            return False

    def lottery(self):
        gmt = 8
        with open("coin/cooldown.json", "r") as f:
            txt = f.read()
            database = json.loads(txt)
            today = func.getCurrentDay(gmt)
            if int(today) != database["lottery"]:
                return True
            return False

    # 今天還沒人用過回傳False
    def mission(self, id):
        gmt = 8
        with open("coin/cooldown.json", "r") as f:
            txt = f.read()
            database = json.loads(txt)
            today = func.getCurrentDay(gmt)
            if today not in database["mission"].keys():
                return False
            elif id in database["mission"][today]:
                return True
            return False

    def clear(self, id):
        with open("coin/cooldown.json", "r") as f:
            txt = f.read()
            database = json.loads(txt)
            now = time.time()
            if str(id) not in database["clear"].keys():
                return False
            elif now-database["clear"][str(id)] > 30:
                return False
            return True


class changeUserCooldown:
    def sign(self, id):
        gmt = 8
        with open("coin/cooldown.json", "r") as f:
            txt = f.read()
            database = json.loads(txt)
            today = func.getCurrentDay(gmt)
            if today not in database["sign"].keys():
                database["sign"] = {f"{today}": [int(id)]}
            else:
                database["sign"][today].append(int(id))
        with open("coin/cooldown.json", "w") as f1:
            json.dump(database, f1, indent=4, ensure_ascii=False)

    def played(self, id):
        gmt = 8
        with open("coin/cooldown.json", "r") as f:
            txt = f.read()
            database = json.loads(txt)
            today = func.getCurrentDay(gmt)
            if today not in database["played"].keys():
                database["played"] = {f"{today}": [int(id)]}
            else:
                database["played"][today].append(int(id))
        with open("coin/cooldown.json", "w") as f1:
            json.dump(database, f1, indent=4, ensure_ascii=False)

    def lottery(self):
        gmt = 8
        with open("coin/cooldown.json", "r") as f:
            txt = f.read()
            database = json.loads(txt)
            today = func.getCurrentDay(gmt)
            if int(today) != database["lottery"]:
                database["lottery"] = int(today)
        with open("coin/cooldown.json", "w") as f1:
            json.dump(database, f1, indent=4, ensure_ascii=False)

    def mission(self, id):
        gmt = 8
        with open("coin/cooldown.json", "r") as f:
            txt = f.read()
            database = json.loads(txt)
            today = func.getCurrentDay(gmt)
            if today not in database["mission"].keys():
                database["mission"] = {f"{today}": [int(id)]}
            elif int(id) not in database["mission"][today]:
                database["mission"][today].append(int(id))
        with open("coin/cooldown.json", "w") as f1:
            json.dump(database, f1, indent=4, ensure_ascii=False)

    def clear(self, id):
        with open("coin/cooldown.json", "r") as f:
            txt = f.read()
            database = json.loads(txt)
            now = time.time()
            database["clear"][str(id)] = now
        with open("coin/cooldown.json", "w") as f1:
            json.dump(database, f1, indent=4, ensure_ascii=False)


class lottery:
    def choseWinner(self, bonus=5000):
        with open("coin/lottery.json", "r") as f:
            txt = f.read()
            database = json.loads(txt)
            # 過夜，回前一天
            current_date = datetime.now()+timedelta(hours=7)
            formatted_date = current_date.strftime("%y%m%d")
            if formatted_date not in database["pool"].keys():
                self.recordWinner(None, None, None)
                return None, None, None
            a = database["pool"][formatted_date]
            total_value = sum(a.values())
            probabilities = {key: value /
                             total_value for key, value in a.items()}
            winner_id = random.choices(
                list(probabilities.keys()), weights=list(probabilities.values()))[0]
            self.recordWinner(winner_id, probabilities[winner_id], total_value)

            UserCoin, FirstUse = getUserData(winner_id, "coin")
            total_value += bonus
            UserCoin += total_value
            changeUserData(winner_id, "coin", UserCoin,
                           total_value, "lottery winner")
            return winner_id, probabilities[winner_id], total_value-bonus

    def changeBetValue(self, id, value, gmt=8):
        # return 機率, 原投注金額
        with open("coin/lottery.json", "r") as f:
            txt = f.read()
            database = json.loads(txt)
            current_date = datetime.now()+timedelta(hours=gmt)
            formatted_date = current_date.strftime("%y%m%d")
            total_value = 1
            key = 0
            original_value = 0
            if formatted_date not in database["pool"].keys():
                database["pool"] = {formatted_date: {str(id): int(value)}}
                key = 1
            elif str(id) in database["pool"][formatted_date].keys():
                original_value = database["pool"][formatted_date][str(id)]
                key = 2
            if key != 1:
                database["pool"][formatted_date][str(id)] = int(value)
                a = database["pool"][formatted_date]
                total_value = sum(a.values())
        with open("coin/lottery.json", "w") as f1:
            json.dump(database, f1, indent=4, ensure_ascii=False)
        if key == 1:
            return 1, 0
        else:
            return 0 if total_value == 0 else value/total_value, original_value

    def recordWinner(self, id, percent, prize):
        with open("coin/lottery.json", "r") as f:
            txt = f.read()
            database = json.loads(txt)
            # 過夜，回前一天
            current_date = datetime.now()+timedelta(hours=7)
            formatted_date = current_date.strftime("%y%m%d")
            if formatted_date not in database["history"].keys():
                database["history"][formatted_date] = {
                    "winner": id, "percent": percent, "prize": prize}
        with open("coin/lottery.json", "w") as f1:
            json.dump(database, f1, indent=4, ensure_ascii=False)

    def getWinner(self, ymd):
        with open("coin/lottery.json", "r") as f:
            txt = f.read()
            database = json.loads(txt)
            if ymd not in database["history"].keys():
                return None, None, None
            return database["history"][ymd].values()


class mission:
    def choseChart(self, id):
        changeUserCooldown().mission(id)
        min_diff, max_diff = getUserAttrib(
            str(id), "setting", "lvrank")  # type:ignore
        chart_list = [[random.randint(min_diff, max_diff), random.randint(
            0, 19), random.randint(0, 9)] for i in range(3)]
        result = []
        for diff, page, num in chart_list:
            url = f"https://services.cytoid.io/search/levels?&sort=rating&difficulty={diff}&limit=10&page={page}"
            raw_data = requests.get(url).content.decode("utf-8")
            levelData = json.loads(raw_data)[num]
            chart = levelData["charts"]
            chart_id, type = [(item["id"], item["type"])
                              for item in chart if item["difficulty"] == diff][0]
            result.append(
                {"title": levelData["title"], "type": type, "diff": diff, "uid": levelData["uid"], "id": chart_id, "coin": 0, "acc": 0, "clear": False})
        self.recordChart(id, result)

    def recordChart(self, id, chart_list):
        with open("coin/mission.json", "r") as f:
            txt = f.read()
            database = json.loads(txt)
            today = func.getCurrentDay(8)
            if str(today) not in database.keys():
                database = {str(today): {str(id): chart_list}}
            elif str(id) not in database[today].keys():
                database[str(today)][str(id)] = chart_list
        with open("coin/mission.json", "w") as f1:
            json.dump(database, f1, indent=4, ensure_ascii=False)

    def getMission(self, id):
        UserCooldown = getUserCooldown().sign(id)
        if not UserCooldown:
            self.choseChart(id)
        with open("coin/mission.json", "r") as f:
            txt = f.read()
            database = json.loads(txt)
            today = str(func.getCurrentDay(8))
            return database[today][id]

    def clearMission(self, id, num, coin, acc):
        with open("coin/mission.json", "r") as f:
            txt = f.read()
            database = json.loads(txt)
            today = func.getCurrentDay(8)
            mission = database[today][str(id)][int(num)]
            mission["coin"] = coin
            mission["acc"] = acc
            mission["clear"] = True
        with open("coin/mission.json", "w") as f1:
            json.dump(database, f1, indent=4, ensure_ascii=False)


def text(command_cate, lang, directly=True):
    text_dict = {"sign": {
        "en": ["✅  |  **Signed in!**", "'s total cash"], "zh": ["✅  |  **簽到成功！**", "的總金額"]}, "sign_cooldown": {"en": ["❌  |  **Cooling down**", "Sign in again tomorrow please."], "zh": ["❌  |  **正在冷卻中**", "請明天再來簽到。"]}, "played": {"en": ["<:cytoid_dy:1179750758900584458>  |  **Played Cytoid!**", "'s total cash"], "zh": ["<:cytoid_dy:1179750758900584458>  |  **遊玩Cytoid！**", "的總金額"]}, "played_cooldown": {"en": ["❌  |  **Cooling down**", "Playing Cytoid again tomorrow please."], "zh": ["❌  |  **正在冷卻中**", "明天再玩一次吧。"]}, "lottery": {"winner": {"en": ["🎊  |  **Lottery**", "**Winner**", "**Invest**", "**Winning amount**"], "zh": ["🎊  |  **彩票開獎**", "**得獎者**", "**投注金額**", "**中獎金額**"]}, "bet": {"en": ["💰  |  **Lottery**", "**Bet amount**", "**Probability**", "You can use `dy lottery winner` to check who are winner tomorrow (GMT+8)"], "zh": ["💰  |  **彩票系統**", "**投注金額**", "**中獎機率**", "你可以在明天輸入`dy lottery winner`查詢得獎者。"]}, "unpayable": {"en": ["❌  |  **Unpayable**", "You don't have enough cash."], "zh": ["❌  |  **支付失敗**", "你沒有足夠的錢。"]}, "wrong_value": {"en": ["❌  |  **Illegal value**", "You cant't type the value < 0 or not a interger"], "zh": ["❌  |  **數值錯誤**", "你只能輸入>=0的整數。"]}}, "coupon": {"not_found": {"en": ["❌  |  **Failed**", "Coupon code incorrect."], "zh": ["❌  |  **兌換失敗**", "無效的兌換碼。"]}, "used": {"en": ["❌  |  **Failed**", "You have already used."], "zh": ["❌  |  **兌換失敗**", "你已經使用過此兌換碼。"]}, "main": {"en": ["🎁  |  **Use coupon**", "'s total cash"], "zh": ["🎁  |  **兌換成功**", "的總金額"]}, "limit": {"en": ["❌  |  **Failed**", "This code has reached the usage limit."], "zh": ["❌  |  **兌換失敗**", "此兌換碼已達使用次數限制。"]}}, "mission_embed": {"uid": {"en": "Level ID", "zh": "關卡ID"}, "title": {"en": "Song", "zh": "曲目"}, "mission": {"en": "📋  |  **Missions**", "zh": "📋  |  **任務系統**"}, "type": {"en": "Type", "zh": "類別"}, "diff": {"en": "Diff", "zh": "難度"}, "clear": {"en": "Cleared.", "zh": "已通關。"}, "readme": {"en": "\n\nif you want to clear the mission,\nenter `dy mission clear <mission no.>` to receive the reward.\n\nThe system will calculate based on the max acc in the latest 8 records.", "zh": "\n\n輸入`dy mission clear <任務序號>`以結算任務報酬。\n系統會根據最近8筆記錄中的最大acc來計算。"}}, "mission_clear": {"mission": {"en": "📋  |  **Missions**", "zh": "📋  |  **任務系統**"}, "had": {"en": "**Cleared!**", "zh": "**已通關！**"}, "title": {"en": "Song", "zh": "曲目"}, "clear": {"en": "✅  |  **Mission claer!**", "zh": "✅  |  **任務完成！**"}, "failed": {"en": "❌  |  **Failed**", "zh": "❌  |  **驗證失敗**"}, "acc": {"en": "Accuracy", "zh": "準確率"}, "reward": {"en": "Reward", "zh": "報酬"}, "cd": {"en": "❌  |  **Cooling down**", "zh": "❌  |  **正在冷卻中**"}, "no_record": {"en": "No record.\nPlease play the correct chart.", "zh": "沒有遊玩記錄。\n請遊玩指定的譜面。"}}, "setting": {"en": ["Please select a category:", "Language", "Mission Lv."], "zh": ["請選擇設定分類：", "語言 (Language)", "任務難度區間"], "lang": {"en": "Please select a language:", "zh": "請選擇語言 (Language)："}, "complt": {"lang": {"en": ["✅  |  **Settings configured!**", "Your selection is **English**."], "zh": ["✅  |  **設定完成！**", "你選擇的語言是**正體中文**。"]}, "lv": {"en": ["✅  |  **Settings configured!**", "Mission min difficulty = **Lv.", "Mission max difficulty = **Lv."], "zh": ["✅  |  **設定完成！**", "任務難度下限：**Lv.", "任務難度上限：**Lv."]}}, "lv": {"en": ["Please select a min difficulty:", "Please select a max difficulty:"], "zh": ["請選擇任務難度下限：", "請選擇任務難度上限："]}}}
    if directly:
        return text_dict[command_cate][lang]
    else:
        return text_dict[command_cate]


def emb(title, content, color):
    return discord.Embed(
        title=title,
        description=content,
        color=color
    )
