#!/usr/bin/env python3
"""
GRAVITYchat - Quick Question Test
-------------------------------
Test a single question quickly from command line.

Usage: python quick_test.py "Your question here"
"""

import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from app.main import get_mock_documents, generate_mock_response

def quick_test(question: str):
    """Quick test of a single question."""
    print(f"🚀 GRAVITYchat Quick Test")
    print(f"❓ Question: {question}")
    print("=" * 60)
    
    # Get documents and response
    documents = get_mock_documents(question, top_k=3)
    response = generate_mock_response(question, documents)
    
    print(f"📚 Found {len(documents)} relevant documents")
    print(f"\n🤖 Answer:\n{response}")
    
    print(f"\n📖 Citations:")
    for doc in documents:
        print(f"  • {doc['title']} - {doc['authors']} ({doc['year']})")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        question = " ".join(sys.argv[1:])
        quick_test(question)
    else:
        print("Usage: python quick_test.py 'Your question here'")
        print("\nExample: python quick_test.py 'What is LIGO?'")
