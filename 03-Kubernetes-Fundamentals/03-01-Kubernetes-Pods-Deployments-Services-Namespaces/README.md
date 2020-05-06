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

# Verify Current Namespace kubectl using 
kubectl config view --minify | grep namespace:

# Create Namespace
kubectl create namespace firstdemo

# Set the namespace to newly created
kubectl config set-context --current --namespace=<insert-namespace-name-here>
kubectl config set-context --current --namespace=firstdemo

# Verify the Current Namespace kubectl using 
kubectl config view --minify | grep namespace:
```

## Step-03: Create Kubernetes Deployment
- Create a Kubernetes Deployment
- Verify Deployment & Pod
- Describe Deployment and Understand
- Describe Pod and Understand
```
# Create Deployment
kubectl create deployment kubenginx --image=stacksimplify/kubenginx:1.0.0

# Verify & Describe Deployment
kubectl get deployments
kubectl describe deployment <deployment-name>
kubectl describe deployment kubenginx

# Verify & Describe Pod
kubectl get pods
kubectl get po
kubectl describe pod <pod-name>
```

## Step-04: Create Kubernetes Service 
- Create Kubernetes Service
- Verify the Service
- Describe the Service and Understand 
```
# Create Service
kubectl get deployments
kubectl expose deployment kubenginx --type="NodePort" --port 80 --name=kubenginx-svc

# Verify Service
kubectl get service
kubectl get svc

# Describe Service
kubectl describe service kubenginx-svc
```

## Step-05: Test by accessing the NGINX Application via Internet
- Update Security Group  to allow access from internet
    - Security Group Name: eks-remoteAccess-(some-id)
    - Example Security Group name: eks-remoteAccess-08b8f410-774d-9a68-ebe3-34586336c2df
    - Create a Rule
        - Type: All Traffic
        - Protocol: All
        - Port Range: All
        - Source: Anywhere (0.0.0.0/0)
        - Description: Allow access from internet to All Ports on Kubernetes Worker Node

- Access the NGINX Application
```
# Get the Node Port from Service
kubectl get svc

# Sample Output
[root@ip-10-0-12-106 ~]# kubectl get svc
NAME            TYPE       CLUSTER-IP     EXTERNAL-IP   PORT(S)        AGE
kubenginx-svc   NodePort   10.100.52.95   <none>        80:31507/TCP   3m39s
[root@ip-10-0-12-106 ~]#


# Application URL 
http://<EKS-Worker-NodeIP>:<Port-from-kubectl-get-svc-output>
http://54.91.88.200:31507
```


## Step-06: Verify the POD Logs 
- Verify POD logs
```
# Pod logs
kubectl get po
kubectl logs <pod-name>
```
- **Important Notes**
    - Refer below link and search for **Interacting with running Pods** for additional log options
    - Troubleshooting skills are very important. So please go through all logging options available and master them.
    - Reference: https://kubernetes.io/docs/reference/kubectl/cheatsheet/

## Step-07: Connect to Container in a POD
- **Connect to a Container in POD and execute commands**
```
# Connect to Nginx Container in a POD
kubectl exec -it <pod-name> -- /bin/bash

# Execute some commands in Nginx container
ls
cd /etc/nginx
ls
exit
```
- **Running individual commands in a Container**
```
kubectl exec -it <pod-name> env
```
## Step-08: Namespaces - Advanced
- **Delete all resources by deleting Namespace**
```
kubectl delete namespace firstdemo
```

- **Recreate them back**
```
kubectl create namespace firstdemo
kubectl create deployment kubenginx --image=stacksimplify/kubenginx:1.0.0
kubectl expose deployment kubenginx --type="NodePort" --port 80 --name=kubenginx-svc
kubectl get svc

# Test Application URL 
http://<EKS-Worker-NodeIP>:<Port-from-kubectl-get-svc-output>
http://54.91.88.200:31507
```

- **Switch Contexts**
    - Switch to default context
```
# Set the namespace to default created
kubectl config set-context --current --namespace=<insert-namespace-name-here>
kubectl config set-context --current --namespace=default

# Verify the Current Namespace kubectl using 
kubectl config view --minify | grep namespace:
```

- **Namespace & Non-Namespace Resources**
    - Understand about Namespace and Non-Namespace resources in Kubernetes
```
# In a namespace
kubectl api-resources --namespaced=true

# Not in a namespace
kubectl api-resources --namespaced=false
```

