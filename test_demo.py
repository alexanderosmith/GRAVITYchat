#!/usr/bin/env python3
"""
GRAVITYchat - Demo Test Script
-----------------------------
Test the RAG functionality without needing a running server.

Author: Alexander O. Smith (2025–present)
Maintainer: Alexander O. Smith <aosmith@syr.edu>
"""

import sys
import os
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

import json
from app.main import get_mock_documents, generate_mock_response, MOCK_DOCUMENTS

def test_rag_functionality():
    """Test the RAG functionality with sample questions."""
    
    print("🚀 GRAVITYchat RAG System Demo")
    print("=" * 50)
    
    # Test questions
    test_questions = [
        "What is LIGO?",
        "How does Gravity Spy work?",
        "What are aLOGs?",
        "Tell me about gravitational wave detection",
        "What causes glitches in LIGO data?",
        "Where is Gravity Spy located?"
    ]
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n📝 Question {i}: {question}")
        print("-" * 40)
        
        # Step 1: Retrieve documents
        documents = get_mock_documents(question, top_k=3)
        print(f"📚 Retrieved {len(documents)} relevant documents:")
        
        for doc in documents:
            print(f"  • {doc['title']} ({doc['source']})")
        
        # Step 2: Generate response
        response = generate_mock_response(question, documents)
        print(f"\n🤖 Generated Response:")
        print(response)
        
        # Step 3: Show citations
        print(f"\n📖 Citations:")
        for doc in documents:
            print(f"  • {doc['title']} - {doc['authors']} ({doc['year']})")
            if doc['url']:
                print(f"    URL: {doc['url']}")
        
        print("\n" + "="*50)

def show_api_structure():
    """Show the API structure and endpoints."""
    
    print("\n🌐 API Endpoints Available:")
    print("=" * 50)
    
    endpoints = [
        ("GET", "/", "Root health check"),
        ("GET", "/healthz", "Detailed health status"),
        ("POST", "/ask", "Main RAG question endpoint"),
        ("GET", "/index/status", "Document index statistics"),
        ("GET", "/docs", "Interactive API documentation")
    ]
    
    for method, endpoint, description in endpoints:
        print(f"{method:6} {endpoint:20} - {description}")
    
    print("\n📋 Example API Request:")
    print("=" * 50)
    
    example_request = {
        "question": "What is LIGO and how does it detect gravitational waves?",
        "top_k": 3,
        "max_tokens": 500
    }
    
    print("POST /ask")
    print("Content-Type: application/json")
    print()
    print(json.dumps(example_request, indent=2))
    
    print("\n📋 Example API Response:")
    print("=" * 50)
    
    example_response = {
        "answer": "LIGO (Laser Interferometer Gravitational-Wave Observatory) is a large-scale physics experiment designed to detect cosmic gravitational waves...",
        "citations": [
            {
                "title": "Introduction to LIGO",
                "authors": "LIGO Scientific Collaboration",
                "url": "https://www.ligo.org/science.php",
                "year": 2023,
                "source": "LIGO Documentation"
            }
        ],
        "sources_used": 2,
        "confidence": "high"
    }
    
    print(json.dumps(example_response, indent=2))

def show_project_structure():
    """Show the project structure."""
    
    print("\n📁 Project Structure:")
    print("=" * 50)
    
    structure = """
GRAVITYchat/
├── app/                    # FastAPI application
│   ├── main.py            # Main API endpoints (simplified)
│   ├── schemas.py         # Pydantic data models
│   ├── config.py          # Configuration management
│   ├── retriever.py       # Azure AI Search client
│   ├── generator.py       # Azure OpenAI client
│   └── prompts.py         # RAG prompt management
├── ingestion/             # Data ingestion
│   └── zotero_sync.py     # Zotero integration
├── tests/                 # Test suite
│   └── test_basic.py      # Basic functionality tests
├── infra/                 # Infrastructure (Terraform/Bicep)
├── requirements.txt       # Python dependencies
├── Dockerfile            # Container configuration
├── run_demo.py           # Demo startup script
└── test_demo.py          # This test script
"""
    
    print(structure)

def main():
    """Main demo function."""
    
    print("🎯 GRAVITYchat RAG System - Complete Demo")
    print("🔬 LIGO/Gravity Spy Citizen Science Chatbot")
    print("🚀 Built with FastAPI + Azure Services")
    print()
    
    # Show project structure
    show_project_structure()
    
    # Test RAG functionality
    test_rag_functionality()
    
    # Show API structure
    show_api_structure()
    
    print("\n✅ Demo Complete!")
    print("\n🚀 To run the full API server:")
    print("   python app/main.py")
    print("\n📖 To view interactive API docs:")
    print("   http://localhost:8000/docs")
    print("\n🔧 To configure Azure services:")
    print("   Copy env.example to .env and add your Azure credentials")

if __name__ == "__main__":
    main()
