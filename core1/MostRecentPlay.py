import core1.CytoidData as CytoidData
from PIL import Image, ImageFilter, ImageEnhance, ImageFont, ImageDraw, ImageOps
import requests
from datetime import datetime, timedelta
from fontTools.ttLib import TTFont
from io import BytesIO
import math
import re


def getImage(image_url):
    response = requests.get(image_url)
    if response.status_code == 200:
        pil_image = Image.open(BytesIO(response.content))
        return pil_image
    else:
        print("Failed to download image. Status code: ", response.status_code)
        print("Fail url: " + image_url)


def colorInterpolation(val, color_palette):
    max_index = len(color_palette) - 1
    v_index = val * max_index
    i1, i2 = int(v_index), min(int(v_index) + 1, max_index)
    (r1, g1, b1, a1), (r2, g2, b2, a2) = color_palette[i1], color_palette[i2]
    f = v_index - i1
    return (
        int(r1 + f * (r2 - r1)),
        int(g1 + f * (g2 - g1)),
        int(b1 + f * (b2 - b1)),
        int(a1 + f * (a2 - a1)),
    )


def randomDirectionGradient(size, color_palette, slope):
    width, height = size
    image = Image.new("RGBA", size)
    draw = ImageDraw.Draw(image)

    if slope < 0:
        slope = -slope
        flip = True
    else:
        flip = False

    if slope < height / width:
        h_intercept = round(height * slope)
        for y in range(0, height + h_intercept):
            val = y / (height + h_intercept)
            color = colorInterpolation(val, color_palette)
            draw.line([(0, y - h_intercept), (width - 1, y)], fill=color)
    else:
        slope = 1 / slope
        w_intercept = round(width * slope)
        for x in range(0, width + w_intercept):
            val = x / (width + w_intercept)
            color = colorInterpolation(1 - val, color_palette)
            draw.line([(x - w_intercept, 0), (x, height - 1)], fill=color)
    if flip:
        image = image.transpose(Image.FLIP_LEFT_RIGHT)
    return image


def getPlayerAvatarImg(profile_data):
    avatar_square = getImage(profile_data["user"]["avatar"]["medium"])
    _, radius = avatar_square.size
    if radius != 128:
        avatar_square = avatar_square.resize((128, 128))
        radius = 128

    mask = Image.new("L", avatar_square.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, radius, radius), fill=255)

    avatar_circle = Image.new("RGBA", avatar_square.size)
    avatar_circle.paste(avatar_square, mask=mask)

    size = w, h = round(radius * 3.5), radius

    avatar_img = Image.new("RGBA", size)
    avatar_img.paste(avatar_circle,
                     mask=avatar_circle,
                     box=(round(radius * 2.5), 0))
    draw = ImageDraw.Draw(avatar_img)
    font_bold = ImageFont.truetype("font/MPLUSRounded1c-Bold.ttf", 32)
    font_regular = ImageFont.truetype("font/MPLUSRounded1c-Regular.ttf", 24)
    draw.text(
        (round(radius * 2.2), round(radius * 0.3)),
        profile_data["user"]["uid"],
        font=font_bold,
        anchor="rm",
    )
    draw.text(
        (round(radius * 1.5), round(radius * 0.7)),
        f'Level {profile_data["exp"]["currentLevel"]}',
        font=font_regular,
        anchor="lm",
    )
    draw.text(
        (round(radius * 0.1), round(radius * 0.7)),
        "Rating {:.2f}".format(float(profile_data["rating"])),
        font=font_regular,
        anchor="lm",
    )

    return avatar_img


def char_in_font(unicode_char, ttfont):
    try:
        for cmap in ttfont["cmap"].tables:
            if cmap.isUnicode():
                if ord(unicode_char) in cmap.cmap:
                    return True
        return False
    except:
        return False


