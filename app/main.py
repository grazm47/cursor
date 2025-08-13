from __future__ import annotations

from typing import Optional, List, Dict, Any
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from fastapi.responses import FileResponse

from .assistant.logic import handle_message


app = FastAPI(title="Rabitsa Sales Assistant", version="1.0.0")

# Статика
app.mount("/static", StaticFiles(directory="app/static", html=True), name="static")


class ChatRequest(BaseModel):
    session_id: Optional[str] = None
    message: str


class ChatResponse(BaseModel):
    session_id: str
    reply: str
    suggestions: List[str]
    state: Dict[str, Any]
    quote: Optional[Dict[str, Any]] = None


@app.get("/")
async def index() -> FileResponse:
    return FileResponse("app/static/index.html")


@app.get("/health")
async def health() -> Dict[str, str]:
    return {"status": "ok"}


@app.post("/api/chat", response_model=ChatResponse)
async def api_chat(req: ChatRequest) -> ChatResponse:
    result = handle_message(req.session_id, req.message)
    return ChatResponse(**result)