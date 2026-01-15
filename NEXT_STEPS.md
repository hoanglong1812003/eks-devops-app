# 🎯 HƯỚNG DẪN BƯỚC TIẾP THEO

## ✅ Đã hoàn thành

Dự án của bạn đã được chuẩn hóa hoàn toàn! Tất cả files và cấu trúc đã sẵn sàng.

---

## 📝 Bước tiếp theo (Làm ngay bây giờ)

### 1. Kiểm tra cấu trúc ✅
```bash
python test_structure.py
```
**Kết quả mong đợi**: "ALL TESTS PASSED!"

### 2. Test chạy local 🧪

```bash
# Tạo virtual environment (nếu chưa có)
python -m venv venv

# Activate
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
copy .env.example .env

# Mở .env và thêm GROQ_API_KEY của bạn
notepad .env

# Process documents (nếu chưa có vectorstore)
python src\process_docs.py

# Run application
streamlit run src\main.py
```

**Kết quả mong đợi**: App chạy tại http://localhost:8501

### 3. Test Docker 🐳

```bash
# Build và run
docker-compose up -d

# Check logs
docker-compose logs -f

# Test app
# Mở browser: http://localhost:8501

# Stop
docker-compose down
```

**Kết quả mong đợi**: App chạy trong container

---

## 🚀 Chuẩn bị deploy lên AWS EKS

### Bước 1: Setup AWS Account

1. **Tạo AWS Account** (nếu chưa có)
   - Truy cập: https://aws.amazon.com/
   - Sign up for free tier

2. **Cài đặt AWS CLI**
   ```bash
   # Download từ: https://aws.amazon.com/cli/
   
   # Configure
   aws configure
   # Nhập: Access Key ID, Secret Access Key, Region (ap-southeast-1)
   ```

3. **Cài đặt kubectl**
   ```bash
   # Download từ: https://kubernetes.io/docs/tasks/tools/
   ```

4. **Cài đặt eksctl**
   ```bash
   # Download từ: https://eksctl.io/
   ```

### Bước 2: Tạo ECR Repository

```bash
# Tạo repository
aws ecr create-repository \
  --repository-name fcj-chatbot \
  --region ap-southeast-1

# Lưu lại ECR URI
# Ví dụ: 123456789.dkr.ecr.ap-southeast-1.amazonaws.com/fcj-chatbot
```

### Bước 3: Tạo EKS Cluster

```bash
# Tạo cluster (mất ~15-20 phút)
eksctl create cluster \
  --name fcj-eks-cluster \
  --region ap-southeast-1 \
  --nodegroup-name fcj-nodes \
  --node-type t3.medium \
  --nodes 2 \
  --nodes-min 1 \
  --nodes-max 3 \
  --managed

# Verify
kubectl get nodes
```

### Bước 4: Deploy Application

```bash
# Sử dụng script tự động
bash deploy-eks.sh <YOUR_ECR_URI> <YOUR_GROQ_API_KEY>

# Hoặc manual:
# 1. Build và push image
aws ecr get-login-password --region ap-southeast-1 | docker login --username AWS --password-stdin <ECR_URI>
docker build -t fcj-chatbot .
docker tag fcj-chatbot:latest <ECR_URI>:latest
docker push <ECR_URI>:latest

# 2. Update kubeconfig
aws eks update-kubeconfig --name fcj-eks-cluster --region ap-southeast-1

# 3. Create secret
kubectl create secret generic fcj-secrets --from-literal=groq-api-key=<YOUR_KEY>

# 4. Update deployment.yaml với ECR URI
# Edit k8s/deployment.yaml: thay <YOUR_ECR_REPO> bằng ECR URI

# 5. Deploy
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/pvc.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml

# 6. Get URL
kubectl get svc fcj-chatbot-service
```

---

## 🔄 Setup CI/CD (GitHub Actions)

### Bước 1: Push code lên GitHub

