# FCAJ Chatbot 12345

Chatbot hỗ trợ cộng đồng First Cloud AI Journey (FCAJ) - AWS Vietnam, sử dụng RAG (Retrieval-Augmented Generation) với LangChain và Groq LLM.

## Tổng quan

Dự án này là một chatbot AI được xây dựng để hỗ trợ cộng đồng FCAJ trong việc:
- Trả lời câu hỏi về AWS và Cloud Computing
- Cung cấp thông tin về quy định và nội quy FCAJ
- Hỗ trợ học tập và tìm kiếm tài liệu
- Tư vấn về kiến trúc AWS

## Công nghệ sử dụng

- **Framework**: Streamlit
- **LLM**: Groq (llama-3.1-8b-instant)
- **Embeddings**: HuggingFace (paraphrase-multilingual-MiniLM-L12-v2)
- **Vector Store**: FAISS
- **Orchestration**: LangChain
- **Containerization**: Docker
- **Orchestration**: Kubernetes

## Cấu trúc dự án

```
app/
├── src/
│   ├── config/              # Configuration management
│   │   ├── __init__.py
│   │   └── settings.py
│   ├── services/            # Business logic
│   │   ├── __init__.py
│   │   └── rag_service.py
│   ├── utils/               # Utility functions
│   │   ├── __init__.py
│   │   └── helpers.py
│   ├── main.py              # Application entry point
│   └── process_docs.py      # Document processing
│
├── k8s/                     # Kubernetes manifests
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── configmap.yaml
│   ├── pvc.yaml
│   └── secret.yaml.example
│
├── .github/workflows/       # CI/CD pipeline
│   └── ci-cd.yaml
│
├── data/                    # Training documents (gitignored)
├── vectorstore/             # Vector database (gitignored)
├── public/static/           # Static assets
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
└── README.md
```

## Yêu cầu hệ thống

- Python 3.11+
- Docker & Docker Compose (optional)
- 4GB RAM minimum
- GROQ API Key

## Cài đặt và chạy

### 1. Chạy local

```bash
# Clone repository
git clone <repository-url>
cd app

# Tạo virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Cài đặt dependencies
pip install -r requirements.txt

# Tạo file .env
copy .env.example .env
# Chỉnh sửa .env và thêm GROQ_API_KEY

# Xử lý documents (lần đầu tiên)
python src/process_docs.py

# Chạy application
streamlit run src/main.py
```

Truy cập: http://localhost:8501

### 2. Chạy với Docker

```bash
# Tạo file .env
copy .env.example .env
# Chỉnh sửa .env và thêm GROQ_API_KEY

# Build và chạy
docker-compose up -d

# Xem logs
docker-compose logs -f

# Dừng
docker-compose down
```

### 3. Deploy lên Kubernetes/EKS

#### Yêu cầu
- kubectl installed
- AWS CLI configured
- EKS cluster created
- ECR repository created

#### Các bước deploy

```bash
# 1. Build và push Docker image
aws ecr get-login-password --region ap-southeast-1 | docker login --username AWS --password-stdin <ECR_URI>
docker build -t fcj-chatbot .
docker tag fcj-chatbot:latest <ECR_URI>:latest
docker push <ECR_URI>:latest

# 2. Update kubeconfig
aws eks update-kubeconfig --name fcj-eks-cluster --region ap-southeast-1

# 3. Tạo Kubernetes Secret
kubectl create secret generic fcj-secrets \
  --from-literal=groq-api-key=<YOUR_GROQ_API_KEY>

# 4. Update deployment.yaml
# Thay <YOUR_ECR_REPO> bằng ECR URI trong k8s/deployment.yaml

# 5. Deploy
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/pvc.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml

# 6. Kiểm tra
kubectl get pods
kubectl get svc fcj-chatbot-service
```

## Cấu hình

### Environment Variables

Tạo file `.env` từ `.env.example`:

```env
GROQ_API_KEY=your_groq_api_key_here
```

### Cấu hình nâng cao

Chỉnh sửa `src/config/settings.py`:

```python
class Settings:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    EMBEDDING_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    LLM_MODEL = "llama-3.1-8b-instant"
    LLM_TEMPERATURE = 0.1
    VECTORSTORE_PATH = "vectorstore"
    DATA_PATH = "data"
    CHUNK_SIZE = 500
    CHUNK_OVERLAP = 100
```

## CI/CD

Dự án sử dụng GitHub Actions để tự động:
1. Build Docker image
2. Push to Amazon ECR
3. Deploy to EKS cluster
4. Rolling update

