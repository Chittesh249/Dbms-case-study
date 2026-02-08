# Milvus Implementation - Setup Guide

This project consists of a FastAPI backend with Milvus vector database integration and a React frontend.

## Prerequisites

1. **Python 3.8+** installed
2. **Node.js 16+** installed
3. **OpenAI API Key** - Get one from https://platform.openai.com/api-keys
4. **Milvus Lite** - Will be installed automatically with pymilvus

## Backend Setup

1. Navigate to the Backend directory:
   ```bash
   cd Backend
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the Backend directory with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

4. Start the backend server:
   ```bash
   python -m uvicorn app:app --reload --host 0.0.0.0 --port 8000
   ```

   Or use the provided batch file:
   ```bash
   start-backend.bat
   ```

## Frontend Setup

1. Navigate to the project root directory:
   ```bash
   cd milvus-implementation
   ```

2. Install Node.js dependencies:
   ```bash
   npm install
   ```

3. Start the frontend development server:
   ```bash
   npm run dev
   ```

   Or use the provided batch file:
   ```bash
   start-frontend.bat
   ```

## Running the Application

1. **Start the Backend first** (Terminal 1):
   - Run `start-backend.bat` or the uvicorn command
   - Backend will be available at http://localhost:8000

2. **Start the Frontend** (Terminal 2):
   - Run `start-frontend.bat` or `npm run dev`
   - Frontend will be available at http://localhost:5173

3. **Open your browser** and go to http://localhost:5173

## API Endpoints

- `POST /chat` - Chat with the AI assistant
- `POST /add-data` - Add new data to the knowledge base

## Features

- **Vector Search**: Uses Milvus for semantic search
- **AI Chat**: Powered by OpenAI GPT-4o-mini
- **Real-time Chat**: React frontend with Material-UI
- **Knowledge Base**: Add and search through documents

## Troubleshooting

1. **Backend not starting**: Make sure you have the OpenAI API key in the `.env` file
2. **Frontend can't connect**: Ensure the backend is running on port 8000
3. **Milvus connection issues**: The app will automatically start Milvus Lite

## Adding Data to Knowledge Base

You can add data to the knowledge base by making a POST request to `/add-data`:

```bash
curl -X POST "http://localhost:8000/add-data" \
     -H "Content-Type: application/json" \
     -d '{"text": "Your knowledge content here"}'
```
