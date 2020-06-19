# Kubernetes Storage -  Storage Classes, Persistent Volume Claims


## Step-01: Introduction
- We are going to create a MySQL Database with persistence storage using AWS EBS Volumes

| Kubernetes Object  | YAML File |
| ------------- | ------------- |
| Storage Class  | 01-storage-class.yml |
| Persistent Volume Claim | 02-persistent-volume-claim.yml   |
| Config Map  | 03-UserManagement-ConfigMap.yml  |
| Deployment, Environment Variables, Volumes, VolumeMounts  | 04-mysql-deployment.yml  |
| ClusterIP Service  | 05-mysql-clusterip-service.yml  |

## Step-02: Create following Kubernetes manifests
### Create Storage Class manifest
- https://kubernetes.io/docs/concepts/storage/storage-classes/#volume-binding-mode
- **Important Note:** `WaitForFirstConsumer` mode will delay the volume binding and provisioning  of a PersistentVolume until a Pod using the PersistentVolumeClaim is created. 

### Create Persistent Volume Claims manifest
```
# Create Storage Class & PVC
kubectl apply -f kube-manifests/

# List Storage Classes
kubectl get sc

# List PVC
kubectl get pvc 

# List PV
kubectl get pv
```
### Create ConfigMap manifest
- We are going to create a `usermgt` database schema during the mysql pod creation time. 

### Create MySQL Deployment manifest
- Environment Variables
- Volumes
- Volume Mounts

### Create MySQL ClusterIP Service manifest
- At any point of time we are going to have only one mysql pod in this design so `ClusterIP: none` will use the `Pod IP Address` instead of creating or allocating a separate IP for MySQL Cluster IP service.   

## Step-03: Create MySQL Database with all above manifests
```
# Create MySQL Database
kubectl apply -f kube-manifests/

# List Storage Classes
kubectl get sc

# List PVC
kubectl get pvc 

# List PV
kubectl get pv

# List pods
kubectl get pods 

# List pods based on  label name
kubectl get pods -l app=mysql
```

## Step-04: Connect to MySQL Database
```
# Connect to MYSQL Database
kubectl run -it --rm --image=mysql:5.6 --restart=Never mysql-client -- mysql -h mysql -ppassword

# Verify usermgmt schema got created which we provided in ConfigMap
mysql> show schemas;
```

## References:
- **Examples:** https://github.com/kubernetes-sigs/aws-ebs-csi-driver/tree/master/examples/kubernetes/dynamic-provisioning
- **EBS CSI Driver Dynamic Provisioning:**  https://github.com/kubernetes-sigs/aws-ebs-csi-driver/tree/master/examples/kubernetes/dynamic-provisioning
- **EBS CSI Driver - Other Examples like Resizing, Snapshot etc:** https://github.com/kubernetes-sigs/aws-ebs-csi-driver/tree/master/examples/kubernetes



