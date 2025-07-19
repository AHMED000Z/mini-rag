# Mini-RAG (Retrieval-Augmented Generation) Application

A lightweight, scalable RAG application built with FastAPI that enables document upload, processing, and intelligent querying using LangChain and MongoDB. This project demonstrates a complete RAG pipeline from document ingestion to semantic search and response generation.

## Features

- **Document Upload & Processing**: Upload PDF and text documents with automatic validation
- **Asset Management**: Track uploaded files with metadata (size, type, project association)
- **Text Chunking**: Intelligent document splitting using LangChain's RecursiveCharacterTextSplitter
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
- **Document Processing**: LangChain, PyMuPDF
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
│   ├── controllers/          # Business logic controllers
│   │   ├── BaseController.py    # Base controller class
│   │   ├── DataController.py    # File upload/validation
│   │   ├── ProcessController.py # Document processing
│   │   └── ProjectController.py # Project management
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
│   │   └── schemas/           # Request/Response schemas
│   │       └── data.py           # Data processing schemas
│   └── helpers/
│       └── config.py         # Configuration management
```

## Requirements

- **Python**: 3.8 or later
- **Docker**: For MongoDB container
- **OpenAI API Key**: For embeddings and completions (optional)

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
OPENAI_API_KEY=your_openai_api_key_here

FILE_ALLOWED_TYPES=["application/pdf", "text/plain"]
FILE_MAX_SIZE=10
FILE_DEFAULT_CHUNK_SIZE=1000

MONGODB_URL=mongodb://localhost:27007
MONGODB_DATABASE=minirag
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

## Request/Response Schemas

### ProcessRequest Schema

```json
{
  "file_id": "string",           // Asset ID from upload response
  "chunk_size": 100,             // Optional: Size of text chunks (default: 100)
  "overlap_size": 20,            // Optional: Overlap between chunks (default: 20)
  "do_reset": 0                  // Optional: Reset existing chunks (0=false, 1=true)
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

## Configuration

The application uses environment variables for configuration. Key settings include:

- **File Settings**: Allowed file types, maximum file size, chunk size
- **Database**: MongoDB connection URL and database name  
- **API Keys**: OpenAI API key for embeddings (if used)

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

### Chunk Reset Functionality

The `do_reset` parameter allows you to:

- `0` (default): Append new chunks to existing ones
- `1`: Delete existing chunks before adding new ones

### MongoDB Collections

- **Projects**: Store project metadata and settings
- **Assets**: Track uploaded files and their properties  
- **Chunks**: Store processed text segments with metadata

## Development

This project follows a clean architecture pattern with:

- **Controllers**: Handle business logic and file operations
- **Models**: Define data structures and database operations  
- **Routes**: Define API endpoints and request handling
- **Helpers**: Utility functions and configuration management
- **Schemas**: Request/response data validation

## Credits

This project is inspired by and follows tutorials from **Abu Bakr Soliman** ([YouTube Channel](https://www.youtube.com/@bakrianoo)). Special thanks for the educational content that made this implementation possible.
