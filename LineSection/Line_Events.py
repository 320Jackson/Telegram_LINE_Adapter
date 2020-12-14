from LineSection.Line_SourceDetail import LINE_DetailHandler
from FileControl import FileControl
from TelegramSection.Tg_Bot_Client import Telegram_MessageHandler
from datetime import datetime
import Global_Element

class msgEvents_Handler:
    @staticmethod
    def EventHandler(Source, Mode, Content):
        TimeNow = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]"
        Key = ""
        Value = ""
        Output = ""
        HistoryStr = ""

        #群組來源
        if(Source['type'] == "group"):
            GroupDetail = LINE_DetailHandler.getGroupDetail(Source)
            Key = GroupDetail['groupName']
            Value = Source['groupId']
            if(Mode == "message"):
                UserDetail = LINE_DetailHandler.getMemberDetail(Source)
                Output = f"{UserDetail['displayName']}\n{Key}\n{Content}"
                HistoryStr = f"{TimeNow}{UserDetail['displayName']}\n{Content}\n\n"
        #使用者來源
        else:
            UserDetail = LINE_DetailHandler.getUserDetail(Source)
            Key = UserDetail['displayName']
            Value = Source['userId']
            if(Mode == "message"):
                Output = f"{Key}\n{Content}"
                HistoryStr = f"{TimeNow}{Content}\n\n"
        #加入群組
        if(Mode == "join"):
            msgEvents_Handler.AddTable(Key, Value)
        elif(Mode == "message"):
            FileControl.Save_ChatHistory(Key, HistoryStr, "Line")
            if((Key in Global_Element.LINETable) == False):
                msgEvents_Handler.AddTable(Key, Value)
            if((Key in Global_Element.TelegramTable) == True):
                Telegram_MessageHandler.Telegram_MessagePoster(Global_Element.TelegramTable[Key], Output)


    @staticmethod
    def AddTable(Name, ID):
        #更新索引
        Global_Element.LINETable[Name] = ID
        FileControl.Save_Table("LINE")