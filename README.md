# AWS Fargate & EKS (Elastic Kubernetes Service) - Masterclass

## Course Modules

## List of Docker Images  on Docker Hub

| Application Name  | Docker Image Name |
| ----------------- | ----------------- |
| Simple Nginx V1  | stacksimplify/kubenginx:1.0.0  |
| Spring Boot Hello World API  | stacksimplify/kube-helloworld:1.0.0  |
| Simple Nginx V2  | stacksimplify/kubenginx:2.0.0  |
| Simple Nginx V3  | stacksimplify/kubenginx:3.0.0  |
| Simple Nginx V4  | stacksimplify/kubenginx:4.0.0  |
| Backend Application  | stacksimplify/kube-helloworld:1.0.0  |
| Frontend Application  | stacksimplify/kube-frontend-nginx:1.0.0  |
| Kube Nginx App1  | stacksimplify/kube-nginxapp1:1.0.0  |
| Kube Nginx App2  | stacksimplify/kube-nginxapp2:1.0.0  |
| Kube Nginx App2  | stacksimplify/kube-nginxapp2:1.0.0  |
| User Management Microservice with MySQLDB  | stacksimplify/kube-usermanagement-microservice:1.0.0  |
| User Management Microservice with H2 DB  | stacksimplify/kube-usermanagement-microservice:2.0.0-H2DB  |
| User Management Microservice with MySQL DB and AWS X-Ray  | stacksimplify/kube-usermanagement-microservice:3.0.0-AWS-XRay-MySQLDB  |
| User Management Microservice with H2 DB and AWS X-Ray  | stacksimplify/kube-usermanagement-microservice:4.0.0-AWS-XRay-H2DB  |
| Notification Microservice V1  | stacksimplify/kube-notifications-microservice:1.0.0  |
| Notification Microservice V2  | stacksimplify/kube-notifications-microservice:2.0.0  |
| Notification Microservice V1 with AWS X-Ray  | stacksimplify/kube-notifications-microservice:3.0.0-AWS-XRay  |
| Notification Microservice V2 with AWS X-Ray  | stacksimplify/kube-notifications-microservice:4.0.0-AWS-XRay  |


## List of Docker Images you build in AWS ECR

| Application Name  | Docker Image Name |
| ----------------- | ----------------- |
| AWS Elastic Container Registry  | YOUR-AWS-ACCOUNT-ID.dkr.ecr.us-east-1.amazonaws.com/aws-ecr-kubenginx:DATETIME-REPOID  |
| DevOps Usecase  | YOUR-AWS-ACCOUNT-ID.dkr.ecr.us-east-1.amazonaws.com/eks-devops-nginx:DATETIME-REPOID  |


## AWS Services - Covered as part of this course
1. AWS Elastic Kubernetes Service - EKS
2. AWS EKS Fargate (Serverless)
3. AWS Elastic Container Registry - ECR
3. AWS Elastic Block Storage - EBS
4. AWS Elastic File Storage - EFS
5. AWS VPC - Virtual Private Cloud
6. AWS ELB - Elastic Load Balancer
    - CLB - Classic Load Balancer
    - NLB - Network Load Balancer
    - ALB - Application Load Balancer
7. AWS RDS - Relation Database Service
8. AWS EC2 Instances
9. AWS EC2 Autoscaling
10. AWS AppMesh
11. AWS X-Ray
12. AWS CloudFormation
13. AWS CloudWatch
14. AWS CloudTrial
15. AWS Parameter Store (for secrets - CICD)
16. AWS Lambda (For secrets - CICD)

## AWS EFS with EKS
17. AWS Datasync
18. AWS S3 Buckets
19. AWS EFS
    - https://docs.aws.amazon.com/datasync/latest/userguide/creating-task.html#in-coud-setup
20. Cerficate Manager (For ALB SSL)

