# Provision Azure AKS Cluster using Terraform

## Step-01: Introduction
- Create SSH Keys for AKS Linux VMs
- Declare Windows Username, Passwords for Windows nodepools. This needs to be done during the creation of cluster for 1st time itself if you have plans for Windows workloads on your cluster
- Understand about Datasources and Create Datasource for Azure AKS latest Version
- Create Azure Log Analytics Workspace Resource in Terraform
- Create Azure AD AKS Admins Group Resource in Terraform
- Create AKS Cluster with default nodepool
- Create AKS Cluster Output Values
- Provision Azure AKS Cluster using Terraform
- Access and Test using Azure AKS default admin `--admin`
- Access and Test using Azure AD User as AKS Admin

## Step-02: Create SSH Public Key for Linux VMs
```
# Create Folder
mkdir $HOME/.ssh/aks-prod-sshkeys-terraform

# Create SSH Key
ssh-keygen \
    -m PEM \
    -t rsa \
    -b 4096 \
    -C "azureuser@myserver" \
    -f ~/.ssh/aks-prod-sshkeys-terraform/aksprodsshkey \
    -N mypassphrase

# List Files
ls -lrt $HOME/.ssh/aks-prod-sshkeys-terraform
```

## Step-03: Create 3 more Terraform Input Vairables to variables.tf
- SSH Public Key for Linux VMs
- Windows Admin username
- Windows Admin Password
```
# V2 Changes
# SSH Public Key for Linux VMs
variable "ssh_public_key" {
  default = "~/.ssh/aks-prod-sshkeys-terraform/aksprodsshkey.pub"
  description = "This variable defines the SSH Public Key for Linux k8s Worker nodes"  
}

# Windows Admin Username for k8s worker nodes
variable "windows_admin_username" {
  type = string
  default = "azureuser"
  description = "This variable defines the Windows admin username k8s Worker nodes"  
}

# Windows Admin Password for k8s worker nodes
variable "windows_admin_password" {
  type = string
  default = "P@ssw0rd1234"
  description = "This variable defines the Windows admin password k8s Worker nodes"  
}
```

