# AWS Fargate & EKS (Elastic Kubernetes Service) - Masterclass

## Course Modules

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


## CloudFormation References
- https://github.com/aws-quickstart/quickstart-amazon-eks
- https://s3.amazonaws.com/aws-quickstart/quickstart-amazon-eks/doc/amazon-eks-architecture.pdf