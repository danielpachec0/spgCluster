#!/bin/zsh

cd gke
terraform init && terraform apply -auto-approve

~/google-cloud-sdk/bin/gcloud container clusters get-credentials spg-cluster --zone us-east1 --project spgclus

kubectl create namespace argocd

helm repo add argo https://argoproj.github.io/argo-helm
helm repo update
helm upgrade argocd argo/argo-cd --namespace argocd --version 6.0.5 --set configs.secret.argocdServerAdminPassword=admin

kubectl apply -f ../appGrafana.yaml
kubectl apply -f  ../k6app.yaml

