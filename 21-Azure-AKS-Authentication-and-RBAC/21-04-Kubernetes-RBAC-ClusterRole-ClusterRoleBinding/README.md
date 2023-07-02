---
title: K8S RBAC Cluster Role & Role Binding with AD on AKS
description: Restrict Access to k8s resources using Kubernetes RBAC Cluster Role and Role Binding with Azure AD
---
# K8S RBAC Cluster Role & Role Binding with AD on AKS

## Step-01: Introduction
- AKS can be configured to use Azure AD for Authentication which we have seen in our previous section
- In addition, we can also configure Kubernetes role-based access control (RBAC) to limit access to cluster resources based a user's identity or group membership.
- Understand about Kubernetes RBAC **Cluster Role & Cluster Role Binding**

[![Image](https://stacksimplify.com/course-images/azure-kubernetes-service-RBAC-CR-CRB-1.png "Azure AKS Kubernetes - Masterclass")](https://stacksimplify.com/course-images/azure-kubernetes-service-RBAC-CR-CRB-1.png)

[![Image](https://stacksimplify.com/course-images/azure-kubernetes-service-RBAC-CR-CRB-2.png "Azure AKS Kubernetes - Masterclass")](https://stacksimplify.com/course-images/azure-kubernetes-service-RBAC-CR-CRB-2.png)


## Step-02: Create AD Group, Role Assignment and User
```
# Get Azure AKS Cluster Id
AKS_CLUSTER_ID=$(az aks show --resource-group aks-rg3 --name aksdemo3 --query id -o tsv)
echo $AKS_CLUSTER_ID

# Create Azure AD Group
AKS_READONLY_GROUP_ID=$(az ad group create --display-name aksreadonly --mail-nickname aksreadonly --query objectId -o tsv)    
echo $AKS_READONLY_GROUP_ID

# Create Role Assignment 
az role assignment create \
  --assignee $AKS_READONLY_GROUP_ID \
  --role "Azure Kubernetes Service Cluster User Role" \
  --scope $AKS_CLUSTER_ID

# Create AKS ReadOnly User in Azure AD
AKS_READONLY_USER_OBJECT_ID=$(az ad user create \
  --display-name "AKS READ1" \
  --user-principal-name aksread1@stacksimplifygmail.onmicrosoft.com \
  --password @AKSDemo123 \
  --query objectId -o tsv)
echo $AKS_READONLY_USER_OBJECT_ID

# Associate aksread1 User to aksreadonly Group in Azure AD
az ad group member add --group aksreadonly --member-id $AKS_READONLY_USER_OBJECT_ID
```

## Step-03: Test aksreadonly User Authentication to Portal
- URL: https://portal.azure.com
- Username: aksread1@stacksimplifygmail.onmicrosoft.com
- Password: @AKSDemo123


## Step-04: Review Kubernetes RBAC ClusterRole & ClusterRoleBinding
### Kubernetes RBAC Role for aksreadonly User Access
- **File Name:** ClusterRole-ReadOnlyAccess.yaml
```yaml
kind: ClusterRole
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: aks-cluster-readonly-role
rules:
- apiGroups: ["", "extensions", "apps"]
  resources: ["*"]
  verbs: ["get", "list", "watch"]
- apiGroups: ["batch"]
  resources:
  - jobs
  - cronjobs
  verbs: ["get", "list", "watch"]
```
### Get Object Id for aksreadonly AD Group
```
# Get Object ID for AD Group aksreadonly
az ad group show --group aksreadonly --query objectId -o tsv

# Output
e808215d-d159-49ba-8bb6-9661ba478842
```

[![Image](https://stacksimplify.com/course-images/azure-kubernetes-service-RBAC-ClusterRole.png "Azure AKS Kubernetes - Masterclass")](https://stacksimplify.com/course-images/azure-kubernetes-service-RBAC-ClusterRole.png)

### Review & Update Kubernetes RBAC ClusterRoleBinding with Azure AD Group ID
- Update Azure AD Group **aksreadonly** Object ID in Cluster Role Binding k8s manifest
- **File Name:** ClusterRoleBinding-ReadOnlyAccess.yaml
```yaml
kind: ClusterRoleBinding
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: aks-cluster-readonly-rolebinding
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: aks-cluster-readonly-role
subjects:
- kind: Group
  #name: groupObjectId
  name: "e808215d-d159-49ba-8bb6-9661ba478842"   
```

[![Image](https://stacksimplify.com/course-images/azure-kubernetes-service-RBAC-ClusterRoleBinding.png "Azure AKS Kubernetes - Masterclass")](https://stacksimplify.com/course-images/azure-kubernetes-service-RBAC-ClusterRoleBinding.png)

## Step-05: Create Kubernetes RBAC ClusterRole & ClusterRoleBinding 
```
# As AKS Cluster Admin (--admin)
az aks get-credentials --resource-group aks-rg3 --name aksdemo3 --admin

# Create Kubernetes Role and Role Binding
kubectl apply -f kube-manifests/

# Verify ClusterRole & ClusterRoleBinding 
kubectl get clusterrole
kubectl get clusterrolebinding
```

## Step-06: Access AKS Cluster
```
# Overwrite kubectl credentials
az aks get-credentials --resource-group aks-rg3 --name aksdemo3 --overwrite-existing

# List Pods 
kubectl get pods --all-namespaces
- URL: https://microsoft.com/devicelogin
- Code: GCHL8J45R (Sample)(View on terminal)
- Username: aksread1@stacksimplifygmail.onmicrosoft.com
- Password: @AKSDemo123

# List Nodes
kubectl get nodes
```


## Step-07: Create any resource on k8s and observe message
- Create a namespace and see what happems
- We should see forbidder error as this user (aksread1) has only read access to cluster. This use cannot create k8s resources
```
# Create Namespaces dev and qa
kubectl create namespace dev
kubectl create namespace qa

# Error Message
Kalyans-Mac-mini:21-04-Kubernetes-RBAC-ClusterRole-ClusterRoleBinding kalyanreddy$ kubectl create namespace dev
Error from server (Forbidden): namespaces is forbidden: User "aksread1@stacksimplifygmail.onmicrosoft.com" cannot create resource "namespaces" in API group "" at the cluster scope
Kalyans-Mac-mini:21-04-Kubernetes-RBAC-ClusterRole-ClusterRoleBinding kalyanreddy$ 
```


## Step-08: Clean-Up
```
# Clean-Up Clusters Delete Clusters aksdemo3, aksdemo4
Go to All Services -> Resource Groups -> Delete Resource group  aks-rg3
Go to All Services -> Resource Groups -> Delete Resource group  aks-rg4

# Delete Azure AD Users & Groups
# Users
  - user1aksadmin@stacksimplifygmail.onmicrosoft.com 
  - aksdev1@stacksimplifygmail.onmicrosoft.com
  - aksread1@stacksimplifygmail.onmicrosoft.com
# Groups
  - k8sadmins
  - devaksteam
  - aksreadonly
```

