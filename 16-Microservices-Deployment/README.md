# Microservices Deployment on Kubernetes

## Step-01: What are we going to learn in this section?
- We are going to deploy two microservices.
    - User Management Service
    - Notification Service

### Usecase Description
- User Management **Create User API**  will call Notification service **Send Notification API** to send an email to user when we create a user. 

### Architecture Diagram about our Buildout
-  For introduction slides refer the [presentation slides](/presentations/AWS-Fargate-and-EKS-Masterclass.pdf). 

### List of Docker Images used in this section
| Application Name                 | Docker Image Name                          |
| ------------------------------- | --------------------------------------------- |
| User Management Microservice | stacksimplify/kube-usermanagement-microservice:1.0.0 |
| Notifications Microservice | stacksimplify/kube-notifications-microservice:1.0.0 |

## Step-02: Pre-requisite -1: Create AWS RDS Database
- We have created AWS RDS Database as part of section [07-EKS-Storage-with-RDS-Database](/07-EKS-Storage-with-RDS-Database/README.md)
- We even created a `externalName service: 01-MySQL-externalName-Service.yml` in our Kubernetes manifests to point to that RDS Database. 

## Step-03: Pre-requisite-2: Create Simple Email Service - SES SMTP Credentials
### SMTP Credentials
- Go to Services -> Simple Email Service
- SMTP Settings --> Create My SMTP Credentials
- **IAM User Name:** append the default generated name with microservice or something so we have a reference of this IAM user created for our ECS Microservice deployment
- Download the credentials and update the same for below environment variables which you are going to provide in kubernetes manifest `04-NotificationMicroservice-Deployment.yml`
```
AWS_MAIL_SERVER_HOST=email-smtp.us-east-1.amazonaws.com
AWS_MAIL_SERVER_USERNAME=
AWS_MAIL_SERVER_PASSWORD=
AWS_MAIL_SERVER_FROM_ADDRESS= use-a-valid-email@gmail.com 
```
- **Important Note:** Environment variable AWS_MAIL_SERVER_FROM_ADDRESS value should be a **valid** email address and also verified in SES. 

### Verfiy Email Addresses to which notifications we need to send.
- We need two email addresses for testing Notification Service.  
-  **Email Addresses**
    - Verify a New Email Address
    - Email Address Verification Request will be sent to that address, click on link to verify your email. 
    - From Address: stacksimplify@gmail.com (replace with your ids during verification)
    - To Address: dkalyanreddy@gmail.com (replace with your ids during verification)
- **Important Note:** We need to ensure all the emails (FromAddress email) and (ToAddress emails) to be verified here. 
    - Reference Link: https://docs.aws.amazon.com/ses/latest/DeveloperGuide/verify-email-addresses.html    
- Environment Variables
    - AWS_MAIL_SERVER_HOST=email-smtp.us-east-1.amazonaws.com
    - AWS_MAIL_SERVER_USERNAME=*****
    - AWS_MAIL_SERVER_PASSWORD=*****
    - AWS_MAIL_SERVER_FROM_ADDRESS=stacksimplify@gmail.com


## Step-04: Create Notification Microservice Deployment Manifest
- Update environment Variables for Notification Microservice
```yml
          - name: AWS_MAIL_SERVER_HOST
            value: "smtp-service"
          - name: AWS_MAIL_SERVER_USERNAME
            value: "AKIAV7WTN3CFUBKLDOAX"
          - name: AWS_MAIL_SERVER_PASSWORD
            value: "BBLJ8fpyf89AHLmAH+B4oLo7kMgmKZqhJtEipuE5unLx"
          - name: AWS_MAIL_SERVER_FROM_ADDRESS
            value: "kalyanreddyd@gmail.com"
```
- **Notification Microservice Deployment**
```yml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: notification-microservice
  labels:
    app: notification-restapp
spec:
  replicas: 1
  selector:
    matchLabels:
      app: notification-restapp
  template:
    metadata:
      labels:
        app: notification-restapp
    spec:
      containers:
      - name: notification-service
        image: stacksimplify/kube-notifications-microservice:1.0.0
        ports:
        - containerPort: 8096
        env:
          - name: AWS_MAIL_SERVER_HOST
            value: "smtp-service"
          - name: AWS_MAIL_SERVER_USERNAME
            value: "AKIAV7WTN3CFUBKLDOAX"
          - name: AWS_MAIL_SERVER_PASSWORD
            value: "BBLJ8fpyf89AHLmAH+B4oLo7kMgmKZqhJtEipuE5unLx"
          - name: AWS_MAIL_SERVER_FROM_ADDRESS
            value: "kalyanreddyd@gmail.com"
```

## Step-05: Create Notification Microservice SMTP ExternalName Service
```yml
apiVersion: v1
kind: Service
metadata:
  name: smtp-service
spec:
  type: ExternalName
  externalName: email-smtp.us-east-1.amazonaws.com
```

