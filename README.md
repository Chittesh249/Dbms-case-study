# Milvus Vector Database Implementation

<div align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Node.js](https://img.shields.io/badge/node.js-16%2B-green.svg)](https://nodejs.org/)
[![FastAPI](https://img.shields.io/badge/fastapi-0.104.1-orange.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/react-18.2.0-blue.svg)](https://reactjs.org/)

**A comprehensive RAG (Retrieval-Augmented Generation) application powered by Milvus vector database and OpenAI integration**

</div>

## 🌟 Overview

This project demonstrates a complete implementation of a Retrieval-Augmented Generation (RAG) system using **Milvus Vector Database** for semantic search and **OpenAI** for intelligent responses. The application provides a real-time chat interface where users can query a knowledge base stored as high-dimensional vectors, enabling semantic search and context-aware AI responses.

## ✨ Features

### Backend Features
- **Milvus Vector Database Integration**: High-performance similarity search using vector embeddings
- **OpenAI Integration**: Powered by GPT-4o-mini for intelligent responses
- **Automatic Fallback**: Seamless transition to in-memory storage when Milvus is unavailable
- **Comprehensive API**: RESTful endpoints for chat, data addition, and system monitoring
- **Real-time Monitoring**: Health checks and system status endpoints
- **Auto-indexing**: Automatic vector indexing for optimal search performance

### Frontend Features
- **Modern UI/UX**: Built with React and Material-UI for an intuitive experience
- **Real-time Chat**: Interactive chat interface with loading indicators
- **Responsive Design**: Works seamlessly across desktop and mobile devices
- **Error Handling**: Graceful error management and user feedback
- **Clean Architecture**: Component-based design for maintainability

### Technical Features
- **Semantic Search**: Understands meaning, not just keywords
- **Vector Embeddings**: 1536-dimensional vectors using OpenAI embeddings
- **COSINE Similarity**: Advanced similarity algorithm for accurate results
- **Scalable Architecture**: Designed for horizontal scaling
- **Production Ready**: Proper error handling and fallback mechanisms

## 🏗️ Architecture

```
┌─────────────┐    ┌─────────────┐    ┌──────────────────┐
│   React   │◄──►│   FastAPI   │◄──►│  Milvus Vector   │
│   Frontend│    │   Backend   │    │    Database      │
└─────────────┘    └─────────────┘    └──────────────────┘
                        │
                   ┌─────────────┐
                   │   OpenAI    │
                   │ Embeddings  │
                   └─────────────┘
```

## 🚀 Quick Start

### Prerequisites
- **Python 3.8+** installed
- **Node.js 16+** installed  
- **OpenAI API Key** (optional, but recommended for full functionality)
- **Docker** (optional, for Milvus server)

### Installation

#### 1. Clone the Repository
```bash
git clone <repository-url>
cd milvus-implementation
```

#### 2. Backend Setup
```bash
# Navigate to backend directory
cd Backend

# Install Python dependencies
pip install -r requirements.txt

# Create environment file
echo "OPENAI_API_KEY=your_openai_api_key_here" > .env

# Start Milvus server (optional, using Docker)
docker run -d --name milvus-standalone \
  -p 19530:19530 \
  -p 9091:9091 \
  milvusdb/milvus:latest \
  milvus run standalone

# Start the backend server
python -m uvicorn app:app --host 0.0.0.0 --port 8001
```

#### 3. Frontend Setup
```bash
# In a new terminal, navigate to project root
cd milvus-implementation

# Install Node.js dependencies
npm install

# Start the frontend development server
npm run dev
```

#### 4. Access the Application
- Frontend: [http://localhost:5173](http://localhost:5173)
- Backend API: [http://localhost:8001](http://localhost:8001)
- Backend API Docs: [http://localhost:8001/docs](http://localhost:8001/docs)

## 🛠️ Configuration

### Environment Variables
Create a `.env` file in the `Backend` directory:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

### Milvus Configuration
The application connects to Milvus at:
- Host: `localhost`
- Port: `19530`
- Collection: `milvus_chatbot_data`

## 📡 API Endpoints

### Chat Endpoint
- **POST** `/chat`
- Query the knowledge base with semantic search
- Request: `{"message": "your question here"}`
- Response: AI-generated answer with context information

### Add Data Endpoint
- **POST** `/add-data`
- Add new documents to the knowledge base
- Request: `{"text": "document content", "metadata": "optional tag"}`
- Response: Success status

### System Endpoints
- **GET** `/` - Health check and system status
- **GET** `/milvus-info` - Milvus collection information
- **POST** `/add-sample-data` - Add sample documents for testing
- **GET** `/test-openai` - Test OpenAI connectivity

## 🧪 Testing

### Add Sample Data
```bash
curl -X POST "http://localhost:8001/add-sample-data"
```

### Test Semantic Search
```bash
curl -X POST "http://localhost:8001/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "What is Milvus?"}'
```

### Check System Status
```bash
curl -X GET "http://localhost:8001/"
```

## 📊 Vector Database Schema

```python
fields = [
    FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
    FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=1536),  # OpenAI embedding
    FieldSchema(name="text", dtype=DataType.VARCHAR, max_length=2000),      # Document content
    FieldSchema(name="metadata", dtype=DataType.VARCHAR, max_length=1000),  # Metadata
]
```

## 🤖 Use Cases

This implementation is perfect for:
- **Enterprise Knowledge Bases**: Internal documentation search
- **Customer Support Chatbots**: Context-aware support automation
- **Research Applications**: Semantic document search
- **Educational Platforms**: Content discovery systems
- **E-commerce**: Product recommendation with semantic understanding

## 🚀 Deployment

### Production Deployment
For production deployment, consider:
- Using a managed Milvus service (Zilliz Cloud)
- Setting up proper SSL certificates
- Configuring environment-specific settings
- Implementing proper logging and monitoring
- Scaling backend instances based on demand

### Docker Deployment
Coming soon - Docker Compose configuration for easy deployment.

## 🤝 Contributing

We welcome contributions! Please see our [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to contribute to this project.

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

If you encounter any issues or have questions:

1. Check the [Troubleshooting](#troubleshooting) section below
2. Review the [API Documentation](http://localhost:8001/docs) when running locally
3. Open an issue in the repository
4. Contact the maintainers

### Troubleshooting

**Issue**: Backend won't start
- Solution: Ensure OpenAI API key is set in `.env` file

**Issue**: Frontend can't connect to backend
- Solution: Verify backend is running on port 8001 and CORS settings

**Issue**: Milvus connection fails
- Solution: The application will automatically fall back to in-memory storage

**Issue**: OpenAI API errors
- Solution: Check API key validity and billing status

---

<div align="center">

Made with ❤️ using FastAPI, React, and Milvus

[Back to top ↑](#milvus-vector-database-implementation)

</div>