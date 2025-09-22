#!/bin/bash

# Deployment script for Kubernetes Microservices Lab
# This script automates the deployment of the microservices architecture

echo "=========================================="
echo "Kubernetes Microservices Lab Deployment"
echo "=========================================="

# Check if kubectl is available
if ! command -v kubectl &> /dev/null; then
    echo "Error: kubectl is required but not installed."
    echo "Please install kubectl first."
    exit 1
fi

# Check if cluster is accessible
if ! kubectl cluster-info &> /dev/null; then
    echo "Error: Cannot connect to Kubernetes cluster."
    echo "Please ensure your cluster is running (minikube start, etc.)"
    exit 1
fi

echo "kubectl is available and cluster is accessible"
echo ""

# Create namespace (optional)
echo "Creating namespace 'micro-lab'..."
kubectl create namespace micro-lab --dry-run=client -o yaml | kubectl apply -f -

# Set context to use the namespace
kubectl config set-context --current --namespace=micro-lab

echo "Namespace 'micro-lab' created and set as default"
echo ""

# Deploy services
echo "Deploying microservices..."
echo "----------------------------------------"

echo "Deploying Users Service..."
kubectl apply -f users-deploy.yaml
echo "Users service deployed"

echo "Deploying Catalog Service..."  
kubectl apply -f catalog-deploy.yaml
echo "Catalog service deployed"

echo "Deploying Orders Service..."
kubectl apply -f orders-deploy.yaml
echo "Orders service deployed"

echo "Deploying Ingress Gateway..."
kubectl apply -f gateway-ingress.yaml
echo "Ingress gateway deployed"

echo ""
echo "Waiting for pods to be ready..."
kubectl wait --for=condition=ready pod -l app=users --timeout=60s
kubectl wait --for=condition=ready pod -l app=catalog --timeout=60s  
kubectl wait --for=condition=ready pod -l app=orders --timeout=60s

echo ""
echo "Deployment Status:"
echo "----------------------------------------"
kubectl get pods
echo ""
kubectl get services
echo ""
kubectl get ingress

echo ""
echo "=========================================="
echo "Deployment completed successfully!"
echo ""
echo "Next steps:"
echo "1. For Minikube users:"
echo "   - Run: minikube tunnel (in separate terminal)"
echo "   - Or add to /etc/hosts: \$(minikube ip) micro.local"
echo ""
echo "2. Test the services:"
echo "   - curl http://micro.local/users"
echo "   - curl http://micro.local/catalog"  
echo "   - curl http://micro.local/orders"
echo ""
echo "3. Scale services (example):"
echo "   - kubectl scale deploy catalog-deploy --replicas=3"
echo ""
echo "4. Clean up when done:"
echo "   - ./cleanup.sh"
echo "=========================================="





