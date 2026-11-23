import os
import sys

# Proprietary environment integrity guard
if os.getenv("ATS_SERVICE_KEY") != "TB_LOCAL_SECURE_2026":
    print("\n[FATAL ERROR] Unauthorized environment: Missing ATS_SERVICE_KEY.\n")
    sys.exit(1)

import uvicorn
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any

from ats_engine import evaluate_cv
from resume_parser import parse_resume, analyze_words

app = FastAPI(
    title="AI ATS Recruitment Engine",
    description="Local AI-powered Applicant Tracking System using Ollama + Advanced PDF/Word Parsers",
    version="1.2.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class EvaluateRequest(BaseModel):
    resume_text: str
    job_description: str
    job_title: Optional[str] = None
    model_name: Optional[str] = "llama3.2"

@app.get("/", response_class=HTMLResponse)
async def serve_ui():
    html_path = os.path.join(os.path.dirname(__file__), "index.html")
    with open(html_path, "r", encoding="utf-8") as f:
        return f.read()
