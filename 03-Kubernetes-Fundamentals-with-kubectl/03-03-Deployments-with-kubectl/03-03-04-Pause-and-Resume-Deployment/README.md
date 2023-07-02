# Pause & Resume Deployments

## Step-00: Introduction
- Why do we need Pausing & Resuming Deployments?
  - If we want to make multiple changes to our Deployment, we can pause the deployment make all changes and resume it. 
- We are going to update our Application Version from **V3 to V4** as part of learning "Pause and Resume Deployments"  

## Step-01: Pausing & Resuming Deployments
### Check current State of Deployment & Application
 ```
# Check the Rollout History of a Deployment
kubectl rollout history deployment/my-first-deployment  
Observation: Make a note of last version number

# Get list of ReplicaSets
kubectl get rs
Observation: Make a note of number of replicaSets present.

# Access the Application 
http://<External-IP-from-get-service-output>
Observation: Make a note of application version
```

### Pause Deployment and Two Changes
```
# Pause the Deployment
kubectl rollout pause deployment/<Deployment-Name>
kubectl rollout pause deployment/my-first-deployment

# Update Deployment - Application Version from V3 to V4
kubectl set image deployment/my-first-deployment kubenginx=stacksimplify/kubenginx:4.0.0 --record=true

# Check the Rollout History of a Deployment
kubectl rollout history deployment/my-first-deployment  
Observation: No new rollout should start, we should see same number of versions as we check earlier with last version number matches which we have noted earlier.

# Get list of ReplicaSets
kubectl get rs
Observation: No new replicaSet created. We should have same number of replicaSets as earlier when we took note. 

# Make one more change: set limits to our container
kubectl set resources deployment/my-first-deployment -c=kubenginx --limits=cpu=20m,memory=30Mi
```
### Resume Deployment 
```
# Resume the Deployment
kubectl rollout resume deployment/my-first-deployment

# Check the Rollout History of a Deployment
kubectl rollout history deployment/my-first-deployment  
Observation: You should see a new version got created

# Get list of ReplicaSets
kubectl get rs
Observation: You should see new ReplicaSet.

# Get Load Balancer IP
kubectl get svc
```
### Access Application
```
# Access the Application 
http://<External-IP-from-get-service-output>
Observation: You should see Application V4 version
```


## Step-02: Clean-Up
```
# Delete Deployment
kubectl delete deployment my-first-deployment

# Delete Service
kubectl delete svc my-first-deployment-service

# Get all Objects from Kubernetes default namespace
kubectl get all
```