import json
import os
import Global_Element

class FileControl:
    @staticmethod
    def Save_Table(Mode):
        #取得Dictionary, 建立為Json物件
        JsonObj = None
        if(Mode == "Telegram"):
            JsonObj = json.dumps(Global_Element.TelegramTable)
            IndexJson = json.dumps(Global_Element.TelegramIndex)
            with open("./TargetTable/TelegramIndex.json", 'w') as JsonFile:
                JsonFile.write(IndexJson)
        elif(Mode == "LINE"):
            JsonObj = json.dumps(Global_Element.LINETable)
        
        #存檔作業
        with open(f"./TargetTable/{Mode}.json", 'w') as JsonFile:
            JsonFile.write(JsonObj)

    @staticmethod
    def Load_Table():
        #載入清單及索引
        JsonStr = ""
        with open("./TargetTable/Telegram.json", 'r') as JsonFile:
            JsonStr = JsonFile.read()
        if(JsonStr != ""):
            Global_Element.TelegramTable = json.loads(JsonStr)

        with open("./TargetTable/LINE.json", 'r') as JsonFile:
            JsonStr = JsonFile.read()
        if(JsonStr != ""):
            Global_Element.LINETable = json.loads(JsonStr)

        with open("./TargetTable/TelegramIndex.json", 'r') as JsonFile:
            JsonStr = JsonFile.read()
        if(JsonStr != ""):
            Global_Element.TelegramIndex = json.loads(JsonStr)

    @staticmethod
    def Save_ChatHistory(FromSource, msg, Mode):
        #儲存LINE聊天紀錄
        with open(f"./{Mode}Section/Chat_History/{FromSource}.log", 'a') as File:
            File.write(msg)