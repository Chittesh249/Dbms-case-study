# Development Guide

Welcome to the development guide for the Milvus Vector Database Implementation project. This document provides comprehensive information for developers who want to contribute to or extend this project.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Project Structure](#project-structure)
- [Development Setup](#development-setup)
- [Running the Application](#running-the-application)
- [Testing](#testing)
- [Code Style](#code-style)
- [Debugging](#debugging)
- [Building for Production](#building-for-production)
- [Deployment](#deployment)
- [Troubleshooting](#troubleshooting)

## Prerequisites

Before starting development, ensure you have the following installed:

### Backend (Python)
- **Python 3.8+** - Check with `python --version`
- **pip** - Python package installer
- **Virtual environment tool** (recommended: `venv` or `virtualenv`)

### Frontend (JavaScript/React)
- **Node.js 16+** - Check with `node --version`
- **npm 8+** or **yarn** - Package manager

### Optional Dependencies
- **Docker** - For running Milvus server locally
- **Git** - Version control system
- **OpenAI API Key** - For full functionality

## Project Structure

```
milvus-implementation/
├── Backend/                    # FastAPI backend
│   ├── app.py                 # Main application file
│   ├── requirements.txt       # Python dependencies
│   ├── .env                   # Environment variables
│   ├── comprehensive_milvus_docs.py  # Documentation dataset
│   └── start_backend.py       # Backend startup script
├── src/                       # React frontend source
│   ├── components/            # React components
│   │   ├── Chat/
│   │   ├── Searchbar/
│   │   └── Sidebar/
│   ├── App.jsx               # Main App component
│   ├── main.jsx              # Entry point
│   └── App.css               # Global styles
├── public/                    # Static assets
├── package.json              # Frontend dependencies
├── README.md                 # Main documentation
├── DEVELOPMENT.md            # This file
├── CONTRIBUTING.md           # Contribution guidelines
└── LICENSE                   # License information
```

## Development Setup

### Backend Setup

1. **Navigate to the Backend directory:**
   ```bash
   cd Backend
   ```

2. **Create and activate a virtual environment:**
   ```bash
   # On Windows
   python -m venv venv
   venv\Scripts\activate
   
   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   Create a `.env` file in the Backend directory:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   ```

### Frontend Setup

1. **Navigate to the project root:**
   ```bash
   cd milvus-implementation  # From Backend directory
   ```

2. **Install Node.js dependencies:**
   ```bash
   npm install
   ```

## Running the Application

### Development Mode

#### Backend (with auto-reload)
```bash
cd Backend
python -m uvicorn app:app --reload --host 0.0.0.0 --port 8001
```

Or using the start script:
```bash
python start_backend.py
```

#### Frontend (with hot reloading)
```bash
cd milvus-implementation
npm run dev
```

The application will be available at:
- Frontend: [http://localhost:5173](http://localhost:5173)
- Backend API: [http://localhost:8001](http://localhost:8001)
- Backend API Docs: [http://localhost:8001/docs](http://localhost:8001/docs)

### With Milvus Server

For full vector database functionality, run Milvus separately:

```bash
# Using Docker
docker run -d --name milvus-standalone \
  -p 19530:19530 \
  -p 9091:9091 \
  milvusdb/milvus:latest \
  milvus run standalone
```

Then start the backend as usual.

## Testing

### Backend Testing

#### Unit Tests
```bash
cd Backend
pytest
```

#### Manual Testing
Test API endpoints using curl or Postman:

```bash
# Add sample data
curl -X POST "http://localhost:8001/add-sample-data"

# Test chat functionality
curl -X POST "http://localhost:8001/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "What is Milvus?"}'

# Check Milvus info
curl -X GET "http://localhost:8001/milvus-info"
```

### Frontend Testing
```bash
npm test
```

## Code Style

### Python Style Guide
- Follow [PEP 8](https://pep8.org/) style guide
- Use type hints for all function parameters and return values
- Write docstrings for all functions, classes, and modules using Google style
- Keep functions small and focused on a single responsibility
- Use descriptive variable and function names

Example:
```python
def calculate_similarity_score(vector_a: List[float], vector_b: List[float]) -> float:
    """Calculate cosine similarity between two vectors.
    
    Args:
        vector_a: First vector for comparison
        vector_b: Second vector for comparison
        
    Returns:
        Cosine similarity score between -1 and 1
    """
    # Implementation here
```

### JavaScript/React Style Guide
- Follow [Airbnb JavaScript Style Guide](https://github.com/airbnb/javascript)
- Use functional components with hooks
- Use TypeScript or provide PropTypes for component prop validation
- Keep components small and focused on a single responsibility
- Use descriptive variable and function names
- Prefer arrow functions for component definitions

Example:
```javascript
const ChatMessage = ({ message, isUser }) => {
  // Component implementation
};
```

## Debugging

### Backend Debugging

#### Enable Debug Logging
Add the following to your `.env` file:
```env
LOG_LEVEL=DEBUG
```

#### Common Debugging Commands
```bash
# Check if Milvus is running
telnet localhost 19530

# View application logs
tail -f app.log

# Run with detailed output
python -m uvicorn app:app --reload --debug
```

### Frontend Debugging

#### Browser Developer Tools
- Use React Developer Tools extension
- Check Console tab for errors
- Use Network tab to inspect API calls

#### Common Debugging Commands
```bash
# Run with verbose output
npm run dev -- --verbose

# Clear cache and reinstall
npm run clean
```

## Building for Production

### Backend
The backend is designed to run with production-grade ASGI servers:

```bash
# Using uvicorn in production mode
uvicorn app:app --host 0.0.0.0 --port 8001 --workers 4

# Or using gunicorn (install separately)
pip install gunicorn
gunicorn app:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8001
```

### Frontend
```bash
# Build for production
npm run build

# Preview production build
npm run preview
```

## Deployment

### Environment Configuration
For production deployment, ensure these environment variables are set:

**Backend (.env):**
```env
OPENAI_API_KEY=your_production_api_key
LOG_LEVEL=INFO
WORKERS=4
HOST=0.0.0.0
PORT=8001
```

### Docker Deployment
Coming soon - Docker Compose configuration for easy deployment.

## Troubleshooting

### Common Issues

#### Backend won't start
- Check if the port is already in use: `netstat -ano | findstr :8001`
- Verify Python dependencies are installed
- Ensure environment variables are set correctly

#### Frontend can't connect to backend
- Verify backend is running on the correct port
- Check CORS settings in `app.py`
- Ensure both applications are running

#### Milvus connection fails
- Check if Milvus server is running
- Verify connection parameters in `app.py`
- The application will automatically fall back to in-memory storage

#### OpenAI API errors
- Check API key validity
- Verify billing status
- Ensure rate limits are not exceeded

### Getting Help

1. Check the logs for error messages
2. Verify all prerequisites are installed and configured
3. Review the API documentation at `/docs`
4. Consult the README for setup instructions
5. Create an issue in the repository

## Performance Tips

### Backend Optimization
- Use connection pooling for database connections
- Implement caching for frequently accessed data
- Optimize vector search parameters based on your data size
- Monitor memory usage with large datasets

### Frontend Optimization
- Implement lazy loading for components
- Use React.memo for expensive components
- Optimize bundle size with code splitting
- Implement proper error boundaries

---

<div align="center">

Made with ❤️ by the development team

[Back to top ↑](#development-guide)

</div>