```bash
# Initialize git (nếu chưa có)
git init
git add .
git commit -m "feat: restructure project for DevOps/Cloud/EKS"

# Add remote
git remote add origin <your-github-repo-url>

# Push
git push -u origin main
```

### Bước 2: Setup GitHub Secrets

1. Vào GitHub repo → Settings → Secrets and variables → Actions
2. Thêm secrets:
   - `AWS_ACCESS_KEY_ID`: Your AWS access key
   - `AWS_SECRET_ACCESS_KEY`: Your AWS secret key
   - `GROQ_API_KEY`: Your Groq API key

### Bước 3: Trigger deployment

```bash
# Mỗi khi push code
git add .
git commit -m "feat: your changes"
git push origin main

# GitHub Actions sẽ tự động:
# 1. Build Docker image
# 2. Push to ECR
# 3. Deploy to EKS
```

---

## 📊 Monitoring & Maintenance

### Check application status
```bash
# Pods
kubectl get pods -l app=fcj-chatbot

# Logs
kubectl logs -f deployment/fcj-chatbot

# Service
kubectl get svc fcj-chatbot-service

# Resources
kubectl top pods
```

### Update application
```bash
# Method 1: CI/CD (Recommended)
git push origin main

# Method 2: Manual
docker build -t <ECR_URI>:latest .
docker push <ECR_URI>:latest
kubectl rollout restart deployment/fcj-chatbot
```

### Scale application
```bash
# Manual
kubectl scale deployment fcj-chatbot --replicas=3

# Auto (HPA)
kubectl autoscale deployment fcj-chatbot --cpu-percent=70 --min=2 --max=5
```

---

## 📚 Tài liệu tham khảo

### Trong dự án:
- **README.md** - Tổng quan dự án
- **QUICKSTART.md** - Hướng dẫn nhanh
- **DEPLOYMENT.md** - Hướng dẫn deploy chi tiết
- **CHANGELOG.md** - Lịch sử thay đổi
- **SUMMARY.md** - Tóm tắt dự án

### External:
- AWS EKS: https://docs.aws.amazon.com/eks/
- Kubernetes: https://kubernetes.io/docs/
- Docker: https://docs.docker.com/
- GitHub Actions: https://docs.github.com/actions

---

## ❓ Troubleshooting

### App không chạy local?
```bash
# Check Python version
python --version  # Should be 3.11+

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Check vectorstore
python src\process_docs.py
```

### Docker build fails?
```bash
# Clean Docker
docker system prune -a

# Rebuild
docker-compose build --no-cache
```

### EKS deployment fails?
```bash
# Check pods
kubectl describe pod <pod-name>

# Check logs
kubectl logs <pod-name>

# Check secrets
kubectl get secrets
```

---

## 🎯 Checklist cuối cùng

Trước khi deploy production:

- [ ] ✅ Test local thành công
- [ ] ✅ Test Docker thành công
- [ ] ✅ Code đã push lên GitHub
- [ ] ✅ AWS credentials đã setup
- [ ] ✅ ECR repository đã tạo
- [ ] ✅ EKS cluster đã tạo
- [ ] ✅ GitHub Secrets đã setup
- [ ] ✅ Đã đọc DEPLOYMENT.md
- [ ] ✅ Đã backup data quan trọng

---

## 🎉 Chúc mừng!

Bạn đã có một dự án:
- ✅ Clean code
- ✅ Modular architecture
- ✅ Docker ready
- ✅ Kubernetes ready
- ✅ CI/CD ready
- ✅ Production ready

**Good luck với deployment! 🚀**

---

## 📞 Cần hỗ trợ?

- FCAJ Community: https://rules.fcjuni.com/
- GitHub Issues: <your-repo>/issues
- Documentation: Xem các file .md trong dự án

---

*File này: NEXT_STEPS.md*
*Tạo bởi: DevOps Engineer*
*Ngày: 2025*
