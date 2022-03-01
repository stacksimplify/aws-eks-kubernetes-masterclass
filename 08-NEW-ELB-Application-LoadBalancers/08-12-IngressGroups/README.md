---
title: AWS Load Balancer Controller - Ingress Groups
description: Learn AWS Load Balancer Controller - Ingress Groups
---

## Step-01: Introduction
- IngressGroup feature enables you to group multiple Ingress resources together. 
- The controller will automatically merge Ingress rules for all Ingresses within IngressGroup and support them with a single ALB. 
- In addition, most annotations defined on a Ingress only applies to the paths defined by that Ingress.
- Demonstrate Ingress Groups concept with two Applications. 

## Step-02: Review App1 Ingress Manifest - Key Lines
- **File Name:** `kube-manifests/app1/02-App1-Ingress.yml`
```yaml
    # Ingress Groups
    alb.ingress.kubernetes.io/group.name: myapps.web
    alb.ingress.kubernetes.io/group.order: '10'
```

## Step-03: Review App2 Ingress Manifest - Key Lines
- **File Name:** `kube-manifests/app2/02-App2-Ingress.yml`
```yaml
    # Ingress Groups
    alb.ingress.kubernetes.io/group.name: myapps.web
    alb.ingress.kubernetes.io/group.order: '20'
```

## Step-04: Review App3 Ingress Manifest - Key Lines
```yaml
    # Ingress Groups
    alb.ingress.kubernetes.io/group.name: myapps.web
    alb.ingress.kubernetes.io/group.order: '30'
```

## Step-05: Deploy Apps with two Ingress Resources
```t
# Deploy both Apps
kubectl apply -R -f kube-manifests

# Verify Pods
kubectl get pods

# Verify Ingress
kubectl  get ingress
Observation:
1. Three Ingress resources will be created with same ADDRESS value
2. Three Ingress Resources are merged to a single Application Load Balancer as those belong to same Ingress group "myapps.web"
```

## Step-06: Verify on AWS Mgmt Console
- Go to Services -> EC2 -> Load Balancers 
- Verify Routing Rules for `/app1` and `/app2` and `default backend`

## Step-07: Verify by accessing in browser
```t
# Web URLs
http://ingress-groups-demo601.stacksimplify.com/app1/index.html
http://ingress-groups-demo601.stacksimplify.com/app2/index.html
http://ingress-groups-demo601.stacksimplify.com
```

## Step-08: Clean-Up
```t
# Delete Apps from k8s cluster
kubectl delete -R -f kube-manifests/

## Verify Route53 Record Set to ensure our DNS records got deleted
- Go to Route53 -> Hosted Zones -> Records 
- The below records should be deleted automatically
  - ingress-groups-demo601.stacksimplify.com
```
