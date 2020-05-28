# Containers for demonstrating Load Balancers Context path based Routing

## Step-01: Build two container images with their context paths as /app1 and /app2.
- nginxapp1 - /app1
- nginxapp2 - /app2
```
# Build Docker Image for App1
cd kube-nginxapp1
docker build -t stacksimplify/kube-nginxapp1:1.0.0 .
docker build -t <replace-with-your-docker-hub-id>/kube-nginxapp1:1.0.0 .

# Build Docker Image for App2
cd ../kube-nginxapp2
docker build -t stacksimplify/kube-nginxapp2:1.0.0 .
docker build -t <replace-with-your-docker-hub-id>/kube-nginxapp2:1.0.0 .
```    
## Step-02: Run the docker images and test those containers locally  
- **App1:** http://localhost:81/app1
- **App2:** http://localhost:82/app2
```
# Run on local docker environment and test
docker run --name kubenginxapp1 -p 81:80 --rm -d stacksimplify/kube-nginxapp1:1.0.0
docker run --name kubenginxapp2 -p 82:80 --rm -d stacksimplify/kube-nginxapp2:1.0.0

# Replace with your docker hub id before running locally (as you built images with your docker hub id)
docker run --name kubenginxapp1 -p 81:80 --rm -d <replace-with-your-docker-hub-id>/kubenginxapp1:1.0.0
docker run --name kubenginxapp2 -p 82:80 --rm -d <replace-with-your-docker-hub-id>/kubenginxapp2:1.0.0
```
## Step-03: Stop the docker containers
```
docker ps
docker stop kubenginxapp1
docker stop kubenginxapp2
docker ps -a
```    
## Step-04: Push these two containers to your Docker Hub Repository
```
# Push Docker Images to Docker Hub
docker images
docker push stacksimplify/kube-nginxapp1:1.0.0
docker push stacksimplify/kube-nginxapp2:1.0.0

# Replace with your Docker Hub Id
docker push <replace-with-your-docker-hub-id>/kube-nginxapp1:1.0.0
docker push <replace-with-your-docker-hub-id>/kube-nginxapp2:1.0.0
```
