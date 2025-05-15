---
title: AWS Load Balancer Controller - NLB Elastic IP
description: Learn to use AWS Network Load Balancer & Elastic IP with AWS Load Balancer Controller
---

## Step-01: Introduction
- Create Elastic IPs
- Update NLB Service k8s manifest with Elastic IP Annotation with EIP Allocation IDs

## Step-02: Create two Elastic IPs and get EIP Allocation IDs
- This configuration is optional and use can use it to assign static IP addresses to your NLB
- You must specify the same number of eip allocations as load balancer subnets annotation
- NLB must be internet-facing
```t
# Elastic IP Allocation IDs
eipalloc-07daf60991cfd21f0 
eipalloc-0a8e8f70a6c735d16
```

## Step-03: Review Elastic IP Annotations
- **File Name:** `kube-manifests\02-LBC-NLB-LoadBalancer-Service.yml`
```yaml
    # Elastic IPs
    service.beta.kubernetes.io/aws-load-balancer-eip-allocations: eipalloc-07daf60991cfd21f0, eipalloc-0a8e8f70a6c735d16
```

## Step-04: Deploy all kube-manifests
```t
# Deploy kube-manifests
kubectl apply -f kube-manifests/

# Verify Pods
kubectl get pods

# Verify Services
kubectl get svc
Observation: 
1. Verify the network lb DNS name

# Verify AWS Load Balancer Controller pod logs
kubectl -n kube-system get pods
kubectl -n kube-system logs -f <aws-load-balancer-controller-POD-NAME>

# Verify using AWS Mgmt Console
Go to Services -> EC2 -> Load Balancing -> Load Balancers
1. Verify Description Tab - DNS Name matching output of "kubectl get svc" External IP
2. Verify Listeners Tab
Observation:  Should see two listeners Port 80 and 443

Go to Services -> EC2 -> Load Balancing -> Target Groups
1. Verify Registered targets
2. Verify Health Check path
Observation: Should see two target groups. 1 Target group for 1 listener

# Perform nslookup Test
nslookup nlbeip201.stacksimplify.com
Observation:
1. Verify the IP Address matches our Elastic IPs we created in Step-02

# Access Application
# Test HTTP URL
http://nlbeip201.stacksimplify.com

# Test HTTPS URL
https://nlbeip201.stacksimplify.com
```

## Step-05: Clean-Up
```t
# Delete or Undeploy kube-manifests
kubectl delete -f kube-manifests/

# Delete Elastic IPs created
In AWS Mgmt Console, 
Go to Services -> EC2 -> Network & Security -> Elastic IPs
Delete two EIPs created

# Verify if NLB deleted 
In AWS Mgmt Console, 
Go to Services -> EC2 -> Load Balancing -> Load Balancers
```

## References
- [Network Load Balancer](https://docs.aws.amazon.com/eks/latest/userguide/network-load-balancing.html)
- [NLB Service](https://kubernetes-sigs.github.io/aws-load-balancer-controller/v2.4/guide/service/nlb/)
- [NLB Service Annotations](https://kubernetes-sigs.github.io/aws-load-balancer-controller/v2.4/guide/service/annotations/)

