# Enable AppMesh for Microservices

## Step-01: Introduction


## Step-02: Create Namespace for Microservices & Enable Sidecar Injection
### Create Namespace
```
kubectl create ns microservices
```
### Enable sidecar injection for the microservices namespace
- Any pods that you want to use with App Mesh must have the App Mesh sidecar containers added to them. 
- The injector automatically adds the sidecar containers to any pod deployed into a namespace that you
```
kubectl label namespace microservices appmesh.k8s.aws/sidecarInjectorWebhook=enabled
```

## Step-03: Create AppMesh Objects for Notification Microservice V1
- V1 states notification microservice application version is V1

### Create AppMesh Virtual Node & Virtual Service
- 01-virtual-node-notification-microservice-v1.yml
- 02-virtual-service-notification-microservice.yml

### Deploy AppMesh Virtual Node & Virtual Service
```
# Deploy Virtual Node
kubectl apply -f 01-virtual-node-notification-microservice-v1.yml

# Deploy Virtual Service
kubectl apply -f 02-virtual-service-notification-microservice.yml

# Get Virtual Nodes
kubectl -n microservices get virtualnode
kubectl -n microservices get virtualservice
```

####  Verify virtual node & Virtual Service created in AppMesh using AWS Management Console
- Go to Services -> AWS App Mesh -> appmesh
  - Verify Virtual Nodes
  - Verify Virtual Services
  - Verify Virtual Router
- You should see all the objects created for Notification Microservice.


## Step-04: Enable proxy authorization
- Update `proxy-auth.json` with respective virtual node ARN. 
  - Notification V1
  - Notification V2
  - UserMgmt V1
- Even though we didnt create remaining two virtual nodes, as we are following thoroguh naming conventions, we can update them accordingly in `proxy-auth.json`  

### Create IAM Policy
```
aws iam create-policy --policy-name appmesh-microservices-policy --policy-document file://03-proxy-auth.json
```
### Create IAM Role
```
# Template
eksctl create iamserviceaccount \
    --cluster $CLUSTER_NAME \
    --namespace microservices \
    --name my-microservices-sa1 \
    --attach-policy-arn <REPLACE appmesh-microservices-policy ARN>  \
    --override-existing-serviceaccounts \
    --approve

# Replaced policy-arn from the IAM policy creation output
eksctl create iamserviceaccount \
    --cluster $CLUSTER_NAME \
    --namespace microservices \
    --name my-microservices-sa1 \
    --attach-policy-arn arn:aws:iam::411686525067:policy/appmesh-microservices-policy \
    --override-existing-serviceaccounts \
    --approve
```

## Step-05: Create & Deploy Notification Microservice V1 Deployment & Service
```
# Deploy Notificaiton Microservice
kubectl apply -f 04-notification-microservice-Deployment-Service-v1.yml

# List Pods
kubectl -n microservices get pods

# Describe Pod (Should have proxyinit and envoy containers)
kubectl -n microservices describe pod <pod-name>
kubectl -n microservices describe pod notification-v1-7647966cc5-zkvqf 

# Notification Service logs
kubectl logs -n microservices -f -c notification-v1  <pod-name> 
kubectl logs -n microservices -f -c notification-v1  notification-v1-7647966cc5-zkvqf  

# Envoy Logs
kubectl logs -n microservices -f -c envoy  <pod-name> 
kubectl logs -n microservices -f -c envoy  notification-v1-7647966cc5-zkvqf  
```
## Step-06: Create AppMesh Objects for User Management Microservice V1
- V1 states UserManagement microservice application version is V1

### Create AppMesh Virtual Node & Virtual Service
- 05-virtual-node-usermgmt-microservice-v1.yml
- 06-virtual-service-usermgmt-microservice.yml

### Deploy AppMesh Virtual Node & Virtual Service
```
# Deploy Virtual Node
kubectl apply -f 05-virtual-node-usermgmt-microservice-v1.yml

# Deploy Virtual Service
kubectl apply -f 06-virtual-service-usermgmt-microservice.yml

# Get Virtual Nodes
kubectl -n microservices get virtualnode
kubectl -n microservices get virtualservice
```

####  Verify virtual node & Virtual Service created in AppMesh using AWS Management Console
- Go to Services -> AWS App Mesh -> appmesh
  - Verify Virtual Nodes
  - Verify Virtual Services
  - Verify Virtual Router
- You should see all the objects created for User Management Microservice.


## Step-07: Create & Deploy UserMgmt Microservice V1 Deployment & Service
```
# Deploy User Management Microservice
kubectl apply -f 07-usermgmt-microservice-Deployment-Service-H2DB.yml

# List Pods
kubectl -n microservices get pods

# Describe Pod (Should have init and envoy containers)
kubectl -n microservices describe pod <pod-name>
kubectl -n microservices describe pod usermgmt-v1-7647966cc5-zkvqf 

# Notification Service logs
kubectl logs -n microservices -f -c usermgmt-v1  <pod-name> 
kubectl logs -n microservices -f -c usermgmt-v1  notification-v1-7647966cc5-zkvqf  

# Envoy Logs
kubectl logs -n microservices -f -c envoy  <pod-name> 
kubectl logs -n microservices -f -c envoy  usermgmt-v1-7647966cc5-zkvqf  
```

## Step-08: Test the Services
- Verify Services
```
kubectl get svc -n microservices
```
- Deploy a NodePort Service to access User Management Service via browser
```
# NodePort Service
kubectl expose service usermgmt-v1 --port=8095 --target-port=8095 --name=ums1 --type=NodePort -n microservices

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
- **Observation-1:** We should see V1 version of notification service sample message: `Notification Service is UP and Running - V1` 
- **Observation-2:** We have 100% of traffic going to only notification service V1.  

## Step-09: Verify AppMesh Grafana Dashboard
- Enable proxy to access Grafana Dashboard from local machine
```
kubectl -n appmesh-system port-forward svc/appmesh-grafana 3000:3000
```
- Access in local browser
```
http://localhost:3000
```
- Generate some traffic via Postman Runner to monitor the AppMesh live grafana dashboad to ensure chart getting updated

## References

### AppMesh Controller
- https://github.com/aws/eks-charts/tree/master/stable/appmesh-controller
- https://docs.aws.amazon.com/eks/latest/userguide/mesh-k8s-integration.html
- https://docs.aws.amazon.com/app-mesh/latest/userguide/proxy-authorization.html
- https://github.com/aws/eks-charts/blob/master/stable/appmesh-controller/README.md#configuration
- https://github.com/aws/eks-charts/tree/master/stable/appmesh-inject#configuration

## AppMesh Kubernetes Resources
- https://github.com/aws/aws-app-mesh-controller-for-k8s

### AppMesh EKS Examples
- https://idk.dev/learning-aws-app-mesh-aws-compute-blog/
- https://github.com/aws/aws-app-mesh-examples


### eksctl AppMesh Profile
- https://github.com/weaveworks/eks-appmesh-profile


### Issue about MYSQL and AppMesh (Mid Q3)
- https://github.com/aws/aws-app-mesh-roadmap/issues/62
- https://github.com/aws/aws-app-mesh-inject/pull/58


### Wht proxy Authorization?
- https://github.com/aws/aws-app-mesh-roadmap/issues/80

