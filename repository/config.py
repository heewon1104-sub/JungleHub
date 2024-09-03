
import xml.etree.ElementTree as ET

# XML 파일 로드
tree = ET.parse('keys.xml')
root = tree.getroot()

# 값 추출
clientId = root.find("string[@name='MONGODB_ID']").text
clientKey = root.find("string[@name='MONGODB_SECRET']").text

print(clientId, clientKey)

class RepositoryConfig:
    dbUrl = f'mongodb+srv://{clientId}:{clientKey}@jmcluster.pcbhuo9.mongodb.net/?retryWrites=true&w=majority&appName=jmCluster'






