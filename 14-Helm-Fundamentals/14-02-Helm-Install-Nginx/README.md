# Install Nginx using Helm Charts

## Step-01: Search Nginx in Helm Repo
- We didnt find any standalone NGINX webserver here
```
helm search repo nginx
```
## Step-02: Add Bitnami Chart Repository & Search
```
# Add Bitnami Repo
helm repo add bitnami https://charts.bitnami.com/bitnami

# Update Repo
helm repo update

# Search Bitnami Repo
helm search repo bitnami
```

## Step-03: Search for Nginx Standard webserver
```
helm search repo nginx
helm search repo bitnami/nginx
```

## Step-04: Install Nginx using Helm chart found in bitnami
```
# Install Nginx using Helm
helm install helmwebserver bitnami/nginx

# Verfify Deployment, Pod and Service
kubectl get svc,po,deploy
```

## Step-05: Access Application
- Verify Load Balancer
- Access Application
```
http://<LOAD-BALANCER-DNS-NAME>
```

## Step-06: Uninsall Application using Helm
```
# List 
helm list

# Uninstall Nginx using Helm
helm uninstall helmwebserver

# Verfify Deployment, Pod and Service
kubectl get svc,po,deploy
```