"""
GRAVITYchat - Pydantic Data Models
----------------------------------
Data models for API requests and responses.

Author: Alexander O. Smith (2025–present)
Maintainer: Alexander O. Smith <aosmith@syr.edu>
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """Request model for chat questions."""
    question: str = Field(..., description="The question from the citizen scientist", min_length=1, max_length=1000)
    top_k: Optional[int] = Field(5, description="Number of documents to retrieve", ge=1, le=20)
    max_tokens: Optional[int] = Field(500, description="Maximum tokens in response", ge=100, le=2000)
    filters: Optional[Dict[str, Any]] = Field(None, description="Filters for document retrieval")


class Citation(BaseModel):
    """Citation model for referenced documents."""
    title: str = Field(..., description="Title of the referenced document")
    authors: Optional[str] = Field(None, description="Authors of the document")
    url: Optional[str] = Field(None, description="URL to the document")
    year: Optional[int] = Field(None, description="Publication year")
    source: str = Field(..., description="Source type (Zotero, aLOG, etc.)")
    relevance_score: Optional[float] = Field(None, description="Relevance score from retrieval")


class ChatResponse(BaseModel):
    """Response model for chat answers."""
    answer: str = Field(..., description="The generated answer")
    citations: List[Citation] = Field(..., description="List of citations used")
    sources_used: int = Field(..., description="Number of sources used")
    confidence: str = Field(..., description="Confidence level: low, medium, high")


class HealthResponse(BaseModel):
    """Health check response model."""
    status: str = Field(..., description="Service status")
    message: str = Field(..., description="Status message")
    version: str = Field(..., description="API version")


class DocumentChunk(BaseModel):
    """Model for document chunks in the knowledge base."""
    id: str = Field(..., description="Unique identifier for the chunk")
    content: str = Field(..., description="Text content of the chunk")
    title: str = Field(..., description="Title of the source document")
    authors: Optional[str] = Field(None, description="Authors of the document")
    url: Optional[str] = Field(None, description="URL to the document")
    year: Optional[int] = Field(None, description="Publication year")
    source: str = Field(..., description="Source type")
    chunk_index: int = Field(..., description="Index of this chunk in the document")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")


class RetrievalResult(BaseModel):
    """Model for document retrieval results."""
    documents: List[DocumentChunk] = Field(..., description="Retrieved document chunks")
    total_found: int = Field(..., description="Total number of documents found")
    query_time_ms: float = Field(..., description="Query execution time in milliseconds")
