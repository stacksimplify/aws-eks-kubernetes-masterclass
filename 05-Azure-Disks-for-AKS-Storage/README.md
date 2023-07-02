# Azure AKS Storage - Azure Disks

## Topics
1. Understand about Azure Disks
2. How we are going to use Azure Disks for Applications deployed on AKS for persistent Storage?
3. Understand best possible options available that we can configure in Storage Classess to persist our data, save cost and performance etc.

## Concepts
| Kubernetes Object  | YAML File |
| ------------- | ------------- |
| Storage Class  | 01-storage-class.yml |
| Persistent Volume Claim | 02-persistent-volume-claim.yml   |
| Config Map  | 03-UserManagement-ConfigMap.yml  |
| Deployment | 04-mysql-deployment.yml  |
| Environment Variables | 04-mysql-deployment.yml  |
| Volumes  | 04-mysql-deployment.yml  |
| VolumeMounts  | 04-mysql-deployment.yml  |
| ClusterIP Service  | 05-mysql-clusterip-service.yml  |
| Deployment  | 06-UserMgmtWebApp-Deployment.yml  |
| Environment Variables| 06-UserMgmtWebApp-Deployment.yml |
| Init Containers  | 06-UserMgmtWebApp-Deployment.yml  |
| Load Balancer Service  | 07-UserMgmtWebApp-Service.yml  |


