# Learn ALB Ingress Controller - Basics

## Step-01: Introduction
- Understand about ALB Ingress Annotations. 

## Step-02: Create ALB kubernetes basic Ingress Manifest
- Create a basic ALB Ingress template. 
- **05-ALB-Ingress-Basic.yml**
```yml
# Annotations Reference:  https://kubernetes-sigs.github.io/aws-alb-ingress-controller/guide/ingress/annotation/
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  name: ingress-usermgmt-restapp-service
  labels:
    app: usermgmt-restapp
  annotations:
    kubernetes.io/ingress.class: "alb"
    alb.ingress.kubernetes.io/scheme: internet-facing
    alb.ingress.kubernetes.io/healthcheck-protocol: HTTP 
    alb.ingress.kubernetes.io/healthcheck-port: traffic-port
    alb.ingress.kubernetes.io/healthcheck-path: /usermgmt/health-status
    alb.ingress.kubernetes.io/healthcheck-interval-seconds: '15'
    alb.ingress.kubernetes.io/healthcheck-timeout-seconds: '5'
    alb.ingress.kubernetes.io/success-codes: '200'
    alb.ingress.kubernetes.io/healthy-threshold-count: '2'
    alb.ingress.kubernetes.io/unhealthy-threshold-count: '2'
spec:
  rules:
    - http:
        paths:
          - path: /*
            backend:
              serviceName: usermgmt-restapp-nodeport-service
              servicePort: 8095
```
## Step-03: Deploy Application with ALB Ingress Template included
```
# Deploy Application with ALB Template
kubectl apply -f V1-ALB-Ingress-Basic/

# Get Ingress Controller Status (Make a note of Address field)
kubectl get ingress

# Describe Ingress Controller
kubectl describe ingress ingress-usermgmt-restapp-service 
```

## Step-04: Verify the ALB in AWS Management Console & Access Application using ALB DNS URL
- Verify Load Balancer
    - Listeners Tab
- Verify Target Groups
    - GroupD Details
    - Targets: Ensure they are healthy
- Access Application
```
http://<ALB-DNS-URL>/usermgmt/health-status
```

## Step-05: Clean Up
```
kubectl delete -f V1-ALB-Ingress-Basic/
```