def getTitleImage(txt):
    size = w, h = (900, 80)
    end_out = [(255, 255, 255, 255), (255, 255, 255, 0), (255, 255, 255, 0)]
    end_mask = randomDirectionGradient((h, h), end_out, -9999)
    mask = Image.new("RGBA", size)
    mask.paste(end_mask, box=(w - h, 0))
    mask.paste(Image.new("RGBA", (w - h, h), color="white"))

    font_paths = [
        "font/SourceHanSansHWTC-Regular.otf",
    ]
    x = 0
    ttfont_default = TTFont("font/MPLUSRounded1c-Regular.ttf")
    font_default = ImageFont.truetype("font/MPLUSRounded1c-Regular.ttf", 60)
    txt_img = Image.new("RGBA", size)
    draw = ImageDraw.Draw(txt_img)
    if re.sub("^([^<>]*?)(?=<)|>([^<>]+)<|>([^<>]+)|", "", txt) != txt:
        matches = re.findall(r"^([^<>]*?)(?=<)|>([^<>]+)<|>([^<>]+)|", txt)
        txt = ''.join(''.join(match).strip()
                      for match in matches if any(match))
    font = font_default
    for c in txt:
        if not char_in_font(c, ttfont_default):
            for ff in font_paths:
                ttfont = TTFont(ff)
                if char_in_font(c, ttfont):
                    font = ImageFont.truetype(ff, 60)
                    break

        c_length = font.getlength(c)
        draw.text((x, h / 2), c, font=font, anchor="lm")

        x = x + c_length

    title_img = Image.new("RGBA", size)
    title_img.paste(txt_img, mask=mask)

    del mask
    del end_mask
    del txt_img

    return title_img


def getArtistImage(artist):
    size = w, h = (560, 72)
    end_out = [(255, 255, 255, 255), (255, 255, 255, 0), (255, 255, 255, 0)]
    end_mask = randomDirectionGradient((h, h), end_out, -9999)
    mask = Image.new("RGBA", size)
    mask.paste(end_mask, box=(w - h, 0))
    mask.paste(Image.new("RGBA", (w - h, h), color="white"))

    font_paths = [
        "font/SourceHanSansHWTC-Regular.otf",
    ]
    x = 8
    ttfont_default = TTFont("font/MPLUSRounded1c-Regular.ttf")
    font_default = ImageFont.truetype("font/MPLUSRounded1c-Regular.ttf", 24)

    txt_img = Image.new("RGBA", size)
    draw = ImageDraw.Draw(txt_img)
    for c in artist:
        if not char_in_font(c, ttfont_default):
            for ff in font_paths:
                ttfont = TTFont(ff)
                if char_in_font(c, ttfont):
                    font = ImageFont.truetype(ff, 60)
                    break
        else:
            font = font_default

        c_length = font.getlength(c)
        draw.text((x, h / 2), c, font=font, anchor="lm")

        x = x + c_length

    artist_img = Image.new("RGBA", size)
    artist_img.paste(txt_img, mask=mask)

    del mask
    del end_mask
    del txt_img

    return artist_img


def getScoreImage(score):
    sss_color_palette = [(253, 192, 71, 255), (244, 102, 28, 255)]
    max_color_palette = [(229, 4, 200, 255), (22, 140, 236, 255)]
    size = w, h = (820, 156)

    if score == 1000000:
        color = randomDirectionGradient(size, max_color_palette, -4)
    elif score >= 999000:
        color = randomDirectionGradient(size, sss_color_palette, -50)
    else:
        color = Image.new("RGBA", size, color="white")

    score_img = Image.new("RGBA", size)
    draw = ImageDraw.Draw(score_img)
    font = ImageFont.truetype("font/Nunito-ExtraLight.ttf", 200)
    draw.text(
        (w / 2, h / 2),
        str(score),
        font=font,
        align="center",
        fill="white",
        anchor="mm",
    )

    score_img.paste(color, mask=score_img)

    return score_img


