# Kubernetes - Namespaces

## Step-01: Introduction
- Namespaces allow to split-up resources into different groups.
- Resource names should be unique in a namespace
- We can use namespaces to create multiple environments like dev, staging and production etc
- Kubernetes will always list the resources from `default namespace` unless we provide exclusively from which namespace we need information from.

## Step-02: Namespaces Generic - Deploy in Dev1 and Dev2
### Create Namespace
```
# List Namespaces
kubectl get ns 

# Craete Namespace
kubectl create namespace <namespace-name>
kubectl create namespace dev1
kubectl create namespace dev2

# List Namespaces
kubectl get ns 
```
### Comment NodePort in UserMgmt NodePort Service
- **File: 07-UserManagement-Service.yml**
- **Why?:**
  - Whenever we create with same manifests multiple environments like dev1, dev2 with namespaces, we cannot have same worker node port for multiple services. 
  - We will have port conflict. 
  - Its good for k8s system to provide dynamic nodeport for us in such situations.
```yml
      #nodePort: 31231
```
- **Error** if not commented
```log
The Service "usermgmt-restapp-service" is invalid: spec.ports[0].nodePort: Invalid value: 31231: provided port is already allocated
```
### Deploy All k8s Objects
```
# Deploy All k8s Objects
kubectl apply -f kube-manifests/01-generic/ -n dev1
kubectl apply -f kube-manifests/01-generic/ -n dev2

# List all objects from dev1 & dev2 Namespaces
kubectl get all -n dev1
kubectl get all -n dev2
```
## Step-03: Verify SC,PVC and PV
- **Shorter Note**
  - PVC is a namespace specific resource
  - PV and SC are generic
- **Observation-1:** `Persistent Volume Claim (PVC)` gets created in respective namespaces
```
# List PVC for dev1 and dev2
kubectl get pvc -n dev1
kubectl get pvc -n dev2
```
- **Observation-2:** `Storage Class (SC) and Persistent Volume (PV)` gets created generic. No specifc namespace for them   
```
# List sc,pv
kubect get sc,pv
```
## Step-04: Access Application
### Dev1 Namespace
```
# Get Public IP
kubectl get nodes -o wide

# Get NodePort for dev1 usermgmt service
kubectl get svc -n dev1

# Access Application
http://<Worker-Node-Public-Ip>:<Dev1-NodePort>/usermgmt/health-stauts
```
### Dev2 Namespace
```
# Get Public IP
kubectl get nodes -o wide

# Get NodePort for dev2 usermgmt service
kubectl get svc -n dev2

# Access Application
http://<Worker-Node-Public-Ip>:<Dev2-NodePort>/usermgmt/health-stauts
```
## Step-05: Clean-Up
```
# Delete namespaces dev1 & dev2
kubectl delete ns dev1
kubectl delete ns dev2

# List all objects from dev1 & dev2 Namespaces
kubectl get all -n dev1
kubectl get all -n dev2

# List Namespaces
kubectl get ns

# List sc,pv
kubectl get sc,pv

# Delete Storage Class
kubectl delete sc ebs-sc

# Get all from All Namespaces
kubectl get all -all-namespaces
```

## Step-06: Create Namespace manifest
- **Important Note:** Name the file name with `00-dev3-namespace.yml` sp that when creating it will get created first so it don't throw an error.
```yml
apiVersion: v1
kind: Namespace
metadata:
  name: dev3
```

## Step-07: Update all k8s manifest with namespace
- Update all files from 02 to 08 with `namespace: dev3` in top metadata section in folder `kube-manifests/02-Declarative` 
- **Example**
```yml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: ebs-mysql-pv-claim
  namespace: dev3
```

## Step-08: Create k8s objects & Test
```
# Create All Objects
kubectl apply -f kube-manifests/02-Declarative

# List Pods
kubectl get pods -n dev3

# Get NodePort
kubectl get svc -n dev3

# Access Application Health Status Page
http://<WorkerNode-Public-IP>:<NodePort>/usermgmt/health-status

```
## Step-09: Clean-Up
- Delete all k8s objects created as part of this section
```
# Delete All
kubectl delete -f kube-manifests/02-Declarative
```

## References:
- https://kubernetes.io/docs/tasks/administer-cluster/namespaces-walkthrough/