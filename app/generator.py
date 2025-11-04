"""
GRAVITYchat - Response Generator
-------------------------------
Azure OpenAI client for generating responses in RAG system.

Author: Alexander O. Smith (2025–present)
Maintainer: Alexander O. Smith <aosmith@syr.edu>
"""

import logging
from typing import Optional
from azure.openai import AzureOpenAI
from azure.core.exceptions import AzureError

from app.config import Settings

logger = logging.getLogger(__name__)


class ResponseGenerator:
    """Handles response generation using Azure OpenAI."""
    
    def __init__(self, settings: Settings):
        self.settings = settings
        self.client = None
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize Azure OpenAI client."""
        try:
            self.client = AzureOpenAI(
                azure_endpoint=self.settings.azure_openai_endpoint,
                api_key=self.settings.azure_openai_api_key,
                api_version="2024-02-15-preview"
            )
            logger.info("Azure OpenAI client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Azure OpenAI client: {e}")
            self.client = None
    
    async def generate_response(
        self, 
        user_prompt: str, 
        system_prompt: str, 
        max_tokens: int = 500
    ) -> str:
        """
        Generate a response using Azure OpenAI.
        
        Args:
            user_prompt: The user's question with context
            system_prompt: System instructions for the model
            max_tokens: Maximum tokens in the response
            
        Returns:
            Generated response text
        """
        try:
            if not self.client:
                return self._get_mock_response(user_prompt)
            
            response = self.client.chat.completions.create(
                model=self.settings.azure_openai_deployment_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=max_tokens,
                temperature=0.7,
                top_p=0.9,
                frequency_penalty=0.0,
                presence_penalty=0.0
            )
            
            generated_text = response.choices[0].message.content
            logger.info(f"Generated response with {len(generated_text)} characters")
            return generated_text
            
        except AzureError as e:
            logger.error(f"Azure OpenAI error: {e}")
            return self._get_mock_response(user_prompt)
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return self._get_mock_response(user_prompt)
    
    async def health_check(self) -> bool:
        """Check if the OpenAI service is healthy."""
        try:
            if not self.client:
                return False
            
            # Simple health check - try a minimal request
            response = self.client.chat.completions.create(
                model=self.settings.azure_openai_deployment_name,
                messages=[{"role": "user", "content": "Hello"}],
                max_tokens=10
            )
            return len(response.choices[0].message.content) > 0
        except Exception as e:
            logger.error(f"OpenAI health check failed: {e}")
            return False
    
    def _get_mock_response(self, user_prompt: str) -> str:
        """Return a mock response for development/testing."""
        # Extract the question from the user prompt
        question = user_prompt.split("Question:")[1].split("\n")[0].strip() if "Question:" in user_prompt else "your question"
        
        mock_responses = {
            "ligo": "LIGO (Laser Interferometer Gravitational-Wave Observatory) is a large-scale physics experiment designed to detect cosmic gravitational waves. The observatory uses laser interferometry to measure minute ripples in space-time caused by passing gravitational waves from cataclysmic cosmic events such as merging neutron stars or black holes.",
            "gravity spy": "Gravity Spy is a citizen science project that helps classify glitches in LIGO data. Volunteers examine spectrograms of gravitational wave detector noise to identify and categorize different types of instrumental artifacts that could interfere with gravitational wave detection.",
            "alog": "aLOGs (LIGO Online Glitch Database) contain detailed information about instrumental glitches detected in LIGO data. These logs help scientists understand the sources of noise and improve detector sensitivity by identifying and mitigating systematic issues.",
            "glitch": "Glitches in LIGO data are instrumental artifacts that can interfere with gravitational wave detection. They can be caused by various sources including environmental factors, detector hardware issues, or external disturbances. Gravity Spy helps classify these glitches to improve data quality."
        }
        
        question_lower = question.lower()
        for keyword, response in mock_responses.items():
            if keyword in question_lower:
                return f"Based on the LIGO/Gravity Spy knowledge base, {response}"
        
        return f"Thank you for your question about '{question}'. Based on the available LIGO and Gravity Spy documentation, I can provide information about gravitational wave detection, detector technology, and citizen science opportunities. Could you please be more specific about what aspect you'd like to learn about?"

