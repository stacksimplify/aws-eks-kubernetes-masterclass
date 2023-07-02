# Rollback Deployment

## Step-00: Introduction
- We can rollback a deployment in two ways.
  - Previous Version
  - Specific Version

## Step-01: Rollback a Deployment to previous version

### Check the Rollout History of a Deployment
```
# List Deployment Rollout History
kubectl rollout history deployment/<Deployment-Name>
kubectl rollout history deployment/my-first-deployment  
```

### Verify changes in each revision
- **Observation:** Review the "Annotations" and "Image" tags for clear understanding about changes.
```
# List Deployment History with revision information
kubectl rollout history deployment/my-first-deployment --revision=1
kubectl rollout history deployment/my-first-deployment --revision=2
kubectl rollout history deployment/my-first-deployment --revision=3
```


### Rollback to previous version
- **Observation:** If we rollback, it will go back to revision-2 and its number increases to revision-4
```
# Undo Deployment
kubectl rollout undo deployment/my-first-deployment

# List Deployment Rollout History
kubectl rollout history deployment/my-first-deployment  
```

### Verify Deployment, Pods, ReplicaSets
```
kubectl get deploy
kubectl get rs
kubectl get po
kubectl describe deploy my-first-deployment
```

### Access the Application using Public IP
- We should see `Application Version:V2` whenever we access the application in browser
```
# Get Load Balancer IP
kubectl get svc

# Application URL
http://<External-IP-from-get-service-output>
```


## Step-02: Rollback to specific revision
### Check the Rollout History of a Deployment
```
# List Deployment Rollout History
kubectl rollout history deployment/<Deployment-Name>
kubectl rollout history deployment/my-first-deployment 
```
### Rollback to specific revision
```
# Rollback Deployment to Specific Revision
kubectl rollout undo deployment/my-first-deployment --to-revision=3
```

### List Deployment History
- **Observation:** If we rollback to revision 3, it will go back to revision-3 and its number increases to revision-5 in rollout history
```
# List Deployment Rollout History
kubectl rollout history deployment/my-first-deployment  
```


### Access the Application using Public IP
- We should see `Application Version:V3` whenever we access the application in browser
```
# Get Load Balancer IP
kubectl get svc

# Application URL
http://<Load-Balancer-IP>
```

## Step-03: Rolling Restarts of Application
- Rolling restarts will kill the existing pods and recreate new pods in a rolling fashion. 
```
# Rolling Restarts
kubectl rollout restart deployment/<Deployment-Name>
kubectl rollout restart deployment/my-first-deployment

# Get list of Pods
kubectl get po
```