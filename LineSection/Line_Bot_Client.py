from LineSection.Line_SourceDetail import LINE_DetailHandler
import json
from NetworkTask import WebCrawler
from LineSection.Line_Events import msgEvents_Handler

class LINE_MessageHandler:
    #訊息接收器
    @staticmethod
    def LINE_MessageReceive(msg):
        #解析JSON格式訊息
        msgObj = json.loads(msg)
        Source = msgObj['events'][0]['source']
        EventType = msgObj['events'][0]['type']

        #事件判斷
        if(EventType == "message"):
            Message = msgObj['events'][0]['message']
            #取得訊息
            MessageContent = LINE_MessageHandler.getMessageContent(Message)
            msgEvents_Handler.EventHandler(Source, EventType, MessageContent)
        else:
            msgEvents_Handler.EventHandler(Source, EventType, "")

    @staticmethod
    def getMessageContent(Message):
        #取得訊息類型
        msgType = Message['type']
        if(msgType == 'text'):
            return Message[msgType]
        else:
            return str(Message)