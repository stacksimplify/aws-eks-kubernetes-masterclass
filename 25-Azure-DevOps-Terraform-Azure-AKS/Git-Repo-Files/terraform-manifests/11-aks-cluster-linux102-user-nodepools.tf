# Create Linux Azure AKS Node Pool
/*
resource "azurerm_kubernetes_cluster_node_pool" "linux102" {
  availability_zones    = [1, 2, 3]
  enable_auto_scaling   = true
  kubernetes_cluster_id = azurerm_kubernetes_cluster.aks_cluster.id
  max_count             = 3
  min_count             = 1
  mode                  = "User"
  name                  = "linux102"
  orchestrator_version  = data.azurerm_kubernetes_service_versions.current.latest_version
  os_disk_size_gb       = 30
  os_type               = "Linux" # Default is Linux, we can change to Windows
  vm_size               = "Standard_DS2_v2"
  priority              = "Regular"  # Default is Regular, we can change to Spot with additional settings like eviction_policy, spot_max_price, node_labels and node_taints
  node_labels = {
    "nodepool-type" = "user"
    "environment"   = var.environment
    "nodepoolos"    = "linux"
    "ui-app"        = "reactjs-apps"
  }
  tags = {
    "nodepool-type" = "user"
    "environment"   = var.environment
    "nodepoolos"    = "linux"
    "ui-app"        = "reactjs-apps" 
  }
}
*/