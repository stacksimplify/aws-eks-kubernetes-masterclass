# Microservices Canary Deployments with AppMesh

## Step-01: Introduction


## Step-02: Create AppMesh Objects for Notification Microservice V2
- V2 states notification microservice application version is V2
- We only need to create `Virtual Node` for V2 version Notification Microservice and update `Notification Virtual Service` with 50% traffic to V1 and 50% traffic to V2

### Create AppMesh Virtual Node & Update Virtual Service
- 08-virtual-node-notification-microservice-v2.yml
- 09-virtual-service-notification-microservice.yml

### Deploy AppMesh Virtual Node & Virtual Service
```
# Deploy Virtual Node
kubectl apply -f 08-virtual-node-notification-microservice-v2.yml

# Deploy Updated Virtual Service
kubectl apply -f 09-virtual-service-notification-microservice.yml

# Get Virtual Nodes
kubectl -n microservices get virtualnode
kubectl -n microservices get virtualservice
```

####  Verify virtual node & Virtual Service created in AppMesh using AWS Management Console
- Go to Services -> AWS App Mesh -> appmesh
  - Verify Virtual Nodes
  - Verify Virtual Services
  - Verify Virtual Router: You should see traffic routing update to 50% to V1 and 50% to V2 notification vnodes. 


## Step-03: Create & Deploy Notification Microservice V2 Deployment & Service
```
# Deploy Notificaiton Microservice V2
kubectl apply -f 10-notification-microservice-Deployment-Service-v2.yml

# List Pods
kubectl -n microservices get pods

# Describe Pod (Should have init and envoy containers)
kubectl -n microservices describe pod <pod-name>
kubectl -n microservices describe pod notification-v2-7647966cc5-zkvqf 

# Notification Service logs
kubectl logs -n microservices -f -c notification-v2  <pod-name> 
kubectl logs -n microservices -f -c notification-v2  notification-v1-7647966cc5-zkvqf  

# Envoy Logs
kubectl logs -n microservices -f -c envoy  <pod-name> 
kubectl logs -n microservices -f -c envoy  notification-v2-7647966cc5-zkvqf  
```


## Step-04: Test the Services
```
# Get Public IP of a Node
kubectl get nodes -o wide

# Get NodePort port
kubectl get svc -n microservices
```
- Access in browser
```
# User Management Service Health-Status
http://<Worker-Node-Public-IP>:NodePort/usermgmt/health-status

# Notification Service Health-Status calling via User Management Service
http://<Worker-Node-Public-IP>:NodePort/usermgmt/notification-health-status
```
- **Observation-1:** We should see V1 version of notification service sample message: `Notification Service is UP and Running - V1` & also V2 version ``Notification Service is UP and Running - V2`  switching alternatively when we refresh browser
- **Observation-2:** We will observe 50% traffic to V1 and 50% traffic to V2

## Step-05: Verify AppMesh Grafana Dashboard
- Enable proxy to access Grafana Dashboard from local machine
```
kubectl -n appmesh-system port-forward svc/appmesh-grafana 3000:3000
```
- Access in local browser
```
http://localhost:3000
```
- Generate some traffic via Postman Runner to monitor the AppMesh live grafana dashboad to ensure chart getting updated
