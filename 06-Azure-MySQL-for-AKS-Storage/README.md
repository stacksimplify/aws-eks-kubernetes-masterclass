# Use Azure Database for MySQL for AKS Workloads

## Step-01: Introduction
- What are the problems with MySQL Pod & Azure Disks? 
- How we are going to solve them using Azure MySQL Database?

## Step-02: Create Azure Database for MySQL servers
- Go to Service **Azure Database for MySQL servers**
- Click on **Add**
- **Basics**
- **Project details**
  - Subscription: Free Trial
  - Resource Group: aks-rg1
- **Server Details**
  - Server name: akswebappdb (This name is based on availability - in your case it might be something else)
  - Data source: none
  - Location: (US) East US
  - Version: 5.7 (default)
  - **Compute + Storage**
    - Pricing Tier: Basic
    - VCore: 1
    - Storage: 5GB
    - Storage Auto Growth: Yes
    - Backup Retention: 7 days
    - Locally Redundant: Yes
- **Administrative Account**      
  - Admin username: dbadmin
  - Password: Redhat1449
  - Confirm password: Redhat1449
- **Review + Create**  
- It will take close to 15 minutes to create the database. 

## Step-03: Update Security Settings for Database
- Go to **Azure Database for MySQL Servers** -> **akswebappdb**
- **Settings -> Connection Security**
  - **Very Important**: Enable **Allow Access to Azure Services**
  - Update Firewall rules to allow from local desktop (Add current client IP Address)
  - **SSL Settings**: Disabled  
  - Click on **Save**
- It will take close to 15 minutes for changes to take place. 

```
# Template
mysql --host=mydemoserver.mysql.database.azure.com --user=myadmin@mydemoserver -p

# 
mysql --host=akswebappdb.mysql.database.azure.com --user=dbadmin@akswebappdb -p
```

## Step-04: Create Kubernetes externalName service Manifest and Deploy
- Create mysql externalName Service
- **01-MySQL-externalName-Service.yml**
```yml
apiVersion: v1
kind: Service
metadata:
  name: mysql
spec:
  type: ExternalName
  externalName: akswebappdb.mysql.database.azure.com
```
 - **Deploy Manifest**
```
kubectl apply -f kube-manifests/01-MySQL-externalName-Service.yml
```
## Step-04:  Connect to RDS Database using kubectl and create usermgmt schema/db
```
# Template
kubectl run -it --rm --image=mysql:5.7.22 --restart=Never mysql-client -- mysql -h <AZURE-MYSQ-DB-HOSTNAME> -u <USER_NAME> -p<PASSWORD>

# Replace Host Name of Azure MySQL Database and Username and Password
kubectl run -it --rm --image=mysql:5.7.22 --restart=Never mysql-client -- mysql -h akswebappdb.mysql.database.azure.com -u dbadmin@akswebappdb -pRedhat1449

mysql> show schemas;
mysql> create database webappdb;
mysql> show schemas;
mysql> exit
```
## Step-05: In User Management WebApp deployment file change username from `root` to `dbadmin@akswebappdb`
- **02-UserMgmtWebApp-Deployment.yml**
```yml
# Change From
          - name: DB_USERNAME
            value: "root"
          - name: DB_PASSWORD
            value: "dbpassword11"               

# Change To dbadmin@<YOUR-Azure-MYSQL-DB-NAME>
            - name: DB_USERNAME
              value: "dbadmin@akswebappdb"            
            - name: DB_PASSWORD
              value: "Redhat1449"                  
             
```

## Step-06: Deploy User Management WebApp and Test
```
# Deploy all Manifests
kubectl apply -f kube-manifests/

# List Pods
kubectl get pods

# Stream pod logs to verify DB Connection is successful from SpringBoot Application
kubectl logs -f <pod-name>
```
## Step-07: Access Application
```
# Get Public IP
kubectl get svc

# Access Application
http://<External-IP-from-get-service-output>
Username: admin101
Password: password101
```

## Step-08: Clean Up 
```
# Delete all Objects created
kubectl delete -f kube-manifests/

# Verify current Kubernetes Objects
kubectl get all

# Delete Azure MySQL Database
```
