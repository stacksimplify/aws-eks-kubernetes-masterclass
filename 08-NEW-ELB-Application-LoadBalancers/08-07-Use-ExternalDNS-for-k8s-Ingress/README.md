---
title: AWS Load Balancer Controller - External DNS & Ingress
description: Learn AWS Load Balancer Controller - External DNS & Ingress
---

## Step-01: Update Ingress manifest by adding External DNS Annotation
- Added annotation with two DNS Names
  - dnstest901.kubeoncloud.com
  - dnstest902.kubeoncloud.com
- Once we deploy the application, we should be able to access our Applications with both DNS Names.   
- **File Name:** 04-ALB-Ingress-SSL-Redirect-ExternalDNS.yml
```yaml
    # External DNS - For creating a Record Set in Route53
    external-dns.alpha.kubernetes.io/hostname: dnstest901.stacksimplify.com, dnstest902.stacksimplify.com
```
- In your case it is going to be, replace `yourdomain` with your domain name
  - dnstest901.yourdoamin.com
  - dnstest902.yourdoamin.com

## Step-02: Deploy all Application Kubernetes Manifests
### Deploy
```t
# Deploy kube-manifests
kubectl apply -f kube-manifests/

# Verify Ingress Resource
kubectl get ingress

# Verify Apps
kubectl get deploy
kubectl get pods

# Verify NodePort Services
kubectl get svc
```
### Verify Load Balancer & Target Groups
- Load Balancer -  Listeneres (Verify both 80 & 443) 
- Load Balancer - Rules (Verify both 80 & 443 listeners) 
- Target Groups - Group Details (Verify Health check path)
- Target Groups - Targets (Verify all 3 targets are healthy)

### Verify External DNS Log
```t
# Verify External DNS logs
kubectl logs -f $(kubectl get po | egrep -o 'external-dns[A-Za-z0-9-]+')
```
### Verify Route53
- Go to Services -> Route53
- You should see **Record Sets** added for `dnstest901.stacksimplify.com`, `dnstest902.stacksimplify.com`

## Step-04: Access Application using newly registered DNS Name
### Perform nslookup tests before accessing Application
- Test if our new DNS entries registered and resolving to an IP Address
```t
# nslookup commands
nslookup dnstest901.stacksimplify.com
nslookup dnstest902.stacksimplify.com
```
### Access Application using dnstest1 domain
```t
# HTTP URLs (Should Redirect to HTTPS)
http://dnstest901.stacksimplify.com/app1/index.html
http://dnstest901.stacksimplify.com/app2/index.html
http://dnstest901.stacksimplify.com/
```

### Access Application using dnstest2 domain
```t
# HTTP URLs (Should Redirect to HTTPS)
http://dnstest902.stacksimplify.com/app1/index.html
http://dnstest902.stacksimplify.com/app2/index.html
http://dnstest902.stacksimplify.com/
```


## Step-05: Clean Up
```t
# Delete Manifests
kubectl delete -f kube-manifests/

## Verify Route53 Record Set to ensure our DNS records got deleted
- Go to Route53 -> Hosted Zones -> Records 
- The below records should be deleted automatically
  - dnstest901.stacksimplify.com
  - dnstest902.stacksimplify.com
```


## References
- https://github.com/kubernetes-sigs/external-dns/blob/master/docs/tutorials/alb-ingress.md
- https://github.com/kubernetes-sigs/external-dns/blob/master/docs/tutorials/aws.md


