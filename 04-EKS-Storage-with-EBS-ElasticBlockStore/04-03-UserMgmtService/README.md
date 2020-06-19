# Deploy UserManagement Service with MySQL Database


## Step-01: Introduction
- We are going to deploy a **User Management Microservice** which will connect to MySQL Database schema **usermgmt** during startup.
- Then we can test the following APIs
  - Create Users
  - List Users
  - Delete User
  - Health Status 

| Kubernetes Object  | YAML File |
| ------------- | ------------- |
| Deployment, Environment Variables  | 06-UserManagementMicroservice-Deployment.yml  |
| NodePort Service  | 07-UserManagement-Service.yml  |

## Step-02: Create following Kubernetes manifests
- User Management Microservice Deployment with MySQL as Database
  - Deployment
  - Environment Variables
| First Header  | Second Header |
| ------------- | ------------- |
| DB_HOSTNAME  | mysql |
| DB_PORT  | 3306  |
| DB_NAME  | usermgmt  |
| DB_USERNAME  | root  |
| DB_PASSWORD | dbpassword11  |  

- User Management Service
  - NodePort Service

## Step-03: Create UserManagement Service Deployment & Service 
```
# Create Deployment & NodePort Service
kubectl apply -f kube-manifests/V

# List Pods
kubectl get pods
```
- **Access Application**
```
# List Services
kubectl get svc

# Get Public IP
kubectl get nodes -o wide

# Access Health Status API for User Management Service
http://<EKS-WorkerNode-Public-IP>:31231/usermgmt/health-status
```

## Step-04: Test User Management Service using Postman
- Download Postman client 
  - https://www.postman.com/downloads/ 
- Import the postman project `EKS-Masterclass.postman_collection.json`
- **Create User Service**
- **List User Service**

## Step-05: Verify Users in MySQL Database
```
# Connect to MYSQL Database
kubectl run -it --rm --image=mysql:5.6 --restart=Never mysql-client -- mysql -h mysql -ppassword

# Verify usermgmt schema got created which we provided in ConfigMap
mysql> show schemas;
mysql> use usermgmt;
mysql> show tables;
mysql> select * from users;
```


