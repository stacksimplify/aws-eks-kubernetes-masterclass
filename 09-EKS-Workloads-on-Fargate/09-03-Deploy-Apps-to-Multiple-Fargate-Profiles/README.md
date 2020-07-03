# Create 3 environments using Namespaces

## Step-01: Introduction


## Step-02: Review the Manifests with naemspaces which already created
- 01-fp-dev
- 02-fp-stage
- 03-fp-prod

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



## Step-05: Verify Route53 DNS Names
- Go to Services -> Route53 -> Hosted Zones -> kubeoncloud.com
- Verify Record Sets

### Access Application (One URL per Environment)
```
http://dev1.kubeoncloud.com/app1/index.html
http://stage1.kubeoncloud.com/app2/index.html
http://prod1.kubeoncloud.com/usermgmt/health-status
```




### Delete Fargate Profile
```
eksctl delete fargateprofile --cluster eksdemo1 --name fp-dev --wait
```

