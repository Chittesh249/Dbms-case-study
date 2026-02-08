from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pymilvus import connections, Collection, CollectionSchema, FieldSchema, DataType
from openai import OpenAI
from dotenv import load_dotenv
import os
import json
import time
import logging
from typing import Dict, List, Optional, Any

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 🔹 Load environment variables
load_dotenv()

app = FastAPI(
    title="Milvus Vector Database API",
    description="A comprehensive RAG (Retrieval-Augmented Generation) API powered by Milvus vector database and OpenAI integration",
    version="1.0.0",
    contact={
        "name": "API Support",
        "email": "support@example.com",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
)

# 🔹 Allow frontend to connect (change "*" to your frontend URL if hosted)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    # Expose custom headers for client-side access
    expose_headers=["Access-Control-Allow-Origin"]
)

# 🔹 Initialize OpenAI client only if API key is available
api_key = os.getenv("OPENAI_API_KEY")
if api_key and api_key != "your_openai_api_key_here":
    client = OpenAI(api_key=api_key)
    logger.info("✅ OpenAI client initialized successfully")
else:
    client = None
    logger.warning("⚠️  No valid OpenAI API key found. Using demo responses.")

# 🔹 Milvus Vector Database Setup
logger.info("🔹 Initializing Milvus Vector Database...")

try:
    # Connect to Milvus (using default local connection)
    connections.connect(alias="default", host="localhost", port="19530")
    logger.info("✅ Connected to Milvus successfully")
    
    # Define collection schema for vector storage
    fields = [
        FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
        FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=1536),  # OpenAI embedding dimension
        FieldSchema(name="text", dtype=DataType.VARCHAR, max_length=2000),
        FieldSchema(name="metadata", dtype=DataType.VARCHAR, max_length=1000),
    ]
    
    schema = CollectionSchema(fields, description="Milvus Vector Database for AI Chatbot")
    collection_name = "milvus_chatbot_data"
    
    # Create or get collection
    existing_collections = Collection.list_collections()
    if collection_name in existing_collections:
        collection = Collection(collection_name)
        logger.info(f"✅ Using existing Milvus collection: {collection_name}")
    else:
        collection = Collection(name=collection_name, schema=schema)
        logger.info(f"✅ Created new Milvus collection: {collection_name}")
        
        # Create index for vector search
        index_params = {
            "metric_type": "COSINE",
            "index_type": "IVF_FLAT",
            "params": {"nlist": 128}
        }
        collection.create_index(field_name="embedding", index_params=index_params)
        logger.info("✅ Created vector index for similarity search")
    
    # Load collection for search
    collection.load()
    logger.info("✅ Milvus collection loaded and ready for operations")
    
    milvus_available = True
    
except Exception as e:
    logger.error(f"⚠️  Milvus connection failed: {e}")
    logger.info("📝 Using in-memory storage as fallback")
    collection = None
    milvus_available = False
    # Fallback to simple storage
    knowledge_base = []
    
    # Import comprehensive Milvus documentation
    try:
        from comprehensive_milvus_docs import get_comprehensive_milvus_docs
        milvus_docs = get_comprehensive_milvus_docs()
        logger.info(f"📚 Loaded {len(milvus_docs)} comprehensive Milvus documentation entries")
    except ImportError as import_error:
        logger.warning(f"⚠️  Could not import comprehensive docs: {import_error}")
        # Fallback to basic documentation if comprehensive docs not available
        milvus_docs = [
            {
                "text": "Milvus is an open-source vector database designed for AI applications. It provides high-performance similarity search and supports various vector operations. Milvus is built for scalability and can handle billions of vectors with sub-second search latency.",
                "metadata": "milvus_overview"
            },
            {
                "text": "Vector databases like Milvus store data as high-dimensional vectors and enable fast similarity search using algorithms like cosine similarity, Euclidean distance, and dot product. This makes them perfect for AI applications that need to find similar content based on meaning rather than exact matches.",
                "metadata": "vector_database_concept"
            }
        ]
        logger.info(f"📚 Loaded {len(milvus_docs)} basic Milvus documentation entries (comprehensive docs not available)")
    
    # Add Milvus documentation to knowledge base
    for doc in milvus_docs:
        knowledge_base.append({
            "text": doc["text"],
            "metadata": doc["metadata"],
            "id": len(knowledge_base)
        })
    
    logger.info(f"✅ Added {len(milvus_docs)} Milvus documentation entries to knowledge base")

