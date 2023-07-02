---
title: Azure AD Integration with Azure AKS for Authentication
description: Azure Active Directory Integration with Azure Kubernetes Service Cluster Admins 
---

# Azure AD Authentication for AKS Cluster Admins

## Step-00: Pre-requisites
- We should have Azure AKS Cluster Up and Running.
```
# Configure Command Line Credentials for kubectl
az aks get-credentials --name aksdemo3 --resource-group aks-rg3

# Verify Nodes
kubectl get nodes 
kubectl get nodes -o wide

# Get Cluster Information
kubectl cluster-info
```

## Step-01: Introduction
- We can use Azure AD Users and Groups to Manage AKS Clusters
- We can create Admin Users in Azure AD and Associate to Azure AD Group named `k8sadmins` and those users can access Azure AKS Cluster using kubectl. 
- [Three important things](https://docs.microsoft.com/en-us/azure/aks/managed-aad#limitations) we need to remember before making any changes to our existing AKS Clusters
- **Important Note-1:** AKS-managed Azure AD integration can't be disabled
- **Important Note-2:** non-RBAC enabled clusters aren't supported for AKS-managed Azure AD integration
- **Important Note-3:** Changing the Azure AD tenant associated with AKS-managed Azure AD integration isn't supported

[![Image](https://stacksimplify.com/course-images/azure-kubernetes-service-ad-authentication-part-1.png "Azure AKS Kubernetes - Masterclass")](https://stacksimplify.com/course-images/azure-kubernetes-service-ad-authentication-part-1.png)

[![Image](https://stacksimplify.com/course-images/azure-kubernetes-service-ad-authentication-part-2.png "Azure AKS Kubernetes - Masterclass")](https://stacksimplify.com/course-images/azure-kubernetes-service-ad-authentication-part-2.png)



## Step-02: Create Azure AD Group and User in Azure AD 
### Create Azure AD Group 
- Group Type: security 
- Group Name: k8sadmins
- Group Description: AKS Cluster Admins who has full access to Kubernetes Clusters 
- Click on **Create**

### Create Azure AD User & Associate User to Group
- Create User in Azure Active Directory &  Associate User to **k8sadmins** group
- Go to All Services -> Azure Active Directory -> Users -> New User
- **Identity**
  - Username: user1aksadmin
  - Name: User1 AKSAdmin
  - First Name: User1
  - Last Name: AKSAdmin
- **Password**
  - Let me create the password: check the radio button
  - Initial Password: @AKSDemo123
- **Groups & Role**
  - Groups: k8sadmins
  - Roles: User
- Rest all leave to defaults
- Click on **Create**

### Complete First Time user Password Change
- Gather Full username from AD
- URL: https://portal.azure.com
- Username: user1aksadmin@stacksimplifygmail.onmicrosoft.com 
- Current Password: @AKSDemo123
- New Password: @AKSADAuth1011
- Confirm Password: @AKSADAuth1011

### Final Username and Password
- Username: user1aksadmin@stacksimplifygmail.onmicrosoft.com 
- Password: @AKSADAuth1011


## Step-03: Enable AKS Cluster with AKS-managed Azure Active Directory feature
- Go to All Services -> Kubernetes Services -> aksdemo3 -> Settings -> Configuration
- **AKS-managed Azure Active Directory:** Select **Enabled** radio button
- **Admin Azure AD groups:** k8sadmins
- Click on **SAVE**


## Step-04: Access an Azure AD enabled AKS cluster using Azure AD User
- **Important Note:** Once we do **devicelogin** credentials are cached for all subsequent kubectl commands.
```
# Configure kubectl
az aks get-credentials --resource-group aks-rg3 --name aksdemo3 --overwrite-existing

# View Cluster Information
kubectl cluster-info
URL: https://microsoft.com/devicelogin
Code: H8VP9YE7F (Sample)(View on terminal)
Username: user1aksadmin@stacksimplifygmail.onmicrosoft.com 
Password: @AKSADAuth1011

# List Nodes
kubectl get nodes

# List Pods
kubectl get pods -n kube-system

# List Everything
kubectl get all --all-namespaces
```

## Step-05: How to re-login with different user for kubectl ?
- **Important Note:** The moment we change the `$HOME/.kube/config` you will be re-prompted for Azure Device Login for all kubectl commands
- We need to overwrite the $HOME/.kube/config to re-login with different user or same user
```
# Overwrite kubectl credentials 
az aks get-credentials --resource-group aks-rg3 --name aksdemo3 --overwrite-existing

# View kubectl config (Observe aksdemo3 user)
kubectl config view 

# List Nodes
kubectl get nodes
URL: https://microsoft.com/devicelogin
Code: H8VP9YE7F (Sample)
Username: user1aksadmin@stacksimplifygmail.onmicrosoft.com 
Password: @AKSADAuth1011

# View kubectl config (Observe aksdemo3 user - Access Token & Refresh token)
kubectl config view 
```

## Step-06: How to bypass or Override AD Authentication and use k8s admin?
- If we have issues with AD Users or Groups and want to override that we can use **--admin** to override and directly connect to AKS Cluster
```
# Template
az aks get-credentials --resource-group myResourceGroup --name myManagedCluster --admin

# Replace RG and Cluster Name
az aks get-credentials --resource-group aks-rg3 --name aksdemo3 --admin

# List Nodes
kubectl get nodes

# List Pods
kubectl get pods -n kube-system
```

## References
- [AKS Managed AAD](https://docs.microsoft.com/en-us/azure/aks/managed-aad)
- [Azure AD RBAC](https://docs.microsoft.com/en-us/azure/aks/azure-ad-rbac)
- [Azure AKS Identity](https://docs.microsoft.com/en-us/azure/aks/concepts-identity)