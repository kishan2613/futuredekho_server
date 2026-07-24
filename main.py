from fastapi import FastAPI
from routes.chat import router as chat_router
from routes.auth import router as auth
from routes.palm import router as analyze_palm
from fastapi.middleware.cors import CORSMiddleware
from routes.conversation import router as conversation_router
from routes.compatibility import router as compatibility_router

app = FastAPI(
    title="FutureDekho API",
    version="1.0.0"
)

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def health():
    return {
        "success": True,
        "message": "Backend Running"
    }

app.include_router(
    auth,
    prefix="/auth",
    tags=["Authentication"]
)

app.include_router(
    analyze_palm,
    prefix="/palm",
    tags=["Palm"]
)

app.include_router(
    conversation_router,
    prefix="/conversation",
    tags=["Conversation"]
)

app.include_router(
    chat_router,
    prefix="/chat",
    tags=["Chat"]
)

app.include_router(compatibility_router)

