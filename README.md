# Mini-RAG (Retrieval-Augmented Generation) Application

A lightweight, scalable RAG application built with FastAPI that enables document upload, processing, and intelligent querying using LangChain and MongoDB. This project demonstrates a complete RAG pipeline from document ingestion to semantic search and response generation.

## Features

- **Document Upload & Processing**: Upload PDF and text documents with automatic validation
- **Text Chunking**: Intelligent document splitting using LangChain's RecursiveCharacterTextSplitter
- **Project Management**: Organize documents into projects for better management
- **MongoDB Integration**: Persistent storage for documents and metadata
- **RESTful API**: Clean API endpoints for all operations
- **Docker Support**: Easy deployment with Docker Compose
- **File Validation**: Built-in file type and size validation

## Tech Stack

- **Backend**: FastAPI (Python)
- **Database**: MongoDB with Motor (async driver)
- **Document Processing**: LangChain, PyMuPDF
- **Vector Operations**: LangChain text splitters
- **Containerization**: Docker & Docker Compose

## Project Structure

```text
mini-rag/
├── Docker/
│   ├── docker-compose.yml      # MongoDB container configuration
│   └── mongodb/               # MongoDB data directory
├── src/
│   ├── main.py               # FastAPI application entry point
│   ├── requirenments.txt     # Python dependencies
│   ├── assets/files/         # Uploaded documents storage
│   ├── controllers/          # Business logic controllers
│   │   ├── DataController.py    # File upload/validation
│   │   ├── ProcessController.py # Document processing
│   │   └── ProjectController.py # Project management
│   ├── models/              # Data models and schemas
│   │   ├── ProjectModel.py     # Project database model
│   │   ├── ChunkModel.py       # Document chunk model
│   │   └── db_schemas/         # Database schemas
│   ├── routes/              # API route definitions
│   │   ├── base.py            # Base routes
│   │   └── data.py            # Data handling routes
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
pip install -r requirenments.txt
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

### Document Processing

- **POST** `/api/v1/data/process/{project_id}`
  - Process uploaded documents into chunks
  - Extract text and create searchable segments

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
        -d '{"file_id": "uploaded_file_id"}'
   ```

## Configuration

The application uses environment variables for configuration. Key settings include:

- **File Settings**: Allowed file types, maximum file size, chunk size
- **Database**: MongoDB connection URL and database name  
- **API Keys**: OpenAI API key for embeddings (if used)

## Development

This project follows a clean architecture pattern with:

- **Controllers**: Handle business logic
- **Models**: Define data structures and database operations
- **Routes**: Define API endpoints
- **Helpers**: Utility functions and configuration

## Credits

This project is inspired by and follows tutorials from **Abu Bakr Soliman** ([YouTube Channel](https://www.youtube.com/@bakrianoo)). Special thanks for the educational content that made this implementation possible.
