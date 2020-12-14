import time
import Global_Element
from linebot.models import TextSendMessage
from FileControl import FileControl
from datetime import datetime

class Telegram_MessageHandler:
    #Telegram接收器
    @staticmethod
    def Telegram_MessageReceive(msg):
        try:
            ContentType = msg['entities'][0]['type']

            #指令處理
            if(ContentType == 'bot_command'):
                Output = Telegram_MessageHandler.Telegram_CommandHandler(msg)
            #訊息處理
            else:
                Telegram_MessageHandler.Transfer_to_LINE(msg)
        except:
            Telegram_MessageHandler.Transfer_to_LINE(msg)


    @staticmethod
    def Telegram_CommandHandler(msg):
        Command = msg['text'].split(' ')
        TargetID = msg['chat']['id']
        #LINE群選擇器
        if(Command[0] == "/start" or Command[0] == "/start@LINE_Adapter_Bot"):            
            #取得目標群組名稱
            TargetName = ""
            for Run in range(1, len(Command)):
                TargetName += " " + Command[Run]
            TargetName = TargetName.strip()

            #更新目的地清單、索引
            Global_Element.TelegramTable[TargetName] = TargetID
            Global_Element.TelegramIndex[str(TargetID)] = TargetName
            FileControl.Save_Table("Telegram")
            Telegram_MessageHandler.Telegram_MessagePoster(TargetID, f"現正接收 {TargetName} 訊息")
        
        #停止接收LINE群訊息
        elif(Command[0] == "/exit" or Command[0] == "/exit@LINE_Adapter_Bot"):
            TargetID = str(msg['chat']['id'])
            #移除目的地清單、索引
            Key = Global_Element.TelegramIndex[TargetID]
            if(Key != ""):
                Global_Element.TelegramTable[Key] = ""
                Global_Element.TelegramIndex[TargetID] = ""
                FileControl.Save_Table("Telegram")
                Telegram_MessageHandler.Telegram_MessagePoster(TargetID, "已停止接收")
            else:
                Telegram_MessageHandler.Telegram_MessagePoster(TargetID, "目前未與LINE群組連結")
        #查看目前已啟用的LINE群
        elif(Command[0] == "/list" or Command[0] == "/list@LINE_Adapter_Bot"):
            Telegram_MessageHandler.Telegram_MessagePoster(TargetID, Telegram_MessageHandler.getLINE_List())

    @staticmethod
    def getLINE_List():
        #取得目前可供連結的LINE群組
        Output = ""
        for Run in Global_Element.LINETable.keys():
            Output += Run + "\n"
        if(Output == ""):
            Output = "清單內無內容"
        return Output

    @staticmethod
    def Telegram_MessagePoster(targetID, msgText):
        Global_Element.Tg_Bot.sendMessage(targetID, msgText)

    @staticmethod
    def Transfer_to_LINE(msg):
        TimeNow = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]"
        #Telegram轉送訊息到LINE
        Key = str(Global_Element.TelegramIndex[str(msg['chat']['id'])])
        if(Key != "" or Key != None):
            Content = str(msg['text'])
            Global_Element.Line_Bot.push_message(Global_Element.LINETable[Key], TextSendMessage(text = Content))
            FileControl.Save_ChatHistory(Key, f"{TimeNow}Bot_{Content}\n\n", "Line")