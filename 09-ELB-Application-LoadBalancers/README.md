# Load Balancing workloads on EKS using ALB

## Introduction
-  Need to understand what are managed and unmanaged nodes? What is the difference? 

# Module - 1: Deploy ALB Ingress Controller
## Step-01: Create EKS Cluster using eksctl
```
# Create Cluster
eksctl create cluster --name=demo1 --version=1.16 --nodes-min=2 --nodes-max=2 --node-type=t3.medium --ssh-access --ssh-public-key=kube-demo-2020 --region=us-east-1 --tags environment=demo1 --node-volume-size=20 --node-volume-type=gp2 --zones=us-east-1a,us-east-1b

# Enable Logging
eksctl utils update-cluster-logging --region=us-east-1 --cluster=demo1

# Get List of clusters
eksctl get cluster

# Our kubectl context should be changed to new cluster
kubectl config view --minify
```

## Step-02: Switch Kubernetes Clusters using use-context for kubectl
```
# To see all cluster contexts config information
kubectl config view

# View current context config information
kubectl config  view --minify

# Switch context 
kubectl config use-context <Name of context - Pick value from contexts.context.name>
kubectl config use-context arn:aws:eks:us-east-1:411686525067:cluster/my-first-eks-cluster

# View the current context config information
kubectl config  view --minify

# List Pods
kubectl get pods
```

## Step-01: ALB Ingress Controller Pre-requisite - 1: Verify Subnet Tagging
### All Subnets
- Go to Services -> VPC -> Subnets
- Select our EKS cluster subnets and add below listed tag.
```
# Format
Key: kubernetes.io/cluster/<cluster-name> 
Value: shared

# Replace with cluster name
Key: kubernetes.io/cluster/my-first-eks-cluster
Value: shared
```
### Public Subnets
- Go to Services -> VPC -> Subnets
- Select our EKS cluster **PUBLIC** subnets and add below listed tag.
```
Key: kubernetes.io/role/elb
Value: 1
```

### Private Subnets
- Go to Services -> VPC -> Subnets
- Select our EKS cluster **PRIVATE** subnets and add below listed tag.
```
Key: kubernetes.io/role/internal-elb
Value: 1
```

## Step-02: ALB Ingress Controller Pre-requisite - 2: Install eksctl
- We need `eksctl` command line utility to perform few ALB Ingress controller tasks.
```
# Install Homebrew on MacOs
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"

# Install the Weaveworks Homebrew tap.
brew tap weaveworks/tap

# Install the Weaveworks Homebrew tap.
brew install weaveworks/tap/eksctl

# Verify eksctl version
eksctl version
```
- For windows and linux OS, you can refer below documentation link. 
- **Reference:** https://docs.aws.amazon.com/eks/latest/userguide/eksctl.html#installing-eksctl

## Step-03: ALB Ingress Controller Pre-requisite - 3: Create & Associate IAM OIDC Provider
- eksctl version should 0.20.0-rc.0 or later 
- Create an IAM OIDC provider and associate it with our cluster.
```
# Template
eksctl utils associate-iam-oidc-provider \
    --region region-code \
    --cluster prod \
    --approve

# Replace with region & cluster name
eksctl utils associate-iam-oidc-provider \
    --region us-east-1 \
    --cluster demo1 \
    --approve

# Above Command in single line
eksctl utils associate-iam-oidc-provider --region us-east-1 --cluster demo1 --approve
```

## PENDING - Step-04: ALB Ingress Controller Pre-requisite - 4: Create IAM Policy
- HAS ISSUE with creating IAM Policy - so created with full ELB access by taking existing policy
- This IAM policy will allow our ALB Ingress Controller pod to make calls to AWS APIs
- Take a note of the Policy ARN, we will use it when creating the ROLE. 
- Created manually using AWS management console and gave full access to ELB
```
# Create IAM Policy
aws iam create-policy \
    --policy-name ALBIngressControllerIAMPolicy \
    --policy-document https://raw.githubusercontent.com/kubernetes-sigs/aws-alb-ingress-controller/master/docs/examples/iam-policy.json

# Make a note of Policy ARN    
Policy ARN:  arn:aws:iam::411686525067:policy/ALBIngressControllerIAMPolicy
```

## PENDING - Step-05: ALB Ingress Controller Pre-requisite - 5: Create a Kubernetes service account named alb-ingress-controller in the kube-system namespace
- We are using master branch instead of v1.1.4 
```
kubectl apply -f https://raw.githubusercontent.com/kubernetes-sigs/aws-alb-ingress-controller/master/docs/examples/rbac-role.yaml
```

