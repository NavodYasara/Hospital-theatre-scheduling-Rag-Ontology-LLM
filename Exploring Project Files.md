# Chat Conversation

Note: _This is purely the output of the chat conversation and does not contain any raw data, codebase snippets, etc. used to generate the output._

### User Input

Go through the project files and understand what is it

### Planner Response

I'll help you understand the project by exploring its structure and files. Let me start by examining the project directory.

*Listed directory [PROJECT](file:///d:/MIT/Accedemics%20Level%204/SEM%202/Simantic/PROJECT) *

### Planner Response

Let me explore the key files and directories to understand the project structure:

*Viewed [README.md](file:///d:/MIT/Accedemics%20Level%204/SEM%202/Simantic/PROJECT/README.md) *

*Viewed [app.py](file:///d:/MIT/Accedemics%20Level%204/SEM%202/Simantic/PROJECT/app.py) *

*Listed directory [ontology](file:///d:/MIT/Accedemics%20Level%204/SEM%202/Simantic/PROJECT/ontology) *

*Listed directory [rag](file:///d:/MIT/Accedemics%20Level%204/SEM%202/Simantic/PROJECT/rag) *

*Listed directory [llm](file:///d:/MIT/Accedemics%20Level%204/SEM%202/Simantic/PROJECT/llm) *

*Listed directory [data](file:///d:/MIT/Accedemics%20Level%204/SEM%202/Simantic/PROJECT/data) *

*Listed directory [utils](file:///d:/MIT/Accedemics%20Level%204/SEM%202/Simantic/PROJECT/utils) *

### Planner Response

Now let me examine some key files to better understand the project:

*Viewed [ontology_manager.py](file:///d:/MIT/Accedemics%20Level%204/SEM%202/Simantic/PROJECT/ontology/ontology_manager.py) *

*Viewed [retriever.py](file:///d:/MIT/Accedemics%20Level%204/SEM%202/Simantic/PROJECT/rag/retriever.py) *

*Viewed [ollama_client.py](file:///d:/MIT/Accedemics%20Level%204/SEM%202/Simantic/PROJECT/llm/ollama_client.py) *

*Viewed [sample_schedules.json](file:///d:/MIT/Accedemics%20Level%204/SEM%202/Simantic/PROJECT/data/sample_schedules.json) *

### Planner Response

Let me check a few more important files:

*Viewed [reasoner.py](file:///d:/MIT/Accedemics%20Level%204/SEM%202/Simantic/PROJECT/ontology/reasoner.py) *

*Viewed [ontology_to_text.py](file:///d:/MIT/Accedemics%20Level%204/SEM%202/Simantic/PROJECT/utils/ontology_to_text.py) *

*Viewed [prompt_templates.py](file:///d:/MIT/Accedemics%20Level%204/SEM%202/Simantic/PROJECT/llm/prompt_templates.py) *

### Planner Response

Now let me check the .gitignore and look at the specification document to get a complete picture:

*Viewed [.gitignore](file:///d:/MIT/Accedemics%20Level%204/SEM%202/Simantic/PROJECT/.gitignore) *

### Planner Response

Let me check the other files in the ontology directory:

*Viewed [vector_store.py](file:///d:/MIT/Accedemics%20Level%204/SEM%202/Simantic/PROJECT/rag/vector_store.py) *

*Viewed [embeddings.py](file:///d:/MIT/Accedemics%20Level%204/SEM%202/Simantic/PROJECT/rag/embeddings.py) *

### Planner Response

Perfect! Now I have a comprehensive understanding of the project. Let me create a summary document for you.

## 📊 Project Analysis: Hospital Theatre Scheduling RAG System

Based on my exploration of your project files, here's a comprehensive overview:

---

### 🎯 **Project Overview**

This is an **Intelligent Ontology-Guided RAG (Retrieval-Augmented Generation) System for Hospital Theatre Scheduling**. It's a semantic web application that combines:
- **OWL Ontology** for knowledge representation
- **RAG Pipeline** for intelligent information retrieval
- **LLM Integration** (Ollama) for natural language interaction
- **Streamlit UI** for user interface
- **Conflict Detection** using reasoning

---

### 🏗️ **Architecture & Components**

#### **1. Ontology Layer** (`/ontology`)
- **`hospital.owl`**: OWL ontology file containing the knowledge base
- **`ontology_manager.py`**: Main interface for CRUD operations on the ontology
  - Manages entities: Surgeons, Theatres, Surgeries, Patients, Timeslots
  - Defines classes: Person, Location, ClinicalProcess, Resource
  - Object properties: performs_operation, requires_theatre_type, has_timeslot, etc.
  - Data properties: has_license_number, estimated_duration, is_emergency, etc.

- **`reasoner.py`**: Conflict detection using Pellet reasoner + programmatic validation
  - Detects surgeon double-bookings
  - Detects theatre conflicts
  - Detects equipment conflicts
  - Identifies specialization mismatches
  - Uses SWRL rules for inference

#### **2. RAG Pipeline** (`/rag`)
- **`retriever.py`**: Hybrid retrieval combining vector search + ontology queries
  - Converts user queries to context
  - Extracts entities from queries
  - Retrieves relevant information

- **`vector_store.py`**: ChromaDB integration for vector storage
  - Stores embeddings of ontology entities
  - Performs similarity search

- **`embeddings.py`**: Sentence transformer embeddings
  - Uses `all-MiniLM-L6-v2` model
  - Generates text embeddings

#### **3. LLM Integration** (`/llm`)
- **`ollama_client.py`**: Client for local Ollama LLM server
  - Supports models: llama3.1:8b, mistral, phi3:mini, etc.
  - Generates responses based on context

- **`prompt_templates.py`**: Structured prompts for different tasks
  - System prompt for assistant behavior
  - Availability checking
  - Conflict detection
  - Schedule suggestions

#### **4. Utilities** (`/utils`)
- **`ontology_to_text.py`**: Converts ontology entities to natural language
  - Transforms surgeons, theatres, surgeries, patients, timeslots into text
  - Creates searchable documents for RAG

- **`validators.py`**: Validation utilities

#### **5. Data** (`/data`)
- **`sample_schedules.json`**: Sample hospital data
  - 4 surgeons (Dr_Smith, Dr_Johnson, Dr_Williams, Dr_Brown)
  - 4 theatres (Neuro, Ortho, Cardio, General)
  - 4 timeslots (08:00, 10:45, 14:00, 16:45)
  - 4 surgeries with equipment requirements
  - 4 patients with ward and recovery assignments

#### **6. Main Application** (`app.py`)
- **Streamlit web interface** with 4 tabs:
  1. **💬 Chat Assistant**: Natural language queries about schedules
  2. **🔍 Conflict Detection**: Automated conflict scanning
  3. **📊 Schedule View**: View by surgeon, theatre, or timeslot
  4. **➕ Add Schedule**: Add new surgery schedules

---

### 🔑 **Key Features**

1. **Semantic Knowledge Base**
   - OWL ontology with formal semantics
   - Hierarchical class structure
   - Rich relationships between entities

2. **Intelligent Retrieval**
   - Vector similarity search using ChromaDB
   - Entity extraction from queries
   - Hybrid context retrieval

3. **Conflict Detection**
   - Surgeon double-booking detection
   - Theatre overlap detection
   - Equipment conflict detection
   - Specialization mismatch detection
   - SWRL rules for automated reasoning

4. **Natural Language Interface**
   - Chat with LLM about schedules
   - Ask availability questions
   - Get scheduling recommendations
   - Explain conflicts

5. **Interactive UI**
   - Real-time system status
   - Multiple view options
   - Conflict visualization
   - Schedule management

---

### 📦 **Technology Stack**

- **Backend**: Python
- **Ontology**: OWL (owlready2 library)
- **Reasoning**: Pellet reasoner
- **Vector DB**: ChromaDB
- **Embeddings**: sentence-transformers
- **LLM**: Ollama (local)
- **UI**: Streamlit
- **Data Format**: JSON, RDF/XML

---

### 🎓 **Academic Context**

This appears to be a **Semantic Web / Knowledge Engineering project** for:
- **Course**: Semantics (Level 4, Semester 2)
- **Institution**: MIT (based on path)
- **Topic**: Hospital Theatre Scheduling Support System
- **Approach**: Combining ontologies, RAG, and LLMs for intelligent scheduling

---

### 🔄 **Workflow**

1. **Initialization**:
   - Load OWL ontology
   - Convert entities to text documents
   - Store in ChromaDB vector database
   - Initialize Ollama LLM client

2. **User Query**:
   - User asks question via chat
   - System extracts entities
   - Retrieves relevant context (vector + ontology)
   - LLM generates response

3. **Conflict Detection**:
   - Scan all schedules
   - Check for overlaps and mismatches
   - Display conflicts with severity
   - Suggest resolutions

4. **Schedule Management**:
   - View existing schedules
   - Add new surgeries
   - Validate against constraints

---

### 📝 **Sample Data Entities**

- **Surgeons**: 4 specialists (Neurosurgery, Orthopedics, Cardiothoracic, General)
- **Theatres**: 4 specialized operating rooms
- **Timeslots**: 4 daily slots (150 min each)
- **Surgeries**: Brain surgery, Cardiac bypass, Hip replacement, Appendectomy
- **Equipment**: Neuro_Scope, Cardiac_Monitor, Bypass_Machine, Hip_Prosthesis, etc.

---

### 🎯 **Project Goals**

The system aims to:
1. ✅ Represent hospital scheduling knowledge formally
2. ✅ Enable natural language queries about schedules
3. ✅ Automatically detect scheduling conflicts
4. ✅ Provide intelligent scheduling recommendations
5. ✅ Combine semantic reasoning with modern AI (RAG + LLM)

---

This is a well-structured **hybrid AI system** that demonstrates the integration of **symbolic AI (ontologies)** with **neural AI (embeddings + LLMs)** for a practical healthcare application! 🏥🤖