# 🔹 Helper: get embeddings (only if client is available)
def get_embedding(text: str) -> Optional[List[float]]:
    """
    Generate embeddings for the given text using OpenAI's embedding model.
    
    Args:
        text (str): Input text to generate embeddings for
        
    Returns:
        Optional[List[float]]: Embedding vector or None if failed
    """
    if not client:
        logger.warning("OpenAI client not initialized, cannot generate embeddings")
        return None
    
    if not text.strip():
        logger.warning("Empty text provided for embedding generation")
        return None
    
    try:
        response = client.embeddings.create(input=text, model="text-embedding-3-small")
        embedding = response.data[0].embedding
        logger.debug(f"Generated embedding of length {len(embedding)} for text: {text[:50]}...")
        return embedding
    except Exception as e:
        logger.error(f"Error getting embedding for text '{text[:50]}...': {e}")
        return None

# 🔹 Helper: search Milvus for similar vectors
def search_milvus(query_vector: List[float], limit: int = 3) -> List[Any]:
    """
    Search for similar vectors in Milvus collection.
    
    Args:
        query_vector (List[float]): Query vector to search for
        limit (int): Maximum number of results to return
        
    Returns:
        List[Any]: List of search results
    """
    if not milvus_available or not collection:
        logger.warning("Milvus not available, returning empty results")
        return []
    
    if not query_vector:
        logger.warning("Empty query vector provided for search")
        return []
    
    try:
        search_params = {
            "metric_type": "COSINE",
            "params": {"nprobe": 10}
        }
        
        results = collection.search(
            data=[query_vector],
            anns_field="embedding",
            param=search_params,
            limit=limit,
            output_fields=["text", "metadata"]
        )
        
        logger.debug(f"Found {len(results[0]) if results else 0} similar vectors")
        return results[0] if results else []
    except Exception as e:
        logger.error(f"Error searching Milvus: {e}")
        return []

# 🔹 Helper: insert data into Milvus
def insert_to_milvus(text: str, metadata: str = "") -> bool:
    """
    Insert text and metadata into Milvus collection.
    
    Args:
        text (str): Text content to store
        metadata (str): Optional metadata to store
        
    Returns:
        bool: True if insertion was successful, False otherwise
    """
    if not milvus_available or not collection:
        logger.warning("Milvus not available, cannot insert data")
        return False
    
    if not text.strip():
        logger.warning("Cannot insert empty text to Milvus")
        return False
    
    try:
        # Get embedding for the text
        embedding = get_embedding(text)
        if not embedding:
            logger.error(f"Failed to generate embedding for text: {text[:50]}...")
            return False
        
        # Insert into Milvus
        data = [
            [embedding],  # embedding field
            [text],       # text field
            [metadata]    # metadata field
        ]
        
        collection.insert(data)
        collection.flush()  # Ensure data is written
        logger.info(f"Successfully inserted text to Milvus: {text[:50]}...")
        return True
    except Exception as e:
        logger.error(f"Error inserting to Milvus: {e}")
        return False

# 🔹 Endpoint 1: Add new data to Milvus vector database
@app.post("/add-data", summary="Add data to vector database", 
          description="Add new text data to the Milvus vector database for semantic search")
async def add_data(request: Request) -> Dict[str, Any]:
    """
    Add new text data to the Milvus vector database for semantic search.
    
    Args:
        request (Request): HTTP request containing text and metadata
        
    Returns:
        Dict[str, Any]: Response indicating success or failure
    """
    try:
        data = await request.json()
        text = data.get("text", "")
        metadata = data.get("metadata", "")
        
        if not text or not text.strip():
            logger.warning("Attempted to add empty text to database")
            return {"message": "Error: No text provided", "success": False}
        
        if milvus_available:
            # Store in Milvus vector database
            success = insert_to_milvus(text, metadata)
            if success:
                logger.info(f"Successfully added data to Milvus: {text[:50]}...")
                return {
                    "message": "Data added successfully to Milvus vector database", 
                    "success": True,
                    "storage": "Milvus Vector DB"
                }
            else:
                logger.error("Failed to add data to Milvus")
                return {"message": "Failed to add data to Milvus", "success": False}
        else:
            # Fallback to in-memory storage
            knowledge_base.append({
                "text": text,
                "metadata": metadata,
                "id": len(knowledge_base)
            })
            logger.info(f"Added data to in-memory storage: {text[:50]}...")
            return {
                "message": "Data added to in-memory storage (Milvus not available)", 
                "success": True,
                "storage": "In-Memory"
            }
    except Exception as e:
        logger.error(f"Error in add_data endpoint: {e}")
        return {"message": f"Error: {str(e)}", "success": False}

# 🔹 Endpoint 2: Chat with Milvus vector database
@app.post("/chat", summary="Chat with AI assistant",
          description="Chat with the AI assistant using vector search for context")
