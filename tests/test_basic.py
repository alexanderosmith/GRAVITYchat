"""
GRAVITYchat - Basic Tests
------------------------
Simple tests for the RAG chatbot system.

Author: Alexander O. Smith (2025–present)
Maintainer: Alexander O. Smith <aosmith@syr.edu>
"""

import pytest
import asyncio
from app.config import MockSettings
from app.retriever import DocumentRetriever
from app.generator import ResponseGenerator
from app.prompts import RAGPromptManager
from app.schemas import DocumentChunk


@pytest.fixture
def mock_settings():
    """Create mock settings for testing."""
    return MockSettings()


@pytest.fixture
def sample_documents():
    """Create sample documents for testing."""
    return [
        DocumentChunk(
            id="test-1",
            content="LIGO is a gravitational wave detector.",
            title="LIGO Overview",
            authors="LIGO Collaboration",
            url="https://www.ligo.org",
            year=2023,
            source="LIGO Documentation",
            chunk_index=1
        ),
        DocumentChunk(
            id="test-2",
            content="Gravity Spy helps classify glitches in LIGO data.",
            title="Gravity Spy Project",
            authors="Gravity Spy Team",
            url="https://www.zooniverse.org/projects/zooniverse/gravity-spy",
            year=2024,
            source="Zooniverse",
            chunk_index=1
        )
    ]


def test_document_retriever_initialization(mock_settings):
    """Test that DocumentRetriever initializes correctly."""
    retriever = DocumentRetriever(mock_settings)
    assert retriever.settings == mock_settings
    assert retriever.search_client is not None


def test_response_generator_initialization(mock_settings):
    """Test that ResponseGenerator initializes correctly."""
    generator = ResponseGenerator(mock_settings)
    assert generator.settings == mock_settings


def test_prompt_manager_creation():
    """Test that RAGPromptManager works correctly."""
    manager = RAGPromptManager()
    assert manager.DATA_DELIMITER == "~~~"


@pytest.mark.asyncio
async def test_document_retrieval(mock_settings):
    """Test document retrieval functionality."""
    retriever = DocumentRetriever(mock_settings)
    documents = await retriever.retrieve_documents("LIGO gravitational waves", top_k=3)
    
    assert isinstance(documents, list)
    assert len(documents) > 0
    assert all(isinstance(doc, DocumentChunk) for doc in documents)


@pytest.mark.asyncio
async def test_response_generation(mock_settings):
    """Test response generation functionality."""
    generator = ResponseGenerator(mock_settings)
    
    user_prompt = "Question: What is LIGO?\n\nContext: LIGO is a gravitational wave detector."
    system_prompt = "You are a helpful assistant."
    
    response = await generator.generate_response(user_prompt, system_prompt, max_tokens=100)
    
    assert isinstance(response, str)
    assert len(response) > 0


def test_prompt_creation(sample_documents):
    """Test prompt creation with retrieved documents."""
    manager = RAGPromptManager()
    question = "What is LIGO?"
    
    user_prompt, system_prompt = manager.create_rag_prompts(question, sample_documents)
    
    assert isinstance(user_prompt, str)
    assert isinstance(system_prompt, str)
    assert question in user_prompt
    assert "LIGO" in user_prompt
    assert "citizen scientists" in system_prompt


def test_citation_extraction(sample_documents):
    """Test citation extraction from responses."""
    manager = RAGPromptManager()
    response = "LIGO is a gravitational wave detector as mentioned in the LIGO Overview document."
    
    citations = manager.extract_citations(response, sample_documents)
    
    assert isinstance(citations, list)
    assert len(citations) > 0
    assert citations[0]["title"] == "LIGO Overview"

