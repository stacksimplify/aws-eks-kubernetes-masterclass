---
title: AWS Load Balancer Controller - External DNS & Service
description: Learn AWS Load Balancer Controller - External DNS & Kubernetes Service
---

## Step-01: Introduction
- We will create a Kubernetes Service of `type: LoadBalancer`
- We will annotate that Service with external DNS hostname `external-dns.alpha.kubernetes.io/hostname: externaldns-k8s-service-demo101.stacksimplify.com` which will register the DNS in Route53 for that respective load balancer

## Step-02: 02-Nginx-App1-LoadBalancer-Service.yml
```yaml
apiVersion: v1
kind: Service
metadata:
  name: app1-nginx-loadbalancer-service
  labels:
    app: app1-nginx
  annotations:
    external-dns.alpha.kubernetes.io/hostname: externaldns-k8s-service-demo101.stacksimplify.com
spec:
  type: LoadBalancer
  selector:
    app: app1-nginx
  ports:
    - port: 80
      targetPort: 80  
```
## Step-03: Deploy & Verify

### Deploy & Verify
```t
# Deploy kube-manifests
kubectl apply -f kube-manifests/

# Verify Apps
kubectl get deploy
kubectl get pods

# Verify Service
kubectl get svc
```
### Verify Load Balancer 
- Go to EC2 -> Load Balancers -> Verify Load Balancer Settings

### Verify External DNS Log
```t
# Verify External DNS logs
kubectl logs -f $(kubectl get po | egrep -o 'external-dns[A-Za-z0-9-]+')
```
### Verify Route53
- Go to Services -> Route53
- You should see **Record Sets** added for `externaldns-k8s-service-demo101.stacksimplify.com`


## Step-04: Access Application using newly registered DNS Name
### Perform nslookup tests before accessing Application
- Test if our new DNS entries registered and resolving to an IP Address
```t
# nslookup commands
nslookup externaldns-k8s-service-demo101.stacksimplify.com
```
### Access Application using DNS domain
```t
# HTTP URL
http://externaldns-k8s-service-demo101.stacksimplify.com/app1/index.html
```

## Step-05: Clean Up
```t
# Delete Manifests
kubectl delete -f kube-manifests/

## Verify Route53 Record Set to ensure our DNS records got deleted
- Go to Route53 -> Hosted Zones -> Records 
- The below records should be deleted automatically
  - externaldns-k8s-service-demo101.stacksimplify.com
```


## References
- https://github.com/kubernetes-sigs/external-dns/blob/master/docs/tutorials/alb-ingress.md
- https://github.com/kubernetes-sigs/external-dns/blob/master/docs/tutorials/aws.md
