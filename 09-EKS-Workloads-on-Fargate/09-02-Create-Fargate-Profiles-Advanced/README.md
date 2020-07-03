# Create 3 environments using Namespaces

## Step-01: Introduction

## Step-02: Create Advanced Fargate Profile with yml

### Create Fargate Profile manifest
```yml
apiVersion: eksctl.io/v1alpha5
kind: ClusterConfig

metadata:
  name: eksdemo1
  region: us-east-1

fargateProfiles:
  - name: fp-stage-profile
    selectors:
      - namespace: fp-stage
  - name: fp-prod-profile
    selectors:
      - namespace: fp-prod
        labels:
          runon: fargate     
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

## Step-03: Deploy our Application Workloads
```
kubectl apply -R -f kube-manifests/02-Apps
```



### Delete Fargate Profile
```
eksctl delete fargateprofile --cluster eksdemo1 --name fp-dev --wait
```


## Step-02: Review the Manifests with naemspaces which already created
- 01-dev
- 02-staging
- 03-prod

## Step-03: Deploy Manifests & Verify
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

### Verify Route53 DNS Names
- Go to Services -> Route53 -> Hosted Zones -> kubeoncloud.com
- Verify Record Sets

### Access Application (One URL per Environment)
```
http://dev1.kubeoncloud.com/app1/index.html
http://stage1.kubeoncloud.com/app2/index.html
http://prod1.kubeoncloud.com/usermgmt/health-status
```

