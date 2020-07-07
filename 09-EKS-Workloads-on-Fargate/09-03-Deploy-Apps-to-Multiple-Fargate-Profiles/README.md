# Deploy workloads to multiple fargate profiles

## Step-01: What are we going to learn?
- We are going to create 3 namespaces and deploy workloads to all 3 namespaces.
- **Namespaces**
  - 01-fp-app1: On Worker Nodes
  - 02-fp-app2: On Fargate 
  - 03-fp-ums: On Fargate
- We are going to review all 3 namespaces. 
- In each environment (dev, stage and prod), as usual we are going to 3 Apps
  - UMS - User Management Microservice with RDS Database
  - App1 -  Nginx App1
  - App2 -  Nginx App2
- **fp-app1** going to run on regular EC2 Worker Node Group
- **fp-app2** and **fp-ums** going to run on fargate when we deploy them.
- We are also going to add labels in `fp-ums` so the kube manifests who have the label `runon: fargate` only going to run on fargate, in simple terms those who have `runon: fargate` label will get scheduled on fargate rest all will be in `pending state`


## Step-02: Review the Manifests with naemspaces which already created
- We are going to deploy a simple NGINX App2 with Ingress Load Balancer in `fp-app2` namespace in `fp-app2-profile`
- We are going to deploy a UMS (User Management Microservice) with Ingress Load Balancer in `fp-ums` namespace in `fp-ums-profile`
- We cannot use NodePort Service for Fargate Pods for two reasons
  - Fargate Pods are created in Private Subnets, so no access to internet to access
  - Fargate Pods are created on random worker nodes whose information is unknown to us to use NodePort Service

### Review Namespace Manifest fp-app2, fp-ums
- This namespace manifest should match the one with we have created the Fargate Profile namespace value `fp-app2, fp-ums`
```yml
apiVersion: v1
kind: Namespace
metadata: 
  name: fp-app2
---
apiVersion: v1
kind: Namespace
metadata: 
  name: fp-ums
```

### Update All other manifests with namespace tag in metadata section in 02-fp-app2
```yml
  namespace: fp-app2 
```

### Update All other manifests with namespace tag in metadata section in 03-fp-ums
```yml
  namespace: fp-ums
```


### Update All Deployment Manifests with Resources in Pod Template 
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
```yml
    # For Fargate
    alb.ingress.kubernetes.io/target-type: ip    
```
- Also update the DNS Names
```yml
# 02-fp-app2
    # External DNS - For creating a Record Set in Route53
    external-dns.alpha.kubernetes.io/hostname: app2.kubeoncloud.com

# 02-fp-ums
    # External DNS - For creating a Record Set in Route53
    external-dns.alpha.kubernetes.io/hostname: ums.kubeoncloud.com
```



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
- Each Pod will have one Fargate Node, for 3 apps in all deployment files we have given `replicas: 2` which means 6 pods. So we should 6 fargate instances created. 
-  Equation here is Number of Pods equal to Number of Fargate Nodes (1 pod per 1 fargate node)
```
# Verify Nodes (we should see nodes starting with name fargate - 6 nodes for 3 apps )
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
http://app1.kubeoncloud.com/app1/index.html
http://app2.kubeoncloud.com/app2/index.html
http://ums.kubeoncloud.com/usermgmt/health-status
```

## Step-06: Delete Fargate Profiles
```
# Switch Directory
cd ../09-02-Fargate-Profiles-Advanced

# Delete Fargate Profiles
eksctl delete fargateprofile --cluster eksdemo1 --name fp-app2-profile --wait
eksctl delete fargateprofile --cluster eksdemo1 --name fp-ums-profile --wait
```
