---
title: Azure AKS Cluster Access with Multiple Clusters
description: Understand how to access multiple Azure Kubernetes AKS Clusters using kubectl
---
# Azure AKS Cluster Access with Multiple Clusters

## Step-01: Introduction
- Azure AKS Cluster Access
- Create Clusters using Command Line
- Understand kube config file $HOME/.kube/config
- Understand kubectl config command
  - kubectl config view
  - kubectl config current-context
  - kubectl config use-context <context-name>

[![Image](https://stacksimplify.com/course-images/azure-kubernetes-service-access-multiple-clusters.png "Azure AKS Kubernetes - Masterclass")](https://stacksimplify.com/course-images/azure-kubernetes-service-access-multiple-clusters.png)


## Step-02: Create AKSDEMO3 cluster using AKS CLI
- Generates SSH Keys with option **--generate-ssh-keys** 
- They will be stored in **$HOME/.ssh** folder in your local desktop
- Backup them if required
```
# Create AKSDEMO3 Cluster
az group create --location centralus --name aks-rg3
az aks create --name aksdemo3 \
              --resource-group aks-rg3 \
              --node-count 1 \
              --enable-managed-identity \
              --generate-ssh-keys

# Backup SSH Keys
cd $HOME/.ssh
mkdir BACKUP-SSH-KEYS-AKSDEMO-Clusters
cp id_rsa* BACKUP-SSH-KEYS-AKSDEMO-Clusters
ls -lrt BACKUP-SSH-KEYS-AKSDEMO-Clusters
```

## Step-03: Create AKSDEMO4 cluster using AKS CLI
- Use same SSH keys for AKSDEMO4 cluster using **--ssh-key-value**
```
# Create AKSDEMO4 Cluster
az group create --location centralus --name aks-rg4
az aks create --name aksdemo4 \
              --resource-group aks-rg4 \
              --node-count 1 \
              --enable-managed-identity \
              --ssh-key-value /Users/kalyanreddy/.ssh/id_rsa.pub              
```

## Step-04: Configure AKSDEMO3 Cluster Access for kubectl
- Understand commands 
  - kubectl config view
  - kubectl config current-context
```
# View kubeconfig
kubectl config view

# Clean existing kube configs
cd $HOME/.kube
>config
cat config

# View kubeconfig
kubectl config view

# Configure AKSDEMO3 & 4 Cluster Access for kubectl
az aks get-credentials --resource-group aks-rg3 --name aksdemo3

# View kubeconfig
kubectl config view

# View Cluster Information
kubectl cluster-info

# View the current context for kubectl
kubectl config current-context
```

## Step-05: Configure AKSDEMO4 Cluster Access for kubectl
```
# Configure AKSDEMO4 Cluster Access for kubectl
az aks get-credentials --resource-group aks-rg4 --name aksdemo4

# View the current context for kubectl
kubectl config current-context

# View Cluster Information
kubectl cluster-info

# View kubeconfig
kubectl config view
```

## Step-06: Switch Contexts between clusters
- Understand the kubectl config command **use-context**
```
# View the current context for kubectl
kubectl config current-context

# View kubeconfig
kubectl config view 
Get contexts.context.name to which you want to switch 

# Switch Context
kubectl config use-context aksdemo3

# View the current context for kubectl
kubectl config current-context

# View Cluster Information
kubectl cluster-info
```