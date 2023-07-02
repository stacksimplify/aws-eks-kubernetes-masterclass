# AKS Storage - Azure Disks

## Step-01: Introduction
- We are going to use Azure AKS provisioned storage class as part of this section

## Step-02: Use AKS Provisioned Azure Disks
- Copy all templates from previous section
- Remove Storage Class Manifest
- **Question-1:** Why do we need to remove storage class Manifests?
- Azure AKS provisions two types of storage classes well in advance during the cluster creation process
  - managed-premium
  - default-
- We can leverage Azure AKS provisioned disk storage classes instead of what we created manually.
- **Question-2:** If that is the case why did we use custom storate class in previous section?
- That is for us to learn the `kind: StorageClass` concept.  

## Step-03: Review PVC Manifest 01-persistent-volume-claim.yml
- Primarily we are going to focus on `storageClassName: managed-premium` which tells us that we are going to use Azure AKS provisioned Azure Disks storage class.
```yml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: azure-managed-disk-pvc
spec:
  accessModes:
  - ReadWriteOnce
  storageClassName: managed-premium 
  resources:
    requests:
      storage: 5Gi  
```

## Step-04: Deploy and Test
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
```

## Step-05: Connect to MySQL Database
```
# Connect to MYSQL Database
kubectl run -it --rm --image=mysql:5.6 --restart=Never mysql-client -- mysql -h mysql -pdbpassword11

# Verify usermgmt schema got created which we provided in ConfigMap
mysql> show schemas;
```

## Step-06: Clean-Up
```
# Delete all manifests
kubectl delete -f kube-manifests/
```