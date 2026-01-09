import os

class ScriptConfig:
    API_KEY = os.getenv("sk-fd10cfdc6006469ab692f714ab027a28")
    MODEL = "deepseek-chat"
    MAX_TOKENS = 2000

script_config = ScriptConfig()
