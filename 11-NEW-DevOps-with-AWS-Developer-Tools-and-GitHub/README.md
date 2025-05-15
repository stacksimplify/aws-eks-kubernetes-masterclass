# DevOps with AWS Developer Tools on AWS EKS

## Step-01: Introduction to DevOps
- Understand DevOps concepts
  - CI - Continuous Integration
  - CD - Continuous Deployment or Delivery
- Understand more about AWS Tools that help us to implement DevOps.
  - GitHub
  - AWS CodeBuild
  - AWS CodePipeline

## Step-02: What are we going to learn?
- We are going to create a ECR Repository for our Docker Images
- We are going to create GitHub Repository and check-in our Docker and Kubernetes Manifests
- Separate `buildspec yaml` files for build and deploy:
  - `buildspec-build.yml` (Build & Push)
  - `buildspec-deploy.yml` (Deploy to EKS)
- Deploy the image to an **EKS Cluster** using `kubectl`
- Use STS Assume Role pattern for secure EKS interaction

## Step-03: Pre-requisite check
- We are going to deploy a application which will also have a `AWS Load Balancer Controller` and also will register its DNS name in Route53 using `External DNS`
- Which means we should have both related pods running in our cluster. 
```t
# Verify aws-load-balancer-controller pod running in namespace kube-system
kubectl get pods -n kube-system

# Verify external-dns pod running in default namespace
kubectl get pods
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
### Step-07-02: DEPLOY STAGE: DEPLOY PHASE: EDIT CodePipeline - BUILD PHASE
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
- In an AWS CodePipeline, we are going to use AWS CodeBuild to deploy changes to our Kubernetes manifests. 
- This requires an AWS IAM role capable of interacting with the EKS cluster.
- In this step, we are going to create an IAM role and add an inline policy `EKS:Describe` that we will use in the CodeBuild stage to interact with the EKS cluster via kubectl.
```
# Export your Account ID
export ACCOUNT_ID=180789647333

# Set Trust Policy
TRUST="{ \"Version\": \"2012-10-17\", \"Statement\": [ { \"Effect\": \"Allow\", \"Principal\": { \"AWS\": \"arn:aws:iam::${ACCOUNT_ID}:root\" }, \"Action\": \"sts:AssumeRole\" } ] }"

# Verify inside Trust policy, your account id got replacd
echo $TRUST

# Create IAM Role for CodeBuild to Interact with EKS
aws iam create-role --role-name EksCodeBuildKubectlRole --assume-role-policy-document "$TRUST" --output text --query 'Role.Arn'

# Define Inline Policy with eks Describe permission in a file iam-eks-describe-policy
echo '{ "Version": "2012-10-17", "Statement": [ { "Effect": "Allow", "Action": "eks:Describe*", "Resource": "*" } ] }' > /tmp/iam-eks-describe-policy

# Associate Inline Policy to our newly created IAM Role
aws iam put-role-policy --role-name EksCodeBuildKubectlRole --policy-name eks-describe --policy-document file:///tmp/iam-eks-describe-policy

# Verify the same on Management Console
```

#### For Windows users who are using Powershell
```t
Here is a solutions to creating the Trust policy from AWS Tech Support

I understand that you are following an instruction to create an IAM role for CodeBuild but the commands do not work for PowerShell.

In PowerShell, the format is different from the scripts in Mac OS. Cmdlets are used in PowerShell. I have used Cmdlets in PowerShell to create a role and attach an inline policy. Please check the following for the details:

1. Create IAM Role for CodeBuild to Interact with EKS

First create a new file NewRoleTrustPolicy.json with the following contents:

{

"Version": "2012-10-17",

"Statement": [

{

"Sid": "",

"Effect": "Allow",

"Principal": {

"AWS": "arn:aws:iam::xxxxxxxxxxxx:root"

},

"Action": "sts:AssumeRole"

}

]

}

Note: please replace your account ID in the above Principal parameter.


New-IAMRole -AssumeRolePolicyDocument (Get-Content -raw NewRoleTrustPolicy.json) -RoleName EksCodeBuildKubectlRole

After the above command, you can check if the IAM role EksCodeBuildKubectlRole is created in your AWS account. Please check the New-IAMRole Cmdlet reference in [1].


