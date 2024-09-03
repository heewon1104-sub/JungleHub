
from configuration.config import Config

config = Config()

clientId = config.find("MONGODB_ID")
clientKey = config.find("MONGODB_SECRET")

class RepositoryConfig:
    dbUrl = f'mongodb+srv://{clientId}:{clientKey}@jmcluster.pcbhuo9.mongodb.net/?retryWrites=true&w=majority&appName=jmCluster'