## Step-06: ALB Ingress Controller Pre-requisite - 6: Create an IAM role for the ALB Ingress Controller and attach the role to the service account created
- Applicable only with `eksctl` managed clusters
```
# Template
eksctl create iamserviceaccount \
    --region region-code \
    --name alb-ingress-controller \
    --namespace kube-system \
    --cluster prod \
    --attach-policy-arn arn:aws:iam::111122223333:policy/ALBIngressControllerIAMPolicy \
    --override-existing-serviceaccounts \
    --approve

# Replaced region, name, cluster and policy arn (Policy arn we took note in step-04)
eksctl create iamserviceaccount \
    --region us-east-1 \
    --name alb-ingress-controller \
    --namespace kube-system \
    --cluster demo1 \
    --attach-policy-arn arn:aws:iam::411686525067:policy/ALBIngressControllerIAMPolicy \
    --override-existing-serviceaccounts \
    --approve
```

## PENDING - Step-07: Deploy ALB Ingress Controller
- We are using Master branch file instead of 1.1.4
```
kubectl apply -f https://raw.githubusercontent.com/kubernetes-sigs/aws-alb-ingress-controller/master/docs/examples/alb-ingress-controller.yaml
```

## Step-08: Edit ALB Ingress Controller Manifest
- Edit ALB Ingress Controller manifest and update cluster name in that. 
```
kubectl edit deployment.apps/alb-ingress-controller -n kube-system

# Template file  
    spec:
      containers:
      - args:
        - --ingress-class=alb
        - --cluster-name=prod

# Replaced cluster-name with our cluster-name
    spec:
      containers:
      - args:
        - --ingress-class=alb
        - --cluster-name=demo1
```

## Step-09: Verify our ALB Ingress Controller is running. 
- Verify for the pod starting with `alb-ingress-controller`
```
kubectl get pods -n kube-system
```

# Module - 2: Deploy ALB Ingress Controller - Basic

## Step-01: Introduction
- Understand about ALB Ingress Annotations. 

## Step-02: Create ALB kubernetes basic Ingress Manifest
- Create a basic ALB Ingress template. 
- **05-ALB-Ingress-Basic.yml**
```yml
# Annotations Reference:  https://kubernetes-sigs.github.io/aws-alb-ingress-controller/guide/ingress/annotation/
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  name: ingress-usermgmt-restapp-service
  labels:
    app: usermgmt-restapp
  annotations:
    kubernetes.io/ingress.class: "alb"
    alb.ingress.kubernetes.io/scheme: internet-facing
    alb.ingress.kubernetes.io/healthcheck-protocol: HTTP 
    alb.ingress.kubernetes.io/healthcheck-port: traffic-port
    alb.ingress.kubernetes.io/healthcheck-path: /usermgmt/health-status
    alb.ingress.kubernetes.io/healthcheck-interval-seconds: '15'
    alb.ingress.kubernetes.io/healthcheck-timeout-seconds: '5'
    alb.ingress.kubernetes.io/success-codes: '200'
    alb.ingress.kubernetes.io/healthy-threshold-count: '2'
    alb.ingress.kubernetes.io/unhealthy-threshold-count: '2'
spec:
  rules:
    - http:
        paths:
          - path: /*
            backend:
              serviceName: usermgmt-restapp-nodeport-service
              servicePort: 8095
```
## Step-03: Deploy Application with ALB Ingress Template included
```
# Deploy Application with ALB Template
kubectl apply -f V1-ALB-Ingress-Basic/

# Get Ingress Controller Status (Make a note of Address field)
kubectl get ingress

# Describe Ingress Controller
kubectl describe ingress ingress-usermgmt-restapp-service 
```

## Step-04: Verify the ALB in AWS Management Console & Access Application using ALB DNS URL
- Verify Load Balancer
    - Listeners Tab
- Verify Target Groups
    - GroupD Details
    - Targets: Ensure they are healthy
- Access Application
```
http://<ALB-DNS-URL>/usermgmt/health-status
```

## Step-05: Clean Up
```
kubectl delete -f V1-ALB-Ingress-Basic/
```

# Module - 2: Deploy ALB Ingress Controller - Path Based Routing

