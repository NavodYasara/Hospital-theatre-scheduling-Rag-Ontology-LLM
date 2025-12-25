# 🏥 Intelligent Hospital Theatre Scheduling System

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.29+-red.svg)](https://streamlit.io/)
[![OWL](https://img.shields.io/badge/OWL-Ontology-green.svg)](https://www.w3.org/OWL/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

An **Ontology-Guided RAG (Retrieval-Augmented Generation) System** that combines semantic web technologies with modern AI to intelligently manage hospital operating theatre schedules, detect conflicts, and provide natural language assistance.

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Key Features](#-key-features)
- [System Architecture](#-system-architecture)
- [Technology Stack](#-technology-stack)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Usage Guide](#-usage-guide)
- [Project Structure](#-project-structure)
- [Configuration](#-configuration)
- [Example Queries](#-example-queries)
- [Troubleshooting](#-troubleshooting)
- [License](#-license)

---

## 🎯 Overview

This system addresses the complex challenge of **hospital operating theatre scheduling** by combining:

- **Semantic Knowledge Representation** using OWL ontologies
- **Automated Reasoning** with SWRL rules and Pellet reasoner
- **Intelligent Retrieval** via RAG pipeline with vector embeddings
- **Natural Language Interface** powered by local LLMs (Ollama)

The system can detect scheduling conflicts, answer natural language queries about schedules, and provide intelligent recommendations—all while maintaining a formal knowledge base that ensures consistency and enables advanced reasoning.

### 🎓 Academic Context

This project demonstrates the integration of:

- **Symbolic AI** (ontology-based reasoning)
- **Neural AI** (embeddings and large language models)
- **Hybrid Retrieval** (vector search + knowledge graph queries)

Perfect for semantic web, knowledge engineering, or AI coursework.

---

## ✨ Key Features

### 🧠 Intelligent Scheduling

- **Ontology-based knowledge representation** using OWL 2
- **Formal reasoning** with SWRL rules
- **Multi-entity management**: Surgeons, Theatres, Patients, Equipment, Timeslots

### 🔍 Conflict Detection

- **Surgeon double-bookings** - Same surgeon scheduled for overlapping surgeries
- **Theatre conflicts** - Same theatre booked for multiple surgeries simultaneously
- **Specialization mismatches** - Surgeons operating outside their specialty

### 💬 Natural Language Interface

- **Chat-based interaction** for querying schedules
- **Context-aware responses** using RAG pipeline
- **Intelligent suggestions** for optimal scheduling

### 📊 Comprehensive UI

- **Real-time conflict scanning** with severity assessment
- **Multiple schedule views** (by surgeon, theatre, or timeslot)
- **Interactive schedule management** with validation
- **System status dashboard** with live metrics

### 🔄 RAG Pipeline

- **Vector similarity search** using ChromaDB
- **Semantic embeddings** via sentence-transformers
- **Hybrid retrieval** combining vector search with ontology queries
- **Context-aware generation** using local LLMs

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Streamlit UI Layer                       │
│  (Chat Interface | Conflict Detection | Schedule Views)     │
└────────────────────────┬────────────────────────────────────┘
                         │
         ┌───────────────┼───────────────┐
         │               │               │
         ▼               ▼               ▼
┌────────────────┐ ┌──────────┐ ┌─────────────────┐
│  RAG Retriever │ │ Conflict │ │ Ontology Manager│
│                │ │ Detector │ │                 │
│ • Vector Search│ │          │ │ • CRUD Ops      │
│ • Entity Extract│ │ • SWRL   │ │ • Queries       │
│ • Context Rank │ │ • Pellet │ │ • Persistence   │
└────────┬───────┘ └────┬─────┘ └────────┬────────┘
         │              │                 │
         ▼              ▼                 ▼
┌────────────────┐ ┌──────────┐ ┌─────────────────┐
│   ChromaDB     │ │ Reasoner │ │  OWL Ontology   │
│ Vector Store   │ │  Engine  │ │  (hospital.owl) │
└────────────────┘ └──────────┘ └─────────────────┘
         │                                │
         ▼                                ▼
┌────────────────┐              ┌─────────────────┐
│ Sentence       │              │ Knowledge Base  │
│ Transformers   │              │ • Classes       │
│ (Embeddings)   │              │ • Properties    │
└────────────────┘              │ • Instances     │
                                │ • SWRL Rules    │
         ┌──────────────────────┴─────────────────┘
         │
         ▼
┌─────────────────┐
│  Ollama LLM     │
│  (llama3.1:8b)  │
└─────────────────┘
```

---

## 🛠️ Technology Stack

| Component       | Technology            | Purpose                       |
| --------------- | --------------------- | ----------------------------- |
| **Backend**     | Python 3.11+          | Core application logic        |
| **Ontology**    | OWL 2 (owlready2)     | Knowledge representation      |
| **Reasoning**   | Pellet Reasoner       | Automated inference           |
| **Vector DB**   | ChromaDB              | Embedding storage & retrieval |
| **Embeddings**  | sentence-transformers | Text vectorization            |
| **LLM**         | Ollama (llama3.1:8b)  | Natural language generation   |
| **UI**          | Streamlit             | Web interface                 |
| **Data Format** | RDF/XML, JSON         | Serialization                 |

---

## 📦 Prerequisites

Before installation, ensure you have:

### Required Software

- **Python 3.11 or higher** ([Download](https://www.python.org/downloads/))
- **Ollama** ([Download](https://ollama.ai/)) - Local LLM server
- **Git** (for cloning the repository)

### System Requirements

- **RAM**: Minimum 8GB (16GB recommended for larger models)
- **Storage**: ~5GB for models and dependencies
- **OS**: Windows, macOS, or Linux

---

## 🚀 Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/NavodYasara/hospital-theatre-scheduling-rag.git
cd hospital-theatre-scheduling-rag
```

### Step 2: Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Python Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**If `requirements.txt` doesn't exist, install manually:**

```bash
pip install owlready2==0.45
pip install streamlit==1.29.0
pip install chromadb==0.4.18
pip install sentence-transformers==2.2.2
pip install requests==2.31.0
pip install numpy
pip install torch
```

### Step 4: Install and Setup Ollama

#### Windows/macOS:

1. Download Ollama from [ollama.ai](https://ollama.ai/)
2. Install and run the application
3. Pull the required model:

```bash
ollama pull llama3.1:8b
```

#### Linux:

```bash
curl -fsSL https://ollama.ai/install.sh | sh
ollama serve &
ollama pull llama3.1:8b
```

**Verify Ollama is running:**

```bash
curl http://localhost:11434/api/tags
```

### Step 5: Initialize the Ontology

Run the ontology initialization script to create the knowledge base:

```bash
python ontology/main.py
```

This will:

- Create the OWL ontology file (`ontology/hospital.owl`)
- Add sample data (surgeons, theatres, timeslots, surgeries)
- Run the reasoner to infer relationships
- Detect any initial conflicts

**Expected output:**

```
✅ Ontology saved successfully to ontology/hospital.owl
✅ Reasoner executed successfully!

=== CONFLICT DETECTION RESULTS ===
📋 Scheduling Conflicts: 0
⚙️  Equipment Conflicts: 0
🏥 Theatre Conflicts: 0
🔍 Specialization Mismatches: 0
🛏️  Recovery Schedules: 6
```

---

## ⚡ Quick Start

### 1. Start the Application

```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

### 2. Explore the Interface

The UI has **4 main tabs**:

#### 💬 **Chat Assistant**

- Ask natural language questions about schedules
- Get intelligent responses based on the knowledge base
- View source documents used for answers

**Try asking:**

- "Is Dr. Smith available tomorrow at 9 AM?"
- "Show me all surgeries scheduled for today"
- "Which surgeons specialize in cardiology?"

#### 🔍 **Conflict Detection**

- Click "Scan for Conflicts" to analyze the schedule
- View detected conflicts by type
- See severity levels and suggested resolutions

#### 📊 **Schedule View**

- View schedules by Surgeon, Theatre, or Timeslot
- See all scheduled surgeries with details
- Check resource allocation

#### ➕ **Add Schedule**

- Schedule new surgeries
- Select surgeon, theatre, and timeslot
- Automatic validation before adding

---

## 📖 Usage Guide

### Managing Schedules

#### Adding a New Surgery

1. Go to the **"Add Schedule"** tab
2. Fill in surgery details:
   - Surgery name (e.g., `Knee_Arthroscopy`)
   - Select surgeon from dropdown
   - Choose theatre type
   - Select available timeslot
   - Set estimated duration
   - Mark as emergency if needed
3. Click **"Add Surgery"**
4. System validates and checks for conflicts
5. Go to **"Conflict Detection"** to verify

#### Querying via Chat

The chat interface understands various query types:

**Availability Queries:**

```
"Is Dr. Smith available at 10:00 AM?"
"Which theatres are free this afternoon?"
```

**Schedule Queries:**

```
"Show me Dr. Johnson's schedule"
"What surgeries are in the Cardio Theatre?"
"List all emergency surgeries"
```

**Conflict Queries:**

```
"Are there any scheduling conflicts?"
"Check if the Neuro Theatre is double-booked"
```

**Information Queries:**

```
"What equipment is needed for cardiac bypass surgery?"
"Which surgeons work in the Ortho Theatre?"
```

### Understanding Conflicts

The system detects 4 types of conflicts:

1. **Surgeon Double-Booking** (HIGH severity)

   - Same surgeon scheduled for overlapping surgeries
   - Resolution: Reschedule one surgery or assign different surgeon

2. **Theatre Conflict** (HIGH severity)

   - Same theatre booked for multiple surgeries simultaneously
   - Resolution: Move to different theatre or adjust timeslot

3. **Equipment Conflict** (MEDIUM severity)

   - Same equipment needed by concurrent surgeries
   - Resolution: Reschedule or arrange backup equipment

4. **Specialization Mismatch** (MEDIUM severity)
   - Surgeon operating outside their specialty theatre
   - Resolution: Assign specialized surgeon or relocate surgery

---

## 📁 Project Structure

```
hospital-theatre-scheduling-rag/
│
├── app.py                          # Main Streamlit application
├── initialize_data.py              # Data initialization script
├── README.md                       # This file
├── requirements.txt                # Python dependencies
├── .gitignore                      # Git ignore rules
│
├── ontology/                       # Ontology layer
│   ├── main.py                     # Ontology creation & initialization
│   ├── ontology_manager.py         # CRUD operations on ontology
│   ├── reasoner.py                 # Conflict detection & reasoning
│   └── hospital.owl                # OWL ontology file (generated)
│
├── rag/                            # RAG pipeline
│   ├── retriever.py                # Hybrid retrieval logic
│   ├── vector_store.py             # ChromaDB interface
│   └── embeddings.py               # Sentence transformer embeddings
│
├── llm/                            # LLM integration
│   ├── ollama_client.py            # Ollama API client
│   └── prompt_templates.py         # System prompts & templates
│
├── utils/                          # Utilities
│   ├── ontology_to_text.py         # Convert ontology to text
│   └── validators.py               # Input validation
│
├── data/                           # Sample data
│   └── sample_schedules.json       # Sample scheduling data
│
├── chroma_db/                      # Vector database (generated)
│   └── ...                         # ChromaDB persistence
│
└── test ontologies/                # Test scripts
    └── ...                         # Experimental ontology code
```

---

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root (optional):

```env
# Paths
ONTOLOGY_PATH=ontology/hospital.owl
CHROMA_DB_PATH=chroma_db

# Ollama Settings
OLLAMA_BASE_URL=http://localhost:11434
DEFAULT_MODEL=llama3.1:8b

# Embedding Settings
EMBEDDING_MODEL=all-MiniLM-L6-v2

# RAG Settings
TOP_K_RESULTS=5
```

### Changing the LLM Model

The system supports multiple Ollama models:

**Available models:**

- `llama3.1:8b` (default, recommended)
- `mistral`
- `phi3:mini` (faster, smaller)
- `llama2`
- `qwen:1.8b` (lightweight)

**To change model:**

1. Pull the model: `ollama pull <model-name>`
2. Select from dropdown in the UI sidebar
3. Or modify `app.py` line 46:
   ```python
   llm_client = OllamaClient(model="mistral")
   ```

### Customizing the Ontology

Edit `ontology/main.py` to:

- Add new entity types (e.g., Nurses, Medications)
- Define new properties
- Add more SWRL rules
- Modify sample data

After changes, run:

```bash
python ontology/main.py
```

---

## 💡 Example Queries

### Availability Checks

```
✅ "Is Dr. Smith available tomorrow at 9 AM?"
✅ "Check if the Cardio Theatre is free at 14:00"
✅ "Can we schedule a surgery at 10:45?"
```

### Schedule Information

```
✅ "Show me all surgeries for Dr. Johnson"
✅ "What's scheduled in the Neuro Theatre today?"
✅ "List all emergency surgeries"
✅ "Which patients are in Recovery Room A?"
```

### Resource Queries

```
✅ "What equipment is needed for brain surgery?"
✅ "Which surgeons specialize in cardiology?"
✅ "Show me all available timeslots"
```

### Conflict Detection

```
✅ "Are there any scheduling conflicts?"
✅ "Check for surgeon double-bookings"
✅ "Is any equipment double-booked?"
```

### Recommendations

```
✅ "Suggest a time slot for an emergency appendectomy"
✅ "When can we schedule a hip replacement surgery?"
✅ "Find the best time for Dr. Williams to operate"
```

---

## 🐛 Troubleshooting

### Common Issues

#### 1. **Ollama Connection Error**

**Error:** `❌ Cannot connect to Ollama`

**Solution:**

```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# If not running, start it:
# Windows/macOS: Open Ollama app
# Linux:
ollama serve
```

#### 2. **Model Not Found**

**Error:** `⚠️ Model 'llama3.1:8b' not found`

**Solution:**

```bash
ollama pull llama3.1:8b
```

#### 3. **Ontology File Not Found**

**Error:** `FileNotFoundError: ontology/hospital.owl`

**Solution:**

```bash
python ontology/main.py
```

#### 4. **ChromaDB Errors**

**Error:** `Error adding documents to vector store`

**Solution:**

```bash
# Delete and recreate vector database
rm -rf chroma_db/
# Restart the app
streamlit run app.py
```

#### 5. **Import Errors**

**Error:** `ModuleNotFoundError: No module named 'owlready2'`

**Solution:**

```bash
pip install -r requirements.txt
# Or install individually:
pip install owlready2 streamlit chromadb sentence-transformers
```

#### 6. **Java Not Found (Pellet Reasoner)**

**Error:** `Java not found` when running reasoner

**Solution:**

- Install Java JDK 11 or higher
- Add Java to PATH
- Verify: `java -version`

#### 7. **Streamlit Port Already in Use**

**Error:** `Address already in use`

**Solution:**

```bash
# Use different port
streamlit run app.py --server.port 8502
```

### Performance Issues

**Slow response times:**

- Use smaller LLM model (e.g., `phi3:mini`)
- Reduce `TOP_K_RESULTS` in RAG retrieval
- Ensure sufficient RAM available

**High memory usage:**

- Close other applications
- Use lighter embedding model
- Reduce batch sizes

---

## 🔬 Advanced Usage

### Running the Reasoner Manually

```python
from ontology.ontology_manager import OntologyManager
from ontology.reasoner import ConflictDetector

# Initialize
onto_mgr = OntologyManager("ontology/hospital.owl")
detector = ConflictDetector(onto_mgr)

# Detect conflicts
conflicts = detector.detect_all_conflicts()
print(conflicts)
```

### Querying the Ontology Programmatically

```python
from ontology.ontology_manager import OntologyManager

onto_mgr = OntologyManager("ontology/hospital.owl")

# Get all surgeons
surgeons = onto_mgr.get_all_surgeons()
for surgeon in surgeons:
    print(f"{surgeon.name}: {surgeon.has_license_number}")

# Get surgeon schedule
schedule = onto_mgr.get_surgeon_schedule("Dr_Smith")
print(schedule)
```

### Custom RAG Queries

```python
from rag.retriever import RAGRetriever
from ontology.ontology_manager import OntologyManager

onto_mgr = OntologyManager("ontology/hospital.owl")
retriever = RAGRetriever(onto_mgr)
retriever.initialize()

# Retrieve context
context = retriever.retrieve_context("brain surgery equipment", top_k=3)
print(retriever.get_formatted_context(context))
```

---



---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **owlready2** - Python library for OWL ontologies
- **ChromaDB** - Vector database for embeddings
- **Ollama** - Local LLM inference
- **Streamlit** - Web UI framework
- **sentence-transformers** - Text embeddings

---


## 🎓 Academic Use

This project is suitable for:

- Semantic Web & Knowledge Engineering courses
- AI/ML coursework
- Healthcare Informatics projects
- RAG system demonstrations
- Hybrid AI research

**Citation:**

```bibtex
@software{hospital_scheduling_rag,
  author = {Yasara, Navod},
  title = {Intelligent Hospital Theatre Scheduling System},
  year = {2024},
  url = {https://github.com/NavodYasara/hospital-theatre-scheduling-rag}
}
```

---

