# Kubernetes Fundamentals

## Step-01: Introduction
- Create Docker Image
- Understand Kubernetes core fundamental items
    - Pods
    - Deployments
    - Services

## Step-02: Create a Docker Image Locally & Push to Docker Hub
- Navigate to folder **03-Kubernetes-Fundamentals\03-01-Kubernetes-Pods-Deployments-Services\kube-nginx** from course github content download.
- **Create docker image locally**
```
# Build Docker Image
cd <Course-Repo>\03-Kubernetes-Fundamentals\03-01-Kubernetes-Pods-Deployments-Services\kube-nginx
docker build -t stacksimplify/kubenginx:1.0.0 .
docker run --name kubenginx1 -p 80:80 -d stacksimplify/kubenginx:1.0.0

# Replace your docker hub account Id
docker build -t <your-docker-hub-id>/kube-nginx:1.0.0 .
docker run --name kubenginx1 -p 80:80 -d <your-docker-hub-id>/kubenginx:1.0.0
```
- **Test by accessing locally**
```
# Verify Docker Container is running
docker ps

# Verify by acecsing application in Terminal (Linux or Mac)
curl http://localhost  

# Verify by accessing application in Browser (local desktop)
http://localhost  
```
- **Stop Docker Container**
```
# Verify Docker Container is Running
docker ps

# Stop Container
docker stop kubenginx1

# Verify Stopped Containers
docker ps -a -q
```
- **Push the Docker Image to Docker Hub**
```
# Push to Docker Hub
docker push stacksimplify/kubenginx:1.0.0

# Replace your docker hub account Id
docker push <your-docker-hub-id>/kubenginx:1.0.0
```

## Step-03: Create Kubernetes Namespaces
- Create Namespace
- Switch the context to new namespace
- **Important Note:** Don't worry much about this for now, in upcoming steps we will discuss in detail.
```
# Get Current Namespaces
kubectl get namespace

# Create Namespace
kubectl create namespace firstdemo

# Set the namespace
kubectl config set-context --current --namespace=<insert-namespace-name-here>
kubectl config set-context --current --namespace=firstdemo

# Validate it
kubectl config view --minify | grep namespace:
```

## Step-03: Create Kubernetes Deployment
- Create a Kubernetes Deployment
- Verify Deployment & Pod
- Describe Deployment and Understand
- Describe Pod and Understand
```
# Create Deployment
kubectl create deployment kubenginx-dep --image=stacksimplify/kubenginx:1.0.0

# Verify Deployment & Pods
kubectl get deployments
kubectl get pods

# Describe Deployment & Pod
kubectl describe deployment <deployment-name>
kubectl describe pod <pod-name>
```

## Step-04: Create Kubernetes Service 
- Create Kubernetes Service
- Verify the Service
- Describe the Service and Understand 
```
# Create Service
kubectl expose deployment kube-nginx-dep --type="NodePort" --port 80 --name=kubenginx-svc

# Verify Service
kubectl get services
kubectl get svc

# Describe Service
kubectl describe service mynginx
```

## Step-05: Test by accessing the NGINX Application via Internet
- Update Security Group  to allow access from internet
    - Security Group Name: eks-remoteAccess-(some-id)
    - Example Security Group name: eks-remoteAccess-08b8f410-774d-9a68-ebe3-34586336c2df
    - Create a Rule
        - Type: HTTP
        - Protocol: TCP
        - Port Range: 80
        - Source: Anywhere (0.0.0.0/0)
        - Description: Allow access from internet to port 80 on Kubernetes Worker Node

- Access the NGINX Application
```
# Application URL 
http://<EKS-Worker-NodeIP:Port>
```


## Step-06: Verify the POD Logs 
- Verify POD logs
```
# Pod logs
kubectl logs <pod-name>
kubectl logs 
```

## Step-07: Connect to Container in a POD
```
kubectl exec -ti <pod-name> bash
```


## Step-08: Namespaces - Advanced


