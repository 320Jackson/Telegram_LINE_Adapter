from flask import Flask, request
from pprint import pprint
#Telegram Package
import telepot
from telepot.loop import OrderedWebhook
from TelegramSection import Tg_Bot_Client
import Global_Element
from FileControl import FileControl
#LINE Package
from linebot import LineBotApi, WebhookHandler
from LineSection.Line_Bot_Client import LINE_MessageHandler
#Config Package
import configparser
#Log Package
import logging

#Logging Setting

FormatStr = "[%(asctime)s] %(levelname)s:%(message)s"
logging.basicConfig(filename = "./Bot.log", filemode = "a", format = FormatStr)

#WebHook App
WebApp = Flask(__name__)

#Config Object
Tg_Config = configparser.ConfigParser()
Tg_Config.read("./TelegramSection/Config.ini")
Line_Config = configparser.ConfigParser()
Line_Config.read("./LineSection/Config.ini")

#===================Telegram Section======================
#Telegram Bot Entity
Global_Element.Tg_Bot = telepot.Bot(Tg_Config["TELEGRAM"]["ACCESS_TOKEN"])

#處理Telegram訊息
@WebApp.route('/Telegram', methods = ["POST"])
def Telegram_Handler():
    BotHook.feed(request.data)    
    return '200 OK'

BotHook = OrderedWebhook(Global_Element.Tg_Bot, Tg_Bot_Client.Telegram_MessageHandler.Telegram_MessageReceive)

#======================LINE Section=========================
#LINE Entity
Global_Element.Line_Bot = LineBotApi(Line_Config["line-bot"]["channel_access_token"])
Global_Element.Line_Hookhandler = WebhookHandler(Line_Config["line-bot"]["channel_secret"])

#處理LINE訊息
@WebApp.route('/LINE', methods = ["POST"])
def LINE_Handler():
    Body = request.get_data(as_text = True)
    LINE_MessageHandler.LINE_MessageReceive(Body)
    
    return '200 OK'

if __name__ == '__main__':
    BotHook.run_as_thread()
    FileControl.Load_Table()
    WebApp.run(host = "0.0.0.0", port = 5001)