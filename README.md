# AWS EKS - Elastic Kubernetes Service - Masterclass

## Course Modules

| S.No | AWS Service Name |
| ---- | ---------------- |
| 1.   | Create AWS EKS Cluster using eksctl CLI |
| 2.   | [Docker Fundamentals](https://github.com/stacksimplify/docker-fundamentals) |
| 3.   | [Kubernetes Fundamentals](https://github.com/stacksimplify/kubernetes-fundamentals) |
| 4.   | EKS Storage with AWS EBS CSI Driver |
| 5.   | Kubernetes Important Concepts for Application Deployments |
| 5.1  | Kubernetes - Secrets |
| 5.2  | Kubernetes - Init Containers |
| 5.3  | Kubernetes - Liveness & Readiness Probes |
| 5.4  | Kubernetes - Requests & Limits |
| 5.5  | Kubernetes - Namespaces, Limit Range and Resource Quota |
| 6.   | EKS Storage with AWS RDS MySQL Database |
| 7.   | Load Balancing using CLB & NLB |
| 7.1  | Load Balancing using CLB - AWS Classic Load Balancer |
| 7.2  | Load Balancing using NLB - AWS Network Load Balancer |
| 8.   | Load Balancing using ALB - AWS Application Load Balancer |
| 8.1  | ALB Ingress Controller - Install |
| 8.2  | ALB Ingress - Basics |
| 8.3  | ALB Ingress - Context path based routing |
| 8.4  | ALB Ingress - SSL |
| 8.5  | ALB Ingress - SSL Redirect HTTP to HTTPS |
| 8.6  | ALB Ingress - External DNS |
| 9.   | Deploy Kubernetes workloads on AWS Fargate Serverless |
| 9.1  | AWS Fargate Profiles - Basic |
| 9.2  | AWS Fargate Profiles - Advanced using YAML |
| 10.  | Build and Push Container to AWS ECR and use that in EKS |
| 11.  | DevOps with AWS Developer Tools CodeCommit, CodeBuild and CodePipeline |
| 12.  | Microservices Deployment on EKS - Service Discovery |
| 13.  | Microservices Distributed Tracing using AWS X-Ray |
| 14.  | Microservices Canary Deployments |
| 15.  | EKS HPA - Horizontal Pod Autosaler |
| 16.  | EKS VPA - Vertical Pod Autosaler |
| 17.  | EKS CA - Cluster Autosaler |
| 18.  | EKS Monitoring using CloudWatch Agent & Fluentd - Container Insights |


## AWS Services Covered

| S.No | AWS Service Name |
| ---- | ---------------- |
| 1.   | AWS EKS - Elastic Kubernetes Service  |
| 2.   | AWS EBS - Elastic Block Store  |
| 3.   | AWS RDS - Relational Database Service MySQL  |
| 4.   | AWS CLB - Classic Load Balancer  |
| 5.   | AWS NLB - Network Load Balancer  |
| 6.   | AWS ALB - Application Load Balancer  |
| 7.   | AWS Fargate - Serverless  |
| 8.   | AWS ECR - Elastic Container Registry  |
| 9.   | AWS Developer Tool - CodeCommit  |
| 10.  | AWS Developer Tool - CodeBuild  |
| 11.  | AWS Developer Tool - CodePipeline  |
| 12.  | AWS Developer Tool - CodePipeline  |
| 13.  | AWS X-Ray  |
| 14.  | AWS CloudWatch - Container Insights  |
| 15.  | AWS CloudWatch - Log Groups & Log Insights  |
| 16.  | AWS CloudWatch - Alarms  |
| 17.  | AWS Route53  |
| 18.  | AWS Certificate Manager  |
| 19.  | EKS CLI - eksctl  |


## Kubernetes Concepts Covered

| S.No | Kubernetes Concept Name |
| ---- | ------------------- |
| 1.   | Kubernetes Architecture  |
| 2.   | Pods  |
| 3.   | ReplicaSets  |
| 4.   | Deployments  |
| 5.   | Services - Node Port Service  |
| 6.   | Services - Cluster IP Service  |
| 7.   | Services - External Name Service  |
| 8.   | Services - Ingress Service  |
| 9.   | Services - Ingress SSL & SSL Redirect  |
| 10.  | Services - Ingress & External DNS  |
| 11.  | Imperative - with kubectl  |
| 12.  | Declarative - Declarative with YAML  |
| 13.  | Secrets |
| 14.  | Init Containers |
| 15.  | Liveness & Readiness Probes |
| 16.  | Requests & Limits |
| 17.  | Namespaces - Imperative |
| 18.  | Namespaces - Limit Range |
| 19.  | Namespaces - Resource Quota |
| 20.  | Storage Classes |
| 21.  | Persistent Volumes |
| 22.  | Persistent Volume Claims |
| 23.  | Services - Load Balancers |
| 24.  | Annotations |
| 25.  | Canary Deployments |
| 26.  | HPA - Horizontal Pod Autoscaler |
| 27.  | VPA - Vertical Pod Autoscaler |
| 28.  | CA - Cluster Autoscaler |
| 29.  | DaemonSets |
| 30.  | DaemonSets - Fluentd for logs |
| 31.  | Config Maps |

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


## Sample Applications
- User Management Microservice
- Notification Miroservice
- Nginx Applications

## What will students learn in your course?
- You will 
- You will slowly start by learning Docker Fundamentals and move on to ECS or Fargate. 
- You will learn Docker fundamentals by implementing usecases like download image from Docker Hub and run on local desktop and build an image locally, test and push to Docker Hub.
- You will master the Elastic Container Service core concepts like Task Definition, Task and Service.
- You will learn using ECR - Elastic Container Registry in combination with ECS. 
- You will learn Docker Image Build, Push to ECR, run it as Task on ECS or Fargate Clusters.
- You will learn usage of Application Load Balancers in combination with ECS Tasks (Containers) and also implement URI based routing on ALB.
- You will understand and implement Service Autoscaling concepts of ECS
- You will implement Continuous Integration and Continuous Delivery concepts using AWS Developer Tools like CodeBuild, CodeCommit and CodePipeline.
- You will learn to master microservices deployments on ECS in combination with AWS CloudMap (for Service Discovery) and with AWS App Mesh (Service Mesh).
- You will learn to deploy Microservices Canary Deployments using AWS App Mesh.
- You will write CloudFormation Templates for Fargate Deployments starting from Network stack (VPC) to Service Stack (ECS or Fargate). 
- You will learn to implement Distributed Tracing using X-Ray without making any application level code changes when AWS App Mesh (Envoy Proxy) is in place with ECS Deployments.

## Are there any course requirements or prerequisites?
- You must have an AWS account to follow with me for hands-on activities.
- You dont need to have any basic Docker knowledge also to start this course.  As part of Docker Fundamentals we have covered that too. 

## Who are your target students?
- AWS Architects or Sysadmins or Developers who are planning to master Elastic Container Service (ECS) for Docker deployments.
- Any beginner who is interested in learning Docker fundamentals and moving on to master Docker Container deployments on AWS Cloud. 
- Technologists who want to implement Continuous Integration and Continuos Delivery/Deployment process (CI/CD) in AWS with Docker Container Images.

## Each of my courses come with
- Amazing Hands-on Step By Step Learning Experiences
- Real Implementation Experience
- Friendly Support in the Q&A section
- 30 Day "No Questions Asked" Money Back Guarantee!

## My Other AWS Courses
- [Udemy Enroll](https://github.com/stacksimplify/udemy-enroll)

## Stack Simplify Udemy Profile
- [Udemy Profile](https://www.udemy.com/user/kalyan-reddy-9/)


