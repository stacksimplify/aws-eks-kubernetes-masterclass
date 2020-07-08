# AWS ECR - Elastic Container Registry Integration

## Step-01: Introduction to ECR
-  For introduction slides refer the [presentation slides](/presentation/AWS-Fargate-and-EKS-Masterclass.pptx). 

## Step-02: ECR Terminology
 - **Registry:** An  ECR registry is provided to each AWS account; we can create image repositories in our registry and store images in them. 
- **Repository:** An ECR image repository contains our Docker images. 
- **Repository policy:** We can control access to our repositories and the images within them with repository policies. 
- **Authorization token:** Our Docker client must authenticate to Amazon ECR registries as an AWS user before it can push and pull images. The AWS CLI get-login command provides us with authentication credentials to pass to Docker. 
- **Image:** We can push and pull container images to our repositories. We can use these images locally on your development system, or we can use them in Amazon ECS task definitions. 

## Step-03: Pre-requisites
- Install required CLI software on your local desktop
   - **Install AWS CLI V2 version**
      - We have taken care of this step as part of [01-EKS-Create-Clusters](/01-EKS-Create-Clusters/README.md)
      - Documentation Reference: https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html
   - **Install Docker CLI** 
      - We have taken of Docker local desktop installation as part of [Docker Fundamentals](https://github.com/stacksimplify/docker-fundamentals/tree/master/02-Docker-Installation) section 
      - Docker Desktop for MAC: https://docs.docker.com/docker-for-mac/install/
      - Docker Desktop for Windows: https://docs.docker.com/docker-for-windows/install/
      - Docker on Linux: https://docs.docker.com/install/linux/docker-ce/centos/

   - **On AWS Console**
      - We have taken care of this step as part of [01-EKS-Create-Clusters](/01-EKS-Create-Cluster-using-eksctl/01-01-Install-CLIs/README.md)
      - Create Authorization Token for admin user if not created
      - **Configure AWS CLI with Authorization Token**
```
aws configure
AWS Access Key ID: ****
AWS Secret Access Key: ****
Default Region Name: us-east-1
```   

## Step-04: Create ECR Repository
- Create simple ECR repository via AWS Console 
   - Repository Name: aws-ecr-kubenginx
   - Tag Immutability: Enable
   - Scan on Push: Enable
- Explore ECR console. 
- **Create ECR Repository using AWS CLI**
```
aws ecr create-repository --repository-name aws-ecr-kubenginx --region us-east-1
aws ecr create-repository --repository-name <your-repo-name> --region <your-region>
```

## Step-05: Create Docker Image locally
- Navigate to folder **10-ECR-Elastic-Container-Registry\01-aws-ecs-kubenginx** from course github content download. 
- Create docker image locally
- Run it locally and test
```
# Build Docker Image
docker build -t <ECR-REPOSITORY-URI>:<TAG> . 
docker build -t 180789647333.dkr.ecr.us-east-1.amazonaws.com/aws-ecr-kubenginx:1.0.0 . 

# Run Docker Image locally & Test
docker run --name <name-of-container> -p 80:80 --rm -d <ECR-REPOSITORY-URI>:<TAG>
docker run --name aws-ecr-kubenginx -p 80:80 --rm -d 180789647333.dkr.ecr.us-east-1.amazonaws.com/aws-ecr-kubenginx:1.0.0

# Access Application locally
http://localhost

# Stop Docker Container
docker ps
docker stop aws-ecr-kubenginx
docker ps -a -q
```

## Step-06: Push Docker Image to AWS ECR
- Firstly, login to ECR Repository
- Push the docker image to ECR
- **AWS CLI Version 2.x**
```
# Get Login Password
aws ecr get-login-password --region <your-region> | docker login --username AWS --password-stdin <ECR-REPOSITORY-URI>
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 180789647333.dkr.ecr.us-east-1.amazonaws.com/aws-ecr-kubenginx

# Push the Docker Image
docker push <ECR-REPOSITORY-URI>:<TAG>
docker push 180789647333.dkr.ecr.us-east-1.amazonaws.com/aws-ecr-kubenginx:1.0.0
```
- Verify the newly pushed docker image on AWS ECR. 
- Verify the vulnerability scan results. 

## Step-07: Using ECR Image with Amazon EKS
- Understand the Deployment and Service kubernetes manifests present in folder **10-ECR-Elastic-Container-Registry\02-kube-manifests**
- **Important Note:** We have two objects deployment and service present in single yaml file separated by `---` 
### Deploy the kubernetes manifests
```
cd 10-ECR-Elastic-Container-Registry\02-kube-manifests
kubectl apply -f ecr-kube-deployment-and-service.yml
kubectl get deploy
kubectl get svc
kubectl get po
```
### Access Application
```
# Get external ip of EKS Cluster Kubernetes worker nodes
kubectl get nodes -o wide

# Access Application
http://<External-IP-of-EKS-Cluster-Nodes>:31231
```

## Step-08: Clean Up 
```
cd 10-ECR-Elastic-Container-Registry\02-kube-manifests
kubectl delete -f ecr-kube-deployment-and-service.yml
kubectl get deploy
```