async def chat(request: Request) -> Dict[str, Any]:
    """
    Chat with the AI assistant using vector search for context.
    
    Args:
        request (Request): HTTP request containing user message
        
    Returns:
        Dict[str, Any]: AI response with context information
    """
    try:
        data = await request.json()
        user_message = data.get("message", "")

        if not user_message or not user_message.strip():
            logger.warning("Received empty message in chat endpoint")
            return {"reply": "Please provide a message to chat about."}

        logger.info(f"Processing chat request: {user_message[:100]}...")

        # Step 1: Get embedding for user query
        query_embedding = get_embedding(user_message)
        
        # Step 2: Search Milvus for relevant context using vector similarity
        context = ""
        search_method = ""
        
        if milvus_available and query_embedding:
            # Use Milvus vector search
            search_results = search_milvus(query_embedding, limit=3)
            if search_results:
                relevant_docs = []
                for hit in search_results:
                    entity_text = hit.entity.get("text", "")
                    if entity_text:
                        relevant_docs.append(entity_text)
                context = " ".join(relevant_docs)
                search_method = "Milvus Vector Search"
                logger.info(f"Found {len(relevant_docs)} relevant documents using vector search")
            else:
                logger.info("No relevant documents found in vector search")
        elif not milvus_available and 'knowledge_base' in locals():
            # Fallback to keyword search
            relevant_docs = []
            user_words = user_message.lower().split()
            
            for doc in knowledge_base:
                doc_text = doc["text"].lower()
                # Look for significant words (>3 characters) in the document
                matching_words = [word for word in user_words if len(word) > 3 and word in doc_text]
                if matching_words:
                    relevant_docs.append(doc["text"])
            
            if relevant_docs:
                context = " ".join(relevant_docs[:3])  # Limit to first 3 matches
                search_method = "Keyword Search (Fallback)"
                logger.info(f"Found {len(relevant_docs)} relevant documents using keyword search")
            else:
                logger.info("No relevant documents found in keyword search")

        # Step 3: Combine context + user query
        if context:
            prompt = f"Context from vector database: {context}\n\nUser: {user_message}\n\nAnswer clearly and helpfully based on the context provided."
        else:
            prompt = f"User: {user_message}\n\nAnswer clearly and helpfully."

        # Step 4: Generate LLM response
        try:
            if client:
                logger.debug("Generating AI response with context")
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt}],
                    timeout=30  # Add timeout for API call
                )
                answer = response.choices[0].message.content
                logger.info("Successfully generated AI response")
            else:
                # Fallback response when no API key is set
                logger.info("Using fallback response (no OpenAI API key)")
                if context:
                    answer = f"Based on the context from {search_method}: {context[:100]}... I understand you're asking about: {user_message}. This is a demo response since no OpenAI API key is configured."
                else:
                    answer = f"Hello! I received your message: '{user_message}'. This is a demo response since no OpenAI API key is configured. Please add your OpenAI API key to the .env file to get real AI responses."
        except Exception as e:
            error_msg = str(e)
            logger.error(f"Error calling OpenAI API: {e}")
            if "quota" in error_msg.lower() or "insufficient_quota" in error_msg.lower():
                answer = f"⚠️ OpenAI API quota exceeded. Please check your billing details at https://platform.openai.com/account/billing. For now, here's a demo response: I understand you're asking about '{user_message}'. This is a demo response since your OpenAI API quota has been exceeded."
            elif "rate" in error_msg.lower():
                answer = f"⚠️ Rate limit exceeded. Please wait a moment and try again. For now, here's a demo response: I understand you're asking about '{user_message}'."
            else:
                answer = f"I apologize, but I'm having trouble connecting to the AI service. Error: {error_msg}"

        response_data = {
            "reply": answer,
            "search_method": search_method,
            "milvus_available": milvus_available,
            "context_found": bool(context)
        }
        
        logger.info(f"Chat response generated successfully: {answer[:100]}...")
        return response_data
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing chat request: {e}")
        return {"reply": f"Error processing chat request: {str(e)}"}

# 🔹 Health check endpoint
@app.get("/", summary="Health check",
         description="Check the health status of the backend service")
async def root() -> Dict[str, Any]:
    """
    Health check endpoint to verify backend service status.
    
    Returns:
        Dict[str, Any]: Service status information
    """
    status = {
        "message": "Milvus Vector Database Backend is running!",
        "timestamp": time.time(),
        "openai_client": "Available" if client else "Not available",
        "milvus_status": "Connected" if milvus_available else "Not available",
        "storage_type": "Milvus Vector DB" if milvus_available else "In-Memory Fallback"
    }
    
    if milvus_available and collection:
        try:
            # Get collection statistics
            status["milvus_collection"] = collection.name
            status["total_vectors"] = collection.num_entities
            status["collection_loaded"] = True
        except Exception as e:
            logger.error(f"Error getting collection stats: {e}")
            status["milvus_collection"] = "Unknown"
            status["total_vectors"] = "Unknown"
            status["collection_loaded"] = False
    elif not milvus_available:
        status["in_memory_entries"] = len(knowledge_base) if 'knowledge_base' in locals() else 0
        status["collection_loaded"] = False
    
    logger.info("Health check endpoint accessed")
    return status

