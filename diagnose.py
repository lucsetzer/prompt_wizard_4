# diagnose.py
from main_app import app

print("="*60)
print("🔍 ALL HOOK WIZARD ROUTES (if any):")
print("="*60)

hook_routes_found = False
for route in app.routes:
    if hasattr(route, "path"):
        print(f"  {route.path}")
        if "hook" in route.path.lower():
            hook_routes_found = True

if not hook_routes_found:
    print("\n❌ NO HOOK WIZARD ROUTES FOUND!")
    print("This means either:")
    print("1. hook_wizard.py has no @router.get() routes")
    print("2. The router isn't being included in main_app.py")
    print("3. All routes start with '/' (conflict with other apps)")
