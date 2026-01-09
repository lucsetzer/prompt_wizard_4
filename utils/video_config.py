import os

class VideoConfig:
    API_KEY = os.getenv("sk-849662e0871841a5a4496e006311beb9")
    MODEL = "deepseek-chat"
    MAX_TOKENS = 2000

video_config = VideoConfig()