| S.No  | AWS Services | S.No |Kubernetes Concepts |
| ------------- | ------------- | ------------- | -------------|
| 1.  | AWS EKS - Elastic Kubernetes Service  | 1.  |Pods  |
| 2.  | AWS EKS - Fargate (Serverless)  | 2. |ReplicaSets  |
| 3.  | AWS ECR - Elastic Container Registry  | 3. |Deployments  |
| 4.  | AWS EBS - Elastic Block Store  | 4. |Services - NodePort |  
| 5.  | AWS EFS - Elastic File Store  | 5. |Services - ClusterIp |  
| 6.  | AWS VPC - Virtual Private Cloud  | 6. |Imperative & Delcarative ways to create k8s objects |
| 7.  | AWS ELB - Elastic Load Balancer - ALB  | 7. |YAML Basics - for writing k8s manifests |    


# Kubernetes Topics - For Preparation

## Foundation
- YAML Basics

## Kube Core Topics
- PODs
- Deployments
- Services
- Volumes
- ConfigMaps
- Replication Controller or Replica Sets
- Declarative commands (kubectl)
- Live Template writing for PODS, Deployments & Services

## AWS EKS Topics 
- Create Cluster 
    - AWS Management Console
    - eksctl
- Worker Nodes 
    - Launch a Worker Node (Linux)
    - Managed Node Groups (MNG)
        - Updating (Patching) Managed Node Groups
        - Editing Managed Node Groups
        - Managed Node Group ERRORS
        - Deleting MNG
- Storage
    - EBS CSI Driver
    - EFS CSI Driver
- Autoscaling
    - Cluster Autoscaler
    - Horizontal Pod Autoscaler
    - Vertical Pod Autoscaler
- Load Balancing and Ingress
    - Load Balancing (CLB, NLB)    
    - ALB Ingress Controller
- Networking
    - Creating a VPC for EKS
    - Cluster VPC Considerations
    - EKS Security Group Considerations
    - Understand Pod Networking   
    - CoreDNS (Already exists in new clusters - just intro about it will suffice)
    - Calico (Multi-tenant environment - not needed) 
- Managing Cluster Authentication (Optional)               
    - Important Topic - Managing Users or IAM Roles for your cluster
- Guest Book Application
- Metrics Server
- Prometheus Metrics
- Using Helm
- Deploy Kubernetes Dashboard
- AppMesh Integration with Kubernetes
- Security (IAM role to Kubernetes Service Accounts)       
    - IAM
    - Pod Security Policy
- CloudTrial    
- AWS Fargate (LAST)
    - Important Note: Pods running on Fargate are only supported on private subnets (with NAT gateway access to AWS services, but not a direct route to an Internet Gateway), so your cluster's VPC must have private subnets available.
    - Stateful applications are not recommended for pods running on Fargate. 
    - Daemonsets are not supported on Fargate. 
    - GPUs are currently not available on Fargate.
- Troubleshooting

## Monitoring & Logging
- CloudWatch
- CloudTrail 
- AWS X-Ray

## Kube Tools
- Kubeapps 
- Helm Charts
    - https://github.com/aws/eks-charts
    - https://docs.aws.amazon.com/eks/latest/userguide/helm.html 
    - https://helm.sh/docs/intro/quickstart/
- Kubeadm
- Grafana, Prometheus
- Istio
- Kiali




# Kube Topics List

## Series -1
- Cluster Setup (AWS)
- Architecture
- PODS
- Deployments
- Services
- ReplicaSets
- YAML

## Series-2
- ConfigMaps
- Resources
- Containers
- P Volume Claims
- Networking
- Taints & 
- 

## Series-3
- Ingress
- Secrets
- Persistent Volumes
- Security
- 

## Series-4
- StatefulSets
- Storage
- Administration
- Federation
- Jobs



## Local Dev MySQL Server
```
docker run --name mysql-dev -p 3306:3306 -e MYSQL_ROOT_PASSWORD=redhat -d mysql:latest
docker stop mysql-dev
docker rm mysql-dev
docker exec -it mysql-dev bash

# Docker network
docker network ls

# Connect to MySQL
docker run -it --network some-network --rm mysql mysql -hsome-mysql -uexample-user -p
docker run -it --network host --rm mysql mysql -hmysql-dev -uroot -p
```    

