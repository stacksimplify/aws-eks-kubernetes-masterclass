# Install Kubeapps for Helm Chart Discover & Install instantly

## Step-01: Install Kubeapps
```
helm repo add bitnami https://charts.bitnami.com/bitnami
kubectl create namespace kubeapps
helm install kubeapps --namespace kubeapps bitnami/kubeapps --set useHelm3=true
```

## Step-02: Create a Kubernetes API token
- This is required to login to Kubeapps Application via browser
- Make a note of token
```
# Create Service Account
kubectl create serviceaccount kubeapps-operator

# Create Cluster Role Binding
kubectl create clusterrolebinding kubeapps-operator --clusterrole=cluster-admin --serviceaccount=default:kubeapps-operator

# Get API Token
kubectl get secret $(kubectl get serviceaccount kubeapps-operator -o jsonpath='{range .secrets[*]}{.name}{"\n"}{end}' | grep kubeapps-operator-token) -o jsonpath='{.data.token}' -o go-template='{{.data.token | base64decode}}' && echo
```

## Step-03: Start the Kubeapps Dashboard
- Provide the token noted from previous step on kubeapps login screen
```
# Run the port-forward  
kubectl port-forward -n kubeapps svc/kubeapps 8080:80

# Access from local desktop
http://localhost:8080
```

## Step-04: Explore Catalog
- Explore catalog and deploy existing charts available in catalog.

## Step-05: Cleanup
```
# Helm List
helm list -n kubeapps

# Uninstall Kubeapps
helm uninstall kubeapps -n kubeapps
```