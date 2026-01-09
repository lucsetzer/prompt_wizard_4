import os

class DocumentConfig:
    API_KEY = os.getenv("sk-8834d031717247b4beb438d4de612c10")
    MODEL = "deepseek-chat"
    MAX_TOKENS = 2000

document_config = DocumentConfig()
