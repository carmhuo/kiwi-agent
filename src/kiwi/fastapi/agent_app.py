from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware # For frontend if on different origin
from fastapi.responses import FileResponse
from pathlib import Path

from kiwi.fastapi.routers import router # Import the agent router

APP_DIR = Path(__file__).resolve().parent # Path to fastapi
PROJECT_ROOT_DIR = APP_DIR.parent.parent.parent # Path to project root (e.g., kiwi/)
FRONTEND_DIR = PROJECT_ROOT_DIR / "frontend" / "src"
print(f"app dir: {APP_DIR}, project dir: {PROJECT_ROOT_DIR}, frontend: {FRONTEND_DIR}")

app = FastAPI(
    title="Agent API",
    description="API for interacting with a ReAct Agent.",
    version="0.1.0"
)

# CORS Middleware (if your frontend is on a different port/domain during development)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Or specify your frontend origin e.g., "http://localhost:8000" for dev
    allow_credentials=True,
    allow_methods=["*"], # Allows all methods
    allow_headers=["*"], # Allows all headers
)

app.include_router(router) # Include the agent router


@app.get("/", response_class=FileResponse, tags=["Client"])
async def serve_chat_at_root():
    """Serves the main chat HTML page from the root."""
    # Prioritize index.html, then fall back to chat.html
    index_html_path = FRONTEND_DIR / "index.html"
    chat_html_path = FRONTEND_DIR / "chat.html"

    if index_html_path.exists():
        return FileResponse(str(index_html_path))
    elif chat_html_path.exists():
        return FileResponse(str(chat_html_path))
    else:
        raise HTTPException(status_code=404, detail=f"index.html or chat.html not found in {FRONTEND_DIR}")

# Optional: if you want to run directly with uvicorn.run for simplicity in some cases
if __name__ == "__main__":
    import uvicorn
    # Make sure agent_graph.py has loaded .env and compiled 'graph' before this point.
    # Uvicorn typically handles module loading.
    uvicorn.run(app, host="0.0.0.0", port=8000)