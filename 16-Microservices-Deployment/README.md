# Microservices Deployment on Kubernetes

# Module - 1: Introduction & Pre-requisites
## Step-1: What are we going to learn in this section?
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

## Step-2: Pre-requisite -1: Create AWS RDS Database
- We have created AWS RDS Database as part of section [07-EKS-Storage-with-RDS-Database](/07-EKS-Storage-with-RDS-Database/README.md)
- We even created a `externalName service: 01-MySQL-externalName-Service.yml` in our Kubernetes manifests to point to that RDS Database. 

## Step-3: Pre-requisite-2: Create Simple Email Service - SES SMTP Credentials
### SMTP Credentials
- Go to Services -> Simple Email Service
- SMTP Settings --> Create My SMTP Credentials
- **IAM User Name:** append the default generated name with microservice or something so we have a reference of this IAM user created for our ECS Microservice deployment
- Download the credentials and update the same for below environment variables which you are going to provide in container definition section of Task Definition. 
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
- Verify
```
http://services.stacksimplify.com/notification/health-status
```

```
        - AWS_RDS_HOSTNAME=microservicesdb.cxojydmxwly6.us-east-1.rds.amazonaws.com
        - AWS_RDS_PORT=3306
        - AWS_RDS_DB_NAME=usermgmt
        - AWS_RDS_USERNAME=dbadmin
        - AWS_RDS_PASSWORD=*****
        - NOTIFICATION_SERVICE_HOST=services.stacksimplify.com [or] ALB DNS Name
        - NOTIFICATION_SERVICE_PORT=80
```
- Verify using Load Balancer URL or DNS registered URL
```
http://services.stacksimplify.com/usermgmt/health-status
```

# Module - 4: Test both Microservices using Postman
## Step-1: Import postman project to Postman client on our desktop. 
- Import postman project
- Add environment url 
    - http://services.stacksimplify.com (**Replace with your ALB DNS registered url on your environment**)

## Step-2: Test both Microservices using Postman
### Notification Service
- Send Notification
    - Verify you have got email to the specified email address. 
- Health Status
### User Management Service
- **Create User**
    - Verify the email id to confirm account creation email received.
- **List User**   
    - Verify if newly created user got listed. 

## Drawbacks of this setup
- User management service calling notification service via internet using ALB.
- Both services present in same VPC, same network and sitting next to each other and for communication going over the internet
- How to fix this?
- **Microservices - Service Discovery** concept will be the solution for the same and in our next section we will see how to implement that on **AWS Fargate and ECS**. 