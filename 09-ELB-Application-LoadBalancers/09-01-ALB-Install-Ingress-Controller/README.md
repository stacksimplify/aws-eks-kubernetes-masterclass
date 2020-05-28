# ALB Install Ingress Controller

## Introduction
-  Need to understand what are managed and unmanaged nodes? What is the difference? 

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
