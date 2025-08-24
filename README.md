# Mini-RAG (Retrieval-Augmented Generation) Application

A lightweight, scalable RAG application built with FastAPI that enables document upload, processing, vector indexing, and intelligent semantic search using LangChain, MongoDB, and Qdrant. This project demonstrates a complete RAG pipeline from document ingestion to vector storage and semantic search.

## Features

- **Document Upload & Processing**: Upload PDF and text documents with automatic validation
- **Asset Management**: Track uploaded files with metadata (size, type, project association)
- **Text Chunking**: Intelligent document splitting using LangChain's RecursiveCharacterTextSplitter
- **Vector Database Integration**: Store and search document embeddings using Qdrant vector database
- **Semantic Search**: Find relevant document chunks using vector similarity search
- **Multiple LLM Provider Support**: Support for OpenAI and Cohere for embeddings and text generation
- **Project Management**: Organize documents into projects for better management
- **Chunk Reset Functionality**: Option to reset/replace existing chunks when reprocessing
- **MongoDB Integration**: Persistent storage for documents, chunks, and metadata with ObjectId support
- **RESTful API**: Clean API endpoints for all operations
- **Docker Support**: Easy deployment with Docker Compose
- **File Validation**: Built-in file type and size validation
- **Async Operations**: Full async/await support for better performance

## Tech Stack

- **Backend**: FastAPI (Python 3.8+)
- **Database**: MongoDB with Motor (async driver)
- **Vector Database**: Qdrant for storing and searching document embeddings
- **Document Processing**: LangChain, PyMuPDF
- **LLM Providers**: OpenAI, Cohere (for embeddings and text generation)
- **Data Validation**: Pydantic v2 with custom ObjectId handling
- **Text Processing**: LangChain RecursiveCharacterTextSplitter
- **Containerization**: Docker & Docker Compose

## Project Structure

```text
mini-rag/
├── Docker/
│   ├── docker-compose.yml      # MongoDB container configuration
│   └── mongodb/               # MongoDB data directory
├── src/
│   ├── main.py               # FastAPI application entry point
│   ├── requirements.txt      # Python dependencies
│   ├── assets/files/         # Uploaded documents storage
│   ├── assets/database/      # Vector database storage (Qdrant)
│   ├── controllers/          # Business logic controllers
│   │   ├── BaseController.py    # Base controller class
│   │   ├── DataController.py    # File upload/validation
│   │   ├── ProcessController.py # Document processing
│   │   ├── ProjectController.py # Project management
│   │   └── NLPController.py     # Vector indexing and search
│   ├── models/              # Data models and schemas
│   │   ├── BaseDataModel.py     # Base model with common functionality
│   │   ├── ProjectModel.py      # Project database operations
│   │   ├── ChunkModel.py        # Document chunk operations
│   │   ├── AssetModel.py        # File asset operations
│   │   ├── fields.py            # Custom field types (PyObjectId)
│   │   ├── db_schemas/          # Pydantic schemas
│   │   │   ├── project.py          # Project schema
│   │   │   ├── data_chunk.py       # Chunk schema
│   │   │   └── asset.py            # Asset schema
│   │   └── enums/               # Enumerations
│   │       ├── AssetTypeEnum.py    # Asset type definitions
│   │       ├── DataBaseEnum.py     # Database collection names
│   │       ├── ProcessingEnum.py   # File processing types
│   │       └── ResponseEnums.py    # API response signals
│   ├── routes/              # API route definitions
│   │   ├── base.py            # Base routes
│   │   ├── data.py            # Data handling routes
│   │   ├── nlp.py             # NLP/Vector search routes
│   │   └── schemas/           # Request/Response schemas
│   │       ├── data.py           # Data processing schemas
│   │       └── nlp.py            # NLP request schemas
│   ├── stores/              # External service integrations
│   │   ├── llm/               # LLM provider implementations
│   │   │   ├── providers/        # OpenAI, Cohere providers
│   │   │   ├── LLMInterface.py   # LLM interface definition
│   │   │   └── LLM_Enums.py      # LLM-related enumerations
│   │   └── vectordb/          # Vector database implementations
│   │       ├── providers/        # Qdrant provider
│   │       ├── VectorDBInterface.py  # Vector DB interface
│   │       └── VectorDBEnums.py      # Vector DB enumerations
│   └── helpers/
│       └── config.py         # Configuration management
```

