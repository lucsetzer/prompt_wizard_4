import os

class PromptConfig:
    API_KEY = os.getenv("sk-8dadf46bd95c47f88e8cb1fb4cd1f89e")
    MODEL = "deepseek-chat"
    MAX_TOKENS = 2000

prompt_config = PromptConfig()
