from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/dashboard")
async def dashboard(request: Request):
    apps = [
        {
            "name": "Prompt Wizard",
            "description": "Transform ideas into powerful AI prompts",
            "url": "/prompt-wizard/step/1",
            "icon": "fas fa-magic",
            "color": "#00f5d4",
            "status": "active"
        },
        {
            "name": "Script Wizard",
            "description": "Turn ideas into professional scripts",
            "url": "/script-wizard",
            "icon": "fas fa-scroll",
            "color": "#8b5cf6",
            "status": "active"
        },
        {
            "name": "Hook Wizard",
            "description": "Create attention-grabbing hooks",
            "url": "http://localhost:8003",  # ← Direct URL
            "icon": "fas fa-fish",
            "color": "#f59e0b",
            "status": "active"
        },
        {
            "name": "Document Wizard",
            "description": "Generate professional documents",
            "url": "#",
            "icon": "fas fa-file-alt",
            "color": "#10b981",
            "status": "coming-soon"
        },
        {
            "name": "Video Wizard",
            "description": "Create video scripts and storyboards",
            "url": "#",
            "icon": "fas fa-video",
            "color": "#ef4444",
            "status": "planned"
        },
        {
            "name": "Thumbnail Wizard",
            "description": "Design eye-catching thumbnails",
            "url": "#",
            "icon": "fas fa-image",
            "color": "#06b6d4",
            "status": "planned"
        },
    ]
    
    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request, "apps": apps}
    )
