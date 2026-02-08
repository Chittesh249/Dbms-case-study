# 🐳 Docker Milvus Setup Guide

## 🚀 **Complete Milvus Implementation with Docker**

This guide will help you set up a complete Milvus vector database implementation using Docker.

## 📋 **Prerequisites**

- Docker installed on your system
- Python 3.8+ installed
- Node.js 16+ installed
- OpenAI API key

## 🐳 **Step 1: Start Milvus with Docker**

### **Option A: Standalone Mode (Recommended for Development)**

```bash
# Pull the latest Milvus image
docker pull milvusdb/milvus:latest

# Start Milvus standalone
docker run -d \
  --name milvus-standalone \
  -p 19530:19530 \
  -p 9091:9091 \
  -v /tmp/milvus:/var/lib/milvus \
  milvusdb/milvus:latest \
  milvus run standalone
```

### **Option B: Using Docker Compose (Recommended for Production)**

Create a `docker-compose.yml` file:

```yaml
version: '3.5'

services:
  etcd:
    container_name: milvus-etcd
    image: quay.io/coreos/etcd:v3.5.5
    environment:
      - ETCD_AUTO_COMPACTION_MODE=revision
      - ETCD_AUTO_COMPACTION_RETENTION=1000
      - ETCD_QUOTA_BACKEND_BYTES=4294967296
      - ETCD_SNAPSHOT_COUNT=50000
    volumes:
      - ${DOCKER_VOLUME_DIRECTORY:-.}/volumes/etcd:/etcd
    command: etcd -advertise-client-urls=http://127.0.0.1:2379 -listen-client-urls http://0.0.0.0:2379 --data-dir /etcd
    healthcheck:
      test: ["CMD", "etcdctl", "endpoint", "health"]
      interval: 30s
      timeout: 20s
      retries: 3

  minio:
    container_name: milvus-minio
    image: minio/minio:RELEASE.2023-03-20T20-16-18Z
    environment:
      MINIO_ACCESS_KEY: minioadmin
      MINIO_SECRET_KEY: minioadmin
    ports:
      - "9001:9001"
      - "9000:9000"
    volumes:
      - ${DOCKER_VOLUME_DIRECTORY:-.}/volumes/minio:/minio_data
    command: minio server /minio_data --console-address ":9001"
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:9000/minio/health/live"]
      interval: 30s
      timeout: 20s
      retries: 3

  standalone:
    container_name: milvus-standalone
    image: milvusdb/milvus:v2.3.3
    command: ["milvus", "run", "standalone"]
    security_opt:
    - seccomp:unconfined
    environment:
      ETCD_ENDPOINTS: etcd:2379
      MINIO_ADDRESS: minio:9000
    volumes:
      - ${DOCKER_VOLUME_DIRECTORY:-.}/volumes/milvus:/var/lib/milvus
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:9091/healthz"]
      interval: 30s
      start_period: 90s
      timeout: 20s
      retries: 3
    ports:
      - "19530:19530"
      - "9091:9091"
    depends_on:
      - "etcd"
      - "minio"

networks:
  default:
    name: milvus
```

Then run:
```bash
docker-compose up -d
```

## 🔍 **Step 2: Verify Milvus is Running**

```bash
# Check if Milvus is running
docker ps | grep milvus

# Check Milvus logs
docker logs milvus-standalone

# Test Milvus connection
docker exec -it milvus-standalone curl -X GET "http://localhost:9091/healthz"
```

## 🚀 **Step 3: Start Your Backend**

```bash
cd Backend
python -m uvicorn app:app --host 0.0.0.0 --port 8000
```

You should see:
```
✅ OpenAI client initialized successfully
🔹 Initializing Milvus Vector Database...
✅ Connected to Milvus successfully
✅ Created new Milvus collection: milvus_chatbot_data
✅ Created vector index for similarity search
✅ Milvus collection loaded and ready for operations
```

## 📚 **Step 4: Add Comprehensive Documentation**

```bash
# Run the comprehensive documentation script
python add_comprehensive_docs.py
```

This will add 30+ comprehensive Milvus documentation entries to your database.

## 🎨 **Step 5: Start Your Frontend**

```bash
cd milvus-implementation
npm run dev
```

## 🧪 **Step 6: Test Your Implementation**

1. Go to http://localhost:5173
2. Ask questions like:
   - "What is Milvus?"
   - "How does vector similarity search work?"
   - "What are the different index types in Milvus?"
   - "How do I deploy Milvus with Docker?"
   - "What programming languages does Milvus support?"

## 🔧 **Troubleshooting**

### **Milvus Connection Issues**

```bash
# Check if Milvus is running
docker ps | grep milvus

# Restart Milvus if needed
docker restart milvus-standalone

# Check Milvus logs
docker logs milvus-standalone
```

### **Port Conflicts**

If port 19530 is already in use:
```bash
# Find what's using the port
netstat -ano | grep 19530

# Kill the process or use a different port
docker run -d --name milvus-standalone -p 19531:19530 milvusdb/milvus:latest milvus run standalone
```

### **Memory Issues**

If you get memory errors:
```bash
# Increase Docker memory limit
# Or use a smaller Milvus configuration
```

## 📊 **Expected Results**

When everything is working correctly:

1. **Backend Status**: `http://localhost:8000/`
   ```json
   {
     "message": "Milvus Vector Database Backend is running!",
     "milvus_status": "Connected",
     "storage_type": "Milvus Vector DB",
     "total_vectors": 30
   }
   ```

2. **Frontend Chat**: Questions about Milvus return detailed, accurate answers

3. **Search Method**: Shows "Milvus Vector Search" in responses

## 🎯 **What You'll Have**

✅ **Full Milvus Vector Database** - Running in Docker
✅ **Comprehensive Documentation** - 30+ Milvus topics
✅ **Vector Similarity Search** - Semantic search capabilities
✅ **Real AI Responses** - OpenAI integration with context
✅ **Production Ready** - Scalable and performant

## 🚀 **Next Steps**

1. **Add More Data**: Use the `/add-data` endpoint to add your own documents
2. **Customize Queries**: Modify the search parameters for your use case
3. **Scale Up**: Use distributed Milvus for production workloads
4. **Monitor Performance**: Use Attu or Prometheus for monitoring

Your complete Milvus implementation is now ready! 🎉
