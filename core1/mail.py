import discord
from discord.ext import commands
from core1.emailhandler import Mailer
import core1.func as func
from core1.classes import Cog_Extension
import core1.CytoidData as CytoidData
import core1.MainTask as MainTask
import os


def sendMail(receive_mail, title, content):
    # initiate the Mailer object
    mymailer = Mailer(os.getenv("EMAIL_USER"), os.getenv("EMAIL_PASSWORD"))

    # login
    mymailer.login()

    mymailer.send(
        target=receive_mail,
        content=content,
        subject=title
    )

    print("Email Sent!")

    # close server connection
    mymailer.quit()
