#!/usr/bin/env python3
"""
GRAVITYchat - Interactive Question Tester
----------------------------------------
Ask your own questions and see the RAG responses.

Author: Alexander O. Smith (2025–present)
Maintainer: Alexander O. Smith <aosmith@syr.edu>
"""

import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from app.main import get_mock_documents, generate_mock_response

def ask_question(question: str):
    """Ask a question and get a RAG response."""
    print(f"\n📝 Your Question: {question}")
    print("-" * 60)
    
    # Step 1: Retrieve relevant documents
    documents = get_mock_documents(question, top_k=3)
    print(f"📚 Found {len(documents)} relevant documents:")
    
    for i, doc in enumerate(documents, 1):
        print(f"  {i}. {doc['title']} ({doc['source']})")
    
    # Step 2: Generate response
    response = generate_mock_response(question, documents)
    print(f"\n🤖 GRAVITYchat Answer:")
    print(response)
    
    # Step 3: Show citations
    print(f"\n📖 Citations Used:")
    for doc in documents:
        print(f"  • {doc['title']} - {doc['authors']} ({doc['year']})")
        if doc['url']:
            print(f"    🔗 {doc['url']}")
    
    print("\n" + "="*60)

def main():
    """Interactive question testing."""
    print("🚀 GRAVITYchat Interactive Question Tester")
    print("🔬 LIGO/Gravity Spy Citizen Science Chatbot")
    print("=" * 60)
    
    # Pre-defined questions you can try
    sample_questions = [
        "What is LIGO?",
        "How does Gravity Spy work?", 
        "What are aLOGs?",
        "Tell me about gravitational wave detection",
        "What causes glitches in LIGO data?",
        "How sensitive is LIGO?",
        "What is interferometry?",
        "How do citizen scientists help LIGO?"
    ]
    
    print("\n📋 Sample questions you can try:")
    for i, q in enumerate(sample_questions, 1):
        print(f"  {i}. {q}")
    
    print("\n" + "="*60)
    
    while True:
        print("\n🎯 What would you like to do?")
        print("1. Ask a sample question")
        print("2. Ask your own question")
        print("3. Exit")
        
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == "1":
            print("\n📋 Sample Questions:")
            for i, q in enumerate(sample_questions, 1):
                print(f"  {i}. {q}")
            
            try:
                q_num = int(input(f"\nEnter question number (1-{len(sample_questions)}): "))
                if 1 <= q_num <= len(sample_questions):
                    ask_question(sample_questions[q_num - 1])
                else:
                    print("❌ Invalid question number!")
            except ValueError:
                print("❌ Please enter a valid number!")
                
        elif choice == "2":
            question = input("\n❓ Enter your question: ").strip()
            if question:
                ask_question(question)
            else:
                print("❌ Please enter a question!")
                
        elif choice == "3":
            print("\n👋 Thanks for using GRAVITYchat!")
            break
            
        else:
            print("❌ Invalid choice! Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()
