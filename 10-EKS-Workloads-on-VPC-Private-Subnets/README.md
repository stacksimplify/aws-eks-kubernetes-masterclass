# Deploy Workloads to VPC Private Subnets 

## Step-01: Introduction
- We are going to create a node group in VPC Private Subnets
- We are going to deploy workloads on the private node group wherein workloads will be private subnets and load balancer gets created in public subnet and accessible via internet.


## Step-02: Create Node Group in Private Subnets
- Create Private Node Group in a Cluster
```
# Create Private Node Group   
eksctl create nodegroup --cluster=eksdemo1 \
                        --region=us-east-1 \
                        --name=eksdemo1-ng1-private \
                        --node-type=t3.medium \
                        --nodes-min=2 \
                        --nodes-max=4 \
                        --node-volume-size=20 \
                        --ssh-access \
                        --ssh-public-key=kube-demo-2020 \
                        --managed \
                        --asg-access \
                        --external-dns-access \
                        --full-ecr-access \
                        --appmesh-access \
                        --alb-ingress-access \
                        --node-private-networking 
```
- Verify the node group subnet routes to ensure it created in private subnets
  - Go to Services -> EKS -> eksdemo -> eksdemo1-ng1-private
  - Click on Associated subnet in **Details** tab
  - Click on **Route Table** Tab.
  - We should see that internet route via NAT Gateway (0.0.0.0/0 -> nat-xxxxxxxx)

## Step-03: Verify our exisitng workloads running on new private node group
- external-dns: deployed to default namespace
- alb-ingress-controller: deployed to kube-system namespace
```
# For external-dns
kubectl get pods 

# For alb-ingress-controller
kubectl get pods -n kube-system
```

## Step-04: Deploy the same application which we deployed in 09-06
### Deploy
```
kubectl apply -f V1-ALB-Ingress-ExternalDNS-Private-Subnets/
```

### Verify Ingress - ALB Created  (ADDRESS field should have DNS Name of ALB)
```
kubectl get ingress
```

### Verify Route53
- Go to Services -> Route53
- You should see **Record Sets** added for `dnstest1.stacksimplify.com`, `dnstest2.stacksimplify.com`

## Step-05: Access Application using newly registered DNS Name
- In my case `yourdomain.com` will be `stacksimplify.com`
### Perform nslookup tests before accessing Application
- Test if our new DNS entries registered and resolving to an IP Address
```
# nslookup commands
nslookup dnstest1.stacksimplify.com
nslookup dnstest2.stacksimplify.com

# Sample nslookup output
Kalyans-MacBook-Pro:kube-manifests kdaida$ nslookup dnstest1.stacksimplify.com
Server:		192.168.0.1
Address:	192.168.0.1#53

Non-authoritative answer:
Name:	dnstest1.stacksimplify.com
Address: 18.208.91.193
Name:	dnstest1.stacksimplify.com
Address: 3.213.245.252

Kalyans-MacBook-Pro:kube-manifests kdaida$ nslookup dnstest2.stacksimplify.com
Server:		192.168.0.1
Address:	192.168.0.1#53

Non-authoritative answer:
Name:	dnstest2.stacksimplify.com
Address: 18.208.91.193
Name:	dnstest2.stacksimplify.com
Address: 3.213.245.252

Kalyans-MacBook-Pro:kube-manifests kdaida$ 
```
### Access Application using dnstest1 domain
```
# HTTP URLs (Should Redirect to HTTPS)
http://dnstest1.yourdoamin.com/app1/
http://dnstest1.yourdomain.com/app2/
http://dnstest1.yourdomain.com/usermgmt/health-status

# HTTPS URLs
https://dnstest1.yourdoamin.com/app1/
https://dnstest1.yourdoamin.com/app2/
https://dnstest1.yourdoamin.com/usermgmt/health-status
```

### Access Application using dnstest2 domain
```
# HTTP URLs (Should Redirect to HTTPS)
http://dnstest2.yourdoamin.com/app1/
http://dnstest2.yourdomain.com/app2/
http://dnstest2.yourdomain.com/usermgmt/health-status

# HTTPS URLs
https://dnstest2.yourdoamin.com/app1/
https://dnstest2.yourdoamin.com/app2/
https://dnstest2.yourdoamin.com/usermgmt/health-status
```


## Step-06: Clean Up
```
kubectl delete -f V1-ALB-Ingress-ExternalDNS-Private-Subnets/
```

## Step-07: Delete the Private Node Group in EKS Cluster
```
# Template
eksctl delete nodegroup <NodeGroup-Name> --cluster <Cluster-Name>

# Replace nodegroup name and cluster name
eksctl delete nodegroup eksdemo1-ng1-private --cluster eksdemo1
```
