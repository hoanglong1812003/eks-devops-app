# 🚀 QUICK START GUIDE

## Dự án đã được chuẩn hóa thành công! ✅

### 📁 Cấu trúc mới:
```
eks-devops-app/
├── src/              ← Code chính (đã refactor)
├── k8s/              ← Kubernetes manifests
├── .github/          ← CI/CD workflows
├── data/             ← Training data (gitignored)
├── vectorstore/      ← Vector DB (gitignored)
└── public/           ← Static assets
```

---

## 🎯 Chạy nhanh

### 1️⃣ Local (Development)
```bash
# Setup
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# Copy environment
copy .env.example .env
# Sửa .env và thêm GROQ_API_KEY

# Process documents (lần đầu)
python src\process_docs.py

# Run app
streamlit run src\main.py
```

### 2️⃣ Docker
```bash
# Run
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

### 3️⃣ Kubernetes/EKS
```bash
# Deploy
bash deploy-eks.sh <ECR_URI> <GROQ_API_KEY>

# Check status
kubectl get pods
kubectl get svc
```

---

## 📝 Các lệnh hữu ích

### Makefile commands:
```bash
make help          # Xem tất cả commands
make install       # Install dependencies
make run           # Run local
make process       # Process documents
make docker-build  # Build Docker image
make docker-run    # Run with Docker
make clean         # Clean cache
```

### Git commands:
```bash
# Commit changes
git add .
git commit -m "feat: restructure project for DevOps/Cloud"
git push origin main

# CI/CD sẽ tự động deploy!
```

---

## 🔑 Environment Variables

Cần thiết trong `.env`:
```env
GROQ_API_KEY=your_groq_api_key_here
```

---

## 📚 Documentation

- **README.md** - Tổng quan dự án
- **DEPLOYMENT.md** - Hướng dẫn deploy chi tiết
- **CHANGELOG.md** - Lịch sử thay đổi

---

## ✅ Checklist trước khi deploy

- [ ] Đã test local: `streamlit run src/main.py`
- [ ] Đã test Docker: `docker-compose up`
- [ ] Đã có GROQ_API_KEY
- [ ] Đã có AWS credentials
- [ ] Đã tạo ECR repository
- [ ] Đã tạo EKS cluster
- [ ] Đã update image URI trong k8s/deployment.yaml

---

## 🆘 Troubleshooting

### Lỗi: "Vectorstore not found"
```bash
python src\process_docs.py
```

### Lỗi: "Module not found"
```bash
# Đảm bảo đang ở root directory
cd d:\eks-workshop\app
python src\main.py
```

### Lỗi: Docker build fails
```bash
docker system prune -a
docker-compose build --no-cache
```

---

## 🎓 Next Steps

1. **Test local** ✅
2. **Test Docker** ✅
3. **Push to GitHub** ✅
4. **Setup AWS** (ECR, EKS)
5. **Deploy to EKS** 🚀

---

## 📞 Support

- FCAJ Community: https://rules.fcjuni.com/
- Documentation: Xem README.md và DEPLOYMENT.md

---

🎉 **Chúc mừng! Dự án của bạn đã sẵn sàng cho production!**