## Requirements

- **Python**: 3.8 or later
- **Docker**: For MongoDB container
- **LLM API Keys**: OpenAI API Key or Cohere API Key for embeddings and text generation

## Installation & Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd mini-rag
```

### 2. Create Python Virtual Environment

```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On Linux/Mac
source venv/bin/activate
```

### 3. Install Dependencies

```bash
cd src
pip install -r requirements.txt
```

### 4. Environment Configuration

Create a `.env` file in the project root with the following variables:

```env
APP_NAME=Mini-RAG Application
APP_VERSION=1.0.0

FILE_ALLOWED_TYPES=["application/pdf", "text/plain"]
FILE_MAX_SIZE=10
FILE_DEFAULT_CHUNK_SIZE=1000

MONGODB_URL=mongodb://localhost:27007
MONGODB_DATABASE=minirag

# LLM Configuration
GENERATION_BACKEND=COHERE
EMBEDDING_BACKEND=COHERE

OPENAI_API_KEY=your_openai_api_key_here
OPENAI_API_URL=
COHERE_API_KEY=your_cohere_api_key_here

GENERATION_MODEL_ID=command-r
EMBEDDING_MODEL_ID=embed-multilingual-light-v3.0
EMBEDDING_MODEL_SIZE=384

INPUT_DEFAULT_MAX_CHARACTERS=1024
GENERATION_DEFAULT_MAX_TOKENS=200
GENERATION_DEFAULT_TEMPERATURE=0.1

