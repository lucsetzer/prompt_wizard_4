# utils/api_config.py
import os

class APIConfig:
    # Single key for all apps (simplest)
    DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
    
    # Or per-app keys if you need them:
    # SCRIPT_KEY = os.getenv("DEEPSEEK_SCRIPT_KEY")
    # HOOK_KEY = os.getenv("DEEPSEEK_HOOK_KEY")

api_config = APIConfig()
