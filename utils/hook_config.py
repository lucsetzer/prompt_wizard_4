mport os

class HookConfig:
    API_KEY = os.getenv("sk-221a023bf3d245048184283d594e3334")
    MODEL = "deepseek-chat"
    MAX_TOKENS = 2000

hook_config = HookConfig()
