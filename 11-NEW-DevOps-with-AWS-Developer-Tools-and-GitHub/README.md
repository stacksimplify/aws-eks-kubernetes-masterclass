# DevOps with AWS Developer Tools on AWS EKS

## Step-01: Introduction to DevOps
- Understand DevOps concepts
  - CI - Continuous Integration
  - CD - Continuous Deployment or Delivery
- Understand more about AWS Tools that help us to implement DevOps.
  - GitHub
  - AWS CodeBuild
  - AWS CodePipeline
- GitHub Repsitory used for Demo: [aws-eks-devops](https://github.com/stacksimplify/aws-eks-devops)  

### We are going to implement the following AWS EKS DevOps Pipeline
![AWS EKS DevOps Pipeline](../images/aws-eks-devops-pipeline.png)


## Step-02: What are we going to learn?
- We are going to create a AWS Elastic Container Registry (ECR) for our Docker Images
- We are going to create GitHub Repository and check-in the below to Github Repo
  - **Application code** 
    - app1/index.html
  - **Docker File** 
    - Dockerfile
  - **Kubernetes Manifests**
    - kube-manifests/01-DEVOPS-Nginx-Deployment.yml
    - kube-manifests/02-DEVOPS-Nginx-NodePortService.yml
    - kube-manifests/03-DEVOPS-Nginx-ALB-IngressService.yml
  - **Build Spec files** 
    - buildspec-build.yml
    - buildspec-deploy.yml
- We are going to have two `buildspec yaml` files for build and deploy stages:
  - **Phase-1:** Build Container Image and Push to ECR - `buildspec-build.yml` 
  - **Phase-2:** Authenticate to EKS using STS Assume Role (Secure EKS interaction) and deploy kube-manifests to EKS - `buildspec-deploy.yml`
 

## Step-03: Pre-requisite check
### Step-03-01: Verify AWS Load Balancer Controller and External DNS
- We are going to deploy a application which will also have a `AWS Load Balancer Controller` and also will register its DNS name in Route53 using `External DNS`
- Which means we should have both related pods running in our cluster. 
```sh
# Verify aws-load-balancer-controller pod running in namespace kube-system
kubectl get pods -n kube-system

# Verify external-dns pod running in default namespace
kubectl get pods
```
### Step-03-02: Verify Kubernetes Manifests working as expected before implementing DevOps Pipelines
```sh
# Verify if all templates are working
## Step-01: Update 01-DEVOPS-Nginx-Deployment.yml - "image" 
image: ghcr.io/stacksimplify/kube-nginxapp1:1.0.0 # FOR TESTING

## Step-02: Verify and Update Ingress manifest (03-DEVOPS-Nginx-ALB-IngressService.yml) with DNS Names and SSL Cert
alb.ingress.kubernetes.io/certificate-arn: arn:aws:acm:us-east-1:180789647333:certificate/126847a6-a5ee-41d0-8deb-2d8a85217c73
external-dns.alpha.kubernetes.io/hostname: eksdevops1.stacksimplify.com, eksdevops2.stacksimplify.com

## Step-03: DEPLOY AND VERIFY
cd 11-NEW-DevOps-with-AWS-Developer-Tools-and-GitHub/github-files
kubectl apply -f kube-manifets/

## Step-04: Verify Pods, Deployment, svc, ingress
kubectl get pods
kubectl get deploy
kubectl get svc
kubectl get ingress

## Step-05: Verify External DNS Logs and Route53 Records
kubectl logs -f $(kubectl get po | egrep -o 'external-dns[A-Za-z0-9-]+')
Go to Route53 -> Hosted Zones -> stacksimplify.com -> Verify DNS records "eksdevops1.stacksimplify.com, eksdevops2.stacksimplify.com"

## Step-06: Access Application
http://eksdevops1.stacksimplify.com/app1/index.html

## Step-07: Clean-up
kubectl delete -f kube-manifets/

## Step-08: Update 01-DEVOPS-Nginx-Deployment.yml - "image" 
image: CONTAINER_IMAGE # FOR DEVOPS Pipeline
```

## Step-04: Create ECR Repository for our Application Docker Images
- Go to Services -> Elastic Container Registry -> Create Repository
- Name: eks-devops
- Tag Immutability: Enable
- Scan On Push: Enable
- Click on **Create Repository**
- Make a note of Repository name
```t
# Sample ECR Repository URI
180789647333.dkr.ecr.us-east-1.amazonaws.com/eks-devops-app1
```

## Step-05: Create GitHub Repository
- Create GitHub Repository with name as **aws-eks-devops**
- Create git credentials from IAM Service and make a note of those credentials.
- Clone the git repository from Code Commit to local repository, during the process provide your git credentials generated to login to git repo
```
git clone git@github.com:stacksimplify/aws-eks-devops.git
```
- Copy all files from course section **11-NEW-DevOps-with-AWS-Developer-Tools-and-GitHub/Application-Manifests** to local repository
  - buildspec-build.yml
  - buildspec-deploy.yml
  - Dockerfile
  - app1
    - index.html 
  - kube-manifests
    - 01-DEVOPS-Nginx-Deployment.yml
    - 02-DEVOPS-Nginx-NodePortService.yml
    - 03-DEVOPS-Nginx-ALB-IngressService.yml
- Commit code and Push to GitHub Repo
```t
# Change to Git Repo Directory
cd aws-eks-devops

# Git Commands
git status
git add .
git commit -am "Base Commit"
git push
git status
```
- Verify the same on GitHub Repository [aws-eks-devops](https://github.com/stacksimplify/aws-eks-devops)


## Step-06: Build Stage: Implement Build Stage
### Step-06-01: Build Stage: Review buildspec-build.yaml
```yaml
# buildspec-build.yml

version: 0.2

# Environment variables and values used across phases
env:
  variables:
    # ECR URI where Docker image will be pushed
    IMAGE_URI: "180789647333.dkr.ecr.us-east-1.amazonaws.com/eks-devops"
  exported-variables:
    # Variables that will be shared with downstream phases or pipelines
    - IMAGE_URI
    - IMAGE_TAG

phases:
  install:
    commands:
      # Install phase (empty here since the CodeBuild image has necessary tools)
      - echo "Install Phase - Nothing to do using latest Amazon Linux Docker Image"

  pre_build:
    commands:
      # Generate a short Docker image tag using GitHub commit SHA (7 characters)
      - IMAGE_TAG="$(echo $CODEBUILD_RESOLVED_SOURCE_VERSION | cut -c1-7)"
      - export IMAGE_TAG
      # Authenticate Docker with ECR using AWS CLI
      - echo "Logging into Amazon ECR at $IMAGE_URI..."
      - aws ecr get-login-password | docker login --username AWS --password-stdin $IMAGE_URI

  build:
    commands:
      # Build Docker image using Dockerfile in root directory
      - echo "Building Docker image..."
      - docker build -t $IMAGE_URI:$IMAGE_TAG .

  post_build:
    commands:
      # Push the built Docker image to ECR repository
      - echo "Pushing Docker image to ECR..."
      - docker push $IMAGE_URI:$IMAGE_TAG
      # Export image metadata to be used in the deploy stage
      - echo "Exporting variables for downstream stages..."
      - echo "IMAGE_URI=$IMAGE_URI" >> $CODEBUILD_SRC_DIR/exported-vars.env
      - echo "IMAGE_TAG=$IMAGE_TAG" >> $CODEBUILD_SRC_DIR/exported-vars.env

# Files that will be included as artifacts for the next stage
artifacts:
  files:
    - exported-vars.env
    - buildspec-deploy.yml
    - '**/kube-manifests/**/*'

```

### Step-06-02: Build Stage: Create GitHub Connection in AWS Developer Tools
- Go to Settings -> Connections -> Create Connection
- **Select a Provider:** GitHub
- **Connection name:** eks-devops-github-connection
- Click on **Install a new app**
- WILL BE REDIRECTED TO GITHUB WEBSITE
- Provide **GitHub Authentication Code**
- In **AWS Connectior for GitHub**
  - **Repository Access:** Only Select Repositories
  - Select **aws-eks-devops**
  - Click on **Save**
- WILL BE REDIRECTED BACK TO AWS DEVELOPERS TOOLS (AWS Console)
- Click on **Connect**

### Step-06-03: Build Stage: Create CodePipeline 
#### CodePipeline Introduction
- Get a high level overview about CodePipeline Service
#### Create CodePipeline
- Create CodePipeline
- Go to Services -> CodePipeline -> Create Pipeline
#### Choose creation option
- **Category:** Build custom pipeline
- Click NEXT
#### Choose Pipeline Settings
- Pipeline Name: eks-devops
- Execution Mode: Queued
- Service Role: New Service Role (leave to defaults)
- Role Name: eks-devops-codepipeline-service-role
- Rest all leave to defaults and click Next
#### Add Source Stage
- Source Provider: GitHub (via GitHub App)
- Connection: eks-devops-github-connection
- Repository Name: aws-eks-devops
- Default Branch: main
- REST ALL LEAVE TO DEFAULTS and Click NEXT
#### Add Build Stage
- Build Provider:  Other Build Provider
- Build Providr Name: AWS CodeBuild
- Project Name:  Click on **Create Project**
##### Create Build Project
- **Project Configuration**
  - Project Name: build-eks-devops
  - Project Type: Default Project
- **Environment**
  - Provisioning Model: OnDemamd
  - Environment Image: Managed Image
  - Compute: EC2
  - Running Mode: Container
  - Operating System: Amazon Linux
  - Runtime(s): Standard
  - Image: aws/codebuild/amazonlinux-x86_64-standard:5.0
  - Image version: Always use the latest image for this runtime
  - Service Role: New Service Role
  - Role Name: buildphase-codebuild-eks-devops-service-role
  - REST ALL LEAVE TO DEFAULTS
- **Buildspec**
  - Build specifications: Use a buildspec file
  - Buildspec name: **buildspec-build.yml**
- **Logs**
  - Group Name: buildphase-cb-eks-deveops-group
  - Stream Name:buildphase-cb-eks-deveops-stream
- Click on **Continue to CodePipeline**
- We should see a message `Successfully created build-eks-devops in CodeBuild.`
- Click **Next**
##### Add Test Stage
- Click on **Skip Test Stage**
##### Add Deploy Stage
- Click on **Skip Deploy Stage**
##### Review
- Review and click on **Create Pipeline**

### Step-06-04: Build Stage: Updae CodeBuild Role to have access to ECR full access and CloudWatch Full Access   
- First pipeline run will fail as CodeBuild not able to upload or push newly created Docker Image to ECR Repostory
- Update the CodeBuild Role to have access to ECR to upload images built by codeBuild. 
  - **Role Name:** buildphase-codebuild-eks-devops-service-role
  - **Policy Name:** AmazonEC2ContainerRegistryFullAccess
  - **Policy Name:** CloudWatchLogsFullAccess 
- Make changes to index.html (Update as V2),  locally and push change to CodeCommit
```sh
# Git Commands
git status
git commit -am "V2 Deployment"
git push
```
- Verify CodeBuild Logs
- New image should be uploaded to ECR, verify the ECR with new docker image tag.
- BUILD PHASE SHOULD BE SUCCESSFUL

## Step-07: DEPLOY STAGE: IMPLEMENT DEPLOY PHASE in Code Pipeline
### Step-07-01: DEPLOY STAGE: Review buildspec-deploy.yml
```yaml
# buildspec-deploy.yml

version: 0.2

# Environment variables required for EKS authentication
env:
  variables:
    # Name of the EKS cluster
    EKS_CLUSTER_NAME: "eksdemo1"
    # IAM Role ARN used to assume access to EKS for kubectl
    EKS_KUBECTL_ROLE_ARN: "arn:aws:iam::180789647333:role/EksCodeBuildKubectlRole"

phases:
  install:
    commands:
      # Install dependencies/tools (if any)
      - echo "Install Phase - Installing tools and dependencies"

  pre_build:
    commands:
      # Print info about environment setup
      - echo "Setting up IMAGE_URI and IMAGE_TAG from previous stage..."
      # List files to verify presence of artifacts
      - echo "Listing all files in workspace for debugging:"
      - ls -R .
      # Source exported variables (IMAGE_URI and IMAGE_TAG)
      - echo "Sourcing env variables from file"
      - source ./exported-vars.env
      - echo "IMAGE_URI=$IMAGE_URI"
      - echo "IMAGE_TAG=$IMAGE_TAG"
      # Replace placeholder in Kubernetes YAML with actual image URI and tag
      - echo "Updating container image in the Kubernetes Deployment YAML file..."
      - sed -i 's@CONTAINER_IMAGE@'"$IMAGE_URI:$IMAGE_TAG"'@' kube-manifests/01-DEVOPS-Nginx-Deployment.yml
      - echo "Updated deployment manifest content:"
      - cat kube-manifests/01-DEVOPS-Nginx-Deployment.yml

  build:
    commands:
      # Assume IAM role to gain temporary credentials for kubectl access
      - echo "Assuming IAM Role to access EKS cluster..."
      - CREDENTIALS=$(aws sts assume-role --role-arn $EKS_KUBECTL_ROLE_ARN --role-session-name codebuild-kubectl --duration-seconds 900)
      - export AWS_ACCESS_KEY_ID=$(echo $CREDENTIALS | jq -r '.Credentials.AccessKeyId')
      - export AWS_SECRET_ACCESS_KEY=$(echo $CREDENTIALS | jq -r '.Credentials.SecretAccessKey')
      - export AWS_SESSION_TOKEN=$(echo $CREDENTIALS | jq -r '.Credentials.SessionToken')
      # Setup kubeconfig to interact with the EKS cluster
      - echo "Updating kubeconfig with EKS cluster credentials..."
      - aws eks update-kubeconfig --name $EKS_CLUSTER_NAME
      # Deploy application manifests to EKS
      - echo "Applying Kubernetes manifests..."
      - kubectl apply -f kube-manifests/
      # Wait for deployment rollout to complete
      - echo "Waiting for deployment rollout to complete..."
      - kubectl rollout status deployment/eks-devops-deployment --timeout=180s

  post_build:
    commands:
      # Verification steps to ensure everything is deployed correctly
      - echo "Verifying Kubernetes resources created:"
      - echo "Pods Status:"
      - kubectl get pods -o wide
      - echo "Services Status:"
      - kubectl get svc -o wide
      - echo "Ingress Status:"
      - kubectl get ingress -o wide
```
### Step-07-02: DEPLOY STAGE: DEPLOY PHASE: EDIT CodePipeline 
#### EDIT CodePipeline
- EDIT CodePipeline
- Go to Services -> CodePipeline ->  eks-devops -> EDIT
#### ADD Stage
- **Stage Name:** Deploy
- Click on **Add Stage** 
- Click on **Add Action group**
#### Edit Action
- Action Name: DeployToEKS
- Action Provider: AWS CodeBuild
- Region: United Stages (N.Virginia)
- Input Artifacts: Build Artifacts
- Project Name: Click on **CREATE PROJECT**
#### Create Build Project
- **Project Configuration**
  - Project Name: deploy-eks-devops
  - Project Type: Default Project
- **Environment**
  - Provisioning Model: OnDemamd
  - Environment Image: Managed Image
  - Compute: EC2
  - Running Mode: Container
  - Operating System: Amazon Linux
  - Runtime(s): Standard
  - Image: aws/codebuild/amazonlinux-x86_64-standard:5.0
  - Image version: Always use the latest image for this runtime
  - Service Role: New Service Role
  - Role Name: deployphase-codebuild-eks-devops-service-role
  - REST ALL LEAVE TO DEFAULTS
- **Buildspec**
  - Build specifications: Use a buildspec file
  - Buildspec name: **buildspec-deploy.yml**
- **Logs**
  - Group Name: deployphase-cb-eks-deveops-group
  - Stream Name: deployphase-cb-eks-deveops-stream
- Click on **Continue to CodePipeline**
- We should see a message `Successfully created build-eks-devops in CodeBuild.`
- Click **Next**
#### Build Type
- Build Type: Single Build
- Click on **Done**
- Click on **Save**

### Step-07-03: DEPLOY STAGE: Update CodePipeline Role with CodeBuild Full Access
- Go to Pipelines -> eks-devops -> Settings -> Click on **Service role ARN**
#### IAM CodePipeline Service Role Update
- Role Name: eks-devops-codepipeline-service-role
- Add Policy **AWSCodeBuildAdminAccess** to this role

### Step-07-04: DEPLOY STAGE: Create STS Assume IAM Role for CodeBuild to interact with AWS EKS
- In an AWS CodePipeline, we are going to use AWS CodeBuild to deploy Kubernetes manifests to EKS Cluster. 
- This requires an AWS IAM role capable of interacting with the EKS cluster.
- In this step, we are going to create an IAM role and add an inline policy `EKS:Describe` that we will use in the CodeBuild DEPLOY stage to interact with the EKS cluster via kubectl.
#### Option 1: **macOS / Linux / Windows Git Bash / WSL**
##### ⚠️ Note:
> ✅ This script is designed for **Bash-compatible environments**, such as **macOS Terminal**, **Linux shell**, **Windows Git Bash**, or **Windows Subsystem for Linux (WSL)**.
> ❌ It **will not work in Windows PowerShell or Command Prompt** due to syntax differences.
##### 💻 Script:
```bash
# Set variables
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
ROLE_NAME=EksCodeBuildKubectlRole

# Create IAM Role with trust policy
aws iam create-role \
  --role-name $ROLE_NAME \
  --assume-role-policy-document "{
    \"Version\": \"2012-10-17\",
    \"Statement\": [
      {
        \"Effect\": \"Allow\",
        \"Principal\": { \"AWS\": \"arn:aws:iam::${ACCOUNT_ID}:root\" },
        \"Action\": \"sts:AssumeRole\"
      }
    ]
  }"

# Attach inline policy to allow EKS describe actions
aws iam put-role-policy \
  --role-name $ROLE_NAME \
  --policy-name eks-describe \
  --policy-document "{
    \"Version\": \"2012-10-17\",
    \"Statement\": [
      {
        \"Effect\": \"Allow\",
        \"Action\": \"eks:Describe*\",
        \"Resource\": \"*\"
      }
    ]
  }"
```
#### Option 2: **Windows PowerShell**
##### ⚠️ Note:
> ✅ This script is designed for **Windows PowerShell**.
> ❌ Do not use it in Git Bash, WSL, macOS, or Linux — it will fail due to syntax and escaping differences.
##### Script:
```powershell
# Set variables
$ACCOUNT_ID = (aws sts get-caller-identity --query Account --output text)
$ROLE_NAME = "EksCodeBuildKubectlRole"

# Create IAM Role with trust policy
aws iam create-role `
  --role-name $ROLE_NAME `
  --assume-role-policy-document "{
    `"Version`": `"2012-10-17`",
    `"Statement`": [
      {
        `"Effect`": `"Allow`",
        `"Principal`": { `"AWS`": `"arn:aws:iam::${ACCOUNT_ID}:root`" },
        `"Action`": `"sts:AssumeRole`"
      }
    ]
  }"

# Attach inline policy to allow EKS Describe actions
aws iam put-role-policy `
  --role-name $ROLE_NAME `
  --policy-name "eks-describe" `
  --policy-document "{
    `"Version`": `"2012-10-17`",
    `"Statement`": [
      {
        `"Effect`": `"Allow`",
        `"Action`": `"eks:Describe*`",
        `"Resource`": `"*`"
      }
    ]
  }"
```


### Step-07-05: Update `aws-auth` ConfigMap with IAM Role for CodeBuild
- In this step, we will automatically update the EKS cluster's `aws-auth` ConfigMap to include the IAM role created in the previous step (`EksCodeBuildKubectlRole`). This grants the role access to the cluster, which is required for `kubectl` commands in the CodeBuild deployment stage.

#### ⚠️ Works on:
* **macOS / Linux / WSL / Git Bash**
* **Windows PowerShell**

#### 📁 Directory Structure
- Make sure you're in the project root (e.g., `11-NEW-DevOps-with-AWS-Developer-Tools-and-GitHub`) and there's a folder named `aws-auth/`:
```bash
cd 11-NEW-DevOps-with-AWS-Developer-Tools-and-GitHub
mkdir -p aws-auth
```

#### 🧪 Step-by-step Commands
##### 🖥️ macOS / Linux / Git Bash / WSL (Bash shell)
```bash
# Set variables
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
echo $ACCOUNT_ID
ROLE_ARN="arn:aws:iam::$ACCOUNT_ID:role/EksCodeBuildKubectlRole"
echo $ROLE_ARN

# Backup current aws-auth ConfigMap
kubectl get configmap aws-auth -n kube-system -o yaml > aws-auth/aws-auth-backup.yml

# Generate patched configmap YAML
kubectl get configmap aws-auth -n kube-system -o yaml | \
  awk -v role="    - rolearn: $ROLE_ARN\n      username: build\n      groups:\n        - system:masters" \
  '/mapRoles: \|/ {print; print role; next} 1' > aws-auth/aws-auth-patch.yml

# Apply updated configmap
kubectl apply -f aws-auth/aws-auth-patch.yml

# Verify updated config
kubectl get configmap aws-auth -n kube-system -o yaml
```

##### 🪟 Windows PowerShell

```powershell
# Set variables
$ACCOUNT_ID = (aws sts get-caller-identity --query Account --output text)
$ROLE_ARN = "arn:aws:iam::$ACCOUNT_ID:role/EksCodeBuildKubectlRole"
$BackupPath = "aws-auth\aws-auth-backup.yml"
$PatchPath = "aws-auth\aws-auth-patch.yml"

# Backup current config
kubectl get configmap aws-auth -n kube-system -o yaml > $BackupPath

# Inject new role into mapRoles
(Get-Content $BackupPath) | ForEach-Object {
    if ($_ -match "mapRoles: \|") {
        $_
        "    - rolearn: $ROLE_ARN"
        "      username: build"
        "      groups:"
        "        - system:masters"
    } else {
        $_
    }
} > $PatchPath

# Apply updated configmap
kubectl apply -f $PatchPath

# Verify update
kubectl get configmap aws-auth -n kube-system -o yaml
```

---

### ✅ Outcome
- The IAM role `EksCodeBuildKubectlRole` is now authorized to access the EKS cluster with `system:masters` permissions. This enables `kubectl` to be used in the CodeBuild stage of your pipeline.



### Step-07-06: DEPLOY STAGE: Update CodeBuild Role to have access to STS Assume Role we have created using STS Assume Role Policy
- DEPLOY PHASE Build should be failed due to CodeBuild dont have access to perform updates in EKS Cluster.
- It even cannot assume the STS Assume role whatever we created. 
- Create STS Assume Policy and Associate that to DEPLOY PHASE CodeBuild Role `deployphase-codebuild-eks-devops-service-role`

#### Create STS Assume Role Policy
- Go to Services IAM -> Policies -> Create Policy
- In **Visual Editor Tab**
- Service: STS
- Actions: Under Write - Select `AssumeRole`
- Resources: Specific
  - Add ARN
  - Specify ARN for Role: arn:aws:iam::180789647333:role/EksCodeBuildKubectlRole
  - Click Add
```
# For Role ARN, replace your account id here, refer step-07 environment variable EKS_KUBECTL_ROLE_ARN for more details
arn:aws:iam::<your-account-id>:role/EksCodeBuildKubectlRole
```
- Click on Review Policy  
- Name: eks-codebuild-sts-assume-role
- Description: CodeBuild to interact with EKS cluster to perform changes
- Click on **Create Policy**

#### Associate Policy to CodeBuild Role
- Role Name: deployphase-codebuild-eks-devops-service-role
- Policy to be associated:  `deployphase-codebuild-eks-devops-service-role`


## Step-08: Test-1: END TO END FLOW (Build and Deploy Stages)
- Commit the changes to local git repository and push to GitHub Repository
- Monitor the codePipeline Build and Deploy projects
- Test by accessing the static html page
```sh
# Update app1/index.html
      <h1>Welcome to Stack Simplify - App Version - V3 </h1>
# Git Commands
git status
git commit -am "V3"
git push
```
- Verify Build Stage - CodeBuild Logs
- Verify Deploy Stage - CodeBuild Logs
- Verify CodePipeline - eks-devops
- Test by accessing the static html page
```t
# Access Application
http://myapp1.stacksimplify.com/app1/index.html
```

## Step-09: Test-2: END TO END FLOW (Build and Deploy Stages)
- Commit the changes to local git repository and push to GitHub Repository
- Monitor the codePipeline Build and Deploy projects
- Test by accessing the static html page
```sh
# Update app1/index.html
      <h1>Welcome to Stack Simplify - App Version - V4 </h1>
# Git Commands
git status
git commit -am "V4"
git push
```
- Verify Build Stage - CodeBuild Logs
- Verify Deploy Stage - CodeBuild Logs
- Verify CodePipeline - eks-devops
- Test by accessing the static html page
```t
# Access Application
http://myapp1.stacksimplify.com/app1/index.html
```

## Step-10: APPROVAL STAGE: Add Manual Approval Stage
### Step-10-01: Create SNS Topic
- Go to Amazon SNS -> Create Topic
- Type: Standard
- Name: eks-devops-topic1
- Display Name: eks-devops-topic1
- REST ALL LEAVE TO DEFAULTS and 
- Click on **Create topic**
### Step-10-02: Create SNS Subscription
- Go to Amazon SNS -> eks-devops-topic1 
- Click on **Create Subscription**
- Topic ARN: Auto-populated (ARN of Topic: eks-devops-topic1 )
- Protocol: Email
- Endpoint: stacksimplify@gmail.com
- Click on **Create subscription**
- Go to email id and click on **Confirm Subscription**
### Step-10-03: APPROVAL STAGE: Add new state in CodePipeline
#### EDIT CodePipeline
- EDIT CodePipeline
- Go to Services -> CodePipeline ->  eks-devops -> EDIT
#### ADD Stage
- **Stage Name:** DeploymentApproval
- Click on **Add Stage** 
- Click on **Add Action group**
#### Edit Action
- Action Name: DeploymentApproval
- Action Provider: Manual Approval
- SNS Topic ARN: arn:aws:sns:us-east-1:180789647333:eks-devops-topic1 
- REST ALL LEAVE TO DEFAULTS
- Click on **DONE**
- Click on **SAVE** to save pipeline
### Step-10-04: Give SNS Full access to AWS CodePipeline Role
- Go to AWS CodePipeline -> eks-devops -> Settings -> Service role ARN
- In IAM for ROLE: **AWSCodePipelineServiceRole-us-east-1-eks-devops-pipeline-551**
- Attach Permissions: **AmazonSNSFullAccess**


## Step-11: Test-3: END TO END FLOW (Build, Approval and Deploy Stages)
- Commit the changes to local git repository and push to GitHub Repository
```sh
# Update app1/index.html
      <h1>Welcome to Stack Simplify - App Version - V5 </h1>
# Git Commands
git status
git commit -am "V5"
git push
```
- Monitor the codePipeline BUILD project logs
- Verify email and Approve the Deployment request after **BUILD STAGE** to move to next step which is **DEPLOY STAGE**
- Monitor the codePipeline DEPLOY project logs
- Verify CodePipeline - eks-devops
- Test by accessing the static html page
```t
# Access Application
http://myapp1.stacksimplify.com/app1/index.html
```

Here’s a clean and simple way to add that to your `readme.md` as **Step-12**:

---

## Step-12: Why does every alternate build fail in the Build Phase?
- This happens because the Docker base image (`nginx:latest`) is being pulled from Docker Hub, which has rate limits for anonymous users. The first build fails due to hitting this limit (`429 Too Many Requests`), but the second one might pass if the image gets cached.

### ✅ Fix: Use Amazon ECR Public image instead of Docker Hub
- Update your `Dockerfile` like this:

```Dockerfile
#FROM nginx
FROM public.ecr.aws/nginx/nginx:latest
COPY app1 /usr/share/nginx/html/app1
```
- This uses AWS's public registry, which has no rate limits in CodeBuild.

## Step-13: Clean-Up
- Delete All kubernetes Objects in EKS Cluster
```sh
# Delete all Kubernetes Resources created as part of this demo
kubectl delete -f kube-manifests/
```
- Delete Pipeline
- Delete CodeBuild Project
- Make GitHub Repository public for students to access it
- Delete Roles and Policies created
- Delete SNS Subscription
- Delete SNS Topic
- Delete AWS Elastic Container Registry (ECR)

## Additional References
- https://docs.aws.amazon.com/codebuild/latest/userguide/build-env-ref-available.html
- **STS Assume Role:** https://docs.aws.amazon.com/cli/latest/reference/sts/assume-role.html
- https://docs.aws.amazon.com/IAM/latest/UserGuide/troubleshoot_roles.html



