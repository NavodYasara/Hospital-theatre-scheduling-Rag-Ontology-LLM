import chromadb
from chromadb.config import Settings
from typing import List, Dict
import os

class VectorStore:
    """
    ChromaDB vector database for storing and retrieving embeddings
    """
    
    def __init__(self, collection_name: str = "hospital_knowledge", persist_directory: str = "./chroma_db"):
        """Initialize ChromaDB"""
        self.collection_name = collection_name
        self.persist_directory = persist_directory
        
        # Create persist directory if it doesn't exist
        os.makedirs(persist_directory, exist_ok=True)
        
        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(path=persist_directory)
        
        # Get or create collection
        try:
            self.collection = self.client.get_collection(name=collection_name)
            print(f"✅ Loaded existing collection: {collection_name}")
        except:
            self.collection = self.client.create_collection(name=collection_name)
            print(f"✅ Created new collection: {collection_name}")
    
    def add_documents(self, documents: List[str], metadatas: List[Dict], ids: List[str]):
        """Add documents to vector store"""
        try:
            self.collection.add(
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
            print(f"✅ Added {len(documents)} documents to vector store")
        except Exception as e:
            print(f"❌ Error adding documents: {e}")
    
    def query(self, query_text: str, n_results: int = 5) -> Dict:
        """Query vector store for similar documents"""
        try:
            results = self.collection.query(
                query_texts=[query_text],
                n_results=n_results
            )
            return results
        except Exception as e:
            print(f"❌ Error querying vector store: {e}")
            return {'documents': [[]], 'metadatas': [[]], 'distances': [[]]}
    
    def clear(self):
        """Clear all documents from collection"""
        try:
            self.client.delete_collection(name=self.collection_name)
            self.collection = self.client.create_collection(name=self.collection_name)
            print("✅ Vector store cleared")
        except Exception as e:
            print(f"❌ Error clearing vector store: {e}")
    
    def count(self) -> int:
        """Count documents in collection"""
        return self.collection.count()