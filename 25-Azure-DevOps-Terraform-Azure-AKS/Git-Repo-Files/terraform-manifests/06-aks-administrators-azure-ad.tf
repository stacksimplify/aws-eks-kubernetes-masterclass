# Create Azure AD Group in Active Directory for AKS Admins
resource "azuread_group" "aks_administrators" {
  #name        = "${azurerm_resource_group.aks_rg.name}-administrators"
  display_name        = "${azurerm_resource_group.aks_rg.name}-${var.environment}-administrators"
  description = "Azure AKS Kubernetes administrators for the ${azurerm_resource_group.aks_rg.name}-${var.environment} cluster."
  security_enabled = true
}
