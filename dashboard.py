from fastapi import APIRouter, Request, FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
router = APIRouter()
templates = Jinja2Templates(directory="templates")

user_tokens = {"testuser: 100"}

@app.middleware("http")
async def check_tokens(request: Request, call_next):
    # Only check /prompt-wizard routes
    if request.url.path.startswith("/prompt-wizard/generate"):
        user_id = "testuser"  # Get from session later
        if user_tokens.get(user_id, 0) < 2:
            return JSONResponse(
                status_code=402,
                content={"error": "Need 2 tokens to use Prompt Wizard"}
            )
        # Deduct
        user_tokens[user_id] -= 2
        print(f"✅ Tokens deducted. {user_id} now has {user_tokens[user_id]}")
    
    # Continue to Prompt Wizard (unchanged!)
    return await call_next(request)



@router.get("/dashboard")
async def dashboard(request: Request):
    if not request.session.get("user_id"):
        from fastapi.responses import RedirectResponse
        return RedirectResponse(url="/", status_code=303)
    
    # Get user data
    user_data = {
        "username": request.session.get("username", "Guest"),
        "token_balance": request.session.get("token_balance", 0)
    }

    apps = [
        {
            "name": "Prompt Wizard",
            "description": "Transform ideas into powerful AI prompts",
            "url": "/prompt-wizard/step/1",
            "icon": "fas fa-magic",
            "color": "#00f5d4",
            "status": "active",
            "tokens": 2
        },
        {
            "name": "Script Wizard",
            "description": "Turn ideas into professional scripts",
            "url": "/script-wizard",
            "icon": "fas fa-scroll",
            "color": "#8b5cf6",
            "status": "active",
            "tokens": 1
        },
        {
            "name": "Hook Wizard",
            "description": "Create attention-grabbing hooks",
            "url": "http://localhost:8003",  # ← Direct URL
            "icon": "fas fa-fish",
            "color": "#f59e0b",
            "status": "active",
            "tokens": 1
        },
        {
            "name": "Document Wizard",
            "description": "Analyze professional documents",
            "url": "#",
            "icon": "fas fa-file-alt",
            "color": "#10b981",
            "status": "active",
            "tokens": 3
        },
        {
            "name": "Video Wizard",
            "description": "Analyze your videos",
            "url": "#",
            "icon": "fas fa-video",
            "color": "#ef4444",
            "status": "active",
            "tokens": 2
        },
        {
            "name": "Thumbnail Wizard",
            "description": "Analyzing your thumbnails",
            "url": "#",
            "icon": "fas fa-image",
            "color": "#06b6d4",
            "status": "active",
            "tokens": 3
        },
    ]
    
    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request, "apps": apps}
    )
