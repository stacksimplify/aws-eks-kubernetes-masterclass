# EKS Storage - Design DB Tier

## Step-00: Introduction
- Kubernetes Concepts we are introducing as part of this section
- V1 Foundation
  - Storage Classes
  - Persistent Volumes
  - Persistent Volume Claims
  - ConfigMaps
  - docker-entrypoint-initdb.d 
  - Environment Variables
- V2 Secrets  
  - Secrets
- V3 Init Containers
  - Init Containers
- V4 Probles
  - Liveness Probes
  - Readiness Probes

# Module-1: Deploy Amazon EBS CSI Driver

## Step-01:  Create IAM policyy
- Go to Services -> IAM
- Create a Policy 
  - Select JSON tab and copy paste the below JSON
```json

{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ec2:AttachVolume",
        "ec2:CreateSnapshot",
        "ec2:CreateTags",
        "ec2:CreateVolume",
        "ec2:DeleteSnapshot",
        "ec2:DeleteTags",
        "ec2:DeleteVolume",
        "ec2:DescribeInstances",
        "ec2:DescribeSnapshots",
        "ec2:DescribeTags",
        "ec2:DescribeVolumes",
        "ec2:DetachVolume"
      ],
      "Resource": "*"
    }
  ]
}
```
  - Review the same in **Visual Editor** 
  - Click on **Review Policy**
  - **Name:** Amazon_EBS_CSI_Driver
  - **Description:** Policy for EC2 Instances to access Elastic Block Store
  - Click on **Create Policy**

## Step-02: Get the IAM role Worker Nodes using and Associate this policy to that role
```
kubectl -n kube-system describe configmap aws-auth

# from output check rolearn
rolearn: arn:aws:iam::411686525067:role/my-first-eks-cluster-worker-node-role
```
- Go to Services -> IAM -> Roles 
- Search for role with name **my-first-eks-cluster-worker-node-role** and open it
- Click on **Permissions** tab
- Click on **Attach Policies**
- Search for **Amazon_EBS_CSI_Driver** and click on **Attach Policy**

## Step-03: Deploy Amazon EBS CSI Driver  
- Verify kubectl version, it should be 1.14 or later
```
kubectl version --client --short
```
- Deploy Amazon EBS CSI Driver
```
kubectl apply -k "github.com/kubernetes-sigs/aws-ebs-csi-driver/deploy/kubernetes/overlays/stable/?ref=master"
```

# Module-2: Deploy V1 version of Application 

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

## Step-06: Create User Management Deployment & Service
- **Environment Variables of User Management Microservice**
| First Header  | Second Header |
| ------------- | ------------- |
| AWS_RDS_HOSTNAME  | mysql |
| AWS_RDS_PORT  | 3306  |
| AWS_RDS_DB_NAME  | usermgmt  |
| AWS_RDS_USERNAME  | root  |
| AWS_RDS_PASSWORD | password  |

```
kubectl apply -f kube-manifests/V1/06-UserManagementMicroservice-Deployment-Service.yml
kubectl apply -f kube-manifests/V1/07-UserManagement-Service.yml
```
- **Access Application**
```
http://<EKS-WorkerNode-Public>:31231/usermgmt/health-status
```




## Step-0x: Resizing EBS Volume
- Add `allowVolumeExpansion: true` in the StorageClass spec
- **01-storage-class.yml**
```yml
kind: StorageClass
apiVersion: storage.k8s.io/v1
metadata:
  name: ebs-sc
provisioner: ebs.csi.aws.com
volumeBindingMode: WaitForFirstConsumer
allowVolumeExpansion: true
```
- Recreate the Application
```
kubectl apply -f kube-manifests/V5-Resizing-EBS/
```
- Expand the volume size by increasing the capacity in PVC's `spec.resources.requests.storage:`
```
kubectl get pvc
kubectl get pv
kubectl edit pvc ebs-mysql-pv-claim
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