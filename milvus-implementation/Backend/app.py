from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pymilvus import connections, Collection, CollectionSchema, FieldSchema, DataType
from openai import OpenAI
from dotenv import load_dotenv
import os
import json
import time

# 🔹 Load environment variables
load_dotenv()

app = FastAPI()

# 🔹 Allow frontend to connect (change "*" to your frontend URL if hosted)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔹 Initialize OpenAI client only if API key is available
api_key = os.getenv("OPENAI_API_KEY")
if api_key and api_key != "your_openai_api_key_here":
    client = OpenAI(api_key=api_key)
    print("✅ OpenAI client initialized successfully")
else:
    client = None
    print("⚠️  No valid OpenAI API key found. Using demo responses.")

# 🔹 Milvus Vector Database Setup
print("🔹 Initializing Milvus Vector Database...")

try:
    # Connect to Milvus (using default local connection)
    connections.connect(alias="default", host="localhost", port="19530")
    print("✅ Connected to Milvus successfully")
    
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
    if collection_name in [c.name for c in Collection.list_collections()]:
        collection = Collection(collection_name)
        print(f"✅ Using existing Milvus collection: {collection_name}")
    else:
        collection = Collection(name=collection_name, schema=schema)
        print(f"✅ Created new Milvus collection: {collection_name}")
        
        # Create index for vector search
        index_params = {
            "metric_type": "COSINE",
            "index_type": "IVF_FLAT",
            "params": {"nlist": 128}
        }
        collection.create_index(field_name="embedding", index_params=index_params)
        print("✅ Created vector index for similarity search")
    
    # Load collection for search
    collection.load()
    print("✅ Milvus collection loaded and ready for operations")
    
    milvus_available = True
    
except Exception as e:
    print(f"⚠️  Milvus connection failed: {e}")
    print("📝 Using in-memory storage as fallback")
    collection = None
    milvus_available = False
    # Fallback to simple storage
    knowledge_base = []
    
    # Import comprehensive Milvus documentation
    try:
        from comprehensive_milvus_docs import get_comprehensive_milvus_docs
        milvus_docs = get_comprehensive_milvus_docs()
        print(f"📚 Loaded {len(milvus_docs)} comprehensive Milvus documentation entries")
    except ImportError:
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
        print(f"📚 Loaded {len(milvus_docs)} basic Milvus documentation entries (comprehensive docs not available)")
    
    # Add Milvus documentation to knowledge base
    for doc in milvus_docs:
        knowledge_base.append({
            "text": doc["text"],
            "metadata": doc["metadata"],
            "id": len(knowledge_base)
        })
    
    print(f"✅ Added {len(milvus_docs)} Milvus documentation entries to knowledge base")

# 🔹 Helper: get embeddings (only if client is available)
def get_embedding(text: str):
    if client:
        try:
            response = client.embeddings.create(input=text, model="text-embedding-3-small")
            return response.data[0].embedding
        except Exception as e:
            print(f"Error getting embedding: {e}")
            return None
    return None

# 🔹 Helper: search Milvus for similar vectors
def search_milvus(query_vector, limit=3):
    if not milvus_available or not collection:
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
        
        return results[0] if results else []
    except Exception as e:
        print(f"Error searching Milvus: {e}")
        return []

# 🔹 Helper: insert data into Milvus
def insert_to_milvus(text: str, metadata: str = ""):
    if not milvus_available or not collection:
        return False
    
    try:
        # Get embedding for the text
        embedding = get_embedding(text)
        if not embedding:
            return False
        
        # Insert into Milvus
        data = [
            [embedding],  # embedding field
            [text],       # text field
            [metadata]    # metadata field
        ]
        
        collection.insert(data)
        collection.flush()  # Ensure data is written
        return True
    except Exception as e:
        print(f"Error inserting to Milvus: {e}")
        return False

# 🔹 Endpoint 1: Add new data to Milvus vector database
@app.post("/add-data")
async def add_data(request: Request):
    try:
        data = await request.json()
        text = data.get("text", "")
        metadata = data.get("metadata", "")
        
        if not text:
            return {"message": "Error: No text provided", "success": False}
        
        if milvus_available:
            # Store in Milvus vector database
            success = insert_to_milvus(text, metadata)
            if success:
                return {
                    "message": "Data added successfully to Milvus vector database", 
                    "success": True,
                    "storage": "Milvus Vector DB"
                }
            else:
                return {"message": "Failed to add data to Milvus", "success": False}
        else:
            # Fallback to in-memory storage
            knowledge_base.append({
                "text": text,
                "metadata": metadata,
                "id": len(knowledge_base)
            })
            return {
                "message": "Data added to in-memory storage (Milvus not available)", 
                "success": True,
                "storage": "In-Memory"
            }
    except Exception as e:
        return {"message": f"Error: {str(e)}", "success": False}

