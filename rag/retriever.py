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
        1. Detect query intent (list all vs specific entity)
        2. Vector similarity search
        3. Ontology-based factual queries
        """
        if not self.is_initialized:
            self.initialize()
        
        # Detect query intent
        query_intent = self._detect_intent(user_query)
        
        # Vector search
        vector_results = self.vector_store.query(user_query, n_results=top_k)
        
        # Extract entities from query
        entities = self._extract_entities(user_query)
        
        # Query ontology for additional facts
        ontology_facts = self._query_ontology(entities, query_intent)
        
        # Format sources
        sources = []
        if vector_results['documents'] and vector_results['documents'][0]:
            sources = vector_results['documents'][0]
        
        # Combine results
        combined_context = {
            'vector_results': sources,
            'ontology_facts': ontology_facts,
            'sources': sources,
            'entities': entities,
            'intent': query_intent
        }
        
        return combined_context
    
    def _detect_intent(self, query: str) -> Dict:
        """Detect query intent to determine what information to retrieve"""
        query_lower = query.lower()
        
        intent = {
            'list_patients': False,
            'list_surgeons': False,
            'list_surgeries': False,
            'list_theatres': False,
            'list_timeslots': False,
            'query_date': None,
            'query_theatre': None
        }
        
        # Detect list/show/get all queries
        list_keywords = ['list', 'show', 'give', 'names', 'all', 'what', 'which', 'who', 'any']
        has_list_keyword = any(kw in query_lower for kw in list_keywords)
        
        if has_list_keyword:
            if 'patient' in query_lower:
                intent['list_patients'] = True
            if 'surgeon' in query_lower or 'doctor' in query_lower:
                intent['list_surgeons'] = True
            if 'surgery' in query_lower or 'surgeries' in query_lower or 'operation' in query_lower:
                intent['list_surgeries'] = True
            if 'theatre' in query_lower or 'theater' in query_lower:
                intent['list_theatres'] = True
            if 'timeslot' in query_lower or 'time slot' in query_lower or 'schedule' in query_lower:
                intent['list_timeslots'] = True
        
        # Parse date from query
        date = self._parse_date_from_query(query)
        if date:
            intent['query_date'] = date
        
        # Extract theatre name if mentioned
        for theatre in self.onto_mgr.get_all_theatres():
            theatre_variants = [
                theatre.name.lower(),
                theatre.name.lower().replace('_', ' '),
                theatre.name.lower().replace('_theatre', '').replace('_', ' ')
            ]
            if any(variant in query_lower for variant in theatre_variants):
                intent['query_theatre'] = theatre.name
                break
        
        return intent
    
    def _parse_date_from_query(self, query: str) -> str:
        """Parse date from natural language query and return YYYY-MM-DD format"""
        import re
        from datetime import datetime, timedelta
        
        query_lower = query.lower()
        
        # Check for specific date formats
        # Format: YYYY-MM-DD
        iso_date = re.search(r'(\d{4})-(\d{2})-(\d{2})', query)
        if iso_date:
            return iso_date.group(0)
        
        # Format: DD/MM/YYYY or MM/DD/YYYY
        slash_date = re.search(r'(\d{1,2})[/-](\d{1,2})[/-](\d{4})', query)
        if slash_date:
            try:
                # Try DD/MM/YYYY first
                day, month, year = slash_date.groups()
                return f"{year}-{month.zfill(2)}-{day.zfill(2)}"
            except:
                pass
        
        # Parse relative dates
        today = datetime.now()
        
        #"today"
        if 'today' in query_lower:
            return today.strftime('%Y-%m-%d')
        
        # "tomorrow"
        if 'tomorrow' in query_lower:
            tomorrow = today + timedelta(days=1)
            return tomorrow.strftime('%Y-%m-%d')
        
        # "yesterday"
        if 'yesterday' in query_lower:
            yesterday = today - timedelta(days=1)
            return yesterday.strftime('%Y-%m-%d')
        
        # Parse month names with day numbers
        months = {
            'january': 1, 'february': 2, 'march': 3, 'april': 4,
            'may': 5, 'june': 6, 'july': 7, 'august': 8,
            'september': 9, 'october': 10, 'november': 11, 'december': 12,
            'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'may': 5, 'jun': 6,
            'jul': 7, 'aug': 8, 'sep': 9, 'oct': 10, 'nov': 11, 'dec': 12
        }
        
        for month_name, month_num in months.items():
            # Pattern: "27th december", "december 27", "27 december"
            pattern1 = rf'(\d{{1,2}})(?:st|nd|rd|th)?\s+{month_name}'
            pattern2 = rf'{month_name}\s+(\d{{1,2}})'
            
            match1 = re.search(pattern1, query_lower)
            match2 = re.search(pattern2, query_lower)
            
            if match1 or match2:
                day = int(match1.group(1) if match1 else match2.group(1))
                # Determine year (use current year or next year if date has passed)
                year = today.year
                test_date = datetime(year, month_num, day)
                if test_date < today and (test_date.month < today.month):
                    year += 1
                
                return f"{year}-{month_num:02d}-{day:02d}"
        
        return None

    
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
        
        # Extract patient names
        for patient in self.onto_mgr.get_all_patients():
            if patient.name.lower().replace('_', ' ') in query_lower:
                entities['patients'].append(patient.name)
        
        return entities
    
    def _query_ontology(self, entities: Dict, intent: Dict = None) -> Dict:
        """Query ontology for factual information about extracted entities or all entities based on intent"""
        facts = {}
        
        # Handle list-all intents
        if intent:
            # List all patients
            if intent.get('list_patients'):
                all_patients = self.onto_mgr.get_all_patients()
                if all_patients:
                    patient_names = [p.name for p in all_patients]
                    facts['All Patients'] = {
                        'type': 'patient_list',
                        'count': len(patient_names),
                        'names': patient_names,
                        'details': [self.onto_mgr.get_patient_info(p.name) for p in all_patients]
                    }
            
            # List all surgeons
            if intent.get('list_surgeons'):
                all_surgeons = self.onto_mgr.get_all_surgeons()
                if all_surgeons:
                    surgeon_info = []
                    for s in all_surgeons:
                        license = s.has_license_number[0] if s.has_license_number else 'N/A'
                        theatre = s.works_in_theatre[0].name if s.works_in_theatre else 'N/A'
                        surgeon_info.append(f"{s.name} (License: {license}, Theatre: {theatre})")
                    facts['All Surgeons'] = {
                        'type': 'surgeon_list',
                        'count': len(all_surgeons),
                        'names': [s.name for s in all_surgeons],
                        'details': surgeon_info
                    }
            
            # List all surgeries (with optional date/theatre filtering)
            if intent.get('list_surgeries') or intent.get('query_date') or intent.get('query_theatre'):
                # Check if we need date/theatre specific query
                query_date = intent.get('query_date')
                query_theatre = intent.get('query_theatre')
                
                if query_date and query_theatre:
                    # Specific date AND theatre
                    surgeries = self.onto_mgr.get_theatre_schedule_by_date(query_theatre, query_date)
                    facts[f'Surgeries at {query_theatre} on {query_date}'] = {
                        'type': 'surgery_list_filtered',
                        'count': len(surgeries),
                        'date': query_date,
                        'theatre': query_theatre,
                        'details': surgeries
                    }
                elif query_date:
                    # Specific date only
                    surgeries = self.onto_mgr.get_surgeries_by_date(query_date)
                    facts[f'Surgeries on {query_date}'] = {
                        'type': 'surgery_list_filtered',
                        'count': len(surgeries),
                        'date': query_date,
                        'details': surgeries
                    }
                elif query_theatre:
                    # Specific theatre only (all dates)
                    schedule = self.onto_mgr.get_theatre_schedule(query_theatre)
                    facts[f'Surgeries at {query_theatre}'] = {
                        'type': 'theatre_schedule',
                        'count': len(schedule),
                        'theatre': query_theatre,
                        'details': schedule
                    }
                elif intent.get('list_surgeries'):
                    # List all surgeries
                    all_surgeries = self.onto_mgr.get_all_surgeries()
                    if all_surgeries:
                        surgery_info = []
                        for s in all_surgeries:
                            surgeon = s.performs_operation[0].name if s.performs_operation else 'N/A'
                            theatre = s.requires_theatre_type[0].name if s.requires_theatre_type else 'N/A'
                            surgery_info.append(f"{s.name} (Surgeon: {surgeon}, Theatre: {theatre})")
                        facts['All Surgeries'] = {
                            'type': 'surgery_list',
                            'count': len(all_surgeries),
                            'names': [s.name for s in all_surgeries],
                            'details': surgery_info
                        }
        
        # Get specific surgeon facts
        for surgeon_name in entities['surgeons']:
            schedule = self.onto_mgr.get_surgeon_schedule(surgeon_name)
            facts[surgeon_name] = {
                'type': 'surgeon',
                'schedule': schedule
            }
        
        # Get specific theatre facts
        for theatre_name in entities['theatres']:
            schedule = self.onto_mgr.get_theatre_schedule(theatre_name)
            facts[theatre_name] = {
                'type': 'theatre',
                'schedule': schedule
            }
        
        # Get specific patient facts
        for patient_name in entities['patients']:
            patient_info = self.onto_mgr.get_patient_info(patient_name)
            if patient_info:
                facts[patient_name] = {
                    'type': 'patient',
                    'info': patient_info
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
                
                # Handle date-filtered surgery lists
                if data.get('type') == 'surgery_list_filtered':
                    formatted.append(f"  Total Count: {data['count']}")
                    if data['count'] > 0:
                        formatted.append(f"  Details:")
                        for surgery in data['details']:
                            formatted.append(f"    • {surgery['surgery']}: Surgeon={surgery['surgeon']}, Theatre={surgery['theatre']}, Time={surgery['start_time']}-{surgery['end_time']}, Emergency={'Yes' if surgery.get('is_emergency') else 'No'}")
                    else:
                        formatted.append(f"  No surgeries scheduled")
                
                # Handle theatre schedules
                elif data.get('type') == 'theatre_schedule':
                    formatted.append(f"  Total Count: {data['count']}")
                    if data['count'] > 0:
                        formatted.append(f"  Details:")
                        for item in data['details']:
                            formatted.append(f"    • {item['surgery']}: Surgeon={item['surgeon']}, Time={item['start_time']}-{item['end_time']}")
                
                # Handle list data (patient_list, surgeon_list, surgery_list)
                elif data.get('type') in ['patient_list', 'surgeon_list', 'surgery_list']:
                    formatted.append(f"  Total Count: {data['count']}")
                    formatted.append(f"  Names: {', '.join(data['names'])}")
                    if 'details' in data:
                        formatted.append(f"  Details:")
                        if data['type'] == 'patient_list':
                            for patient_detail in data['details']:
                                if patient_detail:
                                    formatted.append(f"    • {patient_detail['patient_name']}: Surgery={patient_detail.get('surgery', 'N/A')}, Ward={patient_detail.get('ward', 'N/A')}, Severity={patient_detail.get('severity', 'N/A')}")
                        else:
                            for detail in data['details']:
                                formatted.append(f"    • {detail}")
                
                # Handle schedule data
                elif 'schedule' in data:
                    for item in data['schedule']:
                        formatted.append(f"  - {item}")
                
                # Handle patient info data
                elif 'info' in data:
                    info = data['info']
                    formatted.append(f"  - Patient Name: {info.get('patient_name', 'N/A')}")
                    formatted.append(f"  - Surgery: {info.get('surgery_details', 'N/A')}")
                    formatted.append(f"  - Surgeon: {info.get('surgeon', 'N/A')}")
                    formatted.append(f"  - Ward: {info.get('ward', 'N/A')}")
                    formatted.append(f"  - Recovery Room: {info.get('recovery_room', 'N/A')}")
                    formatted.append(f"  - Severity: {info.get('severity', 'N/A')}")
                    formatted.append(f"  - Admission Time: {info.get('admission_time', 'N/A')}")
        
        return "\n".join(formatted)
