# Create EKS Cluster & Node Groups

## Step-00: Introduction
- Create EKS Cluster
- Associate EKS Cluster to IAM OIDC Provider
- Create EKS Node Groups


## Step-01: Create EKS Cluster using eksctl
```
# Create Cluster
eksctl create cluster --name=eksdemo1 \
                      --region=us-east-1 \
                      --zones=us-east-1a,us-east-1b \
                      --without-nodegroup \
                      --vpc-nat-mode=Single   
```


## Step-02: Associate IAM OIDC Provider to our EKS Cluster
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


## Step-03: Create Node Group with additional Add-Ons in Public Subnets
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
                        --ssh-public-key=kube-demo \
                        --managed \
                        --asg-access \
                        --external-dns-access \
                        --full-ecr-access \
                        --appmesh-access \
                        --alb-ingress-access 
```

## Step-04: Verify Cluster & Nodes
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

## Step-05: Update Worker Nodes Security Group to allow all traffic
- We need to allow `All Traffic` on worker node security group