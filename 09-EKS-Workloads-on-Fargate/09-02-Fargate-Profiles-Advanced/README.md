# Create 3 environments using Namespaces

## Step-01: What are we going to learn?
- We are going to learn about writing Fargate Profiles using YAML wherein with YAML we can create multiple fargate profiles at a time. 
- Understand about `namespaces and labels` in `fargate profiles`

## Step-02: Create Advanced Fargate Profile with yml

### Create Fargate Profile manifest
```yml
apiVersion: eksctl.io/v1alpha5
kind: ClusterConfig
metadata:
  name: eksdemo1  # Name of the EKS Cluster
  region: us-east-1
fargateProfiles:
  - name: fp-app2-profile
    selectors:
      # All workloads in the "fp-app2" Kubernetes namespace will be
      # scheduled onto Fargate:      
      - namespace: fp-app2
  - name: fp-ums-profile
    selectors:
      # All workloads in the "fp-ums" Kubernetes namespace matching the following
      # label selectors will be scheduled onto Fargate:      
      - namespace: fp-ums
        labels:
          runon: fargate     
  - name: fp-default-profile
    selectors:
      # All workloads in the "default" Kubernetes namespace will be
      # scheduled onto Fargate:
      - namespace: default
      # All workloads in the "kube-system" Kubernetes namespace will be
      # scheduled onto Fargate:
      - namespace: kube-system          
```

## Step-03: Create Fargate Profiles
```
eksctl create fargateprofile -f kube-manifests/01-fargate-profiles.yml
```

## Step-04:  Get list of Fargate profiles
```
# List Fargate profiles
eksctl get fargateprofile --cluster eksdemo1

# View in yaml format
eksctl get fargateprofile --cluster eksdemo1 -o yaml
```

## Step-05: Verify pods from kube-system and default namespaces
- All pods should be running on Fargate Nodes.
```
# Get Current Worker Nodes in Kubernetes cluster
kubectl get nodes -o wide

# Verify Pods from namespace: kube-system
kubectl get pods -n kube-system

# Verify pods from namespace: default
kubectl get pods
```
