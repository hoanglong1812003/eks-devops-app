#!/bin/bash

# Deploy FCAJ Chatbot to EKS
# Usage: ./deploy-eks.sh <ecr-uri> <groq-api-key>

set -e

if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <ecr-uri> <groq-api-key>"
    echo "Example: $0 123456789.dkr.ecr.ap-southeast-1.amazonaws.com/fcj-chatbot gsk_xxxxx"
    exit 1
fi

ECR_URI=$1
GROQ_API_KEY=$2
AWS_REGION="ap-southeast-1"
EKS_CLUSTER="fcj-eks-cluster"

echo "🚀 Starting deployment to EKS..."

# 1. Build and push Docker image
echo "📦 Building Docker image..."
docker build -t fcj-chatbot .

echo "🔐 Logging in to ECR..."
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $ECR_URI

echo "🏷️  Tagging image..."
docker tag fcj-chatbot:latest $ECR_URI:latest

echo "⬆️  Pushing to ECR..."
docker push $ECR_URI:latest

# 2. Update kubeconfig
echo "⚙️  Updating kubeconfig..."
aws eks update-kubeconfig --name $EKS_CLUSTER --region $AWS_REGION

# 3. Create secret
echo "🔒 Creating Kubernetes secret..."
kubectl delete secret fcj-secrets --ignore-not-found
kubectl create secret generic fcj-secrets \
  --from-literal=groq-api-key=$GROQ_API_KEY

# 4. Update deployment with ECR URI
echo "📝 Updating deployment manifest..."
sed -i "s|<YOUR_ECR_REPO>|$ECR_URI|g" k8s/deployment.yaml

# 5. Deploy to EKS
echo "🚢 Deploying to EKS..."
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/pvc.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml

# 6. Wait for deployment
echo "⏳ Waiting for deployment to complete..."
kubectl rollout status deployment/fcj-chatbot

# 7. Get service URL
echo "✅ Deployment completed!"
echo ""
echo "📊 Deployment status:"
kubectl get pods -l app=fcj-chatbot
echo ""
echo "🌐 Service information:"
kubectl get svc fcj-chatbot-service
echo ""
echo "🎉 Done! Your chatbot is now running on EKS."
