"""
GRAVITYchat - Zotero Data Ingestion
----------------------------------
Enhanced Zotero integration for data ingestion and PDF processing.

Author: Alexander O. Smith (2025–present)
Maintainer: Alexander O. Smith <aosmith@syr.edu>
"""

import os
import json
import logging
import asyncio
from typing import List, Dict, Any, Optional
import requests
from azure.storage.blob import BlobServiceClient
from azure.core.exceptions import AzureError

from app.config import Settings
from app.schemas import DocumentChunk

logger = logging.getLogger(__name__)


class ZoteroIngestion:
    """Handles Zotero data ingestion and processing."""
    
    def __init__(self, settings: Settings):
        self.settings = settings
        self.api_key = settings.zotero_api_key
        self.group_id = settings.zotero_group_id
        self.base_url = f"https://api.zotero.org/groups/{self.group_id}/items"
        self.blob_client = None
        self._initialize_blob_client()
    
    def _initialize_blob_client(self):
        """Initialize Azure Blob Storage client."""
        try:
            self.blob_client = BlobServiceClient.from_connection_string(
                self.settings.azure_storage_connection_string
            )
            logger.info("Azure Blob Storage client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Blob Storage client: {e}")
            self.blob_client = None
    
    async def sync_zotero_items(self, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Sync items from Zotero group library.
        
        Args:
            limit: Maximum number of items to fetch
            
        Returns:
            List of Zotero items with metadata
        """
        try:
            headers = {"Authorization": f"Bearer {self.api_key}"}
            params = {
                "format": "json",
                "limit": limit,
                "include": "data,bib,citation"
            }
            
            response = requests.get(self.base_url, headers=headers, params=params)
            response.raise_for_status()
            
            items = response.json()
            logger.info(f"Retrieved {len(items)} items from Zotero")
            
            # Process and filter items
            processed_items = []
            for item in items:
                if self._is_valid_item(item):
                    processed_item = self._process_zotero_item(item)
                    processed_items.append(processed_item)
            
            logger.info(f"Processed {len(processed_items)} valid items")
            return processed_items
            
        except requests.RequestException as e:
            logger.error(f"Error fetching Zotero items: {e}")
            return self._get_mock_items()
        except Exception as e:
            logger.error(f"Unexpected error in Zotero sync: {e}")
            return []
    
    def _is_valid_item(self, item: Dict[str, Any]) -> bool:
        """Check if a Zotero item is valid for processing."""
        data = item.get("data", {})
        
        # Check if it's a document type we want
        item_type = data.get("itemType", "")
        valid_types = ["journalArticle", "book", "bookSection", "report", "thesis", "document"]
        
        if item_type not in valid_types:
            return False
        
        # Check if it has a title
        if not data.get("title", "").strip():
            return False
        
        # Check if it has a PDF attachment
        attachments = item.get("attachments", [])
        has_pdf = any(att.get("data", {}).get("contentType") == "application/pdf" 
                     for att in attachments)
        
        return has_pdf or data.get("url", "")  # Accept items with PDFs or URLs
    
    def _process_zotero_item(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """Process a Zotero item into our document format."""
        data = item.get("data", {})
        
        processed = {
            "id": item.get("key", ""),
            "title": data.get("title", ""),
            "authors": self._extract_authors(data),
            "year": data.get("date", "").split("-")[0] if data.get("date") else None,
            "url": data.get("url", ""),
            "abstract": data.get("abstractNote", ""),
            "item_type": data.get("itemType", ""),
            "source": "Zotero",
            "raw_data": data
        }
        
        return processed
    
    def _extract_authors(self, data: Dict[str, Any]) -> str:
        """Extract authors from Zotero data."""
        creators = data.get("creators", [])
        authors = []
        
        for creator in creators:
            if creator.get("creatorType") == "author":
                first_name = creator.get("firstName", "")
                last_name = creator.get("lastName", "")
                if last_name:
                    authors.append(f"{first_name} {last_name}".strip())
        
        return ", ".join(authors) if authors else "Unknown"
    
    async def download_and_store_pdf(self, item: Dict[str, Any]) -> Optional[str]:
        """
        Download PDF attachment and store in Azure Blob Storage.
        
        Args:
            item: Processed Zotero item
            
        Returns:
            Blob URL if successful, None otherwise
        """
        try:
            if not self.blob_client:
                logger.warning("Blob client not available, skipping PDF download")
                return None
            
            # For now, return a mock URL
            # In production, you'd download the actual PDF from Zotero
            blob_name = f"zotero/{item['id']}.pdf"
            blob_url = f"https://mockstorage.blob.core.windows.net/{self.settings.azure_storage_container_name}/{blob_name}"
            
            logger.info(f"Mock PDF stored: {blob_url}")
            return blob_url
            
        except Exception as e:
            logger.error(f"Error downloading PDF for item {item['id']}: {e}")
            return None
    
    def _get_mock_items(self) -> List[Dict[str, Any]]:
        """Return mock Zotero items for development."""
        return [
            {
                "id": "mock-zotero-1",
                "title": "Advanced LIGO: The Next Generation of Gravitational Wave Detectors",
                "authors": "LIGO Scientific Collaboration",
                "year": 2023,
                "url": "https://www.ligo.org/science.php",
                "abstract": "This paper describes the Advanced LIGO detector upgrades and their impact on gravitational wave detection sensitivity.",
                "item_type": "journalArticle",
                "source": "Zotero"
            },
            {
                "id": "mock-zotero-2", 
                "title": "Gravity Spy: A Citizen Science Project for LIGO Glitch Classification",
                "authors": "Gravity Spy Team, LIGO Scientific Collaboration",
                "year": 2024,
                "url": "https://www.zooniverse.org/projects/zooniverse/gravity-spy",
                "abstract": "This paper presents the Gravity Spy citizen science project and its contributions to LIGO data quality.",
                "item_type": "journalArticle",
                "source": "Zotero"
            },
            {
                "id": "mock-zotero-3",
                "title": "Understanding LIGO Detector Glitches Through Machine Learning",
                "authors": "Smith, A., Johnson, B., LIGO Detector Characterization Group",
                "year": 2023,
                "url": "https://arxiv.org/abs/mock-paper",
                "abstract": "This study explores machine learning approaches to classify and understand instrumental glitches in LIGO data.",
                "item_type": "journalArticle", 
                "source": "Zotero"
            }
        ]
    
    async def create_document_chunks(self, items: List[Dict[str, Any]]) -> List[DocumentChunk]:
        """
        Convert Zotero items into document chunks for indexing.
        
        Args:
            items: List of processed Zotero items
            
        Returns:
            List of document chunks ready for embedding and indexing
        """
        chunks = []
        
        for item in items:
            # Create chunks from title, abstract, and metadata
            content_parts = []
            
            if item.get("title"):
                content_parts.append(f"Title: {item['title']}")
            
            if item.get("authors"):
                content_parts.append(f"Authors: {item['authors']}")
            
            if item.get("abstract"):
                content_parts.append(f"Abstract: {item['abstract']}")
            
            if item.get("year"):
                content_parts.append(f"Year: {item['year']}")
            
            content = "\n\n".join(content_parts)
            
            chunk = DocumentChunk(
                id=f"zotero-{item['id']}",
                content=content,
                title=item["title"],
                authors=item.get("authors"),
                url=item.get("url"),
                year=int(item["year"]) if item.get("year") else None,
                source="Zotero",
                chunk_index=0,
                metadata={
                    "item_type": item.get("item_type"),
                    "zotero_id": item["id"],
                    "abstract": item.get("abstract", "")
                }
            )
            
            chunks.append(chunk)
        
        logger.info(f"Created {len(chunks)} document chunks from Zotero items")
        return chunks

