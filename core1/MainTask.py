import discord
import core1.CytoidData as CytoidData
import core1.func as func
import core1.MostRecentPlay as MostRecentPlay
import core1.mail as mail
import os


def checkHack(limit_level=14):
    is_hand_check = limit_level == 0
    white_list = [
        "tento",
        "miko_hmsb",
        "skisk",
        "motleyorc",
        "farrel",
        "tonykrza",
        "yakumoran",
        "aweeeeeeeeeee",
        "se234x",
        "kringus",
        "malygos",
        "2034159367",
        "kcto3",
    ]

    cytoidRecentPlay = CytoidData.getCytoidRecentPlay(100)
    sus = ""
    sus_list = []

    for play in cytoidRecentPlay:
        player_uid = play["owner"]["uid"]
        if (play["owner"]["name"] != "音游王" and play["score"] in [1000000]
            and play["chart"]["difficulty"] >= limit_level
                and player_uid not in white_list and player_uid not in sus_list):
            if func.hack_txt(play["id"]) or is_hand_check:
                sus_list.append(play["owner"]["uid"])

    if len(sus_list) == 0:
        return None, None

    message_start = "**Cheater suspected detector:**\n\n"
    message = []
    embed_list = []
    mail_content = []
    for sus in sus_list:
        message.append(f"https://cytoid.io/profile/{sus}\n")

        is_force_next = False
        embed_message = []
        sus_recent_play = CytoidData.getUserRecentPlay(sus)

        for srp in sus_recent_play:
            score = srp["score"]
            if score not in [1000000, 0] and (not is_hand_check):
                is_force_next = True
                message.pop()
                break
            title = srp["chart"]["level"]["title"]
            diff = srp["chart"]["difficulty"]
            embed_message.append(f"\n{title}  (Lv.{diff}): `{score}`")
        if is_force_next:
            continue
        embed = discord.Embed(
            title=f"{sus}'s recent records",
            description="".join(embed_message),
            color=0xFF2D2D,
        )
        mail_content.append(f"<br>{sus}的游玩纪录：<br>{'<br>'.join(embed_message)}")
        embed_list.append(embed)
    if len(embed_list) == 0:
        return None, None
    for mailadrres in [os.getenv("test")]:
        mail.sendMail(mailadrres, "Cytoid 外挂侦测系统",
                      f"嫌疑清单：<br>{'<br>'.join(message)}<br>{'<br>'.join(mail_content)}")
    return f"{message_start}{''.join(message)}", embed_list


async def getErrorMessage(channel):
    messages = [message async for message in channel.history(limit=5)]
    for msg in messages:
        if msg.content.startswith("dy"):
            return msg.content
    return None


async def getNoCheaterMessageCount(channel):
    messages = [message async for message in channel.history(limit=1)]
    messages = messages[0]
    if messages.content.startswith("No one cheated"):
        return messages
    else:
        return None


def replaceNadekoMention(message):
    replace_message = func.mentionReplacement(message.author,
                                              message.content,
                                              isDisplayed=True,
                                              isRecording=True)
    return f"系統偵測到Nadeko惡意標註訊息，予以刪除\n訊息內容：\n``` {replace_message}```"


def repeatMessage(txt_message, author):
    if len(txt_message) == 0:
        return ""

    ban_words = ["@everyone", "@here"]
    ping_emohi = "<:pingsock:927473651295596614>"
    for bw in ban_words:
        if bw in txt_message:
            output_message = author.mention + "不要ping我" + ping_emohi * 3
            func.say_txt(author, output_message)
            return output_message

    orz_words = ["電", "佬", "強", "神", "god"]
    warning_mentions = [
        "dyliu",
        "830395796490158081",
        "error418",
        "441468734373232640",
        "ya",
        "Ya",
        "YA",
    ]
    orz_emoji = "<:bowdown:889333644202754058>"

    for orz_w in orz_words:
        if orz_w in txt_message:
            for w_m in warning_mentions:
                if w_m in txt_message:
                    output_message = author.mention + "自認是神" + (orz_emoji * 3)
                    func.say_txt(author, output_message)
                    return output_message

    recorded_message = func.mentionReplacement(author,
                                               txt_message,
                                               isRecording=True)
    func.say_txt(author, recorded_message)

    repeated_message = func.mentionReplacement(
        author,
        txt_message,
        isBold=True,
        isDisplayed=True,
        isRecording=True,
    )
    return repeated_message


def generateRecentPlayPic(cytoid_id):
    img, level_id, day_of_month= MostRecentPlay.execute(cytoid_id)
    return img, level_id, day_of_month
