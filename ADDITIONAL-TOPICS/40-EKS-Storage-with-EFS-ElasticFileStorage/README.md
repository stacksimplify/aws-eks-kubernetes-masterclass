# EKS Storage with EFS - Elastic File System

## Step-00: Introduction


## Step-01: Deploy EFS CSI Driver
- Our EKS Cluster should be 1.14 or later to deploy EFS CSI Driver
```
kubectl version --client --short
kubectl apply -k "github.com/kubernetes-sigs/aws-efs-csi-driver/deploy/kubernetes/overlays/stable/?ref=master"
```

## Step-02: Craete Security Group for EFS
- Get the VPC CIDR Range for our VPC where EKS Cluster is running. 
  - **VPC CIDR Range:** 192.168.0.0/16
- Create Security Group  
- Go to Services -> EC2 -> Security Groups
- Create New Security Group
  - Security Group Name: eks-efs-nfs-access
  - Description: EFS access across VPC
  - VPC:  eks-vpc-public-VPC
  - Inbound Rule
    - Type: NFS
    - Source: 192.168.0.0/16
    - Description: Allows inbound NFS traffic from within the VPC

## Step-03: Create EFS File System
- Go to Services -> EFS
- Click on **Create file system**
- Configure Network Access
  - VPC: eks-vpc-public-VPC
  - Mount Targets: Will get autoselected, change security groups to **eks-efs-nfs-access**
- Add Tags
  - Name: my-eks-efs  
- Rest all leave to defaults and create file system  
- Make a note of file system id and DNS name
```
File System ID: fs-dc309e5f	
DNS Name: fs-dc309e5f.efs.us-east-1.amazonaws.com
```

## Step-04: Create Storage Class, Persistent Volume and Persistent Volume Claim
- Create Storage Class
- Create PV and PVC
- Update `volumeHandle:` in PV with which we make a note in previous step (File System ID or DNS Name)
```yml
  csi:
    driver: efs.csi.aws.com
    volumeHandle: fs-dc309e5f
```
- Update `04-mysql-deployment.yml` with new `efs-claim`
```yml
      volumes:
      - name: mysql-persistent-storage
        persistentVolumeClaim:
          claimName: efs-claim
```
- Deploy all templates
```
kubectl apply -f kube-manifests/V1-Foundation/
```
- **References:**
  - https://docs.aws.amazon.com/eks/latest/userguide/efs-csi.html
  - https://github.com/kubernetes-sigs/aws-efs-csi-driver/tree/master/examples/kubernetes/multiple_pods/specs

