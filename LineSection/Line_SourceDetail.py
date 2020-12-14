import configparser
import json
from NetworkTask import WebCrawler

class LINE_DetailHandler:
    @staticmethod
    def getUserDetail(Source):
        #取得ID
        UserID = Source['userId']
        
        #取得使用者細節
        str_URL = f"https://api.line.me/v2/bot/profile/{UserID}"
        status_Code, Content = WebCrawler.DownloadTask.DownloadData(str_URL)
        return LINE_DetailHandler.getJsonObj(Content)


    @staticmethod
    def getGroupDetail(Source):
        #取得ID
        GroupID = Source['groupId']

        #取得群組細節
        str_URL = f"https://api.line.me/v2/bot/group/{GroupID}/summary"
        status_Code, Content = WebCrawler.DownloadTask.DownloadData(str_URL)
        return LINE_DetailHandler.getJsonObj(Content)

    @staticmethod
    def getMemberDetail(Source):
        #取得ID
        GroupID = Source['groupId']
        UserID = Source['userId']

        #取得細節
        str_URL = f"https://api.line.me/v2/bot/group/{GroupID}/member/{UserID}"
        status_Code, Content = WebCrawler.DownloadTask.DownloadData(str_URL)
        return LINE_DetailHandler.getJsonObj(Content)

    
    @staticmethod
    def getJsonObj(strDetail):
        Data = json.loads(strDetail)
        return Data