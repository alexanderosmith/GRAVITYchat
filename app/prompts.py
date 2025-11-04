"""
GRAVITYchat - RAG Prompt Manager
--------------------------------
Enhanced prompt system for RAG with citation formatting and context injection.

Author: Alexander O. Smith (2025–present)
Maintainer: Alexander O. Smith <aosmith@syr.edu>
"""

import re
from typing import List, Tuple
from app.schemas import DocumentChunk


class RAGPromptManager:
    """Manages prompt creation and citation extraction for RAG system."""
    
    DATA_DELIMITER = "~~~"
    
    def create_rag_prompts(self, question: str, retrieved_docs: List[DocumentChunk]) -> Tuple[str, str]:
        """
        Create user and system prompts for RAG with retrieved context.
        
        Args:
            question: User's question
            retrieved_docs: Retrieved document chunks
            
        Returns:
            Tuple of (user_prompt, system_prompt)
        """
        # Format retrieved documents
        context_text = self._format_retrieved_docs(retrieved_docs)
        
        # Create user prompt with context
        user_prompt = f"""
Question: {question}

Context from LIGO/Gravity Spy knowledge base:
{DATA_DELIMITER}
{context_text}
{DATA_DELIMITER}

Please answer the question using ONLY the provided context. If the context doesn't contain enough information to answer the question, please say so clearly.
"""
        
        # Create system prompt
        system_prompt = f"""
You are a LIGO scientist tasked with responding to citizen scientists with factual,
accessible responses. These might be any questions about LIGO technology, scientific
results, or questions about citizen scientist tasks related to Zooniverse or Gravity Spy.
Your goal is to help citizen scientists with factual responses to their questions that
will enable them to interpret Gravity Spy Glitches and their origins. Use clear, simple
language and avoid technical jargon to ensure accessibility. Translate acronyms to full
words based upon LIGO Abbreviations and Acronyms whenever possible.

IMPORTANT INSTRUCTIONS:
1. Answer ONLY using the provided context between the {DATA_DELIMITER} markers
2. Always cite your sources using the format [text](url) for URLs
3. If you reference a document, include the title and authors
4. Use phrases like "according to" or "as mentioned in" when citing
5. If the context doesn't contain enough information, clearly state this
6. Expand acronyms when possible (e.g., LIGO = Laser Interferometer Gravitational-Wave Observatory)
7. Maintain a neutral, informative tone
8. Use "some" rather than "all" when referring to data to avoid extremes

When generating summaries, format all URLs without hashtags following this format:
[template_link_text](template_link_url).

Structure responses logically, highlighting common or recent issues, and
maintain a neutral, informative tone. Phrase interpretations with rhetoric like
"an" (as opposed to "the") and "some" as opposed to "all" when referring to the
data. This will avoid extremes when there is a lack of clarity.
"""
        
        return user_prompt.strip(), system_prompt.strip()
    
    def _format_retrieved_docs(self, docs: List[DocumentChunk]) -> str:
        """Format retrieved documents for inclusion in prompt."""
        formatted_docs = []
        
        for i, doc in enumerate(docs, 1):
            doc_text = f"""
Document {i}:
Title: {doc.title}
Authors: {doc.authors or 'Unknown'}
Source: {doc.source}
Year: {doc.year or 'Unknown'}
URL: {doc.url or 'Not available'}

Content:
{doc.content}
"""
            formatted_docs.append(doc_text.strip())
        
        return "\n\n".join(formatted_docs)
    
    def extract_citations(self, response: str, retrieved_docs: List[DocumentChunk]) -> List[dict]:
        """Extract citations from the generated response."""
        citations = []
        
        # Simple citation extraction - look for document references
        for doc in retrieved_docs:
            if doc.title.lower() in response.lower():
                citation = {
                    "title": doc.title,
                    "authors": doc.authors,
                    "url": doc.url,
                    "year": doc.year,
                    "source": doc.source,
                    "relevance_score": getattr(doc, 'score', None)
                }
                citations.append(citation)
        
        return citations

