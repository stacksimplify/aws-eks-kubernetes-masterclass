# EKS Fargate Profiles - Basics

## Step-01: What are we going to learn?
- **Assumptions:**
  - We already havea EKS Cluster whose name is **eksdemo1** created using eksctl
  - We already have a Managed Node Group with private networking enabled with two worker nodes
- We are going to create a fargate profile using `eksctl` on our existing EKS Cluster eksdemo1
- We are going to deploy a simple workload
  - **Deployment:** Nginx App 1
  - **NodePort Service:** Nginx App1 
  - **Ingress Service:** Application Load Balancer 
- Ingress manifest going to have a additional annotation related to `target-type: ip` as these are going to be fargate workloads we are not going to have `Dedicated EC2 Worker Node - Node Ports`

## Step-02: Pre-requisites
### Pre-requisite Note about eksctl CLI
- eksctl will have continuous releases with new feature additions to it. Its always good to be on latest version of eksctl. 
- You can upgrade to latest version using below command on Mac
- Currently highly evolving space (continuous features and new releases) from Kubernetes in AWS is eksctl and Fargate. 
- **eksctl Releases URL:** https://github.com/weaveworks/eksctl/releases
```
# Check version
eksctl version

# Update eksctl on mac
brew upgrade eksctl && brew link --overwrite eksctl

# Check version
eksctl version
```

### Pre-requisite check about ALB Ingress Controller & external-dns
- We need to have the below two listed components to be already running on our NodeGroup before deploying our application on fargate. 
  - ALB Ingress Controller
  - External DNS
- For our application, in addition to just deploying it we are going to access it via DNS registed url `fpdev.kubeoncloud.com`

```
# Get Current Worker Nodes in Kubernetes cluster
kubectl get nodes -o wide

# Verify Ingress Controller Pod running
kubectl get pods -n kube-system

# Verify external-dns Pod running
kubectl get pods
```

## Step-03: Create Fargate Profile on cluster eksdemo1
### Create Fargate Profile
```
# Get list of Fargate Profiles in a cluster
eksctl get fargateprofile --cluster eksdemo1

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
## Step-04: Review NGINX App1 & Ingress Manifests
- We are going to deploy a simple NGINX App1 with Ingress Load Balancer
- We cannot use Worker Node Node Ports for Fargate Pods for two reasons
  - Fargate Pods are created in Private Subnets, so no access to internet to access
  - Fargate Pods are created on random worker nodes whose information is unknown to us to use NodePort Service
  - But in our case, we are in mixed environment with Node Groups and Fargate, if we create a NodePort service, it will create the service with Node Group EC2 Worker Nodes Ports and it will work but when we delete those Node Groups, we will have an issue. 
  - Always recommended to use `alb.ingress.kubernetes.io/target-type: ip` in ingress manifest for Fargate workloads
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

### Update All Deployment Manifests with Resources in Pod Template
- In Fargate, it is super highly recommended to provide the `resources.requests, resources.limits` about `cpu and memory`.  Almost you can make it mandatory. 
- This will help Fargate to schedule a Fargate Host accordingly. 
- As fargate follows `1:1` ratio `Host:Pod`, one pod per host concept, we defining `resources` section in pod template (Deployment pod template spec) should be our mandatory option.
- Even if we forget to define `resources` in our Deployment Pod Template, low memory using pods like NGINX will come up, high memory using Apps like Spring Boot REST APIs will keep restarting continuously due to unavailable resources.
```yml
          resources:
            requests:
              memory: "128Mi"
              cpu: "500m"
            limits:
              memory: "500Mi"
              cpu: "1000m"    
```

### Update Ingress Manifest
- As we are running our pods on Fargate Serverless, we need to change our target-type to IP as there is no dedicated EC2 worker nodes concept in Fargate. 
- **Important Note:** When we are using same ingress in mixed mode deployments `Node Groups & Fargate` we can use this annotation at service level.
```yml
    # For Fargate
    alb.ingress.kubernetes.io/target-type: ip    
```
- Also update the DNS Names
```yml
    # External DNS - For creating a Record Set in Route53
    external-dns.alpha.kubernetes.io/hostname: fpdev.kubeoncloud.com   
```

## Step-05: Deploy Workload to Fargate
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

## Step-06: Access Application & Test
```
# Access Application
http://fpdev.kubeoncloud.com/app1/index.html
```


## Step-07: Delete Fargate Profile
```
# Get list of Fargate Profiles in a cluster
eksctl get fargateprofile --cluster eksdemo1

# Delete Fargate Profile
eksctl delete fargateprofile --cluster <cluster-name> --name <Fargate-Profile-Name> --wait
eksctl delete fargateprofile --cluster eksdemo1 --name fp-demo --wait
```


## Step-08: Verify NGINX App1 got scheduled on Managed Node Group
- After fargate profile deletions, apps running on fargate will be scheduled on Node Groups if they exists if not will go to pending state
```
# List Pods from fpdev namespace
kubectl get pods -n fp-dev -o wide
```

## Step-09: Clean-up
```
# Delete
kubectl delete -f kube-manifests/
```


## References
- https://eksctl.io/usage/fargate-support/
- https://docs.aws.amazon.com/eks/latest/userguide/fargate.html
- https://kubernetes-sigs.github.io/aws-alb-ingress-controller/guide/ingress/annotation/#annotations
- https://kubernetes-sigs.github.io/aws-alb-ingress-controller/guide/ingress/annotation/#traffic-routing