# Vector Database Configuration
VECTOR_DB_BACKEND=QDRANT
VECTOR_DB_PATH=qdrant_db
VECTOR_DB_DISTANCE_METHOD=cosine
```

### 5. Start MongoDB

```bash
cd Docker
docker-compose up -d
```

### 6. Run the Application

```bash
cd src
python main.py
```

Or using uvicorn:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## API Endpoints

### Document Upload

- **POST** `/api/v1/data/upload/{project_id}`
  - Upload PDF or text files to a specific project
  - Automatic file validation and storage
  - Returns asset ID for tracking uploaded files

### Document Processing

- **POST** `/api/v1/data/process/{project_id}`
  - Process uploaded documents into chunks
  - Extract text and create searchable segments
  - Supports chunk reset functionality
  - Configurable chunk size and overlap

### Vector Indexing

- **POST** `/api/v1/nlp/index/push/{project_id}`
  - Index processed document chunks into vector database
  - Generate embeddings for semantic search
  - Supports collection reset functionality

### Semantic Search

- **POST** `/api/v1/nlp/index/search/{project_id}`
  - Search through indexed documents using semantic similarity
  - Find relevant chunks based on query meaning
  - Configurable result limit

### Collection Information

- **GET** `/api/v1/nlp/index/info/{project_id}`
  - Get information about the vector database collection
  - View indexing status and collection statistics

## Request/Response Schemas

### ProcessRequest Schema

```json
{
  "file_id": "string",           // Asset ID from upload response
  "chunk_size": 500,             // Optional: Size of text chunks (default: 100)
  "overlap_size": 50,            // Optional: Overlap between chunks (default: 20)
  "do_reset": 0                  // Optional: Reset existing chunks (0=false, 1=true)
}
```

### PushRequest Schema

```json
{
  "do_reset": 0                  // Optional: Reset vector collection (0=false, 1=true)
}
```

### SearchRequest Schema

```json
{
  "text": "What is Ronaldo's career?",  // Query text for semantic search
  "limit": 5                     // Optional: Number of results (default: 30)
}
```

## Usage Example

1. **Upload a document**:

   ```bash
   curl -X POST "http://localhost:8000/api/v1/data/upload/my-project" \
        -H "accept: application/json" \
        -H "Content-Type: multipart/form-data" \
        -F "file=@document.pdf"
   ```

2. **Process the document**:

   ```bash
   curl -X POST "http://localhost:8000/api/v1/data/process/my-project" \
        -H "accept: application/json" \
        -H "Content-Type: application/json" \
        -d '{
          "file_id": "uploaded_asset_id",
          "chunk_size": 500,
          "overlap_size": 50,
          "do_reset": 1
        }'
   ```

3. **Index the processed chunks**:

   ```bash
   curl -X POST "http://localhost:8000/api/v1/nlp/index/push/my-project" \
        -H "accept: application/json" \
        -H "Content-Type: application/json" \
        -d '{
          "do_reset": 1
        }'
   ```

4. **Search through the documents**:

   ```bash
   curl -X POST "http://localhost:8000/api/v1/nlp/index/search/my-project" \
        -H "accept: application/json" \
        -H "Content-Type: application/json" \
        -d '{
          "text": "What are the main achievements?",
          "limit": 5
        }'
   ```

## Configuration

The application uses environment variables for configuration. Key settings include:

- **File Settings**: Allowed file types, maximum file size, chunk size
- **Database**: MongoDB connection URL and database name  
- **LLM Configuration**: Provider selection (OpenAI/Cohere), model IDs, API keys
- **Vector Database**: Qdrant settings, distance method, storage path
- **Generation Settings**: Temperature, max tokens, input limits

## Key Features & Architecture

### Asset Management

- Files are stored as assets with metadata tracking
- Each upload generates a unique asset ID
- Asset information includes file size, type, and project association

### Document Processing Pipeline

1. **Upload**: Files are validated and stored in the file system
2. **Asset Creation**: File metadata is stored in MongoDB
3. **Processing**: Documents are split into overlapping text chunks
4. **Storage**: Chunks are stored with references to their source assets

### Vector Indexing Pipeline

1. **Embedding Generation**: Text chunks are converted to vector embeddings using LLM providers
2. **Vector Storage**: Embeddings are stored in Qdrant vector database with metadata
3. **Collection Management**: Each project gets its own vector collection
4. **Indexing**: Chunks are indexed for fast semantic search

### Semantic Search Process

1. **Query Embedding**: Search text is converted to vector representation
2. **Similarity Search**: Vector database finds most similar document chunks
3. **Result Ranking**: Results are ranked by similarity score
4. **Response**: Relevant chunks are returned with metadata and scores

### Chunk Reset Functionality

The `do_reset` parameter allows you to:

- `0` (default): Append new chunks to existing ones
- `1`: Delete existing chunks before adding new ones

### MongoDB Collections

- **Projects**: Store project metadata and settings
- **Assets**: Track uploaded files and their properties  
- **Chunks**: Store processed text segments with metadata

### Vector Database Collections

- **Project Collections**: Each project gets a dedicated Qdrant collection
- **Embeddings**: Store vector representations of text chunks
- **Metadata**: Maintain links between vectors and source documents
- **Search Indices**: Enable fast similarity search operations

## Development

This project follows a clean architecture pattern with:

- **Controllers**: Handle business logic, file operations, and NLP processing
- **Models**: Define data structures and database operations  
- **Routes**: Define API endpoints and request handling
- **Stores**: Abstract external service integrations (LLM providers, vector databases)
- **Helpers**: Utility functions and configuration management
- **Schemas**: Request/response data validation

## Credits

This project is inspired by and follows tutorials from **Abu Bakr Soliman** ([YouTube Channel](https://www.youtube.com/@bakrianoo)). Special thanks for the educational content that made this implementation possible.