## Step-04: Create a Terraform Datasource for getting latest Azure AKS Versions 
- Understand [Terraform Datasources](https://www.terraform.io/docs/configuration/data-sources.html) concept as part of this step
- Data sources allow data to be fetched or computed for use elsewhere in Terraform configuration. 
- Use of data sources allows a Terraform configuration to make use of information defined outside of Terraform, or defined by another separate Terraform configuration.
- Use Azure AKS versions datasource API to get the latest version and use it
```
# Call get-versions API via command line
az aks get-versions --location centralus -o table
```
- Create **04-aks-versions-datasource.tf**
- **Important Note:**
  - `include_preview` defaults to true which means we get preview version as latest version which we should not use in production.
  - So we need to enable this flag in datasource and make it to false to use latest version which is not in preview for our production grade clusters
```
# Datasource to get Latest Azure AKS latest Version
data "azurerm_kubernetes_service_versions" "current" {
  location = azurerm_resource_group.aks_rg.location
  include_preview = false  
}
```
- [Data Source: azurerm_kubernetes_service_versions](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/data-sources/kubernetes_service_versions)

## Step-05: Create Azure Log Analytics Workspace Terraform Resource
- The Azure Monitor for Containers (also known as Container Insights) feature provides performance monitoring for workloads running in the Azure Kubernetes cluster.
- We need to create [Log Analytics workspace](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/log_analytics_workspace) and reference its id in AKS Cluster when enabling the monitoring feature.
- Create a file **05-log-analytics-workspace.tf**
```
# Create Log Analytics Workspace
resource "azurerm_log_analytics_workspace" "insights" {
  name                = "logs-${random_pet.aksrandom.id}"
  location            = azurerm_resource_group.aks_rg.location
  resource_group_name = azurerm_resource_group.aks_rg.name
  retention_in_days   = 30
}
```

## Step-06: Create Azure AD Group for AKS Admins Terraform Resource
- To enable AKS AAD Integration, we need to provide Azure AD group object id. 
- We wil create a [Azure Active Directory group](https://registry.terraform.io/providers/hashicorp/azuread/latest/docs/resources/group) for AKS Admins
```
# Create Azure AD Group in Active Directory for AKS Admins
resource "azuread_group" "aks_administrators" {
  name        = "${azurerm_resource_group.aks_rg.name}-cluster-administrators"
  description = "Azure AKS Kubernetes administrators for the ${azurerm_resource_group.aks_rg.name}-cluster."
}
```

## Step-07: Create AKS Cluster Terraform Resource
- Create a file named  **07-aks-cluster.tf**
- Understand and discuss about the terraform resource named  [azurerm_kubernetes_cluster](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/kubernetes_cluster)
- This is going to be a very big terraform template when compared to what we created so far  we will do it slowly step by step.

```
# Provision AKS Cluster
/*
1. Add Basic Cluster Settings
  - Get Latest Kubernetes Version from datasource (kubernetes_version)
  - Add Node Resource Group (node_resource_group)
2. Add Default Node Pool Settings
  - orchestrator_version (latest kubernetes version using datasource)
  - availability_zones
  - enable_auto_scaling
  - max_count, min_count
  - os_disk_size_gb
  - type
  - node_labels
  - tags
3. Enable MSI
4. Add On Profiles 
  - Azure Policy
  - Azure Monitor (Reference Log Analytics Workspace id)
5. RBAC & Azure AD Integration
6. Admin Profiles
  - Windows Admin Profile
  - Linux Profile
7. Network Profile
8. Cluster Tags  
*/

resource "azurerm_kubernetes_cluster" "aks_cluster" {
  name                = "${azurerm_resource_group.aks_rg.name}-cluster"
  location            = azurerm_resource_group.aks_rg.location
  resource_group_name = azurerm_resource_group.aks_rg.name
  dns_prefix          = "${azurerm_resource_group.aks_rg.name}-cluster"
  kubernetes_version  = data.azurerm_kubernetes_service_versions.current.latest_version
  node_resource_group = "${azurerm_resource_group.aks_rg.name}-nrg"

  default_node_pool {
    name                 = "systempool"
    vm_size              = "Standard_DS2_v2"
    orchestrator_version = data.azurerm_kubernetes_service_versions.current.latest_version
    availability_zones   = [1, 2, 3]
    enable_auto_scaling  = true
    max_count            = 3
    min_count            = 1
    os_disk_size_gb      = 30
    type                 = "VirtualMachineScaleSets"
    node_labels = {
      "nodepool-type"    = "system"
      "environment"      = "dev"
      "nodepoolos"       = "linux"
      "app"              = "system-apps" 
    } 
   tags = {
      "nodepool-type"    = "system"
      "environment"      = "dev"
      "nodepoolos"       = "linux"
      "app"              = "system-apps" 
   } 
  }

# Identity (System Assigned or Service Principal)
  identity {
    type = "SystemAssigned"
  }

# Add On Profiles
  addon_profile {
    azure_policy {enabled =  true}
    oms_agent {
      enabled =  true
      log_analytics_workspace_id = azurerm_log_analytics_workspace.insights.id
    }
  }

# RBAC and Azure AD Integration Block
  role_based_access_control {
    enabled = true
    azure_active_directory {
      managed = true
      admin_group_object_ids = [azuread_group.aks_administrators.id]
    }
  }

# Windows Profile
  windows_profile {
    admin_username = var.windows_admin_username
    admin_password = var.windows_admin_password
  }

# Linux Profile
  linux_profile {
    admin_username = "ubuntu"
    ssh_key {
      key_data = file(var.ssh_public_key)
    }
  }

# Network Profile
  network_profile {
    network_plugin = "azure"
    load_balancer_sku = "Standard"
  }

  tags = {
    Environment = "dev"
  }
}

```

## Step-08: Create Terraform Output Values for AKS Cluster
- Create a file named **08-outputs.tf**
```
# Create Outputs
# 1. Resource Group Location
# 2. Resource Group Id
# 3. Resource Group Name

# Resource Group Outputs
output "location" {
  value = azurerm_resource_group.aks_rg.location
}

output "resource_group_id" {
  value = azurerm_resource_group.aks_rg.id
}

output "resource_group_name" {
  value = azurerm_resource_group.aks_rg.name
}

# Azure AKS Versions Datasource
output "versions" {
  value = data.azurerm_kubernetes_service_versions.current.versions
}

output "latest_version" {
  value = data.azurerm_kubernetes_service_versions.current.latest_version
}

# Azure AD Group Object Id
output "azure_ad_group_id" {
  value = azuread_group.aks_administrators.id
}
output "azure_ad_group_objectid" {
  value = azuread_group.aks_administrators.object_id
}


# Azure AKS Outputs

output "aks_cluster_id" {
  value = azurerm_kubernetes_cluster.aks_cluster.id
}

output "aks_cluster_name" {
  value = azurerm_kubernetes_cluster.aks_cluster.name
}

output "aks_cluster_kubernetes_version" {
  value = azurerm_kubernetes_cluster.aks_cluster.kubernetes_version
}

```


## Step-09: Deploy Terraform Resources
```
# Change Directory 
cd 24-03-Create-AKS-Cluster/terraform-manifests-aks

# Initialize Terraform from this new folder
# Anyway our state storage is from Azure Storage we are good from any folder
terraform init

# Validate Terraform manifests
terraform validate

# Review the Terraform Plan
terraform plan

# Deploy Terraform manifests
terraform apply 
```

## Step-10: Access Terraform created AKS cluster using AKS default admin
```
# Azure AKS Get Credentials with --admin
az aks get-credentials --resource-group terraform-aks-dev --name terraform-aks-dev-cluster --admin

# Get Full Cluster Information
az aks show --resource-group terraform-aks-dev --name terraform-aks-dev-cluster
az aks show --resource-group terraform-aks-dev --name terraform-aks-dev-cluster -o table

# Get AKS Cluster Information using kubectl
kubectl cluster-info

# List Kubernetes Nodes
kubectl get nodes
```

## Step-11: Verify Resources using Azure Management Console
- Resource Group
  - terraform-aks-dev
  - terraform-aks-dev-nrg
- AKS Cluster & Node Pool
  - Cluster: terraform-aks-dev-cluster
  - AKS System Pool
- Log Analytics Workspace
- Azure AD Group
  - terraform-aks-dev-cluster-administrators


## Step-12: Create a User in Azure AD and Associate User to AKS Admin Group in Azure AD
- Create a user in Azure Active Directory
  - User Name: taksadmin1
  - Name: taksadmin1
  - First Name: taks
  - Last Name: admin1
  - Password: @AKSadmin11
  - Groups: terraform-aks-prod-administrators
  - Click on Create
- Login and change password 
  - URL: https://portal.azure.com
  - Username: taksadmin1@stacksimplifygmail.onmicrosoft.com  (Change your domain name)
  - Old Password: @AKSadmin11
  - New Password: @AKSadmin22
  - Confirm Password: @AKSadmin22


## Step-13: Access Terraform created AKS Cluster 
```
# Azure AKS Get Credentials with --admin
az aks get-credentials --resource-group terraform-aks-dev --name terraform-aks-dev-cluster --overwrite-existing

# List Kubernetes Nodes
kubectl get nodes
URL: https://microsoft.com/devicelogin
Code: GUKJ3T9AC (sample)
Username: taksadmin1@stacksimplifygmail.onmicrosoft.com  (Change your domain name)
Password: @AKSadmin22
```