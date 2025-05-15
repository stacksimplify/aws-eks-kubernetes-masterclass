# Microservices Canary Deployments 

## Step-01: Introduction
### Usecase Description
- User Management **getNotificationAppInfo**  will call Notification service V1 and V2 versions.
- We will distribute traffic between V1 and V2 versions of Notification service as per our choice based on Replicas

| NS V1 Replicas | NS V2 Replicas | Traffic Distribution | 
| -------------- | -------------- | -------------------- |
| 4 | 0 | 100% traffic to NS V1 Version |
| 3 | 1 | 25% traffic to NS V2 Version |
| 2 | 2 | 50% traffic to NS V2 Version |
| 1 | 3 | 75% traffic to NS V2 Version |
| 0 | 4 | 100% traffic to NS V2 Version |

- In our demo, we are going to distribute 50% traffic to each version (V1 and V2). 
- NS V1 - 2 replicas and NS V2 - 2 replicas
- We are going to depict one Microservice calling other Microservices with different versions in AWS X-Ray

### List of Docker Images used in this section
| Application Name                 | Docker Image Name                          |
| ------------------------------- | --------------------------------------------- |
| User Management Microservice | stacksimplify/kube-usermanagement-microservice:3.0.0-AWS-XRay-MySQLDB |
| Notifications Microservice V1 | stacksimplify/kube-notifications-microservice:3.0.0-AWS-XRay |
| Notifications Microservice V2 | stacksimplify/kube-notifications-microservice:4.0.0-AWS-XRay |

## Step-02: Pre-requisite: AWS RDS Database, ALB Ingress Controller, External DNS & X-Ray Daemon

### AWS RDS Database
- We have created AWS RDS Database as part of section [06-EKS-Storage-with-RDS-Database](/06-EKS-Storage-with-RDS-Database/README.md)
- We even created a `externalName service: 01-MySQL-externalName-Service.yml` in our Kubernetes manifests to point to that RDS Database. 

### ALB Ingress Controller & External DNS
- We are going to deploy a application which will also have a `ALB Ingress Service` and also will register its DNS name in Route53 using `External DNS`
- Which means we should have both related pods running in our EKS cluster. 
- We have installed **ALB Ingress Controller** as part of section [08-01-ALB-Ingress-Install](/08-ELB-Application-LoadBalancers/08-01-ALB-Ingress-Install/README.md)
- We have installed **External DNS** as part of section [08-06-01-Deploy-ExternalDNS-on-EKS](/08-ELB-Application-LoadBalancers/08-06-ALB-Ingress-ExternalDNS/08-06-01-Deploy-ExternalDNS-on-EKS/README.md)

### XRay Daemon
- We are going to view the application traces in AWS X-Ray.
- We need XRay Daemon running as Daemonset for that. 
```
# Verify alb-ingress-controller pod running in namespace kube-system
kubectl get pods -n kube-system

# Verify external-dns & xray-daemon pod running in default namespace
kubectl get pods
```

## Step-03: Review Deployment Manifest for V2 Notification Service
- We are going to distribute 50% traffic to each of the V1 and V2 version of application


| NS V1 Replicas | NS V2 Replicas | Traffic Distribution | 
| -------------- | -------------- | -------------------- |
| 2 | 2 | 50% traffic to NS V2 Version |

- **08-V2-NotificationMicroservice-Deployment.yml**
```yml
# Change-1: Image Tag is 4.0.0-AWS-XRay
    spec:
      containers:
        - name: notification-service
          image: stacksimplify/kube-notifications-microservice:4.0.0-AWS-XRay

# Change-2: New Environment Variables related to AWS X-Ray
            - name: AWS_XRAY_TRACING_NAME 
              value: "V2-Notification-Microservice"              
            - name: AWS_XRAY_DAEMON_ADDRESS
              value: "xray-service.default:2000"      
            - name: AWS_XRAY_CONTEXT_MISSING 
              value: "LOG_ERROR"  # Log an error and continue, Ideally RUNTIME_ERROR – Throw a runtime exception which is default option if not configured    
```


## Step-04: Review Ingress Manifest
- **07-ALB-Ingress-SSL-Redirect-ExternalDNS.yml**
```yml
# Change-1-For-You: Update with your SSL Cert ARN when using template
    alb.ingress.kubernetes.io/certificate-arn: arn:aws:acm:us-east-1:180789647333:certificate/9f042b5d-86fd-4fad-96d0-c81c5abc71e1

# Change-2-For-You: Update with your "yourdomainname.com"
    # External DNS - For creating a Record Set in Route53
    external-dns.alpha.kubernetes.io/hostname: canarydemo.kubeoncloud.com
```

## Step-05: Deploy Manifests
```
# Deploy
kubectl apply -f kube-manifests/

# Verify
kubectl get deploy,svc,pod
```
## Step-06: Test
```
# Test
https://canarydemo.kubeoncloud.com/usermgmt/notification-xray

# Your Domain Name
https://<Replace-your-domain-name>/usermgmt/notification-xray
```

## Step-07: What is happening in the background?
- As far as `Notification Cluster IP Service` selector label matches to `Notificaiton V1 and V2 Deployment manifests selector.matchLables`  those respective pods are picked to send traffic.
```yml
# Notification Cluster IP Service - Selector Label
  selector:
    app: notification-restapp

# Notification V1 and V2 Deployment - Selector Match Labels
  selector:
    matchLabels:
      app: notification-restapp         
```

## Step-08: Clean-Up
- We are going to delete applications created as part of this section
```
# Delete Apps
kubectl delete -f kube-manifests/
```

## Step-09: Downside of this approach
- We will review the downside in a presentation

## Step-10: Best ways for Canary Deployments
- Istio (Open Source)
- AWS AppMesh (AWS version of Istio)