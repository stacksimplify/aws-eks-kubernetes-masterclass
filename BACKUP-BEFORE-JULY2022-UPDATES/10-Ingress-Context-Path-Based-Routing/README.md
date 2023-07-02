# Ingress - Context Path Based Routing

## Step-01: Introduction
- We are going to implement context path based routing using Ingress

[![Image](https://www.stacksimplify.com/course-images/azure-aks-ingress-path-based-routing.png "Azure AKS Kubernetes - Masterclass")](https://www.udemy.com/course/aws-eks-kubernetes-masterclass-devops-microservices/?referralCode=257C9AD5B5AF8D12D1E1)

## Step-02: Review k8s Application Manifests
- 01-NginxApp1-Manifests
- 02-NginxApp2-Manifests
- 03-UserMgmtmWebApp-Manifests

## Step-03: Review Ingress Service Manifests
- 04-IngressService-Manifests

## Step-04: Deploy and Verify
```
# Deploy Apps
kubectl apply -R -f kube-manifests/

# List Pods
kubectl get pods

# List Services
kubectl get svc

# List Ingress
kubectl get ingress

# Verify Ingress Controller Logs
kubectl get pods -n ingress-basic
kubectl logs -f <pod-name> -n ingress-basic
```

## Step-05: Access Applications
```
# Access App1
http://<Public-IP-created-for-Ingress>/app1/index.html

# Access App2
http://<Public-IP-created-for-Ingress>/app2/index.html

# Access Usermgmt Web App
http://<Public-IP-created-for-Ingress>
Username: admin101
Password: password101

```

## Step-06: Clean-Up Applications
```
# Delete Apps
kubectl delete -f kube-manifests/

# Delete Azure Disk created for Usermgmt Web App
Go to All Services -> Azure Disks -> Delete disk
```

## Ingress Annotation Reference
- https://kubernetes.github.io/ingress-nginx/user-guide/nginx-configuration/annotations/

