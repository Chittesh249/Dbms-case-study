#!/usr/bin/env python3
"""
Comprehensive Milvus Documentation Dataset
This file contains extensive Milvus documentation to be added to the vector database
"""

COMPREHENSIVE_MILVUS_DOCS = [
    {
        "text": "Milvus is an open-source vector database designed for AI applications. It provides high-performance similarity search and supports various vector operations. Milvus is built for scalability and can handle billions of vectors with sub-second search latency. It's particularly useful for applications like recommendation systems, image search, natural language processing, and machine learning workflows.",
        "metadata": "milvus_overview"
    },
    {
        "text": "Vector databases like Milvus store data as high-dimensional vectors and enable fast similarity search using algorithms like cosine similarity, Euclidean distance, and dot product. This makes them perfect for AI applications that need to find similar content based on meaning rather than exact matches. Unlike traditional databases that use exact matching, vector databases understand semantic relationships between data points.",
        "metadata": "vector_database_concept"
    },
    {
        "text": "Milvus supports multiple index types including IVF_FLAT, IVF_SQ8, IVF_PQ, HNSW, and ANNOY. IVF_FLAT provides the best accuracy but uses more memory, while HNSW offers fast search with good accuracy. IVF_SQ8 and IVF_PQ use quantization to reduce memory usage. ANNOY is good for approximate nearest neighbor search. Each index type has different trade-offs between search speed, memory usage, and accuracy.",
        "metadata": "milvus_index_types"
    },
    {
        "text": "Milvus collections are similar to tables in traditional databases. Each collection has a schema that defines the fields and their data types. The primary field is typically an auto-incrementing ID, and vector fields store the actual vector data. Collections can also have scalar fields for metadata. You can create collections with different vector dimensions depending on your embedding model.",
        "metadata": "milvus_collections"
    },
    {
        "text": "Milvus supports various distance metrics for similarity search including L2 (Euclidean distance), IP (Inner Product), and COSINE similarity. COSINE similarity is often preferred for text embeddings as it measures the angle between vectors regardless of their magnitude. L2 distance measures the straight-line distance between vectors. IP is useful when vector magnitudes are important.",
        "metadata": "milvus_distance_metrics"
    },
    {
        "text": "Milvus can be deployed in different modes: standalone mode for development and testing, and distributed mode for production. Standalone mode uses SQLite for metadata storage, while distributed mode uses MySQL or PostgreSQL for metadata and MinIO or S3 for object storage. Docker deployment is the easiest way to get started with Milvus.",
        "metadata": "milvus_deployment_modes"
    },
    {
        "text": "Milvus provides Python, Java, Go, and Node.js SDKs for easy integration. The Python SDK (pymilvus) is the most popular and provides a simple API for connecting to Milvus, creating collections, inserting vectors, and performing similarity searches. The SDK handles connection management, retries, and error handling automatically.",
        "metadata": "milvus_sdks"
    },
    {
        "text": "Milvus supports real-time search and can handle both batch and streaming data ingestion. It provides automatic load balancing and can scale horizontally by adding more query nodes. Milvus also supports data persistence and can recover from failures. It can handle millions of queries per second with proper configuration.",
        "metadata": "milvus_scalability"
    },
    {
        "text": "Milvus integrates well with popular AI frameworks and tools. It works with OpenAI embeddings, Hugging Face models, and other embedding services. Milvus is commonly used in RAG (Retrieval-Augmented Generation) applications, recommendation systems, and semantic search engines. It's also compatible with machine learning pipelines and data science workflows.",
        "metadata": "milvus_ai_integration"
    },
    {
        "text": "Milvus provides comprehensive monitoring and observability features. It includes built-in metrics for query performance, memory usage, and system health. Milvus also supports logging and can be integrated with monitoring tools like Prometheus and Grafana. You can monitor collection statistics, query latency, and resource utilization.",
        "metadata": "milvus_monitoring"
    },
    {
        "text": "Milvus supports data partitioning for better performance and organization. You can partition collections based on different criteria and query specific partitions. This is useful for multi-tenant applications or when you want to organize data by categories or time periods. Partitions help improve query performance and data management.",
        "metadata": "milvus_partitioning"
    },
    {
        "text": "Milvus provides data consistency guarantees and supports ACID transactions. It ensures that data is not lost during failures and maintains consistency across distributed deployments. Milvus also supports data backup and recovery operations. The system is designed to be fault-tolerant and resilient.",
        "metadata": "milvus_consistency"
    },
    {
        "text": "Milvus is optimized for both CPU and GPU acceleration. It can leverage GPU resources for faster vector operations and supports various hardware configurations. Milvus also provides memory-efficient storage options and can handle large-scale deployments. Performance can be tuned based on your specific use case and hardware resources.",
        "metadata": "milvus_performance"
    },
    {
        "text": "Milvus supports hybrid search combining vector similarity with scalar filtering. You can filter results based on metadata fields while still using vector similarity for ranking. This enables complex queries that combine semantic search with traditional database filtering. For example, you can search for similar products within a specific price range.",
        "metadata": "milvus_hybrid_search"
    },
    {
        "text": "Milvus provides a web-based management interface called Attu for easy administration. Attu allows you to manage collections, view data, perform searches, and monitor system performance through a user-friendly web interface. It's particularly useful for development and debugging purposes.",
        "metadata": "milvus_attu_interface"
    },
    {
        "text": "Milvus supports various data types including INT8, INT16, INT32, INT64, FLOAT, DOUBLE, VARCHAR, and BOOL. Vector fields can store dense vectors of different dimensions, typically ranging from 64 to 32768 dimensions depending on the embedding model used. The system is flexible and can handle different data types for metadata.",
        "metadata": "milvus_data_types"
    },
    {
        "text": "Milvus provides automatic index building and optimization. It can automatically choose the best index type based on your data characteristics and query patterns. Milvus also supports index updates and can rebuild indexes when data changes significantly. This helps maintain optimal search performance over time.",
        "metadata": "milvus_index_optimization"
    },
    {
        "text": "Milvus supports both synchronous and asynchronous operations. You can perform batch operations for better throughput or use streaming APIs for real-time data ingestion. Milvus also provides connection pooling and supports multiple concurrent connections. This makes it suitable for high-throughput applications.",
        "metadata": "milvus_operations"
    },
    {
        "text": "Milvus is designed for cloud-native deployment and supports containerization with Docker and Kubernetes. It can be deployed on major cloud platforms including AWS, GCP, and Azure. Milvus also provides Helm charts for easy Kubernetes deployment. This makes it easy to scale and manage in cloud environments.",
        "metadata": "milvus_cloud_deployment"
    },
    {
        "text": "Milvus provides comprehensive security features including authentication, authorization, and data encryption. It supports role-based access control and can integrate with external authentication systems. Milvus also supports TLS encryption for secure communication. This ensures that your vector data is protected and access is controlled.",
        "metadata": "milvus_security"
    },
    {
        "text": "Milvus supports multiple programming languages and frameworks. You can use it with Python, Java, Go, Node.js, and other languages. It integrates well with popular machine learning frameworks like TensorFlow, PyTorch, and scikit-learn. This makes it easy to integrate into existing AI and ML workflows.",
        "metadata": "milvus_programming_languages"
    },
    {
        "text": "Milvus provides excellent performance for large-scale vector operations. It can handle billions of vectors with sub-second search latency. The system is optimized for both read and write operations. It supports parallel processing and can utilize multiple CPU cores and GPU resources for faster operations.",
        "metadata": "milvus_large_scale_performance"
    },
    {
        "text": "Milvus supports various embedding models and vector dimensions. It works with OpenAI's text-embedding-3-small (1536 dimensions), text-embedding-3-large (3072 dimensions), and other embedding models. You can also use custom embedding models as long as they produce consistent vector dimensions.",
        "metadata": "milvus_embedding_models"
    },
    {
        "text": "Milvus provides data import and export capabilities. You can import data from various formats including CSV, JSON, and Parquet. The system supports batch import for large datasets and streaming import for real-time data. You can also export data for backup or migration purposes.",
        "metadata": "milvus_data_import_export"
    },
    {
        "text": "Milvus supports time-series data and temporal queries. You can store time-stamped vectors and perform time-based filtering and search. This is useful for applications that need to track changes over time or perform temporal analysis. The system can handle both historical and real-time data.",
        "metadata": "milvus_time_series"
    },
    {
        "text": "Milvus provides comprehensive documentation and community support. It has extensive tutorials, API documentation, and examples. The community is active and provides support through forums, GitHub, and other channels. There are also many third-party tools and integrations available.",
        "metadata": "milvus_documentation_support"
    },
    {
        "text": "Milvus supports multi-modal data including text, images, audio, and video embeddings. You can store different types of embeddings in the same collection or separate collections. The system can handle mixed data types and perform cross-modal searches. This makes it suitable for complex AI applications.",
        "metadata": "milvus_multimodal"
    },
    {
        "text": "Milvus provides data versioning and rollback capabilities. You can maintain multiple versions of your data and roll back to previous versions if needed. This is useful for A/B testing, model versioning, and data governance. The system tracks changes and maintains data lineage.",
        "metadata": "milvus_data_versioning"
    },
    {
        "text": "Milvus supports federated search across multiple collections or databases. You can perform searches that span multiple data sources and combine results. This is useful for applications that need to search across different domains or data types. The system can handle complex query routing and result aggregation.",
        "metadata": "milvus_federated_search"
    },
    {
        "text": "Milvus provides machine learning model integration and serving capabilities. You can deploy and serve ML models alongside your vector database. The system supports model versioning, A/B testing, and can handle model updates without downtime. This makes it a complete platform for AI applications.",
        "metadata": "milvus_ml_integration"
    },
    {
        "text": "Milvus supports real-time analytics and streaming data processing. You can process data streams in real-time and update your vector database continuously. The system supports event-driven architectures and can handle high-throughput data ingestion. This makes it suitable for real-time AI applications.",
        "metadata": "milvus_real_time_analytics"
    },
    {
        "text": "Milvus provides data governance and compliance features. It supports data lineage tracking, audit logging, and compliance reporting. The system can help you meet regulatory requirements and maintain data quality. It also supports data retention policies and automated cleanup.",
        "metadata": "milvus_data_governance"
    },
    {
        "text": "Milvus supports edge computing and distributed deployments. You can deploy Milvus on edge devices and synchronize data with central servers. The system supports offline operation and can handle network interruptions gracefully. This makes it suitable for IoT and edge AI applications.",
        "metadata": "milvus_edge_computing"
    },
    {
        "text": "Milvus provides cost optimization features for cloud deployments. It supports auto-scaling, resource optimization, and cost monitoring. The system can automatically adjust resources based on workload and help you optimize cloud costs. It also supports multi-cloud deployments for redundancy.",
        "metadata": "milvus_cost_optimization"
    }
]

def get_comprehensive_milvus_docs():
    """Return the comprehensive Milvus documentation"""
    return COMPREHENSIVE_MILVUS_DOCS

def get_doc_count():
    """Return the number of documentation entries"""
    return len(COMPREHENSIVE_MILVUS_DOCS)

if __name__ == "__main__":
    print(f"📚 Comprehensive Milvus Documentation Dataset")
    print(f"📊 Total entries: {get_doc_count()}")
    print(f"🔍 Topics covered:")
    for i, doc in enumerate(COMPREHENSIVE_MILVUS_DOCS, 1):
        print(f"   {i:2d}. {doc['metadata']}")