## Step-06: Create Notification Microservice NodePort Service
```yml
apiVersion: v1
kind: Service
metadata:
  name: notification-clusterip-service
  labels:
    app: notification-restapp
spec:
  type: ClusterIP
  selector:
    app: notification-restapp
  ports:
  - port: 8096
    targetPort: 8096
```
## Step-07: Update User Management Microservice Deployment Manifest with Notification Service Environment Variables. 
- User Management Service new environment varibales related to Notification Microservice in addition to already which were configured related to MySQL
```yml
          - name: NOTIFICATION_SERVICE_HOST
            value: "notification-clusterip-service"
          - name: NOTIFICATION_SERVICE_PORT
            value: "8096"    
```
## Step-08: Clean-Up ALB Ingress Service 
- Clean-up Ingress Service to ensure only target it is going to have is User Management Service
- Remove /app1, /app2 contexts
```yml
# Annotations Reference:  https://kubernetes-sigs.github.io/aws-alb-ingress-controller/guide/ingress/annotation/
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  name: ingress-usermgmt-restapp-service
  labels:
    app: usermgmt-restapp
  annotations:
    # Ingress Core Settings  
    kubernetes.io/ingress.class: "alb"
    alb.ingress.kubernetes.io/scheme: internet-facing
    # Health Check Settings
    alb.ingress.kubernetes.io/healthcheck-protocol: HTTP 
    alb.ingress.kubernetes.io/healthcheck-port: traffic-port
    #Important Note:  Need to add health check path annotations in service level if we are planning to use multiple targets in a load balancer    
    #alb.ingress.kubernetes.io/healthcheck-path: /usermgmt/health-status
    alb.ingress.kubernetes.io/healthcheck-interval-seconds: '15'
    alb.ingress.kubernetes.io/healthcheck-timeout-seconds: '5'
    alb.ingress.kubernetes.io/success-codes: '200'
    alb.ingress.kubernetes.io/healthy-threshold-count: '2'
    alb.ingress.kubernetes.io/unhealthy-threshold-count: '2'
    # SSL Settings
    alb.ingress.kubernetes.io/listen-ports: '[{"HTTPS":443}, {"HTTP":80}]'
    alb.ingress.kubernetes.io/certificate-arn: arn:aws:acm:us-east-1:411686525067:certificate/8adf7812-a1af-4eae-af1b-ea425a238a67
    #alb.ingress.kubernetes.io/ssl-policy: ELBSecurityPolicy-TLS-1-1-2017-01 #Optional (Picks default if not used)    
    # SSL Redirect Setting
    alb.ingress.kubernetes.io/actions.ssl-redirect: '{"Type": "redirect", "RedirectConfig": { "Protocol": "HTTPS", "Port": "443", "StatusCode": "HTTP_301"}}'   
    # External DNS - For creating a Record Set in Route53
    external-dns.alpha.kubernetes.io/hostname: services.zetaoptdemo.com, restapi.zetaoptdemo.com    
spec:
  rules:
    #- host: kubedemo.stacksimplify.com    # SSL Setting (Optional only if we are not using certificate-arn annotation)
    - http:
        paths:
          - path: /* # SSL Redirect Setting
            backend:
              serviceName: ssl-redirect
              servicePort: use-annotation                   
          - path: /*
            backend:
              serviceName: usermgmt-restapp-nodeport-service
              servicePort: 8095              
# Important Note-1: In path based routing order is very important, if we are going to use  "/*", try to use it at the end of all rules.         
```

## Step-09: Deploy Microservices manifests
```
# Deploy Microservices manifests
kubectl apply -f V1-Microservices/
```

## Step-10: Verify the Deployment using kubectl
```
# List Pods
kubectl get pods

# User Management Microservice Logs
kubectl logs -f $(kubectl get po | egrep -o 'usermgmt-microservice-[A-Za-z0-9-]+')

# Notification Microservice Logs
kubectl logs -f $(kubectl get po | egrep -o 'notification-microservice-[A-Za-z0-9-]+')

# External DNS Logs
kubectl logs -f $(kubectl get po | egrep -o 'external-dns-[A-Za-z0-9-]+')

# List Ingress
kubectl get ingress
```

## Step-11: Verify Microservices via browser
```
# User Management Service Health-Status
https://services.stacksimplify.com/usermgmt/health-status

# Notification Microservice Health-Status via User Management
https://services.stacksimplify.com/usermgmt/notification-health-status
https://services.stacksimplify.com/usermgmt/notification-service-info
```

## Step-12: Import postman project to Postman client on our desktop. 
- Import postman project
- Add environment url 
    - https://services.stacksimplify.com (**Replace with your ALB DNS registered url on your environment**)

## Step-13: Test both Microservices using Postman
### User Management Service
- **Create User**
    - Verify the email id to confirm account creation email received.
- **List User**   
    - Verify if newly created user got listed. 

## Step-14: Clean-up
```
kubectl delete -f V1-Microservices/    
```

## Drawbacks of this setup
- User management service calling notification service via internet using ALB.
- Both services present in same VPC, same network and sitting next to each other and for communication going over the internet
- How to fix this?
- **Microservices - Service Discovery** concept will be the solution for the same and in our next section we will see how to implement that on **AWS Fargate and ECS**. 