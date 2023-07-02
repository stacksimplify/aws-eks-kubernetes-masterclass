# Terraform Command Basics

## Step-01: Introduction
- Install Terraform
- Understand what is Terraform
- Understand Terrafom basic / essential commands
  - terraform version
  - terraform init
  - terraform plan
  - terraform validate
  - terraform apply
  - terraform show
  - terraform refresh
  - terraform providers
  - terraform destroy


## Pre-requisite-1: Install Visual Studio Code (VS Code Editor)
- [Download Visual Studio Code](https://code.visualstudio.com/download)

## Pre-requisite-2: Install HashiCorp Terraform plugin for VS Code
- [Install Terraform Plugin for VS Code](https://marketplace.visualstudio.com/items?itemName=HashiCorp.terraform)

## Step-02: Terraform Install
- **Referene Link:**
- [Download Terraform](https://www.terraform.io/downloads.html)
- [Install Terraform](https://learn.hashicorp.com/tutorials/terraform/install-cli)

### MAC OS
```
# Install on MAC OS
brew install hashicorp/tap/terraform

# Verify Terraform Version
terraform version

# To Upgrade on MAC OS
brew upgrade hashicorp/tap/terraform

# Verify Terraform Version
terraform version

# Verify Installation
terraform help
terraform help plan

# Enable Tab Completion
terraform -install-autocomplete
```

## Step-03: Install Azure CLI
```
# AZ CLI Current Version (if installed)
az --version

# Install Azure CLI (if not installed)
brew update && brew install azure-cli

# Upgrade az cli version
az --version
brew upgrade azure-cli 
[or]
az upgrade
az --version

# Azure CLI Login
az login

# List Subscriptions
az account list

# Set Specific Subscription (if we have multiple subscriptions)
az account set --subscription="SUBSCRIPTION_ID"
```

## Step-04: Understand terrafrom init & provider azurerm
- Understand about [Terraform Providers](https://www.terraform.io/docs/providers/index.html)
- Understand about [azurerm terraform provider](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs), version and features
- terraform init: Initialize a Terraform working directory
- terraform apply: Builds or changes infrastructure
```
# Change Directory to v1 folder
cd v1-terraform-azurerm-provider

# Initialize Terraform
terraform init

# Explore ".terraform" folder
cd .terraform
Go inside folders and review (.terraform/plugins/registry.terraform.io/hashicorp/azurerm/2.35.0/darwin_amd64)

# Execute terraform apply
terraform apply 
ls -lrta
discuss about "terraform.tfstate"

# Delete .terraform folder (Understand what happens)
rm -rf .terraform 
terraform apply (Should say could not load plugin)
To fix execute "terraform init" 

# Clean-Up V1 folder
rm terraform.tfstate
ls -lrta
```

## Step-04: Understand terraform plan, apply & Create Azure Resource Group
- Authenticate to Azure using Azure CLI `az login`
- Understand about `terraform plan`
- Understand about `terraform apply`
- Create Azure Resource Group using Terraform
- terraform init: Initialize a Terraform working directory
- terraform plan: Generate and show an execution plan
- terraform apply: Builds or changes infrastructure
```
# Change Directory to v2 folder
cd ../
cd v2-terraform-azurerm-resource-group

# Initialize Terraform
terraform init

# Validate terraform templates
terraform validate

# Dry run to see what resources gets created
terraform plan

# Create Resource Group in Azure
terraform apply
```
- Verify if resource group created in Azure using Management Console


## Step-05: Make changes to Resource Group and Deploy
- Add tags to Resource Group as below
```
# Create a Azure Resource Group
resource "azurerm_resource_group" "aksdev" {
  name     = "aks-rg2-tf"
  location = "Central US"

# Add Tags
  tags = {
    "environment" = "k8sdev"
  }
}
```
- Run terraform plan and apply
```
# Dry run to see what resources gets created
terraform plan

# Create Resource Group in Azure
terraform apply
```
- Verify if resource group created in Azure using Management Console

## Step-06: Modify Resource Group Name and Understand what happens
- Change Resource Group name from `aks-rg2-tf` to `aks-rg2-tf2` in main.tf
```
# Understand what happens with this change
terraform plan

# Apply changes
terraform apply
```
- Verify if resource group with new name got re-created in Azure using Management Console


## Step-07: Understand terraform refresh in detail
- **terraform refresh:** Update local state file against real resources in cloud
- **Desired State:** Local Terraform Manifest (main.tf)
- **Current State:**  Real Resources present in your cloud
- **Command Order of Execution:** refresh, plan, make a decision, apply
- Why? Lets understand that in detail about this order of execution
### Step-07-01: Add a new tag to Resource Group using Azure Portal Management console 
```
demotag: refreshtest
```

### Step-07-02: Execute terraform plan  
- You should observe no changes to local state file because plan does the comparison in memory 
- no update to tfstate file locally about the change 
```
# Execute Terraform plan
terraform plan 
```
### Step-07-03: Execute terraform refresh 
- You should see local state file updated with new demo tag
```
# Execute terraform refresh
ls -lrta
terraform refresh
diff terraform.tfstate.backup terraform.tfstate
```
### Step-07-04: Why you need to the execution in this order (refresh, plan, make a decision, apply) ?
- There are changes happened in your infra manually and not via terraform.
- Now decision to be made if you want those changes or not.
- **Choice-1:** If you dont want those changes proceed with terraform apply so manual changes will be removed.
- **Choice-2:** If you want those changes, refer terraform.tfstate file about changes and embed them in your terraform manifests (example: main.tf) and proceed with flow (referesh, plan, review execution plan and apply)

### Step-07-05: I picked choice-2, so i will update the tags in main.tf
- Update in main.tf
```
  tags = {
    "environment" = "k8sdev"
    "demotag"     = "refreshtest"
  }
```
### Step-07-06: Execute the commands to make our manual change official in terraform manifests and tfstate files perspective  
```
# Execute commands
ls -lrta
terraform refresh
diff terraform.tfstate.backup terraform.tfstate
terraform plan
terraform apply
```

## Step-08: Understand terraform show, providers
- **terraform show:** Inspect Terraform state or plan
- **terraform providers:** Prints a tree of the providers used in the configuration
```
# Terraform Show
terraform show

# Terraform Providers
terraform providers
```


## Step-09: Understand terraform destroy
- Understand about `terraform destroy`
```
# Delete newly created Resource Group in Azure 
terraform destroy

# Delete State (Deleting for github repo case for course purpose)
rm -rf .terraform
rm -rf terraform.tfstate
```


## References
- [Main Azure Resource Manager Reference](https://www.terraform.io/docs/providers/azurerm/index.html)
- [Azure Get Started on Terraform](https://learn.hashicorp.com/collections/terraform/azure-get-started)
- [Terraform Resources and Modules](https://www.terraform.io/docs/configuration/index.html#resources-and-modules)