## Step-01: Create Nginx App1 Deployment & Service
- **05-Nginx-App1-Deployment-and-NodePortService.yml**
```yml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app1-nginx-deployment
  labels:
    app: app1-nginx
spec:
  replicas: 1
  selector:
    matchLabels:
      app: app1-nginx
  template:
    metadata:
      labels:
        app: app1-nginx
    spec:
      containers:
      - name: app1-nginx
        image: stacksimplify/kube-nginxapp1:1.0.0
        ports:
        - containerPort: 80
---
apiVersion: v1
kind: Service
metadata:
  name: app1-nginx-service
  labels:
    app: app1-nginx
  annotations:
#Important Note:  Need to add health check path annotations in service level if we are planning to use multiple targets in a load balancer    
    alb.ingress.kubernetes.io/healthcheck-path: /app1/index.html
spec:
  type: NodePort
  selector:
    app: app1-nginx
  ports:
  - port: 80
    targetPort: 80
```
## Step-02: Create Nginx App1 Deployment & Service
- **06-Nginx-App2-Deployment-and-NodePortService copy.yml**
```yml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app2-nginx-deployment
  labels:
    app: app2-nginx 
spec:
  replicas: 1
  selector:
    matchLabels:
      app: app2-nginx
  template:
    metadata:
      labels:
        app: app2-nginx
    spec:
      containers:
      - name: app2-nginx
        image: stacksimplify/kube-nginxapp2:1.0.0
        ports:
        - containerPort: 80
---
apiVersion: v1
kind: Service
metadata:
  name: app2-nginx-service
  labels:
    app: app2-nginx
  annotations:
#Important Note:  Need to add health check path annotations in service level if we are planning to use multiple targets in a load balancer
    alb.ingress.kubernetes.io/healthcheck-path: /app2/index.html
spec:
  type: NodePort
  selector:
    app: app2-nginx
  ports:
  - port: 80
    targetPort: 80   
```
## Step-03: Update Health Check Path Annotation in User Management Node Port Service
- Health check path annotation should be moved to respective node port services if we have to route to multiple targets using single load balancer.
- **04-UserManagement-NodePort-Service.yml**
```yml
apiVersion: v1
kind: Service
metadata:
  name: usermgmt-restapp-nodeport-service
  labels:
    app: usermgmt-restapp
  annotations:
#Important Note:  Need to add health check path annotations in service level if we are planning to use multiple targets in a load balancer  
    alb.ingress.kubernetes.io/healthcheck-path: /usermgmt/health-status
spec:
  type: NodePort
  selector:
    app: usermgmt-restapp
  ports:
  - port: 8095
    targetPort: 8095
```

## Step-04: Create ALB Ingress Context path based Routing Kubernetes manifest
- **07-ALB-Ingress-ContextPath-Based-Routing.yml**
```yml
# Annotations Reference:  https://kubernetes-sigs.github.io/aws-alb-ingress-controller/guide/ingress/annotation/
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  name: ingress-usermgmt-restapp-service
  labels:
    app: usermgmt-restapp
  annotations:
    kubernetes.io/ingress.class: "alb"
    alb.ingress.kubernetes.io/scheme: internet-facing
    alb.ingress.kubernetes.io/healthcheck-protocol: HTTP 
    alb.ingress.kubernetes.io/healthcheck-port: traffic-port
#Important Note:  Need to add health check path annotations in service level if we are planning to use multiple targets in a load balancer    
    #alb.ingress.kubernetes.io/healthcheck-path: /usermgmt/health-status
    alb.ingress.kubernetes.io/healthcheck-interval-seconds: '15'
    alb.ingress.kubernetes.io/healthcheck-timeout-seconds: '5'
    alb.ingress.kubernetes.io/success-codes: '200'
    alb.ingress.kubernetes.io/healthy-threshold-count: '2'
    alb.ingress.kubernetes.io/unhealthy-threshold-count: '2'
spec:
  rules:
    - http:
        paths:
          - path: /app1/*
            backend:
              serviceName: app1-nginx-service
              servicePort: 80                        
          - path: /app2/*
            backend:
              serviceName: app2-nginx-service
              servicePort: 80            
          - path: /*
            backend:
              serviceName: usermgmt-restapp-nodeport-service
              servicePort: 8095              
# Important Note-1: In path based routing order is very important, if we are going to use  "/*", try to use it at the end of all rules.                  
```

## Step-05: Deploy all manifests and test
- **Deploy**
```
kubectl apply -f V2-ALB-Ingress-ContextPath-Based-Routing/
```
- **Verify**
    - Load Balancer - Rules
    - Target Groups - Group Details (Verify Health check path)
    - Target Groups - Targets (Verify all 3 targets are healthy)
- **Access Application**
```
http://<ALB-DNS-URL>/app1
http://<ALB-DNS-URL>/app2
http://<ALB-DNS-URL>/usermgmt/health-status
```


## References: 
- Good to refer all the below for additional understanding.

### ALB Pre-requisite Setup - References: 
- https://github.com/kubernetes-sigs/aws-alb-ingress-controller
- Examples:
  - https://github.com/kubernetes-sigs/aws-alb-ingress-controller/tree/master/docs/examples/2048

### AWS ALB Ingress Annotations Reference
- https://kubernetes-sigs.github.io/aws-alb-ingress-controller/guide/ingress/annotation/

### eksctl getting started
- https://eksctl.io/introduction/#getting-started