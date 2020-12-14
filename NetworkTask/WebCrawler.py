import requests
import configparser
import os

class DownloadTask:
    @staticmethod
    def DownloadData(URL):
        #header設定
        AuthorizationText = f"Bearer {DownloadTask.getSecret()}"
        HeaderData = {"Authorization":AuthorizationText}

        #建立新連線
        Connection = requests.session()
        Data = Connection.get(URL, headers = HeaderData)
        Data.encoding = "UTF-8"
        Connection.close()

        return Data.status_code, Data.text

    @staticmethod
    def getSecret():        
        #取得Channel Secret
        LINE_Config = configparser.ConfigParser()
        LINE_Config.read(os.path.dirname(__file__) + '/../LineSection/Config.ini')
        return LINE_Config['line-bot']['channel_access_token']
