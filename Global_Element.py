import telepot
from linebot import LineBotApi, WebhookHandler

Tg_Bot = None
Line_Bot = None
Line_Hookhandler = None

TargetID = ""

#ID Table
TelegramTable = {}
TelegramIndex = {}
LINETable = {}