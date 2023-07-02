---
title: Azure AKS Kubernetes  Namespaces Introduction
description: Understand Kubernetes Namespace basics on Azure Kubernetes Service AKS Cluster
---
# Kubernetes Namespaces - Imperative using kubectl

## Step-01: Introduction
- Namespaces allow to split-up resources into different groups.
- Resource names should be unique in a namespace
- We can use namespaces to create multiple environments like dev, staging and production etc
- Kubernetes will always list the resources from `default namespace` unless we provide exclusively from which namespace we need information from.

[![Image](https://stacksimplify.com/course-images/azure-kubernetes-service-namespaces-1.png "Azure Kubernetes Service - Masterclass")](https://stacksimplify.com/course-images/azure-kubernetes-service-namespaces-1.png){:target="_blank"}  

[![Image](https://stacksimplify.com/course-images/azure-kubernetes-service-namespaces-2.png "Azure Kubernetes Service - Masterclass")](https://stacksimplify.com/course-images/azure-kubernetes-service-namespaces-2.png){:target="_blank"}  

[![Image](https://stacksimplify.com/course-images/azure-kubernetes-service-namespaces-3.png "Azure Kubernetes Service - Masterclass")](https://stacksimplify.com/course-images/azure-kubernetes-service-namespaces-3.png){:target="_blank"}  

## Pre-requisite Check (Optional)
- We should already have our AKS Cluster UP and Running. 
- We should have configured our AKS Cluster credentials in command line to execute `kubectl` commands
```
# Configure AKS Cluster Credentials from command line
az aks get-credentials --name aksdemo1 --resource-group aks-rg1

# List Worker Nodes
kubectl get nodes
kubectl get nodes -o wide
```


## Step-02: Namespaces Generic - Deploy in Dev1 and Dev2
### Create Namespace
```
# List Namespaces
kubectl get ns 

# Craete Namespace
kubectl create namespace <namespace-name>
kubectl create namespace dev1
kubectl create namespace dev2

# List Namespaces
kubectl get ns 
```
### Deploy All k8s Objects to default, dev1 and dev2 namespaces
```
# Deploy All k8s Objects
kubectl apply -f kube-manifests/  
kubectl apply -f kube-manifests/ -n dev1
kubectl apply -f kube-manifests/ -n dev2

# List all objects from default, dev1 & dev2 Namespaces
kubectl get all -n default
kubectl get all -n dev1
kubectl get all -n dev2
```

## Step-04: Access Application

### Default Namesapace
```
# List Services
kubectl get svc

# Access Application
http://<Public-IP-from-List-Services-Output>/app1/index.html
```

### Dev1 Namespace
```
# List Services
kubectl get svc -n dev1

# Access Application
http://<Public-IP-from-List-Services-Output>/app1/index.html
```
### Dev2 Namespace
```
# List Services
kubectl get svc -n dev2

# Access Application
http://<Public-IP-from-List-Services-Output>/app1/index.html
```
## Step-05: Clean-Up
```
# Delete namespaces dev1 & dev2
kubectl delete ns dev1
kubectl delete ns dev2

# List all objects from dev1 & dev2 Namespaces
kubectl get all -n dev1
kubectl get all -n dev2

# List Namespaces
kubectl get ns

# Delete App from default Namespace (Dont Delete default Namespace - k8s default service exists in it)
kubectl delete -f kube-manifests/

# Get all from All Namespaces
kubectl get all -all-namespaces
```

## References:
- https://kubernetes.io/docs/tasks/administer-cluster/namespaces-walkthrough/