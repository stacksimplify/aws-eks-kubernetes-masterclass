# Deploy workloads to multiple fargate profiles

## Step-01: What are we going to learn?
- We are going to create 3 namespaces and deploy workloads to all 3 namespaces.
- **Namespaces**
  - 01-fp-dev
  - 02-fp-stage
  - 03-fp-prod
- We are going to review all 3 namespaces. 
- In each environment (dev, stage and prod), as usual we are going to 3 Apps
  - UMS - User Management Microservice with RDS Database
  - App1 -  Nginx App1
  - App2 -  Nginx App2
- **fp-dev** going to run on regular EC2 Worker Node Group
- **fp-stage** and **fp-prod** going to run on fargate when we deploy them.
- We are also going to add labels in `fp-prod` so the kube manifests who have the label `runon: fargate` only going to run on fargate, in simple terms those who have `runon: fargate` label will get scheduled on fargate rest all will be in `pending state`


## Step-02: Review the Manifests with naemspaces which already created
- 01-fp-dev
- 02-fp-stage
- 03-fp-prod

## Step-03: Deploy Manifests & Verify

### Deploy & Verify
```
# Deploy all 3 environments
kubectl apply -R -f kube-manifests/

# Verify ingress from all Namespaces
kubectl get ingress --all-namespaces

# Verify Pods from all Namespaces
kubectl get pods --all-namespaces

# Verify all Objets
kubectl get all --all-namespaces
```

### Verify Fargate Only resources
```
# Verify Nodes (we should see nodes starting with name fargate)
kubectl get nodes -o wide

# List Pods (We should see few pods scheduled on fargate nodes)
kubectl get pods -o wide
```

### Verify Application Load Balancer Target Groups
- Go to Services -> EC2 -> Load Balancers -> Target Groups
- Open One Target Group
- Verify that 


## Step-04: Verify Route53 DNS Names
- Go to Services -> Route53 -> Hosted Zones -> kubeoncloud.com
- Verify Record Sets


## Step-05: Access Application (One App per Environment)
```
http://dev1.kubeoncloud.com/app1/index.html
http://stage1.kubeoncloud.com/app2/index.html
http://prod1.kubeoncloud.com/usermgmt/health-status
```

## Step-06: Delete Fargate Profiles
```
# Switch Directory
cd ../09-02-Fargate-Profiles-Advanced

# Delete Fargate Profiles
eksctl create fargateprofile -f kube-manifests/01-fargate-profiles.yml
```
