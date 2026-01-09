import os

class ThumbnailConfig:
    API_KEY = os.getenv("sk-7197416bed2343a2ade8c49414c235d0")
    MODEL = "deepseek-chat"
    MAX_TOKENS = 2000

thumbnail_config = ThumbnailConfig()