def getDiffModsImage(type, diff, mods):
    mod_pic = {
        "Hard": "HYPER.png",
        "ExHard": "ANOTHER.png",
        "FC": "FC.png",
        "AP": "AP.png",
        "FlipX": "FlipX.png",
        "FlipY": "FlipY.png",
        "FlipAll": "FlipAll.png",
        "HideScanline": "HideScanline.png",
        "HideNotes": "HideNotes.png",
        "Slow": "Slow.png",
        "Fast": "Fast.png",
    }
    size = w, h = (360, 170)
    if diff <= 0:
        diff_txt = "?"
    elif diff >= 16:
        diff_txt = "15+"
    else:
        diff_txt = str(diff)

    if type == "extreme":
        txt = "EX  " + diff_txt
        color = [(103, 0, 3, 255), (38, 1, 31, 255)]
    elif type == "hard":
        txt = "HD  " + diff_txt
        color = [(164, 105, 183, 255), (82, 104, 215, 255)]
    else:
        txt = "EZ  " + diff_txt
        color = [(100, 176, 122, 255), (79, 164, 195, 255)]

    mask = Image.new("L", size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle((0, 0, w, h), fill=255, radius=h / 2)

    bg = randomDirectionGradient(size, color, 0.5)

    diff_image = Image.new("RGBA", size)
    diff_image.paste(bg, mask=mask)

    draw = ImageDraw.Draw(diff_image)
    font = ImageFont.truetype("font/Nunito-Bold.ttf", 72)
    draw.text((w / 2, h / 2),
              txt,
              font=font,
              align="center",
              fill="white",
              anchor="mm")

    del bg, mask

    for m in mods:
        w += 300

        new_image = Image.new("RGBA", (w, h))
        new_image.paste(diff_image, mask=diff_image)

        mod_img = Image.open("mod/" + mod_pic[m])
        new_image.paste(mod_img, mask=mod_img, box=(w - 240, 0))

        del diff_image, mod_img
        diff_image = new_image

    return diff_image


def getRankImg(score, font_size):
    gray_skin = [(146, 153, 170, 255), (76, 88, 102, 255)]
    green_skin = [(146, 188, 96, 255), (77, 142, 127, 255)]
    yellow_skin = [(248, 187, 66, 255), (251, 108, 13, 255)]
    purple_skin = [(229, 4, 200, 255), (22, 140, 236, 255)]
    if score == 1000000:
        rank = "MAX"
        skin = purple_skin
    elif score >= 999000:
        rank = "SSS"
        skin = yellow_skin
    elif score >= 995000:
        rank = "SS"
        skin = yellow_skin
    elif score >= 990000:
        rank = "S"
        skin = yellow_skin
    elif score >= 950000:
        rank = "AA"
        skin = yellow_skin
    elif score >= 900000:
        rank = "A"
        skin = yellow_skin
    elif score >= 800000:
        rank = "B"
        skin = green_skin
    elif score >= 700000:
        rank = "C"
        skin = green_skin
    elif score >= 600000:
        rank = "D"
        skin = gray_skin
    else:
        rank = "E"
        skin = gray_skin

    w = round(font_size * 0.75 * len(rank) - 2)
    h = round(font_size * 0.77)
    size = w, h
    bg = randomDirectionGradient(size, skin, -0.5)

    rank_img = Image.new("RGBA", size)
    draw = ImageDraw.Draw(rank_img)
    font = ImageFont.truetype("font/Nunito-Bold.ttf", font_size)
    draw.text((w / 2, h / 2), rank, font=font, anchor="mm")

    rank_img.paste(bg, mask=rank_img)

    return rank_img


def getDataImg(play_data):
    line_spacing1 = 56
    line_spacing2 = 42
    mergin = 36
    size = (w, h) = (560, line_spacing1 * 2 + line_spacing2 * 5 + mergin)
    left_anchor1 = 36
    right_anchor1 = w - 40
    top_anchor2 = line_spacing1 * 2 + mergin
    left_anchor2 = 0
    right_anchor2 = w / 2 - 20
    left_anchor3 = w / 2 + 20
    right_anchor3 = w

    font_regular = ImageFont.truetype("font/Nunito-Regular.ttf", 36)
    font_bold = ImageFont.truetype("font/Nunito-Bold.ttf", 48)

    data_image = Image.new("RGBA", size)
    draw = ImageDraw.Draw(data_image)

    right = ["Accuracy", "Max Combo"]
    left = []
    left.append(f'{math.floor(play_data["accuracy"]*100000)/1000}%')
    left.append(play_data["details"]["maxCombo"])

    for i in range(len(right)):
        if (i == 1 and play_data["details"]["maxCombo"]
                == play_data["details"]["perfect"] +
                play_data["details"]["great"] + play_data["details"]["good"]):
            draw.text(
                (left_anchor1, i * line_spacing1),
                "Full Combo",
                font=font_bold,
                align="left",
                # fill="#fa9328",
                anchor="la")
            break
        draw.text(
            (left_anchor1, i * line_spacing1),
            right[i],
            font=font_bold,
            align="left",
            anchor="la",
        )
        draw.text(
            (right_anchor1, i * line_spacing1),
            str(left[i]),
            font=font_bold,
            align="right",
            anchor="ra",
        )
    right = ["Perfect", "Great", "Good", "Bad", "Miss"]
    left = []
    left.append(play_data["details"]["perfect"])
    left.append(play_data["details"]["great"])
    left.append(play_data["details"]["good"])
    left.append(play_data["details"]["bad"])
    left.append(play_data["details"]["miss"])
    for i in range(len(right)):
        draw.text(
            (left_anchor2, i * line_spacing2 + top_anchor2),
            right[i],
            font=font_regular,
            align="left",
            anchor="la",
            fill="lightgray",
        )
        draw.text(
            (right_anchor2, i * line_spacing2 + top_anchor2),
            str(left[i]),
            font=font_regular,
            align="right",
            anchor="ra",
            fill="lightgray",
        )
    draw.text(
        (left_anchor3, top_anchor2),
        "Rating",
        font=font_regular,
        align="left",
        anchor="la",
    )
    draw.text(
        (right_anchor3, top_anchor2),
        "{:.2f}".format(play_data["rating"]),
        font=font_regular,
        align="right",
        anchor="ra",
    )

    rank_img = getRankImg(play_data["score"], 100)
    rw, rh = rank_img_size = rank_img.size
    r_corner = round(left_anchor3 + (w - left_anchor3 - rw) / 2)
    t_corner = round(top_anchor2 + 20 + (h - top_anchor2 - rh) / 2)
    data_image.paste(rank_img, mask=rank_img, box=(r_corner, t_corner))
    return data_image


def getPlayTimeImg(play_time_str, tw_time=False):
    play_utc_time = datetime.strptime(play_time_str, "%Y-%m-%dT%H:%M:%S.%fZ")
    play_utc_time = play_utc_time + timedelta(hours=8)
    formatted_play_time = play_utc_time.strftime("%Y-%m-%d %H:%M:%S (GMT+8)")
    if tw_time:
        return formatted_play_time

    size = w, h = (300, 20)
    time_img = Image.new("RGBA", size)
    draw = ImageDraw.Draw(time_img)
    font = ImageFont.truetype("font/Nunito-Bold.ttf", 20)
    draw.text((w, h / 2),
              formatted_play_time,
              font=font,
              anchor="rm",
              fill="gray")
    return time_img


def getLeaderBoardImg(player_id, level_id, diff_type):
    leaderboard = CytoidData.getLevelLeaderboard(level_id, diff_type)

    rank = -1
    for l in leaderboard:
        if l["owner"]["uid"] == player_id:
            rank = l["rank"]
            break
    if rank == -1:
        rank = 1001

    medel_img = Image.open("Icon/Medal.png")
    size = w, h = medel_img.size

    leaderboard_img = Image.new("RGBA", (w * 3, h))
    leaderboard_img.paste(medel_img, mask=medel_img)

    if rank < 1000:
        rank_txt = "#" + str(rank)
    else:
        rank_txt = "#999+"
    draw = ImageDraw.Draw(leaderboard_img)
    font = ImageFont.truetype("font/Nunito-Bold.ttf", 320)
    draw.text((w * 2, h / 2), rank_txt, font=font, anchor="mm")

    return leaderboard_img


def getLevelRatingImg(rating):
    star_img = Image.open("Icon/Star.png")
    size = w, h = star_img.size

    rating_img = Image.new("RGBA", (w * 3, h))
    rating_img.paste(star_img, mask=star_img)

    draw = ImageDraw.Draw(rating_img)
    font = ImageFont.truetype("font/Nunito-Bold.ttf", 320)
    if rating < 0:
        rating_text = "N/A"
    else:
        rating_text = "{:.2f}".format(rating)
    draw.text((w * 2, h / 2), rating_text, font=font, anchor="mm")

    return rating_img


def getCharterInfo(charter, level_id, charter_avatar_url):
    charter_avatar_square = getImage(charter_avatar_url)
    _, radius = charter_avatar_square.size
    if radius != 64:
        charter_avatar_square = charter_avatar_square.resize((64, 64))
        radius = 64
    mask = Image.new("L", charter_avatar_square.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, radius, radius), fill=255)
    charter_avatar = Image.new("RGBA", charter_avatar_square.size)
    charter_avatar.paste(charter_avatar_square, mask=mask)

    charter_avatar = ImageOps.scale(charter_avatar, 0.75)
    _, r = charter_avatar.size

    size = w, h = (420, 60)
    left_anchor = 68
    right_anchor = left_anchor + 88
    line_space = 32

    if len(charter) > 24:
        charter = charter[:24] + "..."
    if len(level_id) > 24:
        level_id = level_id[:24] + "..."

    charter_img = Image.new("RGBA", size)
    draw = ImageDraw.Draw(charter_img)
    font = ImageFont.truetype("font/Nunito-Regular.ttf", 20)
    left = ["Charter:", "Level ID:"]
    right = [charter, level_id]
    for i in range(2):
        draw.text(
            (left_anchor, line_space * i),
            left[i],
            font=font,
            anchor="la",
            align="left",
        )
        draw.text(
            (right_anchor, line_space * i),
            right[i],
            font=font,
            anchor="la",
            align="left",
        )
    charter_img.paste(charter_avatar,
                      mask=charter_avatar,
                      box=(0, round((h - r) / 2)))

    return charter_img


