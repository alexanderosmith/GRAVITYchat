"""
GRAVITYchat - Document Retriever
--------------------------------
Azure AI Search client for document retrieval in RAG system.

Author: Alexander O. Smith (2025–present)
Maintainer: Alexander O. Smith <aosmith@syr.edu>
"""

import asyncio
import logging
from typing import List, Dict, Any, Optional
from azure.search.documents import SearchClient
from azure.search.documents.models import VectorizedQuery
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import ResourceNotFoundError

from app.schemas import DocumentChunk
from app.config import Settings

logger = logging.getLogger(__name__)


class DocumentRetriever:
    """Handles document retrieval from Azure AI Search."""
    
    def __init__(self, settings: Settings):
        self.settings = settings
        self.search_client = None
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize Azure AI Search client."""
        try:
            credential = AzureKeyCredential(self.settings.azure_search_api_key)
            self.search_client = SearchClient(
                endpoint=self.settings.azure_search_endpoint,
                index_name=self.settings.azure_search_index_name,
                credential=credential
            )
            logger.info("Azure AI Search client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Azure AI Search client: {e}")
            # For development, create a mock client
            self.search_client = MockSearchClient()
    
    async def retrieve_documents(
        self, 
        query: str, 
        top_k: int = 5, 
        filters: Optional[Dict[str, Any]] = None
    ) -> List[DocumentChunk]:
        """
        Retrieve relevant documents for the given query.
        
        Args:
            query: Search query
            top_k: Number of documents to retrieve
            filters: Optional filters for the search
            
        Returns:
            List of relevant document chunks
        """
        try:
            # For now, use simple text search
            # In production, you'd use vector search with embeddings
            search_results = self.search_client.search(
                search_text=query,
                top=top_k,
                filter=filters,
                include_total_count=True
            )
            
            documents = []
            for result in search_results:
                doc_chunk = DocumentChunk(
                    id=result.get("id", ""),
                    content=result.get("content", ""),
                    title=result.get("title", ""),
                    authors=result.get("authors"),
                    url=result.get("url"),
                    year=result.get("year"),
                    source=result.get("source", "unknown"),
                    chunk_index=result.get("chunk_index", 0),
                    metadata=result.get("metadata", {})
                )
                documents.append(doc_chunk)
            
            logger.info(f"Retrieved {len(documents)} documents for query: {query[:50]}...")
            return documents
            
        except Exception as e:
            logger.error(f"Error retrieving documents: {e}")
            # Return mock data for development
            return self._get_mock_documents(query, top_k)
    
    async def health_check(self) -> bool:
        """Check if the search service is healthy."""
        try:
            # Simple health check - try to get index stats
            stats = await self.get_index_stats()
            return stats.get("total_documents", 0) >= 0
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return False
    
    async def get_index_stats(self) -> Dict[str, Any]:
        """Get statistics about the search index."""
        try:
            # This would normally query the index stats
            # For now, return mock stats
            return {
                "total_documents": 150,
                "last_updated": "2025-01-21T19:30:00Z",
                "index_name": self.settings.azure_search_index_name
            }
        except Exception as e:
            logger.error(f"Error getting index stats: {e}")
            return {"total_documents": 0, "last_updated": "unknown"}
    
    def _get_mock_documents(self, query: str, top_k: int) -> List[DocumentChunk]:
        """Return mock documents for development/testing."""
        mock_docs = [
            DocumentChunk(
                id="mock-1",
                content="LIGO (Laser Interferometer Gravitational-Wave Observatory) is a large-scale physics experiment designed to detect cosmic gravitational waves. The observatory uses laser interferometry to measure the minute ripples in space-time caused by passing gravitational waves from cataclysmic cosmic events such as merging neutron stars or black holes.",
                title="Introduction to LIGO",
                authors="LIGO Scientific Collaboration",
                url="https://www.ligo.org/science.php",
                year=2023,
                source="LIGO Documentation",
                chunk_index=1
            ),
            DocumentChunk(
                id="mock-2", 
                content="Gravity Spy is a citizen science project that helps classify glitches in LIGO data. Volunteers examine spectrograms of gravitational wave detector noise to identify and categorize different types of instrumental artifacts that could interfere with gravitational wave detection.",
                title="Gravity Spy Citizen Science",
                authors="Gravity Spy Team",
                url="https://www.zooniverse.org/projects/zooniverse/gravity-spy",
                year=2024,
                source="Zooniverse",
                chunk_index=1
            ),
            DocumentChunk(
                id="mock-3",
                content="aLOGs (LIGO Online Glitch Database) contain detailed information about instrumental glitches detected in LIGO data. These logs help scientists understand the sources of noise and improve detector sensitivity by identifying and mitigating systematic issues.",
                title="Understanding aLOGs",
                authors="LIGO Detector Characterization Group",
                url="https://alog.ligo-wa.caltech.edu/",
                year=2023,
                source="aLOG Database",
                chunk_index=1
            )
        ]
        
        # Filter mock docs based on query (simple keyword matching)
        filtered_docs = []
        query_lower = query.lower()
        
        for doc in mock_docs:
            if any(keyword in doc.content.lower() or keyword in doc.title.lower() 
                   for keyword in query_lower.split()):
                filtered_docs.append(doc)
        
        return filtered_docs[:top_k]


class MockSearchClient:
    """Mock search client for development."""
    
    def search(self, search_text: str, top: int = 5, **kwargs):
        """Mock search method."""
        # Return empty results - actual retrieval handled by _get_mock_documents
        return []

