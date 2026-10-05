@echo off
echo ========================================================
echo Starting Multilingual NLP Chatbot Backend (FastAPI)
echo Primary Languages: Sanskrit, English, Tulu
echo ========================================================
python -m uvicorn backend.api.app:app --host 127.0.0.1 --port 8000 --reload
pause
