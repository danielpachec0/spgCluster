#!/bin/zsh

# Step 1: Run Terraform
# Navigate to your Terraform directory if needed
#cd gke
#terraform init && terraform apply -auto-approve

# Assuming your Terraform outputs include the cluster name and location
# CLUSTER_NAME=$(terraform output -raw cluster_name)
# CLUSTER_LOCATION=$(terraform output -raw cluster_location)
# PROJECT_ID=$(terraform output -raw project_id)

# Step 2: Get kubeconfig using gcloud
~/google-cloud-sdk/bin/gcloud container clusters get-credentials spg-cluster --zone us-east1 --project spgclus

# Step 3: Create Namespace for Argo CD
kubectl create namespace argocd

# Step 4: Install Argo CD with Helm
helm repo add argo https://argoproj.github.io/argo-helm
helm repo update
helm upgrade argocd argo/argo-cd --namespace argocd --version 6.0.5 --set configs.secret.argocdServerAdminPassword=admin

kubectl apply -f ../appGrafana.yaml
kubectl apply -f  ../k6app.yaml
# Note: Replace <version_number> with the desired version of Argo CD

