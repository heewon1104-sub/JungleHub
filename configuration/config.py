import xml.etree.ElementTree as ET


class Config:
    tree = ET.parse('configuration/config.xml')
    root = tree.getroot()

    def find(self, key): 
        return self.root.find(f"string[@name='{key}']").text
    

''' 사용법 

from configuration.config import Config

config = Config()

clientId = config.find("MONGODB_ID").text
clientKey = config.find("MONGODB_SECRET").text

'''