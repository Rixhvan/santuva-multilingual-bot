from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from backend.models.schemas import ChatRequest, ChatResponse
from backend.services.nlp_service import nlp_service
from backend.nlp.dialogue.memory import conversation_memory
from backend.config.settings import settings

app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    description="Level 1 Multilingual NLP Conversational Engine (Sanskrit - English - Tulu)"
)

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {
        "status": "online",
        "system": settings.app_name,
        "version": settings.version,
        "languages": settings.language_names,
        "tulu_tiers": settings.tulu_resource_tiers
    }

@app.get("/api/info")
def get_info():
    return {
        "languages": settings.language_names,
        "scripts": settings.supported_scripts,
        "tulu_resource_tiers": settings.tulu_resource_tiers,
        "confidence_thresholds": {
            "language": settings.lang_confidence_threshold,
            "intent": settings.intent_confidence_threshold,
            "clarification": settings.clarification_threshold
        }
    }

@app.post("/api/chat", response_model=ChatResponse)
def chat_endpoint(req: ChatRequest):
    if not req.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty.")
    
    session_id = req.conversation_id or "default"
    response = nlp_service.process_query(
        raw_text=req.text,
        session_id=session_id,
        user_selected_lang=req.user_selected_language
    )
    return response

@app.post("/api/reset")
def reset_conversation(session_id: str = "default"):
    conversation_memory.clear(session_id)
    return {"status": "success", "message": f"Session '{session_id}' cleared."}

@app.get("/api/evaluate")
def run_evaluation_endpoint():
    from tests.evaluate_pipeline import evaluate_language_dataset
    datasets = [
        ("sa_100.json", "sa", "Sanskrit"),
        ("en_100.json", "en", "English"),
        ("tu_100.json", "tcy", "Tulu")
    ]
    results = []
    for filename, code, name in datasets:
        path = settings.evaluation_dir / filename
        results.append(evaluate_language_dataset(path, code, name))
    return {"status": "success", "metrics": results}
