# Ingress - SSL

## Step-01: Introduction
- Implement SSL using Lets Encrypt

[![Image](https://www.stacksimplify.com/course-images/azure-aks-ingress-ssl-letsencrypt.png "Azure AKS Kubernetes - Masterclass")](https://www.udemy.com/course/aws-eks-kubernetes-masterclass-devops-microservices/?referralCode=257C9AD5B5AF8D12D1E1)

## Step-02: Install Cert Manager
```
# Install the CustomResourceDefinition resources separately
kubectl apply --validate=false -f https://raw.githubusercontent.com/jetstack/cert-manager/release-0.13/deploy/manifests/00-crds.yaml

# Label the ingress-basic namespace to disable resource validation
kubectl label namespace ingress-basic cert-manager.io/disable-validation=true

# Add the Jetstack Helm repository
helm repo add jetstack https://charts.jetstack.io

# Update your local Helm chart repository cache
helm repo update

# Install the cert-manager Helm chart
helm install \
  cert-manager \
  --namespace ingress-basic \
  --version v0.13.0 \
  jetstack/cert-manager

# Verify Cert Manager pods
kubectl get pods --namespace ingress-basic
```

## Step-06: Review or Create Cluster Issuer Kubernetes Manifest
### Review Cluster Issuer Kubernetes Manifest
- Create or Review Cert Manager Cluster Issuer Kubernetes Manigest
```yml
apiVersion: cert-manager.io/v1alpha2
kind: ClusterIssuer
metadata:
  name: letsencrypt
spec:
  acme:
    server: https://acme-v02.api.letsencrypt.org/directory
    email: dkalyanreddy@gmail.com
    privateKeySecretRef:
      name: letsencrypt
    solvers:
      - http01:
          ingress:
            class: nginx
```

### Deploy Cluster Issuer
```
# Deploy Cluster Issuer
kubectl apply -f kube-manifests/01-CertManager-ClusterIssuer/cluster-issuer.yml
```


## Step-07: Review Application NginxApp1,2 K8S Manifests
- 01-NginxApp1-Deployment.yml
- 02-NginxApp1-ClusterIP-Service.yml
- 01-NginxApp2-Deployment.yml
- 02-NginxApp2-ClusterIP-Service.yml

## Step-08: Create or Review Ingress SSL Kubernetes Manifest
- 01-Ingress-SSL.yml

## Step-09: Deploy All Manifests & Verify
- Certificate Request, Generation, Approal and Download and be ready might take from 1 hour to couple of days if we make any mistakes and also fail.
- For me it took, only 5 minutes to get the certificate from **https://letsencrypt.org/**
```
# Deploy
kubectl apply -R -f kube-manifests/

# Verify Pods
kubectl get pods

# Verify Cert Manager Pod Logs
kubectl get pods -n ingress-basic
kubectl  logs -f <cert-manager-55d65894c7-sx62f> -n ingress-basic #Replace Pod name


# Verify SSL Certificates (It should turn to True)
kubectl get certificate
```
```log
stack@Azure:~$ kubectl get certificate
NAME                      READY   SECRET                    AGE
app1-kubeoncloud-secret   True    app1-kubeoncloud-secret   45m
app2-kubeoncloud-secret   True    app2-kubeoncloud-secret   45m
stack@Azure:~$
```

```
# Sample Success Log
I0824 13:09:00.495721       1 controller.go:129] cert-manager/controller/orders "msg"="syncing item" "key"="default/app2-kubeoncloud-secret-2792049964-67728538" 
I0824 13:09:00.495900       1 sync.go:102] cert-manager/controller/orders "msg"="Order has already been completed, cleaning up any owned Challenge resources" "resource_kind"="Order" "resource_name"="app2-kubeoncloud-secret-2792049964-67728538" "resource_namespace"="default" 
I0824 13:09:00.496904       1 controller.go:135] cert-manager/controller/orders "msg"="finished processing work item" "key"="default/app2-kubeoncloud-secret-2792049964-67728538
```

## Step-10: Access Application
```
http://sapp1.kubeoncloud.com/app1/index.html
http://sapp2.kubeoncloud.com/app2/index.html
```

## Step-11: Verify Ingress logs for Client IP
```
# List Pods
kubectl -n ingress-basic get pods

# Check logs
kubectl -n ingress-basic logs -f nginx-ingress-controller-xxxxxxxxx
```
## Step-12: Clean-Up
```
# Delete Apps
kubectl delete -R -f kube-manifests/

# Delete Ingress Controller
kubectl delete namespace ingress-basic
```

## Cert Manager
- https://docs.cert-manager.io/en/latest/reference/issuers.html
- https://docs.cert-manager.io/en/latest/reference/ingress-shim.html
- https://cert-manager.io/docs/release-notes/
- https://cert-manager.io/docs/reference/api-docs/#cert-manager.io/v1beta1.Issuer
- https://letsencrypt.org/how-it-works/