2. Define Inline Policy with eks Describe permission in a file iam-eks-describe-policy

First create a new file iam-eks-describe-policy.json with the following contents:

{ "Version": "2012-10-17",

"Statement":

[ { "Effect": "Allow",

"Action": "eks:Describe*",

"Resource": "*" }

]

}

Write-IAMRolePolicy -RoleName EksCodeBuildKubectlRole -PolicyName eks-describe -PolicyDocument (Get-Content -Raw iam-eks-describe-policy.json)


After the above command, you can check if the IAM role EksCodeBuildKubectlRole has the inline policy eks-describe attached. Please check the Write-IAMRolePolicy Cmdlet reference in [2].
I hope the above information can help you.

References
================
[1]: New-IAMRole
https://docs.aws.amazon.com/powershell/latest/reference/items/New-IAMRole.html
[2]: Write-IAMRolePolicy
https://docs.aws.amazon.com/powershell/latest/reference/items/Write-IAMRolePolicy.html


```

### Step-07-05: DEPLOY STAGE: Update EKS Cluster aws-auth ConfigMap with new role created in previous step
- We are going to add the role to the `aws-auth ConfigMap` for the EKS cluster.
- Once the `EKS aws-auth ConfigMap` includes this new role, kubectl in the CodeBuild stage of the pipeline will be able to interact with the EKS cluster via the IAM role.
```t
# Change Directory
cd 11-NEW-DevOps-with-AWS-Developer-Tools-and-GitHub

# Verify what is present in aws-auth configmap before change
kubectl get configmap aws-auth -o yaml -n kube-system

# Backup aws-auth configmap
kubectl get -n kube-system configmap/aws-auth -o yaml > aws-auth/backup-aws-auth-v1.yml

# Export your Account ID
export ACCOUNT_ID=180789647333

# Set ROLE value
ROLE="    - rolearn: arn:aws:iam::$ACCOUNT_ID:role/EksCodeBuildKubectlRole\n      username: build\n      groups:\n        - system:masters"

# Get current aws-auth configMap data and attach new role info to it
kubectl get -n kube-system configmap/aws-auth -o yaml | awk "/mapRoles: \|/{print;print \"$ROLE\";next}1" > aws-auth/aws-auth-patch-v1.yml


# Patch the aws-auth configmap with new role
kubectl patch configmap/aws-auth -n kube-system --patch "$(cat /aws-auth/aws-auth-patch-v1.yml)"

# Verify what is updated in aws-auth configmap after change
kubectl get configmap aws-auth -o yaml -n kube-system
```

#### This is for the changing the Configmap with Windows PowerShell 
```t
This is for the changing the Configmap and PowerShell

In PowerShell, the following steps can be used:

1. kubectl edit -n kube-system configmap/aws-auth
2. In step1, there will be a file opened for you to edit configmap/aws-auth.
In the opened file, there is a mapRoles field such as:
data:
mapRoles: |
- rolearn: <ARN of instance role>
username: system:node:{{EC2PrivateDNSName}}
groups:
- system:bootstrappers
- system:nodes

3. Add the EksCodeBuildKubectlRole information into the mapRoles field of the file such as:
data:
mapRoles: |
- rolearn: arn:aws:iam::018185988195:role/EksCodeBuildKubectlRole
username: build
groups:
- system:masters
- rolearn: <ARN of instance role (not instance profile)>
username: system:node:{{EC2PrivateDNSName}}
groups:
- system:bootstrappers
- system:nodes

Save the file.


4. After the file is saved and closed, configmap/aws-auth has been edited. You can check configmap/aws-auth using the command "kubectl describe -n kube-system configmap/aws-auth".
```



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

## Step-12: Clean-Up
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

## Additional References
- https://docs.aws.amazon.com/codebuild/latest/userguide/build-env-ref-available.html
- https://github.com/aws/aws-codebuild-docker-images/blob/master/al2/x86_64/standard/3.0/Dockerfile
- **STS Assume Role:** https://docs.aws.amazon.com/cli/latest/reference/sts/assume-role.html
- https://docs.aws.amazon.com/IAM/latest/UserGuide/troubleshoot_roles.html



