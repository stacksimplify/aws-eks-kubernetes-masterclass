# Spring Boot Docker Build Commands

## Step-01: Docker Build
```t
# Change Directory
cd 03-notifications-service
mvn clean
mvn install

# Sample
docker build --build-arg JAR_FILE=target/*.jar -t myorg/myapp .

# 1.0.0
#1. Update pom.xml version to 1.0.0
#2. mvn clean, install
docker build --build-arg JAR_FILE=target/*.jar -t stacksimplify/kube-notifications-microservice:1.0.0 .
docker push stacksimplify/kube-notifications-microservice:1.0.0

# 2.0.0 
#1. Update Notification Contoller Java to V2, 
#2. Update pom.xml version to 2.0.0
#3. mvn clean, install
docker build --build-arg JAR_FILE=target/*.jar -t stacksimplify/
kube-notifications-microservice:2.0.0 .
docker push stacksimplify/kube-notifications-microservice:2.0.0

# 3.0.0-AWS-XRay 
#1. Update Notification Contoller Java to V3, 
#2. Update pom.xml version to 3.0.0-AWS-XRay
#3. mvn clean, install
docker build --build-arg JAR_FILE=target/*.jar -t stacksimplify/
kube-notifications-microservice:3.0.0-AWS-XRay  .
docker push stacksimplify/kube-notifications-microservice:3.0.0-AWS-XRay 

```