# ALB Install Ingress Controller

## Step-01: Introduction
- We will install eksctl (if not installed)
- We will create a EKS Cluster with no node groups
- We will create a public **managed** node group with additional add-on policies added to it. 
- We will create kubernetes service account for ALB Ingress Controller
- We wil associate the service account with AWS IAM Role
- We will deploy ALB Ingress Controller and Test if that respective POD is finally running


## Step-02: Install eksctl
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


## Step-03: Create EKS Cluster using eksctl
```
# Create Cluster
eksctl create cluster --name=eksdemo1 \
                      --region=us-east-1 \
                      --zones=us-east-1a,us-east-1b \
                      --without-nodegroup \
                      --vpc-nat-mode=Single   
```


## Step-04: Associate IAM OIDC Provider to our EKS Cluster
- eksctl version should 0.20.0-rc.0 or later 
```                   
# Template
eksctl utils associate-iam-oidc-provider \
    --region region-code \
    --cluster <cluter-name> \
    --approve

# Replace with region & cluster name
eksctl utils associate-iam-oidc-provider \
    --region us-east-1 \
    --cluster eksdemo1 \
    --approve
```



## Step-05: Create Node Group with additional Add-Ons in Public Subnets
- These add-ons will create the respective IAM Roles for us automatically within our Node Group role. 
```
# Create Public Node Group   
eksctl create nodegroup --cluster=eksdemo1 \
                        --region=us-east-1 \
                        --name=eksdemo1-ng-public1 \
                        --node-type=t3.medium \
                        --nodes=2 \
                        --nodes-min=2 \
                        --nodes-max=4 \
                        --node-volume-size=20 \
                        --ssh-access \
                        --ssh-public-key=kube-demo-2020 \
                        --managed \
                        --asg-access \
                        --external-dns-access \
                        --full-ecr-access \
                        --appmesh-access \
                        --alb-ingress-access \
                        --node-labels="app=microservices,tier=backend"
```

## Step-06: Verify Cluster & Nodes
- Verify the node group subnet to ensure it created in public subnets
  - Go to Services -> EKS -> eksdemo -> eksdemo1-ng1-public
  - Click on Associated subnet in **Details** tab
  - Click on **Route Table** Tab.
  - We should see that internet route via Internet Gateway (0.0.0.0/0 -> igw-xxxxxxxx)
```
# Get List of clusters
eksctl get cluster

# Get Nodes in current cluster
kubectl get nodes -o wide

# Our kubectl context should be automatically changed to new cluster
kubectl config view --minify
```

## Step-07: Create IAM Policy for ALB Ingress Controller
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

## Step-08: Create a Kubernetes service account named alb-ingress-controller in the kube-system namespace
- We are using master branch instead of v1.1.4 
```
kubectl apply -f https://raw.githubusercontent.com/kubernetes-sigs/aws-alb-ingress-controller/master/docs/examples/rbac-role.yaml
```

## Step-09: Create an IAM role for the ALB Ingress Controller and attach the role to the service account 
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
    --cluster eksdemo1 \
    --attach-policy-arn arn:aws:iam::411686525067:policy/ALBIngressControllerIAMPolicy \
    --override-existing-serviceaccounts \
    --approve
```


## Step-11: Deploy ALB Ingress Controller
- We are using Master branch file instead of 1.1.4
```
kubectl apply -f https://raw.githubusercontent.com/kubernetes-sigs/aws-alb-ingress-controller/master/docs/examples/alb-ingress-controller.yaml
```

## Step-12: Edit ALB Ingress Controller Manifest
- Edit ALB Ingress Controller manifest and update cluster name in that. 
```
kubectl edit deployment.apps/alb-ingress-controller -n kube-system

# Template file  
    spec:
      containers:
      - args:
        - --ingress-class=alb
        - --cluster-name=cluster-name

# Replaced cluster-name with our cluster-name
    spec:
      containers:
      - args:
        - --ingress-class=alb
        - --cluster-name=eksdemo1
```

## Step-11: Verify our ALB Ingress Controller is running. 
- Verify for the pod starting with `alb-ingress-controller`
- We will know if all our above steps are working or not in our next section **09-02-ALB-Ingress-Basic**, if ALB not created then we something is wrong.
```
# Verify if alb-ingress-controller pod is running
kubectl get pods -n kube-system

# Verify logs
kubectl logs -f $(kubectl get po -n kube-system | egrep -o 'alb-ingress-controller-[A-Za-z0-9-]+') -n kube-system
```
