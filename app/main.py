"""
GRAVITYchat - Minimal Working Demo
----------------------------------
Simplified version that works without Azure dependencies for demonstration.

Author: Alexander O. Smith (2025–present)
Maintainer: Alexander O. Smith <aosmith@syr.edu>
"""

import os
import logging
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="GRAVITYchat API",
    description="RAG chatbot for LIGO/Gravity Spy citizen scientists",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class ChatRequest(BaseModel):
    question: str
    top_k: Optional[int] = 5
    max_tokens: Optional[int] = 500

class Citation(BaseModel):
    title: str
    authors: Optional[str] = None
    url: Optional[str] = None
    year: Optional[int] = None
    source: str

class ChatResponse(BaseModel):
    answer: str
    citations: List[Citation]
    sources_used: int
    confidence: str

class HealthResponse(BaseModel):
    status: str
    message: str
    version: str

# Mock data for demonstration
MOCK_DOCUMENTS = [
    {
        "id": "mock-1",
        "content": "LIGO (Laser Interferometer Gravitational-Wave Observatory) is a large-scale physics experiment designed to detect cosmic gravitational waves. The observatory uses laser interferometry to measure the minute ripples in space-time caused by passing gravitational waves from cataclysmic cosmic events such as merging neutron stars or black holes.",
        "title": "Introduction to LIGO",
        "authors": "LIGO Scientific Collaboration",
        "url": "https://www.ligo.org/science.php",
        "year": 2023,
        "source": "LIGO Documentation"
    },
    {
        "id": "mock-2", 
        "content": "Gravity Spy is a citizen science project that helps classify glitches in LIGO data. Volunteers examine spectrograms of gravitational wave detector noise to identify and categorize different types of instrumental artifacts that could interfere with gravitational wave detection.",
        "title": "Gravity Spy Citizen Science",
        "authors": "Gravity Spy Team",
        "url": "https://www.zooniverse.org/projects/zooniverse/gravity-spy",
        "year": 2024,
        "source": "Zooniverse"
    },
    {
        "id": "mock-3",
        "content": "aLOGs (LIGO Online Glitch Database) contain detailed information about instrumental glitches detected in LIGO data. These logs help scientists understand the sources of noise and improve detector sensitivity by identifying and mitigating systematic issues.",
        "title": "Understanding aLOGs",
        "authors": "LIGO Detector Characterization Group",
        "url": "https://alog.ligo-wa.caltech.edu/",
        "year": 2023,
        "source": "aLOG Database"
    }
]

def get_mock_documents(query: str, top_k: int = 5) -> List[dict]:
    """Return mock documents based on query keywords."""
    query_lower = query.lower()
    filtered_docs = []
    
    for doc in MOCK_DOCUMENTS:
        if any(keyword in doc["content"].lower() or keyword in doc["title"].lower() 
               for keyword in query_lower.split()):
            filtered_docs.append(doc)
    
    return filtered_docs[:top_k]

def generate_mock_response(question: str, documents: List[dict]) -> str:
    """Generate a mock response based on the question and documents."""
    question_lower = question.lower()
    
    if "ligo" in question_lower:
        return f"""Based on the LIGO/Gravity Spy knowledge base, LIGO (Laser Interferometer Gravitational-Wave Observatory) is a large-scale physics experiment designed to detect cosmic gravitational waves. The observatory uses laser interferometry to measure minute ripples in space-time caused by passing gravitational waves from cataclysmic cosmic events such as merging neutron stars or black holes.

LIGO consists of two identical detectors located in Livingston, Louisiana, and Hanford, Washington. Each detector uses laser interferometry to detect gravitational waves by measuring tiny changes in the length of 4-kilometer-long arms arranged in an L-shape."""
    
    elif "gravity spy" in question_lower:
        return f"""Gravity Spy is a citizen science project that helps classify glitches in LIGO data. Volunteers examine spectrograms of gravitational wave detector noise to identify and categorize different types of instrumental artifacts that could interfere with gravitational wave detection.

The project uses machine learning combined with human expertise to improve the classification of detector glitches, which helps scientists understand and mitigate sources of noise in the LIGO detectors."""
    
    elif "alog" in question_lower or "glitch" in question_lower:
        return f"""aLOGs (LIGO Online Glitch Database) contain detailed information about instrumental glitches detected in LIGO data. These logs help scientists understand the sources of noise and improve detector sensitivity by identifying and mitigating systematic issues.

Glitches in LIGO data are instrumental artifacts that can interfere with gravitational wave detection. They can be caused by various sources including environmental factors, detector hardware issues, or external disturbances."""
    
    else:
        return f"""Thank you for your question about '{question}'. Based on the available LIGO and Gravity Spy documentation, I can provide information about:

• **LIGO Technology**: Gravitational wave detectors, interferometry, and sensitivity
• **Gravity Spy**: Citizen science project for glitch classification  
• **aLOGs**: LIGO Online Glitch Database for detector characterization
• **Scientific Results**: Gravitational wave detections and astrophysics

Could you please be more specific about what aspect you'd like to learn about?"""

@app.get("/", response_model=HealthResponse)
async def root():
    """Root endpoint with basic health check."""
    return HealthResponse(
        status="healthy",
        message="GRAVITYchat API is running",
        version="1.0.0"
    )

@app.get("/healthz", response_model=HealthResponse)
async def health_check():
    """Health check endpoint for monitoring."""
    return HealthResponse(
        status="healthy",
        message="All services operational (mock mode)",
        version="1.0.0"
    )

@app.post("/ask", response_model=ChatResponse)
async def ask_question(request: ChatRequest):
    """
    Main RAG endpoint for answering citizen scientist questions.
    """
    try:
        logger.info(f"Processing question: {request.question[:100]}...")
        
        # Step 1: Retrieve relevant documents (mock)
        retrieved_docs = get_mock_documents(request.question, request.top_k)
        
        if not retrieved_docs:
            return ChatResponse(
                answer="I couldn't find relevant information in our knowledge base to answer your question. Please try rephrasing your question or contact a LIGO scientist for assistance.",
                citations=[],
                sources_used=0,
                confidence="low"
            )
        
        # Step 2: Generate response using retrieved context
        response = generate_mock_response(request.question, retrieved_docs)
        
        # Step 3: Create citations
        citations = []
        for doc in retrieved_docs:
            citation = Citation(
                title=doc["title"],
                authors=doc["authors"],
                url=doc["url"],
                year=doc["year"],
                source=doc["source"]
            )
            citations.append(citation)
        
        return ChatResponse(
            answer=response,
            citations=citations,
            sources_used=len(retrieved_docs),
            confidence="high" if len(retrieved_docs) >= 2 else "medium"
        )
        
    except Exception as e:
        logger.error(f"Error processing question: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/index/status")
async def index_status():
    """Check the status of the document index."""
    return {
        "status": "healthy",
        "total_documents": len(MOCK_DOCUMENTS),
        "last_updated": "2025-01-21T19:30:00Z",
        "index_name": "gravitychat-docs-mock",
        "mode": "mock"
    }

if __name__ == "__main__":
    print("🚀 Starting GRAVITYchat RAG System...")
    print("📚 LIGO/Gravity Spy Citizen Science Chatbot")
    print("🔬 Powered by FastAPI (Mock Mode)")
    print("=" * 50)
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )