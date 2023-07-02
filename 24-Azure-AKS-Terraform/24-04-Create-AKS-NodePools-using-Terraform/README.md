# Create Azure AKS Cluster Linux and Windows Node Pools

## Step-01: Introduction
- Create Windows and Linux Nodepools

## Step-02: Create Azure AKS Linux User Node Pool using Terraform
- Understand about Terraform resource [azurerm_kubernetes_cluster_node_pool](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/kubernetes_cluster_node_pool)
- Create Azure AKS Linux User Node pool
- Create a file named **09-aks-cluster-linux-user-nodepools.tf**
```
resource "azurerm_kubernetes_cluster_node_pool" "linux101" {
  availability_zones    = [1, 2, 3]
  enable_auto_scaling   = true
  kubernetes_cluster_id = azurerm_kubernetes_cluster.aks.id
  max_count             = 3
  min_count             = 1
  mode                  = "User"
  name                  = "linux101"
  orchestrator_version  = data.azurerm_kubernetes_service_versions.current.latest_version
  os_disk_size_gb       = 30
  os_type               = "Linux" # Default is Linux, we can change to Windows
  vm_size               = "Standard_DS2_v2"
  priority              = "Regular"  # Default is Regular, we can change to Spot with additional settings like eviction_policy, spot_max_price, node_labels and node_taints
  node_labels = {
    "nodepool-type" = "user"
    "environment"   = "production"
    "nodepoolos"    = "linux"
    "app"           = "java-apps"
  }
  tags = {
    "nodepool-type" = "user"
    "environment"   = "production"
    "nodepoolos"    = "linux"
    "app"           = "java-apps"
  }
}
```

## Step-03: Create Azure AKS Windows User Node Pool using Terraform
- Create Azure AKS Windows User Node pool to run Windows workloads
- Create a file named **10-aks-cluster-windows-user-nodepools.tf**
```
resource "azurerm_kubernetes_cluster_node_pool" "win101" {
  availability_zones    = [1, 2, 3]
  enable_auto_scaling   = true
  kubernetes_cluster_id = azurerm_kubernetes_cluster.aks.id
  max_count             = 3
  min_count             = 1
  mode                  = "User"
  name                  = "win101"
  orchestrator_version  = data.azurerm_kubernetes_service_versions.current.latest_version
  os_disk_size_gb       = 30
  os_type               = "Windows" # Default is Linux, we can change to Windows
  vm_size               = "Standard_DS2_v2"
  priority              = "Regular"  # Default is Regular, we can change to Spot with additional settings like eviction_policy, spot_max_price, node_labels and node_taints
  #vnet_subnet_id        = azurerm_subnet.aks-default.id 
  node_labels = {
    "nodepool-type" = "user"
    "environment"   = "production"
    "nodepoolos"    = "windows"
    "app"           = "dotnet-apps"
  }
  tags = {
    "nodepool-type" = "user"
    "environment"   = "production"
    "nodepoolos"    = "windows"
    "app"           = "dotnet-apps"
  }
}
```

## Step-04: Deploy Terraform Manifests with nodepool additions (Linux & Windows)
```
# Change Directory 
cd 24-04-Create-AKS-NodePools-using-Terraform/terraform-manifests-aks

# Initialize Terraform
terraform init

# Validate Terraform manifests
terraform validate

# Review the Terraform Plan
terraform plan 

# Deploy Terraform manifests
terraform apply 
```

## Step-05: Verify if Nodepools added successfully
```
# List Node Pools
az aks nodepool list --resource-group terraform-aks-dev --cluster-name  terraform-aks-dev-cluster --output table

# List Nodes using Labels
kubectl get nodes -o wide
kubectl get nodes -o wide -l nodepoolos=linux
kubectl get nodes -o wide -l nodepoolos=windows
kubectl get nodes -o wide -l environment=dev
```


## Step-06: Deploy Sample Applications for all 3 node pools
- Webserver App to System Nodepool
- Sample Java App to Linux Nodepool
- Dotnet App to Windows Nodepool
```
# Change Directory 
cd 24-04-Create-AKS-NodePools-using-Terraform/

# Deploy All Apps
kubectl apply -R -f kube-manifests/

# List Pods
kubectl get pods -o wide
```

## Step-07: Access Applications
```
# List Services to get Public IP for each service we deployed 
kubectl get svc

# Access Webserver App (Running on System Nodepool)
http://<public-ip-of-webserver-app>/app1/index.html

# Access Java-App (Running on linux101 nodepool)
http://<public-ip-of-java-app>
Username: admin101
Password: password101

# Access Windows App (Running on win101 nodepool)
http://<public-ip-of-windows-app>
```

## Step-08: Destroy our Terraform Cluster
```
# Change Directory 
cd 24-04-Create-AKS-NodePools-using-Terraform/terraform-manifests-aks

# Destroy all our Terraform Resources
terraform destroy
```
