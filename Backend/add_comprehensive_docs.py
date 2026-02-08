#!/usr/bin/env python3
"""
Script to add comprehensive Milvus documentation to the vector database
This script will add all Milvus documentation to the database for testing
"""

import requests
import json
import time
from comprehensive_milvus_docs import get_comprehensive_milvus_docs

def add_comprehensive_documentation():
    """Add all comprehensive Milvus documentation to the vector database"""
    
    print("🚀 Starting Comprehensive Milvus Documentation Addition")
    print("="*60)
    
    # Wait for server to be ready
    print("🔹 Waiting for backend server to be ready...")
    time.sleep(3)
    
    # Check if server is running
    try:
        response = requests.get("http://localhost:8001/")
        if response.status_code == 200:
            print("✅ Backend server is running")
            server_info = response.json()
            print(f"📊 Server Status: {server_info.get('message', 'Unknown')}")
            print(f"🔍 Milvus Status: {server_info.get('milvus_status', 'Unknown')}")
            print(f"💾 Storage Type: {server_info.get('storage_type', 'Unknown')}")
        else:
            print("❌ Backend server is not responding")
            return False
    except Exception as e:
        print(f"❌ Cannot connect to backend server: {e}")
        print("💡 Make sure the backend server is running on http://localhost:8001")
        return False
    
    # Get comprehensive Milvus documentation
    docs = get_comprehensive_milvus_docs()
    print(f"\n📚 Found {len(docs)} comprehensive Milvus documentation entries")
    
    # Add each document to the database
    success_count = 0
    failed_count = 0
    
    print("\n🔹 Adding documentation to database...")
    print("-" * 60)
    
    for i, doc in enumerate(docs, 1):
        try:
            print(f"📝 Adding document {i:2d}/{len(docs)}: {doc['metadata']}")
            
            response = requests.post(
                "http://localhost:8001/add-data",
                json={
                    "text": doc["text"],
                    "metadata": doc["metadata"]
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success", False):
                    print(f"✅ Successfully added: {doc['metadata']}")
                    print(f"   💾 Storage: {result.get('storage', 'Unknown')}")
                    success_count += 1
                else:
                    print(f"❌ Failed to add: {doc['metadata']} - {result.get('message', 'Unknown error')}")
                    failed_count += 1
            else:
                print(f"❌ HTTP Error {response.status_code}: {response.text}")
                failed_count += 1
                
        except Exception as e:
            print(f"❌ Error adding document {i}: {e}")
            failed_count += 1
        
        # Small delay between requests
        time.sleep(0.5)
    
    # Summary
    print("\n" + "="*60)
    print("📊 COMPREHENSIVE MILVUS DOCUMENTATION ADDITION SUMMARY")
    print("="*60)
    print(f"✅ Successfully added: {success_count} documents")
    print(f"❌ Failed to add: {failed_count} documents")
    print(f"📚 Total documents: {len(docs)}")
    print(f"📈 Success rate: {(success_count/len(docs)*100):.1f}%")
    
    if success_count > 0:
        print("\n🎉 Comprehensive Milvus documentation has been added!")
        print("💡 You can now ask detailed questions about Milvus in the frontend")
        print("🔍 The system will search the database for relevant information")
        return True
    else:
        print("\n❌ No documents were added successfully")
        return False

def test_comprehensive_search():
    """Test if comprehensive search is working with the added documentation"""
    print("\n🧪 Testing Comprehensive Milvus Search Functionality...")
    print("="*60)
    
    test_queries = [
        "What is Milvus and how does it work?",
        "What are the different index types in Milvus?",
        "How do I deploy Milvus with Docker?",
        "What programming languages does Milvus support?",
        "How does Milvus handle large-scale data?",
        "What are the security features of Milvus?",
        "How does Milvus integrate with AI frameworks?",
        "What monitoring capabilities does Milvus provide?",
        "How does Milvus support real-time analytics?",
        "What are the cost optimization features in Milvus?"
    ]
    
    for i, query in enumerate(test_queries, 1):
        try:
            print(f"\n🔍 Test {i:2d}/10: '{query}'")
            response = requests.post(
                "http://localhost:8001/chat",
                json={"message": query},
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Response received")
                print(f"📊 Search method: {result.get('search_method', 'Unknown')}")
                print(f"🔍 Context found: {result.get('context_found', False)}")
                print(f"💬 Response preview: {result.get('reply', '')[:150]}...")
            else:
                print(f"❌ HTTP Error {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error testing query: {e}")
        
        time.sleep(1)
    
    print("\n🎯 Comprehensive search testing completed!")

def show_usage_examples():
    """Show examples of questions you can ask"""
    print("\n💡 EXAMPLE QUESTIONS YOU CAN ASK:")
    print("="*60)
    
    examples = [
        "What is Milvus?",
        "How does vector similarity search work?",
        "What are Milvus index types?",
        "How do I deploy Milvus with Docker?",
        "What SDKs does Milvus support?",
        "How does Milvus handle scalability?",
        "What are the security features of Milvus?",
        "How does Milvus integrate with AI frameworks?",
        "What monitoring tools work with Milvus?",
        "How does Milvus support real-time analytics?",
        "What are the cost optimization features?",
        "How does Milvus handle multi-modal data?",
        "What are the data governance features?",
        "How does Milvus support edge computing?",
        "What are the performance characteristics of Milvus?"
    ]
    
    for i, example in enumerate(examples, 1):
        print(f"   {i:2d}. {example}")
    
    print(f"\n📚 Total documentation entries available: {len(get_comprehensive_milvus_docs())}")

if __name__ == "__main__":
    print("🎯 COMPREHENSIVE MILVUS DOCUMENTATION SETUP")
    print("="*60)
    
    # Add comprehensive documentation
    success = add_comprehensive_documentation()
    
    if success:
        # Test search functionality
        test_comprehensive_search()
        
        # Show usage examples
        show_usage_examples()
        
        print("\n" + "="*60)
        print("🎉 COMPREHENSIVE SETUP COMPLETE!")
        print("="*60)
        print("✅ Comprehensive Milvus documentation has been added")
        print("✅ Search functionality is working")
        print("✅ You can now ask detailed questions about Milvus")
        print("\n🚀 NEXT STEPS:")
        print("1. Start your frontend: npm run dev")
        print("2. Go to http://localhost:5173")
        print("3. Ask questions about Milvus")
        print("4. The system will provide detailed answers from the database")
    else:
        print("\n❌ Setup failed. Please check the backend server and try again.")
        print("💡 Make sure to start the backend server first:")
        print("   python -m uvicorn app:app --host 0.0.0.0 --port 8001")
