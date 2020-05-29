# Create and administer EKS Clusters using eksctl

## Step-01: Creat Cluster using eksctl
```
eksctl create cluster --name=staging --version=1.16 --nodes-min=2 --nodes-max=2 --node-type=t3.medium --ssh-access --ssh-public-key=kube-demo-2020 --region=us-east-1 --tags environment=staging --node-volume-size=20 --node-volume-type=gp2 --zones=us-east-1a,us-east-1b
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


## Delete Node Group
```
# Capture Node Group name
eksctl get nodegroup --cluster=demo1

# Delete Node Group
eksctl delete nodegroup --cluster=<clusterName> --name=<nodegroupName>
eksctl delete nodegroup --cluster=demo1 --name=ng-public-1
```

## Scale a Node Group
```
eksctl scale nodegroup --cluster=<clusterName> --nodes=<desiredCount> --name=<nodegroupName>
eksctl scale nodegroup --cluster=demo1 --nodes=2 --name=ng-621c8574
```

## Create new Node Group
```
eksctl create nodegroup --cluster=demo1 --name=ng-public-1
```

## Delete Cluster  (DONT DELETE)
```
eksctl delete cluster demo1
```
## References:
- https://eksctl.io/introduction/