# 🔹 Milvus collection info endpoint
@app.get("/milvus-info", summary="Get Milvus collection information",
         description="Retrieve detailed information about the Milvus collection")
async def milvus_info() -> Dict[str, Any]:
    """
    Get detailed information about the Milvus collection.
    
    Returns:
        Dict[str, Any]: Collection information including schema and indexes
    """
    if not milvus_available:
        logger.warning("Milvus is not available, returning error")
        return {"error": "Milvus is not available"}
    
    try:
        logger.info(f"Retrieving Milvus collection info for: {collection.name}")
        return {
            "collection_name": collection.name,
            "total_entities": collection.num_entities,
            "schema": {
                "fields": [{"name": field.name, "type": str(field.dtype)} for field in collection.schema.fields]
            },
            "indexes": [{"field": idx.field_name, "type": idx.params} for idx in collection.indexes],
            "loaded": True
        }
    except Exception as e:
        logger.error(f"Failed to get Milvus info: {e}")
        return {"error": f"Failed to get Milvus info: {str(e)}"}

# 🔹 Add sample data endpoint for testing
@app.post("/add-sample-data", summary="Add sample data",
          description="Add sample documents to the vector database for testing purposes")
async def add_sample_data() -> Dict[str, Any]:
    """
    Add sample data to the database for testing purposes.
    
    Returns:
        Dict[str, Any]: Result of the sample data addition
    """
    sample_data = [
        {
            "text": "Milvus is an open-source vector database designed for AI applications. It provides high-performance similarity search and supports various vector operations.",
            "metadata": "milvus_intro"
        },
        {
            "text": "Vector databases store data as high-dimensional vectors and enable fast similarity search using algorithms like cosine similarity, Euclidean distance, and dot product.",
            "metadata": "vector_db_concept"
        },
        {
            "text": "OpenAI provides embedding models like text-embedding-3-small that convert text into 1536-dimensional vectors for semantic search applications.",
            "metadata": "openai_embeddings"
        },
        {
            "text": "FastAPI is a modern Python web framework for building APIs with automatic documentation, type hints, and high performance.",
            "metadata": "fastapi_info"
        },
        {
            "text": "React is a JavaScript library for building user interfaces, particularly for single-page applications with component-based architecture.",
            "metadata": "react_info"
        }
    ]
    
    logger.info(f"Adding {len(sample_data)} sample documents to database")
    
    results = []
    for item in sample_data:
        if milvus_available:
            success = insert_to_milvus(item["text"], item["metadata"])
            result_item = {
                "text": item["text"][:50] + "...",
                "success": success,
                "storage": "Milvus" if success else "Failed"
            }
            results.append(result_item)
        else:
            knowledge_base.append({
                "text": item["text"],
                "metadata": item["metadata"],
                "id": len(knowledge_base)
            })
            result_item = {
                "text": item["text"][:50] + "...",
                "success": True,
                "storage": "In-Memory"
            }
            results.append(result_item)
    
    success_count = sum(1 for r in results if r["success"])
    logger.info(f"Successfully added {success_count}/{len(sample_data)} sample documents")
    
    return {
        "message": f"Added {len(sample_data)} sample documents",
        "results": results,
        "storage_type": "Milvus Vector DB" if milvus_available else "In-Memory Fallback",
        "successful_additions": success_count
    }

# 🔹 Test OpenAI endpoint
@app.get("/test-openai", summary="Test OpenAI connection",
         description="Test the connection to the OpenAI API")
async def test_openai() -> Dict[str, Any]:
    """
    Test the connection to the OpenAI API.
    
    Returns:
        Dict[str, Any]: Test result and response from OpenAI
    """
    if client:
        try:
            logger.info("Testing OpenAI connection")
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": "Say hello"}],
                timeout=10
            )
            logger.info("OpenAI connection test successful")
            return {"status": "success", "response": response.choices[0].message.content}
        except Exception as e:
            logger.error(f"OpenAI connection test failed: {e}")
            return {"status": "error", "error": str(e)}
    else:
        logger.warning("OpenAI client not initialized for test")
        return {"status": "error", "error": "OpenAI client not initialized"}
