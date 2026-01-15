# Source Code Structure

## 📁 Overview

Thư mục `src/` chứa toàn bộ source code của FCAJ Chatbot, được tổ chức theo kiến trúc modular và clean code principles.

## 🏗️ Architecture

```
src/
├── main.py              # Entry point - Streamlit UI
├── process_docs.py      # Document processing script
│
├── config/              # Configuration layer
│   ├── __init__.py
│   └── settings.py      # Centralized settings
│
├── services/            # Business logic layer
│   ├── __init__.py
│   └── rag_service.py   # RAG chain implementation
│
└── utils/               # Utility layer
    ├── __init__.py
    └── helpers.py       # Helper functions
```

## 📄 File Descriptions

### main.py
**Purpose**: Application entry point với Streamlit UI

**Responsibilities**:
- Streamlit page configuration
- UI components (sidebar, chat interface)
- Theme management
- User interaction handling
- Response generation orchestration

**Key Functions**:
- `show_loading_page()` - Loading screen
- `get_response(question)` - Get chatbot response

**Usage**:
```bash
streamlit run src/main.py
```

---

### process_docs.py
**Purpose**: Document processing và vectorstore creation

**Responsibilities**:
- Load documents từ `data/` folder
- Split documents into chunks
- Create embeddings
- Build và save FAISS vectorstore

**Key Functions**:
- `process_documents()` - Main processing function

**Usage**:
```bash
python src/process_docs.py
```

---

### config/settings.py
**Purpose**: Centralized configuration management

**Responsibilities**:
- Environment variables loading
- Application settings
- Model configurations
- Path configurations

**Key Settings**:
- `GROQ_API_KEY` - API key
- `EMBEDDING_MODEL` - Embedding model name
- `LLM_MODEL` - LLM model name
- `VECTORSTORE_PATH` - Vector DB path
- `CHUNK_SIZE` - Document chunk size

**Usage**:
```python
from src.config import settings

api_key = settings.GROQ_API_KEY
model = settings.LLM_MODEL
```

---

### services/rag_service.py
**Purpose**: RAG (Retrieval-Augmented Generation) implementation

**Responsibilities**:
- Vectorstore loading
- RAG chain setup
- LLM configuration
- Retriever configuration
- Prompt template management

**Key Functions**:
- `load_vectorstore()` - Load FAISS vectorstore
- `setup_rag_chain()` - Setup complete RAG chain

**Key Components**:
- `SYSTEM_PROMPT` - System prompt cho chatbot
- LangChain RAG pipeline
- MMR retrieval strategy

**Usage**:
```python
from src.services.rag_service import setup_rag_chain

rag_chain = setup_rag_chain()
response = rag_chain.invoke("Your question")
```

---

### utils/helpers.py
**Purpose**: Utility functions và helpers

**Responsibilities**:
- Query normalization
- Image encoding
- Common utilities

**Key Functions**:
- `normalize_query(question)` - Normalize user queries
- `get_base64_image(path)` - Encode images to base64

**Usage**:
```python
from src.utils.helpers import normalize_query

normalized = normalize_query("anh hưng là ai?")
# Returns: "Nguyễn Gia Hưng là ai?"
```

---

## 🔄 Data Flow

```
User Input
    ↓
main.py (UI Layer)
    ↓
normalize_query() (Utils)
    ↓
setup_rag_chain() (Services)
    ↓
load_vectorstore() (Services)
    ↓
RAG Chain Processing
    ↓
LLM Response
    ↓
Display to User
```

## 🎯 Design Principles

### 1. Separation of Concerns
- **UI Layer** (main.py): Chỉ xử lý presentation
- **Business Logic** (services/): Core functionality
- **Configuration** (config/): Settings management
- **Utilities** (utils/): Reusable functions

### 2. Single Responsibility
Mỗi module có một trách nhiệm rõ ràng:
- `main.py` → UI
- `rag_service.py` → RAG logic
- `settings.py` → Configuration
- `helpers.py` → Utilities

### 3. Dependency Injection
Configuration được inject thông qua `settings`:
```python
from src.config import settings

# Không hardcode
model = settings.LLM_MODEL  # ✅

# Thay vì
model = "llama-3.1-8b-instant"  # ❌
```

### 4. Caching
Sử dụng Streamlit caching cho performance:
```python
@st.cache_resource
def load_vectorstore():
    # Chỉ load một lần
    pass
```

## 🔧 Configuration

### Environment Variables
Tất cả config được quản lý trong `config/settings.py`:

```python
class Settings:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    EMBEDDING_MODEL = "sentence-transformers/..."
    LLM_MODEL = "llama-3.1-8b-instant"
    # ...
```

### Customization
Để thay đổi config:

1. **Via .env file** (Recommended):
```env
GROQ_API_KEY=your_key
```

2. **Via settings.py**:
```python
class Settings:
    LLM_TEMPERATURE = 0.2  # Change from 0.1
```

## 🧪 Testing

### Import Test
```python
# Test imports
from src.config import settings
from src.services.rag_service import setup_rag_chain
from src.utils.helpers import normalize_query

print("All imports successful!")
```

### Function Test
```python
# Test normalization
from src.utils.helpers import normalize_query

result = normalize_query("anh hưng")
assert "Nguyễn Gia Hưng" in result
```

## 📝 Adding New Features

### 1. Add New Service
```python
# src/services/new_service.py
from src.config import settings

def new_function():
    # Your logic
    pass
```

### 2. Add New Utility
```python
# src/utils/helpers.py
def new_helper():
    # Your utility
    pass
```

### 3. Update Configuration
```python
# src/config/settings.py
class Settings:
    NEW_SETTING = "value"
```

## 🐛 Debugging

### Enable Debug Mode
```python
# src/config/settings.py
class Settings:
    DEBUG = True
```

### Logging
```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

logger.debug("Debug message")
```

## 📚 Dependencies

### Core
- `streamlit` - Web UI
- `langchain` - LLM framework
- `langchain-groq` - Groq integration
- `langchain-community` - Community integrations

### ML/AI
- `sentence-transformers` - Embeddings
- `faiss-cpu` - Vector search
- `pypdf` - PDF processing

### Utils
- `python-dotenv` - Environment variables

## 🎓 Best Practices

### ✅ Do
- Import từ `src.` modules
- Use `settings` cho configuration
- Add type hints
- Write docstrings
- Cache expensive operations

### ❌ Don't
- Hardcode values
- Import từ parent directories
- Mix UI và business logic
- Commit secrets
- Ignore errors

## 🔗 Related Documentation

- **[../README.md](../README.md)** - Project overview
- **[../DEPLOYMENT.md](../DEPLOYMENT.md)** - Deployment guide
- **[../QUICKSTART.md](../QUICKSTART.md)** - Quick start

---

**Last updated**: 2025
**Maintainer**: FCAJ Team
