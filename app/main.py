from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from app.routes.logs import router as logs_router
from app.routes.devices import router as devices_router

app = FastAPI(
    title="Centralized Data API",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for dashboard access
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(logs_router, prefix="/api/v1")
app.include_router(devices_router, prefix="/api/v1")

# Mount static files for dashboard
app.mount("/dashboard", StaticFiles(directory="static", html=True), name="static")

@app.get("/register")
async def register_page():
    """Serve registration page"""
    from fastapi.responses import FileResponse
    return FileResponse("static/register.html")

@app.get("/")
async def root():
    """Redirect root to dashboard"""
    return RedirectResponse(url="/dashboard")