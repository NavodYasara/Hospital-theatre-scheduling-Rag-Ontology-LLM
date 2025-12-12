from typing import Dict, List
from .vector_store import VectorStore
from utils.ontology_to_text import OntologyToText

class RAGRetriever:
    """
    Main RAG retrieval logic - combines vector search with ontology queries
    """
    
    def __init__(self, ontology_manager):
        self.onto_mgr = ontology_manager
        self.vector_store = VectorStore()
        self.onto_to_text = OntologyToText(ontology_manager)
        self.is_initialized = False
    
    def initialize(self):
        """Convert ontology to text and populate vector store"""
        if self.is_initialized:
            print("ℹ️ RAG already initialized")
            return
        
        print("🔄 Initializing RAG pipeline...")
        
        # Convert ontology to text documents
        documents = self.onto_to_text.convert_all()
        
        if not documents:
            print("⚠️ No documents to add to vector store")
            return
        
        # Add to vector store
        self.vector_store.add_documents(
            documents=[d['text'] for d in documents],
            metadatas=[{'type': d['type'], 'entity_id': d['entity_id']} for d in documents],
            ids=[f"doc_{i}" for i in range(len(documents))]
        )
        
        self.is_initialized = True
        print(f"✅ RAG initialized with {len(documents)} documents")
    
    def retrieve_context(self, user_query: str, top_k: int = 5) -> Dict:
        """
        Retrieve relevant context using hybrid approach:
        1. Vector similarity search
        2. Ontology-based factual queries
        """
        if not self.is_initialized:
            self.initialize()
        
        # Vector search
        vector_results = self.vector_store.query(user_query, n_results=top_k)
        
        # Extract entities from query
        entities = self._extract_entities(user_query)
        
        # Query ontology for additional facts
        ontology_facts = self._query_ontology(entities)
        
        # Format sources
        sources = []
        if vector_results['documents'] and vector_results['documents'][0]:
            sources = vector_results['documents'][0]
        
        # Combine results
        combined_context = {
            'vector_results': sources,
            'ontology_facts': ontology_facts,
            'sources': sources,
            'entities': entities
        }
        
        return combined_context
    
    def _extract_entities(self, query: str) -> Dict:
        """Extract entity names from query (simple keyword matching)"""
        query_lower = query.lower()
        
        entities = {
            'surgeons': [],
            'theatres': [],
            'surgeries': [],
            'patients': []
        }
        
        # Extract surgeon names
        for surgeon in self.onto_mgr.get_all_surgeons():
            if surgeon.name.lower().replace('_', ' ') in query_lower:
                entities['surgeons'].append(surgeon.name)
        
        # Extract theatre names
        for theatre in self.onto_mgr.get_all_theatres():
            if theatre.name.lower().replace('_', ' ') in query_lower:
                entities['theatres'].append(theatre.name)
        
        # Extract surgery names
        for surgery in self.onto_mgr.get_all_surgeries():
            if surgery.name.lower().replace('_', ' ') in query_lower:
                entities['surgeries'].append(surgery.name)
        
        return entities
    
    def _query_ontology(self, entities: Dict) -> Dict:
        """Query ontology for factual information about extracted entities"""
        facts = {}
        
        # Get surgeon facts
        for surgeon_name in entities['surgeons']:
            schedule = self.onto_mgr.get_surgeon_schedule(surgeon_name)
            facts[surgeon_name] = {
                'type': 'surgeon',
                'schedule': schedule
            }
        
        # Get theatre facts
        for theatre_name in entities['theatres']:
            schedule = self.onto_mgr.get_theatre_schedule(theatre_name)
            facts[theatre_name] = {
                'type': 'theatre',
                'schedule': schedule
            }
        
        return facts
    
    def get_formatted_context(self, context: Dict) -> str:
        """Format context as a string for LLM"""
        formatted = []
        
        # Add vector search results
        if context['sources']:
            formatted.append("=== Relevant Knowledge ===")
            for i, source in enumerate(context['sources'][:3], 1):
                formatted.append(f"{i}. {source}")
        
        # Add ontology facts
        if context['ontology_facts']:
            formatted.append("\n=== Ontology Facts ===")
            for entity, data in context['ontology_facts'].items():
                formatted.append(f"\n{entity}:")
                if 'schedule' in data:
                    for item in data['schedule']:
                        formatted.append(f"  - {item}")
        
        return "\n".join(formatted)