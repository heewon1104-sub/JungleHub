import xml.etree.ElementTree as ET


class Config:
    tree = ET.parse('configuration/config.xml')
    root = tree.getroot()

    def find(self, key): 
        return self.root.find(f"string[@name='{key}']").text
    
    def getHost(self):
        return "127.0.0.1"

    
    def getPort(self):
        if self.isDev():
            return "8000"
        else:
            return "5000"
    
    def isDev(self):
        secretKey = self.find("DEPLOYMENT_ENVIRONMENT")
        return secretKey != "PROD"
    

''' 사용법 

from configuration.config import Config

config = Config()

clientId = config.find("MONGODB_ID")
clientKey = config.find("MONGODB_SECRET")

'''