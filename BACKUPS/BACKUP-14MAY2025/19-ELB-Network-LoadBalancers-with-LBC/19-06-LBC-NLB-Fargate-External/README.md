---
title: AWS Load Balancer Controller - NLB & Fargate
description: Learn to use AWS Network Load Balancer with Fargate Pods
---

## Step-01: Introduction
- Create advanced AWS Fargate Profile
- Schedule App3 on Fargate Pod
- Update NLB Annotation `aws-load-balancer-nlb-target-type` with `ip` from `instance` mode

## Step-02: Review Fargate Profile
- **File Name:** `fargate-profile/01-fargate-profiles.yml`
```yaml
apiVersion: eksctl.io/v1alpha5
kind: ClusterConfig
metadata:
  name: eksdemo1  # Name of the EKS Cluster
  region: us-east-1
fargateProfiles:
  - name: fp-app3
    selectors:
      # All workloads in the "ns-app3" Kubernetes namespace will be
      # scheduled onto Fargate:      
      - namespace: ns-app3
```

## Step-03: Create Fargate Profile
```t
# Change Directory
cd 19-06-LBC-NLB-Fargate-External

# Create Fargate Profile
eksctl create fargateprofile -f fargate-profile/01-fargate-profiles.yml
```

## Step-04: Update Annotation aws-load-balancer-nlb-target-type to IP
- **File Name:** `kube-manifests/02-LBC-NLB-LoadBalancer-Service.yml`
```yaml
service.beta.kubernetes.io/aws-load-balancer-nlb-target-type: ip # For Fargate Workloads we should use target-type as ip
```

## Step-05: Review the k8s Deployment Metadata for namespace
- **File Name:** `kube-manifests/01-Nginx-App3-Deployment.yml`
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app3-nginx-deployment
  labels:
    app: app3-nginx 
  namespace: ns-app3    # Update Namespace given in Fargate Profile 01-fargate-profiles.yml
spec:
  replicas: 1
  selector:
    matchLabels:
      app: app3-nginx
  template:
    metadata:
      labels:
        app: app3-nginx
    spec:
      containers:
        - name: app2-nginx
          image: stacksimplify/kubenginx:1.0.0
          ports:
            - containerPort: 80
          resources:
            requests:
              memory: "128Mi"
              cpu: "500m"
            limits:
              memory: "500Mi"
              cpu: "1000m"           
```

## Step-06: Deploy all kube-manifests
```t
# Deploy kube-manifests
kubectl apply -f kube-manifests/

# Verify Pods
kubectl get pods -o wide
Observation:
1. It will take couple of minutes to get the pod from pending to running state due to Fargate Mode.

# Verify Worker Nodes
kubectl get nodes -o wide
Obseravtion:
1. wait for Fargate worker node to create

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

Go to Services -> EC2 -> Load Balancing -> Target Groups
1. Verify Registered targets
2. Verify Health Check path

# Perform nslookup Test
nslookup nlbfargate901.stacksimplify.com

# Access Application
# Test HTTP URL
http://nlbfargate901.stacksimplify.com

# Test HTTPS URL
https://nlbfargate901.stacksimplify.com
```

## Step-06: Clean-Up
```t
# Delete or Undeploy kube-manifests
kubectl delete -f kube-manifests/

# Verify if NLB deleted 
In AWS Mgmt Console, 
Go to Services -> EC2 -> Load Balancing -> Load Balancers
```

## References
- [Network Load Balancer](https://docs.aws.amazon.com/eks/latest/userguide/network-load-balancing.html)
- [NLB Service](https://kubernetes-sigs.github.io/aws-load-balancer-controller/v2.4/guide/service/nlb/)
- [NLB Service Annotations](https://kubernetes-sigs.github.io/aws-load-balancer-controller/v2.4/guide/service/annotations/)











## Step-09: Delete Fargate Profile
```t
# List Fargate Profiles
eksctl get fargateprofile --cluster eksdemo1 

# Delete Fargate Profile
eksctl delete fargateprofile --cluster eksdemo1 --name <Fargate-Profile-NAME> --wait

eksctl delete fargateprofile --cluster eksdemo1 --name  fp-app3 --wait
```
