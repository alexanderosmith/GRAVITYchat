"""
GRAVITYchat - Configuration Management
-------------------------------------
Settings and configuration for Azure services and application.

Author: Alexander O. Smith (2025–present)
Maintainer: Alexander O. Smith <aosmith@syr.edu>
"""

import os
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Azure OpenAI Configuration
    azure_openai_endpoint: str = Field(..., env="AZURE_OPENAI_ENDPOINT")
    azure_openai_api_key: str = Field(..., env="AZURE_OPENAI_API_KEY")
    azure_openai_deployment_name: str = Field("gpt-4", env="AZURE_OPENAI_DEPLOYMENT_NAME")
    azure_openai_embedding_deployment: str = Field("text-embedding-ada-002", env="AZURE_OPENAI_EMBEDDING_DEPLOYMENT")
    
    # Azure AI Search Configuration
    azure_search_endpoint: str = Field(..., env="AZURE_SEARCH_ENDPOINT")
    azure_search_api_key: str = Field(..., env="AZURE_SEARCH_API_KEY")
    azure_search_index_name: str = Field("gravitychat-docs", env="AZURE_SEARCH_INDEX_NAME")
    
    # Azure Blob Storage Configuration
    azure_storage_connection_string: str = Field(..., env="AZURE_STORAGE_CONNECTION_STRING")
    azure_storage_container_name: str = Field("gravitychat-documents", env="AZURE_STORAGE_CONTAINER_NAME")
    
    # Zotero Configuration
    zotero_api_key: Optional[str] = Field(None, env="ZOTERO_API_KEY")
    zotero_group_id: Optional[str] = Field(None, env="ZOTERO_GROUP_ID")
    
    # Application Configuration
    app_name: str = Field("GRAVITYchat", env="APP_NAME")
    debug: bool = Field(False, env="DEBUG")
    log_level: str = Field("INFO", env="LOG_LEVEL")
    
    # RAG Configuration
    max_retrieval_docs: int = Field(10, env="MAX_RETRIEVAL_DOCS")
    chunk_size: int = Field(1000, env="CHUNK_SIZE")
    chunk_overlap: int = Field(200, env="CHUNK_OVERLAP")
    
    # Privacy Configuration
    disable_data_logging: bool = Field(True, env="DISABLE_DATA_LOGGING")
    max_session_retention_days: int = Field(7, env="MAX_SESSION_RETENTION_DAYS")
    
    class Config:
        env_file = ".env"
        case_sensitive = False


class MockSettings(Settings):
    """Mock settings for development and testing."""
    
    def __init__(self, **kwargs):
        # Set default mock values
        mock_values = {
            "azure_openai_endpoint": "https://mock-openai.openai.azure.com/",
            "azure_openai_api_key": "mock-key-12345",
            "azure_openai_deployment_name": "gpt-4",
            "azure_openai_embedding_deployment": "text-embedding-ada-002",
            "azure_search_endpoint": "https://mock-search.search.windows.net",
            "azure_search_api_key": "mock-search-key-12345",
            "azure_search_index_name": "gravitychat-docs",
            "azure_storage_connection_string": "DefaultEndpointsProtocol=https;AccountName=mockstorage;AccountKey=mock-key;EndpointSuffix=core.windows.net",
            "azure_storage_container_name": "gravitychat-documents",
            "zotero_api_key": "mock-zotero-key",
            "zotero_group_id": "123456",
            "debug": True,
            "log_level": "DEBUG"
        }
        
        # Override with provided kwargs
        mock_values.update(kwargs)
        super().__init__(**mock_values)


def get_settings() -> Settings:
    """Get application settings, with fallback to mock settings for development."""
    try:
        return Settings()
    except Exception as e:
        print(f"Warning: Could not load settings from environment: {e}")
        print("Using mock settings for development...")
        return MockSettings()
