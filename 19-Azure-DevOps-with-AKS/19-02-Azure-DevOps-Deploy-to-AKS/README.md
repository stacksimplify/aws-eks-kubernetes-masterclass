---
title: Azure DevOps Build, Push to ACR and Deploy to AKS
description: Create Azure Pipeline to Build and Push Docker Image to Azure Container Registry and Deploy to AKS Kubernetes Cluster  
---
# Azure DevOps - Build, Push to ACR and Deploy to AKS

## Step-00: Pre-requisites
- We should have Azure AKS Cluster Up and Running.
```
# Configure Command Line Credentials
az aks get-credentials --name aksdemo2 --resource-group aks-rg2

# Verify Nodes
kubectl get nodes 
kubectl get nodes -o wide
```

## Step-01: Introduction
- Add a Deployment Pipeline in Azure Pipelines to Deploy newly built docker image from ACR to Azure AKS

[![Image](https://www.stacksimplify.com/course-images/azure-devops-pipelines-deploy-to-aks.png "Azure AKS Kubernetes - Masterclass")](https://www.stacksimplify.com/course-images/azure-devops-pipelines-deploy-to-aks.png)

## Step-02: Create Pipeline for Deploy to AKS
- Go to Pipleines -> Create new Pipleine
- Where is your code?: Github
- Select a Repository: "select your repo" (stacksimplify/azure-devops-github-acr-aks-app1)
- Configure your pipeline: Deploy to Azure Kubernetes Service
- Select Subscription: stacksimplify-paid-subscription (select your subscription)
- Provide username and password (Azure cloud admin user)
- Deploy to Azure Kubernetes Service
  - Cluster: aksdemo3
  - Namespace: existing (default)
  - Container Registry: aksdevopsacr
  - Image Name: app1nginxaks
  - Service Port: 80
- Click on **Validate and Configure**
- Review your pipeline YAML
  -  Change Pipeline Name: 02-docker-build-push-to-acs-deploy-to-aks-pipeline.yml
- Click on **Save and Run**
- Commit Message: Docker, Build, Push and Deploy to AKS
- Commit directly to master branch: check
- Click on  **Save and Run**

 ## Step-03: Verify Build and Deploy logs
 - Build stage should pass. Verify logs
 - Deploy stage should pass. Verify logs


## Step-04: Verify Build and Deploy pipeline logs
- Go to Pipeline -> Verify logs
```
# Verify Pods
kubectl get pods

# Get Public IP
kubectl get svc

# Access Application
http://<Public-IP-from-Get-Service-Output>
```

 ## Step-05: Rename Pipeline Name
- Go to pipeline -> Rename / Move
- Name: 02-Docker-BuildPushToACR-DeployToAKSCluster
- Folder: App1-Pipelines
- Refresh till changes reflect
- Verify -> Pipelines -> Click on **All** tab

## Step-06: Make Changes to index.html and Verify
```
 # Pull
 git pull

# Make changes to index.html
Change version to V3

# Commit and Push
git commit -am "V3 commit index.html"
git push

# Verify Build and Deploy logs
- Build stage logs
- Deploy stage logs
- Verify ACR Repository

# List Pods (Verify Age of Pod)
kubectl get pods 

# Get Public IP
kubectl get svc

# Access Application
http://<Public-IP-from-Get-Service-Output>

``` 

## Step-07: Disable Pipeline
- Go to Pipeline -> 02-Docker-BuildPushToACR-DeployToAKSCluster -> Settings -> Disable


## Step-08: Review Pipeline code
- Click on Pipeline -> Edit Pipeline
- Review pipeline code
- Review Service Connections
 ```yaml
 # Deploy to Azure Kubernetes Service
# Build and push image to Azure Container Registry; Deploy to Azure Kubernetes Service
# https://docs.microsoft.com/azure/devops/pipelines/languages/docker

trigger:
- master

resources:
- repo: self

variables:

  # Container registry service connection established during pipeline creation
  dockerRegistryServiceConnection: '8e06f498-fd9e-481c-8453-12d8c2da0245'
  imageRepository: 'app1nginxaks'
  containerRegistry: 'aksdevopsacr.azurecr.io'
  dockerfilePath: '**/Dockerfile'
  tag: '$(Build.BuildId)'
  imagePullSecret: 'aksdevopsacr1755e8d5-auth'

  # Agent VM image name
  vmImageName: 'ubuntu-latest'
  

stages:
- stage: Build
  displayName: Build stage
  jobs:  
  - job: Build
    displayName: Build
    pool:
      vmImage: $(vmImageName)
    steps:
    - task: Docker@2
      displayName: Build and push an image to container registry
      inputs:
        command: buildAndPush
        repository: $(imageRepository)
        dockerfile: $(dockerfilePath)
        containerRegistry: $(dockerRegistryServiceConnection)
        tags: |
          $(tag)
          
    - upload: manifests
      artifact: manifests

- stage: Deploy
  displayName: Deploy stage
  dependsOn: Build

  jobs:
  - deployment: Deploy
    displayName: Deploy
    pool:
      vmImage: $(vmImageName)
    environment: 'stacksimplifyazuredevopsgithubacraksapp1internal-1561.default'
    strategy:
      runOnce:
        deploy:
          steps:
          - task: KubernetesManifest@0
            displayName: Create imagePullSecret
            inputs:
              action: createSecret
              secretName: $(imagePullSecret)
              dockerRegistryEndpoint: $(dockerRegistryServiceConnection)
              
          - task: KubernetesManifest@0
            displayName: Deploy to Kubernetes cluster
            inputs:
              action: deploy
              manifests: |
                $(Pipeline.Workspace)/manifests/deployment.yml
                $(Pipeline.Workspace)/manifests/service.yml
              imagePullSecrets: |
                $(imagePullSecret)
              containers: |
                $(containerRegistry)/$(imageRepository):$(tag)
 ``` 

 ## Step-09: Clean-Up Apps in AKS Cluster
 ```
 # Delete Deployment
 kubectl get deploy
 kubectl delete deploy app1nginxaks

 # Delete Service
 kubectl get svc
 kubectl delete svc app1nginxaks
 ```
