import discord
import core.CytoidData as CytoidData
import core.func as func
import core.MostRecentPlay as MostRecentPlay


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
    if (play["owner"]["name"] != "音游王" and play["score"] == 1000000
        and play["chart"]["difficulty"] >= limit_level
        and player_uid not in white_list and player_uid not in sus_list):
      if func.hack_txt(play["id"]) or is_hand_check:
        sus_list.append(play["owner"]["uid"])

  if len(sus_list) == 0:
    return None, None

  message = "**Cheater suspected detector:**\n\n"

  embed_list = []
  for sus in sus_list:
    message += f"https://next.cytoid.io/profile/{sus}\n"

    is_force_next = False
    embed_message = ""
    sus_recent_play = CytoidData.getUserRecentPlay(sus)

    for srp in sus_recent_play:
      score = srp["score"]
      if score != 1000000 and (not is_hand_check):
        is_force_next = True
        break
      title = srp["chart"]["level"]["title"]
      diff = srp["chart"]["difficulty"]
      embed_message += f"=================\n{title}  (Lv.{diff})\n`{score}`\n"
    if is_force_next:
      continue
    embed = discord.Embed(
      title=f"{sus}'s recent records",
      description=embed_message,
      color=0x00FFFF,
    )
    embed_list.append(embed)
  if len(embed_list) == 0:
    return None, None
  return message, embed_list


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
  func.del_txt(message.author, str(replace_message))
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
  fileName,level_id = MostRecentPlay.execute(cytoid_id)
  file = discord.File(fileName)
  return file, fileName,level_id
