# Learn ALB Ingress Controller - Path Based Routing

## Step-01: Create Nginx App1 Deployment & Service
- **05-Nginx-App1-Deployment-and-NodePortService.yml**
```yml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app1-nginx-deployment
  labels:
    app: app1-nginx
spec:
  replicas: 1
  selector:
    matchLabels:
      app: app1-nginx
  template:
    metadata:
      labels:
        app: app1-nginx
    spec:
      containers:
      - name: app1-nginx
        image: stacksimplify/kube-nginxapp1:1.0.0
        ports:
        - containerPort: 80
---
apiVersion: v1
kind: Service
metadata:
  name: app1-nginx-service
  labels:
    app: app1-nginx
  annotations:
#Important Note:  Need to add health check path annotations in service level if we are planning to use multiple targets in a load balancer    
    alb.ingress.kubernetes.io/healthcheck-path: /app1/index.html
spec:
  type: NodePort
  selector:
    app: app1-nginx
  ports:
  - port: 80
    targetPort: 80
```
## Step-02: Create Nginx App1 Deployment & Service
- **06-Nginx-App2-Deployment-and-NodePortService copy.yml**
```yml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app2-nginx-deployment
  labels:
    app: app2-nginx 
spec:
  replicas: 1
  selector:
    matchLabels:
      app: app2-nginx
  template:
    metadata:
      labels:
        app: app2-nginx
    spec:
      containers:
      - name: app2-nginx
        image: stacksimplify/kube-nginxapp2:1.0.0
        ports:
        - containerPort: 80
---
apiVersion: v1
kind: Service
metadata:
  name: app2-nginx-service
  labels:
    app: app2-nginx
  annotations:
#Important Note:  Need to add health check path annotations in service level if we are planning to use multiple targets in a load balancer
    alb.ingress.kubernetes.io/healthcheck-path: /app2/index.html
spec:
  type: NodePort
  selector:
    app: app2-nginx
  ports:
  - port: 80
    targetPort: 80   
```
## Step-03: Update Health Check Path Annotation in User Management Node Port Service
- Health check path annotation should be moved to respective node port services if we have to route to multiple targets using single load balancer.
- **04-UserManagement-NodePort-Service.yml**
```yml
apiVersion: v1
kind: Service
metadata:
  name: usermgmt-restapp-nodeport-service
  labels:
    app: usermgmt-restapp
  annotations:
#Important Note:  Need to add health check path annotations in service level if we are planning to use multiple targets in a load balancer  
    alb.ingress.kubernetes.io/healthcheck-path: /usermgmt/health-status
spec:
  type: NodePort
  selector:
    app: usermgmt-restapp
  ports:
  - port: 8095
    targetPort: 8095
```

## Step-04: Create ALB Ingress Context path based Routing Kubernetes manifest
- **07-ALB-Ingress-ContextPath-Based-Routing.yml**
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
#Important Note:  Need to add health check path annotations in service level if we are planning to use multiple targets in a load balancer    
    #alb.ingress.kubernetes.io/healthcheck-path: /usermgmt/health-status
    alb.ingress.kubernetes.io/healthcheck-interval-seconds: '15'
    alb.ingress.kubernetes.io/healthcheck-timeout-seconds: '5'
    alb.ingress.kubernetes.io/success-codes: '200'
    alb.ingress.kubernetes.io/healthy-threshold-count: '2'
    alb.ingress.kubernetes.io/unhealthy-threshold-count: '2'
spec:
  rules:
    - http:
        paths:
          - path: /app1/*
            backend:
              serviceName: app1-nginx-service
              servicePort: 80                        
          - path: /app2/*
            backend:
              serviceName: app2-nginx-service
              servicePort: 80            
          - path: /*
            backend:
              serviceName: usermgmt-restapp-nodeport-service
              servicePort: 8095              
# Important Note-1: In path based routing order is very important, if we are going to use  "/*", try to use it at the end of all rules.                  
```

## Step-05: Deploy all manifests and test
- **Deploy**
```
kubectl apply -f V2-ALB-Ingress-ContextPath-Based-Routing/
```
- **Verify**
    - Load Balancer - Rules
    - Target Groups - Group Details (Verify Health check path)
    - Target Groups - Targets (Verify all 3 targets are healthy)
- **Access Application**
```
http://<ALB-DNS-URL>/app1
http://<ALB-DNS-URL>/app2
http://<ALB-DNS-URL>/usermgmt/health-status
```
