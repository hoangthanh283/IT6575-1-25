#!/bin/bash

# Cleanup script for Kubernetes Microservices Lab
# This script removes all deployed resources

echo "=========================================="
echo "Kubernetes Microservices Lab Cleanup"
echo "=========================================="

echo "Removing deployed resources..."
echo "----------------------------------------"

# Remove ingress first
echo "Removing Ingress Gateway..."
kubectl delete -f gateway-ingress.yaml --ignore-not-found=true
echo "✅ Ingress gateway removed"

# Remove services and deployments
echo "Removing Orders Service..."
kubectl delete -f orders-deploy.yaml --ignore-not-found=true
echo "✅ Orders service removed"

echo "Removing Catalog Service..."
kubectl delete -f catalog-deploy.yaml --ignore-not-found=true
echo "✅ Catalog service removed"

echo "Removing Users Service..."
kubectl delete -f users-deploy.yaml --ignore-not-found=true
echo "✅ Users service removed"

# Remove namespace
echo "Removing namespace 'micro-lab'..."
kubectl delete namespace micro-lab --ignore-not-found=true
echo "✅ Namespace removed"

# Reset context to default namespace
kubectl config set-context --current --namespace=default

echo ""
echo "Cleanup Status:"
echo "----------------------------------------"
echo "Checking for remaining resources..."

# Check if any resources remain
REMAINING_PODS=$(kubectl get pods -n micro-lab 2>/dev/null | wc -l)
if [ $REMAINING_PODS -eq 0 ]; then
    echo "✅ All resources cleaned up successfully"
else
    echo "⚠️  Some resources may still be terminating..."
    kubectl get pods -n micro-lab 2>/dev/null || echo "Namespace already removed"
fi

echo ""
echo "=========================================="
echo "Cleanup completed!"
echo ""
echo "Note: If you added entries to /etc/hosts,"
echo "you may want to remove them manually:"
echo "sudo vim /etc/hosts"
echo "(Remove the line: <IP> micro.local)"
echo "=========================================="





