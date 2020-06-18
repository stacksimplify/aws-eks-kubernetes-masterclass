# Kubernetes Storage -  Storage Classes, Persistent Volume Claims


## Step-01: Introduction
| Kubernetes Object  | YAML File |
| ------------- | ------------- |
| Storage Class  | 01-storage-class.yml |
| Persistent Volume Claim | 02-persistent-volume-claim.yml   |
| User Management Config Map  | 03-UserManagement-ConfigMap.yml  |
| MySQL Deployment  | 04-mysql-deployment.yml  |
| MySQL ClusterIp  | 05-mysql-clusterip-service.yml  |
| User Management Microservice Deployment  | 06-UserManagementMicroservice-Deployment.yml  |
| User Management NodePort Service  | 07-UserManagement-Service.yml  |

## Step-02: Create Storage Class and Persistent Volume Claim
```
# Create EBS Storage Class
kubectl apply -f kube-manifests/V1/01-storage-class.yml
kubectl get sc

# Create EBS Persistent Volume Claim
kubectl apply -f kube-manifests/V1/02-persistent-volume-claim.yml 
kubectl get pvc 
```
- **Dynamic Volume Provisioning:** https://kubernetes.io/docs/concepts/storage/dynamic-provisioning/
## Step-03: Create ConfigMap for User Management Service 
```
kubectl apply -f kube-manifests/V1/03-UserManagement-ConfigMap.yml
```
## Step-04: Create MySQL Deployment & Service
```
kubectl apply -f kube-manifests/V1/04-mysql-deployment.yml
kubectl apply -f kube-manifests/V1/05-mysql-clusterip-service.yml
kubectl get pods -l app=mysql
kubectl run -it --rm --image=mysql:5.6 --restart=Never mysql-client -- mysql -h mysql -ppassword
```

## Step-05: Create User Management Deployment & Service
- **Environment Variables of User Management Microservice**
| First Header  | Second Header |
| ------------- | ------------- |
| DB_HOSTNAME  | mysql |
| DB_PORT  | 3306  |
| DB_NAME  | usermgmt  |
| DB_USERNAME  | root  |
| DB_PASSWORD | dbpassword11  |

```
kubectl apply -f kube-manifests/V1/06-UserManagementMicroservice-Deployment-Service.yml
kubectl apply -f kube-manifests/V1/07-UserManagement-Service.yml
```
- **Access Application**
```
http://<EKS-WorkerNode-Public-IP>:31231/usermgmt/health-status
```



- Recreate the Application
```
kubectl apply -f kube-manifests/V5-Resizing-EBS/
```


## References:
- https://github.com/kubernetes-sigs/aws-ebs-csi-driver/tree/master/deploy/kubernetes/overlays/stable
- https://docs.aws.amazon.com/eks/latest/userguide/ebs-csi.html
- https://github.com/kubernetes-sigs/aws-ebs-csi-driver
- https://github.com/kubernetes-sigs/aws-ebs-csi-driver/tree/master/examples/kubernetes/dynamic-provisioning
- https://github.com/kubernetes-sigs/aws-ebs-csi-driver/tree/master/deploy/kubernetes/overlays/stable
- https://github.com/kubernetes-sigs/aws-ebs-csi-driver
- **Legacy:** 
  - https://kubernetes.io/docs/concepts/storage/storage-classes/#aws-ebs
  - https://docs.aws.amazon.com/eks/latest/userguide/storage-classes.html