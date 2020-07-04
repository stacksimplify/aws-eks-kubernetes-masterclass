# EKS - Fargate Profiles

## Step-01: What are we going to learn?
- **Assumptions:**
  - We already havea EKS Cluster whose name is eksdemo1 created using eksctl
  - We already have a Managed Node Group with private networking enabled with two worker nodes
- We are going to create a fargate profile using eksctl on our existing EKS Cluster eksdemo1
- We are going to deploy a simple workload
  - Deployment: Nginx App 1
  - NodePort Service: Nginx App1 
  - Ingress Service: Application Load Balancer 
- Ingress manifest going to have a additional annotation related to `target-type: ip` as these are going to be fargate workloads.

## Step-02: Create Fargate Profile
### Create Fargate Profile
```
# Template
eksctl create fargateprofile --cluster <cluster_name> \
                             --name <fargate_profile_name> \
                             --namespace <kubernetes_namespace>


# Replace values
eksctl create fargateprofile --cluster eksdemo1 \
                             --name fp-demo \
                             --namespace fp-dev
```

### Output
```log
[ℹ]  Fargate pod execution role is missing, fixing cluster stack to add Fargate resources
[ℹ]  checking cluster stack for missing resources
[ℹ]  cluster stack is missing resources for Fargate
[ℹ]  adding missing resources to cluster stack
[ℹ]  re-building cluster stack "eksctl-eksdemo1-cluster"
[ℹ]  updating stack to add new resources [FargatePodExecutionRole] and outputs [FargatePodExecutionRoleARN]
[ℹ]  creating Fargate profile "fp-demo" on EKS cluster "eksdemo1"
[ℹ]  created Fargate profile "fp-demo" on EKS cluster "eksdemo1"
```
## Step-03: Review NGINX App1 & Ingress Manifests
- We are going to deploy a simple NGINX App1 with Ingress Load Balancer
- We cannot use NodePort Service for Fargate Pods for two reasons
  - Fargate Pods are created in Private Subnets, so no access to internet to access
  - Fargate Pods are created on random worker nodes whose information is unknown to us to use NodePort Service
### Create Namespace Manifest 
- This namespace manifest should match the one with we have created the Fargate Profile namespace value `fp-dev`
```yml
apiVersion: v1
kind: Namespace
metadata: 
  name: fp-dev
```

### Update All other manifests with namespace tag in metadata section
```yml
  namespace: fp-dev 
```

### Update Ingress Manifest
- As we are running our pods on Fargate Serverless, we need to change our target-type to IP as there is no dedicated EC2 worker nodes concept in Fargate. 
```yml
    # For Fargate
    alb.ingress.kubernetes.io/target-type: ip    
```
- Also update the DNS Names
```yml
    # External DNS - For creating a Record Set in Route53
    external-dns.alpha.kubernetes.io/hostname: fpdev1.kubeoncloud.com, fpdev2.kubeoncloud.com   
```

## Step-04: Deploy Workload
```
# Deploy 
kubectl apply -f kube-manifests/

# List Namespaces
kubectl get ns

# List Pods from fpdev namespace
kubectl get pods -n fp-dev -o wide

# List Worker Nodes
kubectl get nodes -o wide

# List Ingress
kubectl get ingress -n fp-dev
```

## Step-05: Access Application & Test
```
http://fpdev1.kubeoncloud.com/app1/index.html
```


## Step-06: Delete Fargate Profile
```
# Get list of Fargate Profiles in a cluster
eksctl get fargateprofile --cluster eksdemo1

# Delete Fargate Profile
eksctl delete fargateprofile --cluster <cluster-name> --name <Fargate-Profile-Name> --wait
eksctl delete fargateprofile --cluster eksdemo1 --name fp-demo --wait
```

## References
- https://eksctl.io/usage/fargate-support/
- https://docs.aws.amazon.com/eks/latest/userguide/fargate.html