# 🔹 Endpoint 2: Chat with Milvus vector database
@app.post("/chat")
async def chat(request: Request):
    try:
        data = await request.json()
        user_message = data.get("message", "")

        if not user_message:
            return {"reply": "Please provide a message to chat about."}

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
                    relevant_docs.append(hit.entity.get("text", ""))
                context = " ".join(relevant_docs)
                search_method = "Milvus Vector Search"
        elif not milvus_available and 'knowledge_base' in locals():
            # Fallback to keyword search
            relevant_docs = []
            user_words = user_message.lower().split()
            
            for doc in knowledge_base:
                doc_text = doc["text"].lower()
                if any(word in doc_text for word in user_words if len(word) > 3):
                    relevant_docs.append(doc["text"])
            
            if relevant_docs:
                context = " ".join(relevant_docs[:3])
                search_method = "Keyword Search (Fallback)"

        # Step 3: Combine context + user query
        if context:
            prompt = f"Context from vector database: {context}\n\nUser: {user_message}\n\nAnswer clearly and helpfully based on the context provided."
        else:
            prompt = f"User: {user_message}\n\nAnswer clearly and helpfully."

        # Step 4: Generate LLM response
        try:
            if client:
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt}],
                )
                answer = response.choices[0].message.content
            else:
                # Fallback response when no API key is set
                if context:
                    answer = f"Based on the context from {search_method}: {context[:100]}... I understand you're asking about: {user_message}. This is a demo response since no OpenAI API key is configured."
                else:
                    answer = f"Hello! I received your message: '{user_message}'. This is a demo response since no OpenAI API key is configured. Please add your OpenAI API key to the .env file to get real AI responses."
        except Exception as e:
            error_msg = str(e)
            if "quota" in error_msg.lower() or "insufficient_quota" in error_msg.lower():
                answer = f"⚠️ OpenAI API quota exceeded. Please check your billing details at https://platform.openai.com/account/billing. For now, here's a demo response: I understand you're asking about '{user_message}'. This is a demo response since your OpenAI API quota has been exceeded."
            elif "rate" in error_msg.lower():
                answer = f"⚠️ Rate limit exceeded. Please wait a moment and try again. For now, here's a demo response: I understand you're asking about '{user_message}'."
            else:
                answer = f"I apologize, but I'm having trouble connecting to the AI service. Error: {error_msg}"

        return {
            "reply": answer,
            "search_method": search_method,
            "milvus_available": milvus_available,
            "context_found": bool(context)
        }
        
    except Exception as e:
        return {"reply": f"Error processing chat request: {str(e)}"}

# 🔹 Health check endpoint
@app.get("/")
async def root():
    status = {
        "message": "Milvus Vector Database Backend is running!",
        "openai_client": "Available" if client else "Not available",
        "milvus_status": "Connected" if milvus_available else "Not available",
        "storage_type": "Milvus Vector DB" if milvus_available else "In-Memory Fallback"
    }
    
    if milvus_available and collection:
        try:
            # Get collection statistics
            status["milvus_collection"] = collection.name
            status["total_vectors"] = collection.num_entities
        except:
            status["milvus_collection"] = "Unknown"
            status["total_vectors"] = "Unknown"
    elif not milvus_available:
        status["in_memory_entries"] = len(knowledge_base) if 'knowledge_base' in locals() else 0
    
    return status

# 🔹 Milvus collection info endpoint
@app.get("/milvus-info")
async def milvus_info():
    if not milvus_available:
        return {"error": "Milvus is not available"}
    
    try:
        return {
            "collection_name": collection.name,
            "total_entities": collection.num_entities,
            "schema": {
                "fields": [{"name": field.name, "type": str(field.dtype)} for field in collection.schema.fields]
            },
            "indexes": [{"field": idx.field_name, "type": idx.params} for idx in collection.indexes]
        }
    except Exception as e:
        return {"error": f"Failed to get Milvus info: {str(e)}"}

# 🔹 Add sample data endpoint for testing
@app.post("/add-sample-data")
async def add_sample_data():
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
    
    results = []
    for item in sample_data:
        if milvus_available:
            success = insert_to_milvus(item["text"], item["metadata"])
            results.append({
                "text": item["text"][:50] + "...",
                "success": success,
                "storage": "Milvus" if success else "Failed"
            })
        else:
            knowledge_base.append({
                "text": item["text"],
                "metadata": item["metadata"],
                "id": len(knowledge_base)
            })
            results.append({
                "text": item["text"][:50] + "...",
                "success": True,
                "storage": "In-Memory"
            })
    
    return {
        "message": f"Added {len(sample_data)} sample documents",
        "results": results,
        "storage_type": "Milvus Vector DB" if milvus_available else "In-Memory Fallback"
    }

# 🔹 Test OpenAI endpoint
@app.get("/test-openai")
async def test_openai():
    if client:
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": "Say hello"}],
            )
            return {"status": "success", "response": response.choices[0].message.content}
        except Exception as e:
            return {"status": "error", "error": str(e)}
    else:
        return {"status": "error", "error": "OpenAI client not initialized"}