### Setup GitHub Secrets

Thêm secrets trong GitHub repository:
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`

Workflow sẽ tự động chạy khi push code lên branch `main` hoặc `develop`.

## Kiến trúc

### Data Flow

```
User Input
    ↓
Streamlit UI (main.py)
    ↓
Query Normalization (utils/helpers.py)
    ↓
RAG Chain (services/rag_service.py)
    ↓
Vector Store Retrieval (FAISS)
    ↓
LLM Processing (Groq)
    ↓
Response to User
```

### Components

- **main.py**: Streamlit UI và user interaction
- **rag_service.py**: RAG chain implementation với LangChain
- **settings.py**: Centralized configuration
- **helpers.py**: Utility functions (normalization, encoding)
- **process_docs.py**: Document processing và vectorstore creation

## Troubleshooting

### Lỗi: "Vectorstore not found"

```bash
python src/process_docs.py
```

### Lỗi: Docker build fails

```bash
docker system prune -a
docker-compose build --no-cache
```

### Lỗi: Port already in use

```bash
# Dừng container cũ
docker stop <container-name>
docker rm <container-name>

# Hoặc
docker-compose down
```

### Lỗi: Kubernetes pod không start

```bash
# Xem logs
kubectl describe pod <pod-name>
kubectl logs <pod-name>

# Kiểm tra secrets
kubectl get secrets
```

## Development

### Thêm documents mới

1. Thêm file PDF/TXT vào thư mục `data/`
2. Chạy lại: `python src/process_docs.py`
3. Restart application

### Thay đổi LLM model

Chỉnh sửa `src/config/settings.py`:

```python
LLM_MODEL = "llama-3.1-70b-versatile"  # hoặc model khác
```

### Thay đổi embedding model

Chỉnh sửa `src/config/settings.py`:

```python
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
```

## Testing

### Test cấu trúc dự án

```bash
python test_structure.py
```

### Test imports

```python
from src.config import settings
from src.services.rag_service import setup_rag_chain
from src.utils.helpers import normalize_query

print("All imports successful!")
```

## Security

### Best Practices đã implement

- Không commit secrets vào Git
- Sử dụng environment variables
- Kubernetes Secrets cho sensitive data
- .gitignore và .dockerignore đầy đủ
- Health checks cho containers
- Resource limits trong Kubernetes

### Không được commit

- File `.env`
- API keys
- Credentials
- Training data (thư mục `data/`)
- Vector database (thư mục `vectorstore/`)

## Monitoring

### Health Checks

- **Endpoint**: `/_stcore/health`
- **Port**: 8501
- **Liveness Probe**: 40s initial delay, 30s period
- **Readiness Probe**: 30s initial delay, 10s period

### Logs

```bash
# Docker
docker-compose logs -f

# Kubernetes
kubectl logs -f deployment/fcj-chatbot
kubectl logs -f <pod-name>
```

### Metrics

```bash
# Kubernetes resources
kubectl top pods
kubectl top nodes
```

## Scaling

### Manual scaling

```bash
kubectl scale deployment fcj-chatbot --replicas=3
```

### Auto scaling (HPA)

```bash
kubectl autoscale deployment fcj-chatbot \
  --cpu-percent=70 \
  --min=2 \
  --max=5
```

## Contributing

1. Fork repository
2. Tạo feature branch: `git checkout -b feature/your-feature`
3. Commit changes: `git commit -m "Add your feature"`
4. Push to branch: `git push origin feature/your-feature`
5. Tạo Pull Request

## License

MIT License - see LICENSE file

## Team

- **Sư phụ**: Nguyễn Gia Hưng
- **Admin Team**: Lữ Hoàn Thiện, Trần Đại Vĩ, Huỳnh Hoàng Long, Phạm Hoàng Quy, Bùi Hoàng Việt, Đặng Thị Minh Thư, Lý Kiên Huy, Nguyễn Đỗ Thành Đạt

## Links

- FCAJ Rules: https://rules.fcjuni.com/
- YouTube Channel: https://www.youtube.com/@AWSStudyGroup
- Learning Materials: https://cloudjourney.awsstudygroup.com/

## Support

Nếu gặp vấn đề, vui lòng:
1. Kiểm tra phần Troubleshooting
2. Xem logs của application
3. Tạo issue trên GitHub repository
4. Liên hệ FCAJ Community

---

**Version**: 1.0.0  
**Last Updated**: 2025  
**Status**: Production Ready
