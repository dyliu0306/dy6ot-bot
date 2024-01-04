import discord
from discord.ext import commands
import asyncio
import requests
import json
import math
from io import BytesIO
import os
from urllib import request
import core1.func as func
from core1.classes import Cog_Extension
import core1.CytoidData as CytoidData
import core1.MainTask as MainTask
import core1.coin as coin
import core1.ui as ui
import random
from datetime import datetime, timedelta
import re
import time

debuging = False


def btn(s, l, e, u, r=0, ban=False):
    return discord.ui.Button(style=s, label=l, emoji=e, url=u, row=r, disabled=ban)


def slc(p, o, min=1, max=1, ban=False):
    o = [discord.SelectOption(label=l, value=v) for l, v in o]
    return discord.ui.Select(placeholder=p, options=o, min_values=min, max_values=max, disabled=ban)


async def timeout(view, msg):
    for item in view.children:
        item.disabled = True
    await msg.edit(content=msg.content, view=view)


class Coin(Cog_Extension):

    @commands.command()
    async def sign(self, ctx):
        id = ctx.author.id
        UserCooldown = coin.getUserCooldown().sign(id)
        if UserCooldown:
            UserLang = coin.getUserAttrib(id, "setting", "lang")
            embed_text = coin.text("sign_cooldown", UserLang)
            embed = coin.emb(embed_text[0], embed_text[1], 0xFF0000)
            await ctx.send(embed=embed)
            return
        UserCoin, FirstUse = coin.getUserData(id, "coin", name=ctx.author.name)
        if FirstUse:
            await self.firstuse(ctx)
        UserLang = coin.getUserAttrib(id, "setting", "lang")
        getCoin = 100
        UserCoin += getCoin
        coin.changeUserCooldown().sign(id)
        coin.changeUserData(id, "coin", UserCoin, 100,
                            "sign", name=ctx.author.name)
        embed_text = coin.text("sign", UserLang)
        content = f"💵 `+{getCoin}`\n\n**{ctx.author.display_name}{embed_text[1]}**:  `{UserCoin}`"
        embed = coin.emb(embed_text[0], content, 0x28FF28)
        await ctx.send(embed=embed)

    @commands.command()
    async def lottery(self, ctx, value):
        id = ctx.author.id
        if value == "winner":
            UserLang = coin.getUserAttrib(
                id, "setting", "lang", name=ctx.author.name)
            UserLang = "en" if not UserLang else UserLang
            # 確保記錄為昨天
            current_date = datetime.now()+timedelta(hours=-16)
            ymd = current_date.strftime("%y%m%d")
            winner_id, percent, prize = coin.lottery().getWinner(ymd)
            embed_text = coin.text("lottery", UserLang, directly=False)[
                "winner"][UserLang]
            if prize is not None:
                content = f"`{ymd[0:2]}/{ymd[2:4]}/{ymd[4:]}`\n{embed_text[1]}： <@{winner_id}>\n\n{embed_text[2]}\n```{round(prize*percent)}    ({percent:.4%})```\n{embed_text[3]}\n```{prize}```"
                color = 0x28FF28
            else:
                content = f"`{ymd[0:2]}/{ymd[2:4]}/{ymd[4:]}`\n{embed_text[1]}： N/A\n\n{embed_text[2]}\n```N/A```\n{embed_text[3]}\n```N/A```"
                color = 0xFF0000
            embed = coin.emb(embed_text[0], content, color)
            await ctx.send(embed=embed)
            return
        UserCoin, FirstUse = coin.getUserData(id, "coin", name=ctx.author.name)
        if FirstUse:  # 沒做完
            await self.firstuse(ctx)
            UserLang = coin.getUserAttrib(id, "setting", "lang")
            embed_text = coin.text("lottery", UserLang, directly=False)[
                "unpayable"][UserLang]
            embed = coin.emb(embed_text[0], embed_text[1], 0xFF0000)
            await ctx.send(embed=embed)
            return
        UserLang = coin.getUserAttrib(id, "setting", "lang")
        value = re.sub("[^0-9]+", "", value)  # 負號被刪除，不會有負數
        if value == "":  # 請輸入>=0的整數
            embed_text = coin.text("lottery", "en", directly=False)[
                "wrong_value"][UserLang]
            embed = coin.emb(embed_text[0], embed_text[1], 0xFF0000)
            await ctx.send(embed=embed)
            return
        value = int(value)
        if UserCoin < value:  # 金額不足，照抄FirstUse
            embed_text = coin.text("lottery", UserLang, directly=False)[
                "unpayable"][UserLang]
            embed = coin.emb(embed_text[0], embed_text[1], 0xFF0000)
            await ctx.send(embed=embed)
            return
        gmt = 8
        if debuging:
            gmt = 7
        percent, original_value = coin.lottery().changeBetValue(id, value, gmt)
        UserCoin += original_value
        UserCoin -= value
        coin.changeUserData(id, "coin", UserCoin,
                            original_value+value*-1, "lottery")
        embed_text = coin.text("lottery", UserLang, directly=False)[
            "bet"][UserLang]
        content = f"{embed_text[1]}\n```{value}```\n\n{embed_text[2]}\n```{percent:.4%}```\n\n{embed_text[3]}"
        embed = coin.emb(embed_text[0], content, 0x28FF28)
        await ctx.send(embed=embed)

    @commands.command()
    async def coupon(self, ctx, code):
        id = ctx.author.id
        result, UserCoin, getCoin = await coin.useCoupon(
            id, code, self.bot, ctx)
        UserLang = coin.getUserAttrib(id, "setting", "lang")
        if result is None:
            embed_text = coin.text("coupon", UserLang, directly=False)[
                "not_found"][UserLang]
            embed = coin.emb(embed_text[0], embed_text[1], 0xFF0000)
        elif not result:
            embed_text = coin.text("coupon", UserLang, directly=False)[
                "used"][UserLang]
            embed = coin.emb(embed_text[0], embed_text[1], 0xFF0000)
        else:
            embed_text = coin.text("coupon", UserLang, directly=False)[
                "main"][UserLang]
            content = f"💵 `+{getCoin}`\n\n**{ctx.author.display_name}{embed_text[1]}    **:  `{UserCoin}`"
            embed = coin.emb(embed_text[0], content, 0x28FF28)
        await ctx.send(embed=embed)

    @commands.command()
    async def mission(self, ctx, clear="", num=""):
        async with ctx.typing():
            # 是否綁定ctd
            # 全域變數UserCoin、UserLang、ctd_id
            ctd_id = CytoidData.checkCytoidID("me", ctx.author, True)
            if ctd_id in ["nobindctd", "nofindctd"]:
                await ctx.send(func.ebt(ctd_id))
                return
            UserCoin, FirstUse = coin.getUserData(
                ctx.author.id, "coin", ctx.author.name)
            if FirstUse:
                await self.firstuse(ctx)
            UserLang = coin.getUserAttrib(
                ctx.author.id, "setting", "lang", ctx.author.name)
            # clear模組
            if clear == "clear" and re.sub("[^1-3]", "", num) in ["1", "2", "3"]:
                await self.clear(ctx, num, ctd_id, UserCoin, UserLang)
                return
            # 獲取任務清單
            missions = coin.mission().getMission(str(ctx.author.id))
            view = discord.ui.View(timeout=60)

            def missionEmbed(mission, page):
                embed_text = coin.text("mission_embed", "en", directly=False)
                embed = coin.emb(
                    f"**{embed_text['mission'][UserLang]} ({page}/3)**", "", 0x66B3FF)
                for name, value in mission.items():
                    if name == "id":
                        break
                    embed.add_field(
                        name=f"**{embed_text[name][UserLang]}**", value=f"```fix\n{value}\n```", inline=True)
                embed.add_field(
                    name=f"\n", value=f"\n{embed_text['readme'][UserLang]}", inline=False)
                return embed

            async def button_cb_1(interaction, mission=missions[0], page=1):
                if interaction.user.id == ctx.author.id:
                    if mission["clear"] == True:
                        embed_text = coin.text(
                            "mission_clear", UserLang, directly=False)
                        embed = coin.emb(
                            f"{embed_text['mission'][UserLang]} ({page}/3)", f"{embed_text['had'][UserLang]}\n", 0x27ff27)
                        embed.add_field(
                            name=f"**{embed_text['title'][UserLang]} (diff: {mission['diff']})**",
                            value=f"```fix\n{mission['title']}\n```", inline=False)
                        embed.add_field(
                            name=f"**{embed_text['acc'][UserLang]}**",
                            value=f"```fix\n{mission['acc']:.3%}\n```", inline=True)
                        embed.add_field(
                            name=f"**{embed_text['reward'][UserLang]}**",
                            value=f"```fix\n+{mission['coin']} / {UserCoin}\n```", inline=True)
                    else:
                        embed = missionEmbed(mission, page)
                    await interaction.response.edit_message(embed=embed, view=view)

            btn_style = discord.ButtonStyle
            button_1 = btn(btn_style.primary, "", "1️⃣", None)
            button_2 = btn(btn_style.primary, "", "2️⃣", None)
            button_3 = btn(btn_style.primary, "", "3️⃣", None)
            button_4 = btn(btn_style.link, "Open Cytoid", "<:cytoid_dy:1179750758900584458>",
                           f"https://dyliu0306.github.io/run-cytoid?&level1={missions[0]['uid']}&level2={missions[1]['uid']}&level3={missions[2]['uid']}", 1)

            button_1.callback = button_cb_1
            button_2.callback = lambda interaction: button_cb_1(
                interaction, missions[1], 2)
            button_3.callback = lambda interaction: button_cb_1(
                interaction, missions[2], 3)
            view.add_item(button_1)
            view.add_item(button_2)
            view.add_item(button_3)
            view.add_item(button_4)
            if missions[0]["clear"] == True:
                mission = missions[0]
                embed_text = coin.text(
                    "mission_clear", UserLang, directly=False)
                embed = coin.emb(
                    f"{embed_text['mission'][UserLang]} (1/3)", f"{embed_text['had'][UserLang]}\n", 0x27ff27)
                embed.add_field(
                    name=f"**{embed_text['title'][UserLang]} (diff: {mission['diff']})**",
                    value=f"```fix\n{mission['title']}\n```", inline=False)
                embed.add_field(
                    name=f"**{embed_text['acc'][UserLang]}**",
                    value=f"```fix\n{mission['acc']:.3%}\n```", inline=True)
                embed.add_field(
                    name=f"**{embed_text['reward'][UserLang]}**",
                    value=f"```fix\n+{mission['coin']} / {UserCoin}\n```", inline=True)
            else:
                embed = missionEmbed(missions[0], 1)
            msg = await ctx.reply(embed=embed, view=view)
            view.on_timeout = lambda: timeout(view, msg)

    @commands.command()
    async def game(self, ctx):
        pass

    @commands.command()
    async def money(self, ctx, UserId=None):
        UserCoin, FirstUse = coin.getUserData(
            str(ctx.author.id), "coin", name=ctx.author.name)
        if FirstUse:
            await self.firstuse(ctx)
        UserLang = coin.getUserAttrib(str(ctx.author.id), "setting", "lang")
        if UserId:
            pass
        else:
            id = ctx.author.id
        # 查詢的人的資料
        UserCoin, FirstUse = coin.getUserData(
            str(ctx.author.id), "coin", add=False)
        if FirstUse:
            pass
        else:
            pass

    async def sendlotterymsg(self):
        g1 = self.bot.get_guild(910172705863651350)
        ch1 = g1.get_channel(1182189328403800114)
        g2 = self.bot.get_guild(812156057652035615)
        ch2 = g2.get_channel(854878136189452288)
        bonus = 5000
        winner_id, percent, prize = coin.lottery().choseWinner(bonus=bonus)
        current_date = datetime.now()+timedelta(hours=-16)
        ymd = current_date.strftime("%y%m%d")
        for i, j in [["zh", ch2], ["en", ch1]]:
            embed_text = coin.text("lottery", i, directly=False)[
                "winner"][i]
            if percent is not None:
                content = f"`{ymd[0:2]}/{ymd[2:4]}/{ymd[4:]}`\n{embed_text[1]}： <@{winner_id}>\n{embed_text[2]}\n```{round(prize*percent)}        ({percent:.4%})```\n{embed_text[3]}\n```{prize} + {bonus}```"
                color = 0x28FF28
            else:
                content = f"`{ymd[0:2]}/{ymd[2:4]}/{ymd[4:]}`\n{embed_text[1]}： N/A\n    {embed_text[2]}\n```N/A```\n{embed_text[3]}\n```N/A```"
                color = 0xFF0000
            embed = coin.emb(embed_text[0], content, color)
            await j.send(embed=embed)

    async def firstuse(self, ctx):
        chs_lang_msg = await ctx.send("> 請選擇語言 (select language)")
        await chs_lang_msg.add_reaction(func.emo("zh"))
        await chs_lang_msg.add_reaction(func.emo("en"))

        def check(reaction, user):
            return (reaction.message == chs_lang_msg and user == ctx.author and "_dy" in str(reaction.emoji))
        try:
            chs_lang, z1 = await self.bot.wait_for("reaction_add", timeout=60, check=check)
            if "EN" in str(chs_lang.emoji):
                await chs_lang_msg.edit(content="> Your select is **English**.")
            elif "ZH" in str(chs_lang.emoji):
                await chs_lang_msg.edit(content="> 你選擇的是**正體中文**。")
                coin.changeUserAttrib(ctx.author.id, "setting", "lang", "zh")
            await asyncio.sleep(2)
        except asyncio.TimeoutError:
            await chs_lang_msg.edit(content=">>> 超時未選擇，你可以輸入`dy setting`重新設定。 \nTime out, you can enter `dy setting` to set on")

    async def clear(self, ctx, num, ctd_id, UserCoin, UserLang):
        num = int(num)-1
        mission = coin.mission().getMission(str(ctx.author.id))[num]

        def clearEmbed(title=mission["title"], acc=mission["acc"], price=mission["coin"], UserCash=UserCoin):
            embed_text = coin.text("mission_clear", UserLang, False)
            embed = coin.emb(embed_text["clear"][UserLang], "", 0x27ff27)
            embed.add_field(
                name=f"**{embed_text['title'][UserLang]} (diff: {mission['diff']})**",
                value=f"```fix\n{title}\n```", inline=False)
            embed.add_field(
                name=f"**{embed_text['acc'][UserLang]}**",
                value=f"```fix\n{acc:.3%}\n```", inline=True)
            embed.add_field(
                name=f"**{embed_text['reward'][UserLang]}**",
                value=f"```fix\n+{price} / {UserCash}\n```", inline=True)
            return embed
        # 已通關
        if mission["clear"]:
            embed = clearEmbed()
            await ctx.reply(embed=embed)
            return
        # CD
        if coin.getUserCooldown().clear(str(ctx.author.id)):
            embed_text = coin.text("mission_clear", UserLang, False)
            embed = coin.emb(
                embed_text["cd"][UserLang], f"CD: <t:{int(time.time())+30}:R>", 0xff0000)
            await ctx.reply(embed=embed)
            return
        UserRecord = CytoidData.getUserMsnRecord(ctd_id)
        coin.changeUserCooldown().clear(str(ctx.author.id))
        try:
            acc = float(max(
                (record for record in UserRecord if record["chart"]["id"] == mission["id"]), key=lambda x: x["accuracy"])["accuracy"])*100
        except:
            embed_text = coin.text("mission_clear", UserLang, False)
            embed = coin.emb(
                embed_text["failed"][UserLang], embed_text["no_record"][UserLang], 0xff0000)
            await ctx.reply(embed=embed)
            return
        diff = mission["diff"]
        if acc > 99.95:
            price = (5.112**(diff**0.5))*(0.777-0.16 *
                                          (math.log(100-99.95, 10)))*((99.95-96.5)**0.5)*2
            price = int(round(price/10)*10)
        elif acc < 97:
            price = 100+(diff-12)*25
        else:
            price = (5.112**(diff**0.5))*(0.777-0.16 *
                                          (math.log(100-acc, 10)))*((acc-96.5)**0.5)
            price = int(round(price/10)*10)
        acc /= 100
        UserCoin += price
        coin.mission().clearMission(str(ctx.author.id), num, price, acc)
        coin.changeUserData(str(ctx.author.id), "coin",
                            UserCoin, price, "mission")
        embed = clearEmbed(acc=acc, price=price, UserCash=UserCoin)
        await ctx.reply(embed=embed)

    # 設定
    @commands.command()
    async def setting(self, ctx):
        UserCoin, FirstUse = coin.getUserData(
            str(ctx.author.id), "coin", name=ctx.author.name)
        if FirstUse:
            await self.firstuse(ctx)
        UserLang = coin.getUserAttrib(ctx.author.id, "setting", "lang")
        view = discord.ui.View(timeout=15)

        async def slc_cb_1(interaction):
            if interaction.user.id == ctx.author.id:
                selected = interaction.data["values"][0]
                if selected == "lang":
                    await self.set_lang(ctx, UserLang, interaction, view)
                elif selected == "mission":
                    await self.set_lv_min(ctx, UserLang, interaction, view)
                pass
        text_eb = coin.text("setting", UserLang)
        select_1 = slc(
            text_eb[0], [[text_eb[1], "lang"], [text_eb[2], "mission"]])
        select_1.callback = slc_cb_1
        view.add_item(select_1)
        msg = await ctx.send(view=view)
        view.on_timeout = lambda: timeout(view, msg)

    # 語言
    async def set_lang(self, ctx, UserLang, itat, view):
        view.clear_items()

        async def slc_cb_1(interaction):
            if interaction.user.id == ctx.author.id:
                select_lang = interaction.data["values"][0]
                coin.changeUserAttrib(str(ctx.author.id),
                                      "setting", "lang", select_lang)
                view.clear_items()
                view.stop()
                text_eb = coin.text("setting", "complt")["lang"][select_lang]
                embed = coin.emb(text_eb[0], text_eb[1], 0x27ff27)
                await interaction.response.edit_message(embed=embed, view=view)
        text_eb = coin.text("setting", "lang")[UserLang]
        select_1 = slc(
            text_eb, [["English", "en"], ["正體中文", "zh"]], ban=False)
        select_1.callback = slc_cb_1
        view.add_item(select_1)
        await itat.response.edit_message(view=view)

    # 任務難度設置
    async def set_lv_min(self, ctx, UserLang, itat, view):
        view.clear_items()

        async def slc_cb_1(interaction):
            if interaction.user.id == ctx.author.id:
                min_diff = interaction.data["values"][0]
                await self.set_lv_max(ctx, UserLang, interaction,
                                      view, int(min_diff))

        text_eb = coin.text("setting", "lv")[UserLang]
        option = [[i, i] for i in range(1, 17)]
        select_min = slc(text_eb[0], option)
        select_min.callback = slc_cb_1
        view.add_item(select_min)
        await itat.response.edit_message(view=view)

    async def set_lv_max(self, ctx, UserLang, itat, view, min_diff):
        async def slc_cb_2(interaction):
            if interaction.user.id == ctx.author.id:
                max_diff = int(interaction.data["values"][0])
                view.clear_items()
                view.stop()
                coin.changeUserAttrib(str(ctx.author.id), "setting", "lvrank",
                                      [min_diff, max_diff], "")
                text_eb = coin.text("setting", "complt")["lv"][UserLang]
                content = f"{text_eb[1]}{min_diff}**\n{text_eb[2]}{max_diff}**"
                embed = coin.emb(text_eb[0], content, 0x27ff27)
                await interaction.response.edit_message(embed=embed, view=view)
        text_eb = coin.text("setting", "lv")[UserLang]
        option = [[i, i] for i in range(min_diff, 17)]
        select_max = slc(text_eb[1], option)
        select_max.callback = slc_cb_2
        view.clear_items()
        view.add_item(select_max)
        if itat.response:
            await itat.response.edit_message(view=view)
        else:
            await itat.message.edit(view=view)


async def setup(bot):
    await bot.add_cog(Coin(bot))