def generatePlayImg(player_id, isDebug=False):
    play_data = CytoidData.getUserMostRecentPlay(player_id)
    date_object = datetime.strptime(play_data["date"], "%Y-%m-%dT%H:%M:%S.%fZ")
    level_id = play_data["chart"]["level"]["uid"]
    level_data = CytoidData.getLevelData(level_id)
    profile_data = CytoidData.getProfileData(player_id)

    cover_img_url = level_data["cover"]["cover"]
    cover_img = getImage(cover_img_url)

    # h = 800, w = 1280
    size = img_w, img_h = cover_img.size

    cover_img_scale_rate = 0.45

    background_img = Image.new("RGBA", size)
    background_img.paste(cover_img)

    background_img = background_img.filter(ImageFilter.GaussianBlur(10))
    brightness = ImageEnhance.Brightness(background_img)
    background_img = brightness.enhance(0.33)
    title_img = getTitleImage(level_data["title"])
    artist_img = getArtistImage(level_data["metadata"]["artist"]["name"])
    diff_mod_img = getDiffModsImage(play_data["chart"]["type"],
                                    play_data["chart"]["difficulty"],
                                    play_data["mods"])
    diff_mod_img = ImageOps.scale(diff_mod_img, 0.3)
    score_img = getScoreImage(play_data["score"])
    score_img = ImageOps.scale(score_img, 0.6)
    data_img = getDataImg(play_data)
    avatar_img = getPlayerAvatarImg(profile_data)
    avatar_img = ImageOps.scale(avatar_img, 0.75)
    cover_img = ImageOps.scale(cover_img, cover_img_scale_rate)
    leader_board_img = getLeaderBoardImg(player_id, level_data["uid"],
                                         play_data["chart"]["type"])
    leader_board_img = ImageOps.scale(leader_board_img, 0.12)
    rating_img = getLevelRatingImg(CytoidData.getRate(level_data["uid"]))
    rating_img = ImageOps.scale(rating_img, 0.12)
    charter_info_img = getCharterInfo(
        level_data["owner"]["uid"],
        level_data["uid"],
        level_data["owner"]["avatar"]["small"],
    )
    logo_img = Image.open("Icon/LogoText.png")
    logo_img = ImageOps.scale(logo_img, 0.3)
    time_img = getPlayTimeImg(play_data["date"])

    cover_top_edge = 180
    cover_left_edge = 640
    bottom_mergin = 48

    w, h = cover_img.size
    cover_bottom_edge = cover_top_edge + h
    cover_right_edge = cover_left_edge + w
    w, h = title_img.size
    w, h = data_img.size
    data_top_edge = img_h - bottom_mergin - h
    data_left_edge = round((cover_left_edge - w) / 2)
    left_mergin = data_left_edge
    title_top_edge = left_mergin
    w, h = avatar_img.size
    avatar_left_edge = img_w - left_mergin - w
    w, h = artist_img.size
    artist_top_edge = title_top_edge + h
    mod_top_edge = artist_top_edge + h
    w, h = diff_mod_img.size
    mod_bottom_edge = mod_top_edge + h
    w, h = score_img.size
    score_top_edge = round((data_top_edge - mod_bottom_edge - h) / 2 +
                           mod_bottom_edge)
    score_left_edge = round((cover_left_edge - left_mergin - w) / 2 +
                            left_mergin)
    right_bottom_corner_mid_light = round(
        (img_h - bottom_mergin + cover_bottom_edge) / 2)
    w, h = time_img.size
    time_top_edge = img_h - bottom_mergin - h
    w, h = logo_img.size
    logo_top_edge = round((time_top_edge - right_bottom_corner_mid_light - h) /
                          2 + right_bottom_corner_mid_light)
    w, h = leader_board_img.size
    rate_top_edge = (round(
        (img_h - bottom_mergin - logo_top_edge - h) / 2) + logo_top_edge)
    leader_board_top_edge = (round(
        (rate_top_edge - cover_bottom_edge - h) / 2) + cover_bottom_edge)
    badge_right_edge = cover_left_edge + w
    w, h = time_img.size
    time_left_edge = round((img_w - left_mergin - badge_right_edge - w) / 2 +
                           badge_right_edge)
    w, h = logo_img.size
    logo_left_edge = round((img_w - left_mergin - badge_right_edge - w) / 2 +
                           badge_right_edge)

    background_img.paste(title_img,
                         box=(left_mergin, title_top_edge),
                         mask=title_img)  # main title
    background_img.paste(artist_img,
                         box=(left_mergin, artist_top_edge),
                         mask=artist_img)  # main title
    background_img.paste(diff_mod_img,
                         box=(left_mergin, mod_top_edge),
                         mask=diff_mod_img)  # difficulty & mods
    background_img.paste(score_img,
                         box=(score_left_edge, score_top_edge),
                         mask=score_img)  # score
    background_img.paste(data_img,
                         box=(data_left_edge, data_top_edge),
                         mask=data_img)  # data
    background_img.paste(avatar_img,
                         box=(avatar_left_edge, title_top_edge),
                         mask=avatar_img)  # avatar
    background_img.paste(cover_img,
                         box=(cover_left_edge, cover_top_edge))  # cover
    background_img.paste(
        leader_board_img,
        box=(cover_left_edge, leader_board_top_edge),
        mask=leader_board_img,
    )  # leader_board
    background_img.paste(rating_img,
                         box=(cover_left_edge, rate_top_edge),
                         mask=rating_img)  # rating
    background_img.paste(
        charter_info_img,
        box=(logo_left_edge, leader_board_top_edge),
        mask=charter_info_img,
    )  # charter
    background_img.paste(logo_img,
                         box=(logo_left_edge, logo_top_edge),
                         mask=logo_img)  # cytoid logo
    background_img.paste(time_img,
                         box=(time_left_edge, time_top_edge),
                         mask=time_img)  # time

    file_name = f"_{player_id}_RecentPlay.png"

    if isDebug:
        background_img.show()
    else:
        background_img.save(file_name)

    return file_name, level_id, date_object


def execute(player_id, isDebug=False):
    return generatePlayImg(player_id, isDebug)


if __name__ == "__main__":
    execute("cheongsn", True)
