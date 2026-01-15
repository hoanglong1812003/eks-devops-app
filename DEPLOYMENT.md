# Hướng dẫn triển khai FCAJ Chatbot lên AWS EKS

## Mục lục
1. [Chuẩn bị môi trường](#1-chuẩn-bị-môi-trường)
2. [Tạo EKS Cluster](#2-tạo-eks-cluster)
3. [Tạo ECR Repository](#3-tạo-ecr-repository)
4. [Build và Push Docker Image](#4-build-và-push-docker-image)
5. [Deploy lên EKS](#5-deploy-lên-eks)
6. [Kiểm tra và Monitoring](#6-kiểm-tra-và-monitoring)
7. [Troubleshooting](#7-troubleshooting)

---

## 1. Chuẩn bị môi trường

### Cài đặt công cụ cần thiết

```bash
# AWS CLI
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install

# kubectl
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

# eksctl
curl --silent --location "https://github.com/weaveworks/eksctl/releases/latest/download/eksctl_$(uname -s)_amd64.tar.gz" | tar xz -C /tmp
sudo mv /tmp/eksctl /usr/local/bin
```

### Cấu hình AWS CLI

```bash
aws configure
# AWS Access Key ID: <YOUR_ACCESS_KEY>
# AWS Secret Access Key: <YOUR_SECRET_KEY>
# Default region name: ap-southeast-1
# Default output format: json
```

---

## 2. Tạo EKS Cluster

### Option 1: Sử dụng eksctl (Khuyến nghị)

```bash
eksctl create cluster \
  --name fcj-eks-cluster \
  --region ap-southeast-1 \
  --nodegroup-name fcj-nodes \
  --node-type t3.medium \
  --nodes 2 \
  --nodes-min 1 \
  --nodes-max 3 \
  --managed
```

### Option 2: Sử dụng AWS Console

1. Truy cập AWS Console → EKS
2. Click "Create cluster"
3. Điền thông tin:
   - Cluster name: `fcj-eks-cluster`
   - Kubernetes version: 1.28
   - Cluster service role: Tạo mới hoặc chọn existing
4. Networking: Chọn VPC và subnets
5. Tạo Node Group:
   - Name: `fcj-nodes`
   - Instance type: `t3.medium`
   - Desired size: 2

### Cập nhật kubeconfig

```bash
aws eks update-kubeconfig --name fcj-eks-cluster --region ap-southeast-1
```

### Kiểm tra kết nối

```bash
kubectl get nodes
kubectl get namespaces
```

---

## 3. Tạo ECR Repository

```bash
# Tạo repository
aws ecr create-repository \
  --repository-name fcj-chatbot \
  --region ap-southeast-1

# Lấy URI của repository
aws ecr describe-repositories \
  --repository-names fcj-chatbot \
  --region ap-southeast-1 \
  --query 'repositories[0].repositoryUri' \
  --output text
```

Lưu lại ECR URI, ví dụ: `123456789.dkr.ecr.ap-southeast-1.amazonaws.com/fcj-chatbot`

---

## 4. Build và Push Docker Image

```bash
# Login vào ECR
aws ecr get-login-password --region ap-southeast-1 | \
  docker login --username AWS --password-stdin <YOUR_ECR_URI>

# Build image
docker build -t fcj-chatbot .

# Tag image
docker tag fcj-chatbot:latest <YOUR_ECR_URI>:latest

# Push image
docker push <YOUR_ECR_URI>:latest
```

---

## 5. Deploy lên EKS

### Bước 1: Tạo Secret cho API Key

```bash
kubectl create secret generic fcj-secrets \
  --from-literal=groq-api-key=<YOUR_GROQ_API_KEY>
```

### Bước 2: Cập nhật Deployment manifest

Mở file `k8s/deployment.yaml` và thay thế `<YOUR_ECR_REPO>` bằng ECR URI của bạn.

```bash
sed -i "s|<YOUR_ECR_REPO>|<YOUR_ECR_URI>|g" k8s/deployment.yaml
```

### Bước 3: Deploy các resources

```bash
# Deploy ConfigMap
kubectl apply -f k8s/configmap.yaml

# Deploy PVC (nếu sử dụng EFS)
kubectl apply -f k8s/pvc.yaml

# Deploy Deployment
kubectl apply -f k8s/deployment.yaml

# Deploy Service
kubectl apply -f k8s/service.yaml
```

### Bước 4: Kiểm tra deployment

```bash
# Xem pods
kubectl get pods -l app=fcj-chatbot

# Xem logs
kubectl logs -f deployment/fcj-chatbot

# Xem service
kubectl get svc fcj-chatbot-service
```

---

## 6. Kiểm tra và Monitoring

### Lấy URL của ứng dụng

```bash
# Nếu dùng LoadBalancer
kubectl get svc fcj-chatbot-service -o jsonpath='{.status.loadBalancer.ingress[0].hostname}'

# Hoặc
kubectl describe svc fcj-chatbot-service
```

### Kiểm tra health

```bash
# Port forward để test local
kubectl port-forward svc/fcj-chatbot-service 8501:80

# Truy cập: http://localhost:8501
```

### Xem logs

```bash
# Logs của tất cả pods
kubectl logs -l app=fcj-chatbot --tail=100 -f

# Logs của một pod cụ thể
kubectl logs <pod-name> -f
```

### Monitoring resources

```bash
# CPU và Memory usage
kubectl top pods -l app=fcj-chatbot
kubectl top nodes
```

---

## 7. Troubleshooting

### Pod không start được

```bash
# Xem chi tiết pod
kubectl describe pod <pod-name>

# Xem events
kubectl get events --sort-by=.metadata.creationTimestamp

# Xem logs
kubectl logs <pod-name>
```

### ImagePullBackOff error

```bash
# Kiểm tra secret
kubectl get secrets

# Tạo lại secret nếu cần
kubectl delete secret fcj-secrets
kubectl create secret generic fcj-secrets \
  --from-literal=groq-api-key=<YOUR_GROQ_API_KEY>
```

### Service không accessible

```bash
# Kiểm tra service
kubectl get svc fcj-chatbot-service
kubectl describe svc fcj-chatbot-service

# Kiểm tra endpoints
kubectl get endpoints fcj-chatbot-service
```

### Rolling update

```bash
# Update image
kubectl set image deployment/fcj-chatbot \
  chatbot=<YOUR_ECR_URI>:latest

# Xem rollout status
kubectl rollout status deployment/fcj-chatbot

# Rollback nếu cần
kubectl rollout undo deployment/fcj-chatbot
```

---

## 8. Scaling

### Manual scaling

```bash
# Scale up
kubectl scale deployment fcj-chatbot --replicas=3

# Scale down
kubectl scale deployment fcj-chatbot --replicas=1
```

### Auto scaling (HPA)

```bash
# Tạo HPA
kubectl autoscale deployment fcj-chatbot \
  --cpu-percent=70 \
  --min=2 \
  --max=5

# Xem HPA status
kubectl get hpa
```

---

## 9. Cleanup

```bash
# Xóa deployment
kubectl delete -f k8s/

# Xóa cluster (nếu cần)
eksctl delete cluster --name fcj-eks-cluster --region ap-southeast-1
```

---

## 10. Best Practices

✅ **Security:**
- Sử dụng Kubernetes Secrets cho sensitive data
- Không hardcode credentials
- Sử dụng IAM roles cho pods (IRSA)

✅ **Reliability:**
- Set resource requests và limits
- Configure health checks
- Use multiple replicas

✅ **Monitoring:**
- Enable CloudWatch Container Insights
- Set up alerts
- Monitor costs

✅ **CI/CD:**
- Automate deployments với GitHub Actions
- Use GitOps (ArgoCD/Flux)
- Implement blue-green deployments

---

## 📞 Support

Nếu gặp vấn đề, liên hệ:
- FCAJ Community: https://rules.fcjuni.com/
- GitHub Issues: <your-repo-url>/issues

---

🚀 **Good luck with your deployment!**
