from discord import Interaction, SelectOption, app_commands
from discord.ui import View, Select, Item, Modal, TextInput
from discord.ext import commands
from discord import Interaction


class NameModal(Modal):

    def __init__(self):
        super().__init__(title="報名表單")
        self.name = TextInput(
            label='姓名:', default=f"XXX")  # 輸入的值會存在變數中
        self.phone = TextInput(
            label='電話:', default=f"0900123123")
        self.add_item(self.name)
        self.add_item(self.phone)

    async def on_submit(self, ctx):  # 視窗提交時觸發
        await ctx.send(f"姓名:{self.name}，電話:{self.phone}")


class FruitSelectView(View):
    def __init__(self):
        self.fruit = Select(placeholder="選擇你最喜歡的水果?", options=[SelectOption(
            label="香蕉",
            value="Banana",
            emoji="🍌"
        ), SelectOption(
            label="蘋果",
            value="Apple",
            emoji="🍎"
        )])
        self.add(self.fruit, self.select_callback)

    async def select_callback(self, ctx):
        fruit = self.fruit.values[0]  # 所選的選項都會在values的list裡面
        await ctx.send(f"你選的水果是{fruit}")

    def add(self, item: Item, callback):
        self.add_item(item)
        item.callback = callback
