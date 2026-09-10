import sys
from pathlib import Path
import asyncio

# Add repo root to sys.path so src.* imports work
REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from dotenv import load_dotenv
# Load existing .env from repo root
load_dotenv(dotenv_path=REPO_ROOT / ".env")

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import contextlib

from session_store import store
from routers import analysis, impact, ai_router as ai, export

@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    async def cleanup_task():
        while True:
            await asyncio.sleep(600)  # run every 10 mins
            store.cleanup_expired()
    
    task = asyncio.create_task(cleanup_task())
    yield
    # Shutdown
    task.cancel()

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(analysis.router, prefix="/api", tags=["analysis"])
app.include_router(impact.router, prefix="/api", tags=["impact"])
app.include_router(ai.router, prefix="/api", tags=["ai"])
app.include_router(export.router, prefix="/api", tags=["export"])

@app.get("/")
async def health_check():
    return {"status": "ok", "service": "impactx-backend"}
