# GRAVITYchat 

A RAG (Retrieval-Augmented Generation) chatbot for LIGO/Gravity Spy citizen scientists, built with Azure services and privacy-first design.

## 🌟 What It Does

GRAVITYchat helps citizen scientists get accurate, cited answers about:
- **LIGO Technology**: Gravitational wave detectors, interferometry, sensitivity
- **Gravity Spy**: Citizen science project, glitch classification, spectrograms  
- **aLOGs**: LIGO Online Glitch Database, detector characterization
- **Scientific Results**: Gravitational wave detections, astrophysics

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Citizen       │    │   GRAVITYchat    │    │   Azure AI      │
│   Scientist     │───▶│   FastAPI App    │───▶│   Search        │
│   Question      │    │                  │    │   (Vector DB)   │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌──────────────────┐
                       │   Azure OpenAI   │
                       │   (GPT-4)        │
                       └──────────────────┘
```

##  Quick Start

### Prerequisites
- Python 3.12+
- Azure account (for production)
- Zotero API access (optional)

### Installation

1. **Clone and setup**:
```bash
git clone <your-repo>
cd GRAVITYchat
pip install -r requirements.txt
```

2. **Run with mock data** (for demonstration):
```bash
python run_demo.py
```

3. **Access the API**:
- API Docs: http://localhost:8000/docs
- Health Check: http://localhost:8000/healthz
- Ask a question: POST to http://localhost:8000/ask

### Example API Usage

```bash
curl -X POST "http://localhost:8000/ask" \
     -H "Content-Type: application/json" \
     -d '{
       "question": "What is LIGO and how does it detect gravitational waves?",
       "top_k": 3,
       "max_tokens": 500
     }'
```

##  Configuration

### Environment Variables

Copy `env.example` to `.env` and configure:

```bash
# Azure OpenAI
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_KEY=your-key
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4

# Azure AI Search  
AZURE_SEARCH_ENDPOINT=https://your-search.search.windows.net
AZURE_SEARCH_API_KEY=your-search-key
AZURE_SEARCH_INDEX_NAME=gravitychat-docs

# Zotero (optional)
ZOTERO_API_KEY=your-zotero-key
ZOTERO_GROUP_ID=your-group-id
```

##  Project Structure

```
GRAVITYchat/
├── app/                    # FastAPI application
│   ├── main.py            # Main API endpoints
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
└── run_demo.py           # Demo startup script
```

##  Privacy & Security

- **No data logging**: Azure OpenAI configured with data logging disabled
- **Minimal retention**: Session data retained for max 7 days
- **Private endpoints**: All Azure services use private networking
- **RBAC**: Role-based access control for all components
- **Key Vault**: Secure credential management



## 🔄 Data Flow

1. **Question**: Citizen scientist asks a question
2. **Retrieval**: System searches Azure AI Search for relevant documents
3. **Context**: Retrieved documents are formatted with metadata
4. **Generation**: Azure OpenAI generates answer using context
5. **Response**: Answer returned with citations and confidence score



- LIGO Scientific Collaboration
- Gravity Spy Team
- Zooniverse Platform
- Microsoft Azure AI Services
