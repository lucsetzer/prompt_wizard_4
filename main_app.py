# main_app.py - CLEAN VERSION
from fastapi import FastAPI

app = FastAPI(title="Prompts Alchemy")

# DEBUG: List ALL routes on startup
@app.on_event("startup")
async def debug_routes():
    print("\n" + "="*50)
    print("🔍 ALL REGISTERED ROUTES:")
    for route in app.routes:
        if hasattr(route, "path"):
            print(f"  {route.path}")
    print("="*50)

print("🔍 Loading apps...")

# Import from ROOT directory (all files are in root)
try:
    from dashboard import router as dashboard_router
    app.include_router(dashboard_router)
    print("✅ Dashboard loaded")
except Exception as e:
    print(f"❌ Dashboard: {e}")

try:
    from script_wizard import router as script_wizard_router
    app.include_router(script_wizard_router)
    print("✅ Script Wizard loaded")
except Exception as e:
    print(f"❌ Script Wizard: {e}")

try:
    from prompt_wizard import router as prompt_wizard_router
    app.include_router(prompt_wizard_router)
    print("✅ Prompt Wizard loaded")
except Exception as e:
    print(f"❌ Prompt Wizard: {e}")


try:
    from hook_wizard import router as hook_wizard_router
    app.include_router(hook_wizard_router, prefix="/hook-wizard")
    print("✅ Hook Wizard loaded")
except Exception as e:
    print(f"❌ Hook Wizard: {e}")

print("\n📋 REGISTERED ROUTES:")
for route in app.routes:
    if hasattr(route, "path"):
        print(f"  {route.path}")

print("\n🚀 Starting server on http://localhost:8000")

@app.get("/test-hook-now")
async def test_hook_now():
    return {
        "status": "Test route works",
        "next_step": "Go to /hook-wizard manually",
        "dashboard_url": "/dashboard",
        "hook_wizard_should_be_at": "/hook-wizard"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
