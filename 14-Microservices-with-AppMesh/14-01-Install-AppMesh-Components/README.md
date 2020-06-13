# Install AppMesh Components

## Step-01: Introduction

## Step-02: Pre-requisite - Create Github account & Setup SSH Key
### SignUp for Github
- We need to have a github account to perform all AppMesh components automatically using gitops pipeline. 
- SignUp for Github
  - URL: https://github.com/
  - Username:
  - Email:
  - Password:
  - Sign Up for Github

### Install local git client
- URL: https://git-scm.com/downloads   

### Create SSH keys
```
# Template
cd ~/.ssh 
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
cat id_rsa.pub

Example from my MAC: 
cd /Users/kdaida/.ssh)
ssh-keygen -t rsa -b 4096 -C "stacksimplify@gmail.com"   
cat id_rsa.pub
```

### Update SSH Publick Key in github 
- In the upper-right corner of any github page, click your **profile photo**, then click **Settings**.
- In the user settings sidebar, click **SSH and GPG keys**.
- Click **New SSH key** or **Add SSH key**.
- In the **Title** field, add a descriptive label for the new key. For example, if you're using a personal Mac, you might call this key "Personal MacBook Air".
- Paste your key into the "Key" field.

### Test your access from local git client to github
```
# Test git access
ssh -T git@github.com

# Sample Output
Kalyans-MacBook-Pro:V2-AppMesh-Objects kdaida$ ssh -T git@github.com
Hi stacksimplify! You've successfully authenticated, but GitHub does not provide shell access.
Kalyans-MacBook-Pro:V2-AppMesh-Objects kdaida$ 
```

## Step-03: Create EKS Cluster with AppMesh Profile enabled
- The below command will create a EKS Cluster with name `appmesh`
- It will also create a nodegroup with 2 t3.medium EC2 Instances. 
- You can update your existing Keypair name at `--ssh-public-key`
- `--appmesh-access` this will add the AppMesh profile to the cluster. 
- It will take approximately 15 to 20 minutes to create the cluster.
```
eksctl create cluster --name=appmesh \
--region=us-east-1 \
--zones=us-east-1a,us-east-1b \
--node-type=t3.medium \
--nodes 2 \
--nodes-min=2 \
--nodes-max=4 \
--node-volume-size=50 \
--vpc-nat-mode=Single \
--ssh-access \
--ssh-public-key=kube-demo-2020 \
--managed \
--asg-access \
--external-dns-access \
--full-ecr-access \
--appmesh-access \
--alb-ingress-access 
```

## Step-04: Create a Repository in your github Account
- Click on New
- Repository name: appmesh-test1
- Description: Appmesh components deployment automatically using Flux
- Public: checked
- Click on **Create Repository**

## Step-05: Set the below environment variables
- GHUSER: Your github userid
- GHREPO: repository name created in previous step `appmesh-test1`
```
export GHUSER=stacksimplify
export GHREPO=appmesh-test2
export EKSCTL_EXPERIMENTAL=true
```

## Step-06: Enable Repository
- This will install `Flux` and `Helm Operator` in your EKS Cluster. 
```
# Enable Repo
eksctl enable repo \
--cluster=appmesh \
--region=us-east-1 \
--git-url=git@github.com:${GHUSER}/${GHREPO} \
--git-user=${GHUSER} \
--git-email=${GHUSER}@users.noreply.github.com

# Verify the objects in your cluster
kubectl get all -n flux
```
## Step-07: Add Flux's deploy key to your GitHub repository.
- The output from `eksctl enable repo` will provide us the `flux deploy key`. 
- Update the key in your github repository `appmesh-test1`
- Go to your repository `appmesh-test1` -> Click on **Settings**
- Click on **Deploy Keys** -> Click on **Add on Deploy Keys**
  - Title: Flux Deploy Key
  - Key: paste the key copied from the output of `eksctl enable repo`


## Step-08: Enable Profile
- `eksctl enable profile`installs the App Mesh control plane on this cluster, and adds its manifests to the configured repository.
```
# Enable Profile
eksctl enable profile appmesh \
--cluster=appmesh \
--region=us-east-1 \
--git-url=git@github.com:${GHUSER}/${GHREPO} \
--git-user=fluxcd \
--git-email=${GHUSER}@users.noreply.github.com

# Verify the appmesh components installation (Wait for 2 to 3 mins and re-execute, if output is empty for below command)
kubectl get helmreleases --all-namespaces

# List all AppMesh Components in Kubernetes
kubectl -n appmesh-system get deploy,pods,service

# Describe the AppMesh
kubectl describe mesh appmesh
```

## Step-09: Access Grafana Dashboard for AppMesh components
- Access the Grafana Dashboard
```
# Access Grafana Dashboard
kubectl -n appmesh-system port-forward svc/appmesh-grafana 3000:3000
```

## Step-10: Create an OpenID Connect (OIDC) identity provider for your cluster. I
```
# Export names
export CLUSTER_NAME=appmesh
export AWS_REGION=us-east-1

# Create OIDC provider
eksctl utils associate-iam-oidc-provider \
    --region=$AWS_REGION \
    --cluster $CLUSTER_NAME \
    --approve
```

## Reference
### Github SSH Keys
- https://help.github.com/en/enterprise/2.18/user/github/authenticating-to-github/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent#generating-a-new-ssh-key
- https://help.github.com/en/enterprise/2.18/user/github/authenticating-to-github/adding-a-new-ssh-key-to-your-github-account

### AppMesh
- https://github.com/weaveworks/eks-appmesh-profile


