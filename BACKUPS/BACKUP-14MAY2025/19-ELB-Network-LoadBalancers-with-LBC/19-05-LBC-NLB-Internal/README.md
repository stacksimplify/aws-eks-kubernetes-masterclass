---
title: AWS Load Balancer Controller - Internal NLB
description: Learn to create Internal AWS Network Load Balancer with Kubernetes
---

## Step-01: Introduction
- Create Internal NLB
- Update NLB Service k8s manifest with `aws-load-balancer-scheme` Annotation as `internal`
- Deploy curl pod
- Connect to curl pod and access Internal NLB endpoint using `curl command`.


## Step-02: Review LB Scheme Annotation
- **File Name:** `kube-manifests\02-LBC-NLB-LoadBalancer-Service.yml`
```yaml
    # Access Control
    service.beta.kubernetes.io/aws-load-balancer-scheme: "internal"
```

## Step-03: Deploy all kube-manifests
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
Observation:  Should see two listeners Port 80 

Go to Services -> EC2 -> Load Balancing -> Target Groups
1. Verify Registered targets
2. Verify Health Check path
```

## Step-04: Deploy curl pod and test Internal NLB
```t
# Deploy curl-pod
kubectl apply -f kube-manifests-curl

# Will open up a terminal session into the container
kubectl exec -it curl-pod -- sh

# We can now curl external addresses or internal services:
curl http://google.com/
curl <INTERNAL-NETWORK-LB-DNS>

# Internal Network LB Curl Test
curl lbc-network-lb-internal-demo-7031ade4ca457080.elb.us-east-1.amazonaws.com
```


## Step-05: Clean-Up
```t
# Delete or Undeploy kube-manifests
kubectl delete -f kube-manifests/
kubectl delete -f kube-manifests-curl/

# Verify if NLB deleted 
In AWS Mgmt Console, 
Go to Services -> EC2 -> Load Balancing -> Load Balancers
```

## References
- [Network Load Balancer](https://docs.aws.amazon.com/eks/latest/userguide/network-load-balancing.html)
- [NLB Service](https://kubernetes-sigs.github.io/aws-load-balancer-controller/v2.4/guide/service/nlb/)
- [NLB Service Annotations](https://kubernetes-sigs.github.io/aws-load-balancer-controller/v2.4/guide/service/annotations/)


