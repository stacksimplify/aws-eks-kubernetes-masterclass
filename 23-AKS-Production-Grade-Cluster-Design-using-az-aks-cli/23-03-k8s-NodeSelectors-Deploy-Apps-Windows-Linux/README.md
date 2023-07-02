# Deploy Apps to Azure AKS Linux, Windows and Virtual Node Pools

## Step-01: Introduction
- Understand Kubernetes Node Selector concept
- Deploy Apps to different nodepools based on Node Selectors

## Step-02: Review Kubernetes Manifests

### 01-Webserver-Apps: Schedule on System NodePool
- Review kubernetes manifests from **kube-manifests/01-Webserver-Apps**
```yaml
# To schedule pods on based on NodeSelectors
      nodeSelector:
        app: system-apps
```

### 02-Java-Apps: Schedule on Linux101 NodePool
- Review kubernetes manifests from **kube-manifests/02-Java-Apps**
```yaml
# To schedule pods on based on NodeSelectors
      nodeSelector:
        app: java-apps            
```
### 03-Windows-DotNet-Apps: Schedule on Win101 NodePool
```yaml
# To schedule pods on based on NodeSelectors
      nodeSelector:
        #"beta.kubernetes.io/os": windows
        app: dotnet-apps
```
### 04-VirtualNode-Apps : Schedule on Virtual Nodes (Serverless)
```yaml
# To schedule pods on Azure Virtual Nodes            
      nodeSelector:
        kubernetes.io/role: agent
        beta.kubernetes.io/os: linux
        type: virtual-kubelet
      tolerations:
      - key: virtual-kubelet.io/provider
        operator: Exists
      - key: azure.com/aci
        effect: NoSchedule   
```

## Step-03: Deploy Apps based on NodeSelectors and Verify
```
# Deploy Apps
kubectl apply -R -f kube-manifests/

# List Pods
kubectl get pods -o wide
Note-1: Review the Node section in the output to understand on which node each pod is scheduled
Note-2: Windows app tool 12 minutes to download the image and start (sometimes).

# List Pods with Node Name where it scheduled
kubectl get pod -o=custom-columns=NODE-NAME:.spec.nodeName,POD-NAME:.metadata.name 
```

## Step-04: Access Applications
```
# List Services to get Public IP for each service we deployed 
kubectl get svc

# Access Webserver App (Running on System Nodepool)
http://<public-ip-of-webserver-app>/app1/index.html

# Access Java-App (Running on linux101 nodepool)
http://<public-ip-of-java-app>
Username: admin101
Password: password101

# Access Windows App (Running on win101 nodepool)
http://<public-ip-of-windows-app>

# Access App deployed on Virtual Nodes (Running on ACI Virtual Nodes)
http://<public-ip-of-webserver-app>
```

## Step-05: Clean-Up
```
# Delete Apps
kubectl delete -R -f kube-manifests/

# Delete Resource Group to delete all NodePools and Cluster
az group delete -n ${AKS_RESOURCE_GROUP}

# Delete Users and Groups in AD
Group: aksadmins
User: aksadmin1@stacksimplifygmail.onmicrosoft.com
```

