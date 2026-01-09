# main_app.py - CLEAN VERSION
from fastapi import Request, Form, Depends, FastAPI
from fastapi.responses import RedirectResponse
from core.database import SessionLocal, User
from sqlalchemy.exc import IntegrityError
from core.tokens_simple import check_tokens_simple
from fastapi.templating import Jinja2Templates


templates = Jinja2Templates(directory="templates")

app = FastAPI(title="Prompts Alchemy")


from starlette.middleware.sessions import SessionMiddleware
from dashboard import router as dashboard_router
app.include_router(dashboard_router)

app.add_middleware(SessionMiddleware, secret_key="your-secret-key-change-this")


# Public homepage
@app.get("/")
async def root(request: Request):
    """Public landing page with login/signup"""
    return templates.TemplateResponse("index.html", {"request": request})

# Login route
@app.post("/login")
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    db = SessionLocal()
    user = db.query(User).filter_by(username=username).first()
    db.close()
    
    # TEMPORARY: For demo, accept any password for testuser
    # TODO: Replace with proper password checking: user.check_password(password)
    if user and user.check_password(password):
        request.session["user_id"] = user.id
        request.session["username"] = user.username
        return RedirectResponse(url="/dashboard", status_code=303)
    
        # TODO: Set up proper sessions (FastAPI's `fastapi-users` or JWT)
        # For now, we'll use a simple cookie/session simulation
        response = RedirectResponse(url="/dashboard", status_code=303)
        # Store user ID in session (simplified)
        # In production, use proper signed cookies or JWT
        return response
    else:
        # Return to homepage with error
        return templates.TemplateResponse("index.html", {
            "request": request,
            "error": "Invalid username or password"
        })

# Signup route
@app.post("/signup")
async def signup(
    request: Request,
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...)
):
    print("===== SIGNUP ATTEMPT =====")
    print(f"Username: {username}, Email: {email}")
    
    db = SessionLocal()
    
    # Check if user exists
    if db.query(User).filter_by(username=username).first():
        db.close()
        return templates.TemplateResponse("index.html", {
            "request": request,
            "error": "Username already taken"
        })
    
    # Create user with 10 free tokens
    try:
        user = User(
            username=username,
            email=email,
            token_balance=10  # Free starter tokens
        )
        user.set_password(password)  # Make sure this method exists in User model
        db.add(user)
        db.commit()
        
        # Auto-login after signup
        response = RedirectResponse(url="/dashboard", status_code=303)
        # TODO: Set session cookie
        return response
        
    except IntegrityError:
        db.rollback()
        return templates.TemplateResponse("index.html", {
            "request": request,
            "error": "Email already registered"
        })
    finally:
        db.close()

# Logout route
@app.get("/logout")
async def logout():
    response = RedirectResponse(url="/")
    # TODO: Clear session cookie
    return response



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
