---
title: AWS Load Balancer Controller - Ingress Internal LB
description: Learn AWS Load Balancer Controller - Ingress Internal LB
---

## Step-01: Introduction
- Create Internal Application Load Balancer using Ingress
- To test the Internal LB, use the `curl-pod`
- Deploy `curl-pod`
- Connect to `curl-pod` and test Internal LB from `curl-pod`

## Step-02: Update Ingress Scheme annotation to Internal
- **File Name:** 04-ALB-Ingress-Internal-LB.yml
```yaml
    # Creates Internal Application Load Balancer
    alb.ingress.kubernetes.io/scheme: internal 
```

## Step-03: Deploy all Application Kubernetes Manifests and Verify
```t
# Deploy kube-manifests
kubectl apply -f kube-manifests/

# Verify Ingress Resource
kubectl get ingress

# Verify Apps
kubectl get deploy
kubectl get pods

# Verify NodePort Services
kubectl get svc
```
### Verify Load Balancer & Target Groups
- Load Balancer -  Listeneres (Verify both 80 & 443) 
- Load Balancer - Rules (Verify both 80 & 443 listeners) 
- Target Groups - Group Details (Verify Health check path)
- Target Groups - Targets (Verify all 3 targets are healthy)

## Step-04: How to test this Internal Load Balancer? 
- We are going to deploy a `curl-pod` in EKS Cluster
- We connect to that `curl-pod` in EKS Cluster and test using `curl commands` for our sample applications load balanced using this Internal Application Load Balancer


## Step-05: curl-pod Kubernetes Manifest
- **File Name:** kube-manifests-curl/01-curl-pod.yml
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: curl-pod
spec:
  containers:
  - name: curl
    image: curlimages/curl 
    command: [ "sleep", "600" ]
```

## Step-06: Deploy curl-pod and Verify Internal LB
```t
# Deploy curl-pod
kubectl apply -f kube-manifests-curl

# Will open up a terminal session into the container
kubectl exec -it curl-pod -- sh

# We can now curl external addresses or internal services:
curl http://google.com/
curl <INTERNAL-INGRESS-LB-DNS>

# Default Backend Curl Test
curl internal-ingress-internal-lb-1839544354.us-east-1.elb.amazonaws.com

# App1 Curl Test
curl internal-ingress-internal-lb-1839544354.us-east-1.elb.amazonaws.com/app1/index.html

# App2 Curl Test
curl internal-ingress-internal-lb-1839544354.us-east-1.elb.amazonaws.com/app2/index.html

# App3 Curl Test
curl internal-ingress-internal-lb-1839544354.us-east-1.elb.amazonaws.com
```


## Step-07: Clean Up
```t
# Delete Manifests
kubectl delete -f kube-manifests/
kubectl delete -f kube-manifests-curl/
```

