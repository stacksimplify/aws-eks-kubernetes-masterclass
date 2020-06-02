# External DNS 

# Module-1: Deploy External DNS

## Step-01: Create IAM Policy
- Go to Services -> IAM -> Policies -> Create Policy
  - Click on **JSON** Tab and copy paste below JSON
  - Click on **Visual editor** tab to validate
  - Click on **Review Policy**
  - **Name:** AllowExternalDNSUpdates 
  - **Description:** Allow access to Route53 Resources for ExternalDNS
  - Click on **Create Policy**  

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "route53:ChangeResourceRecordSets"
      ],
      "Resource": [
        "arn:aws:route53:::hostedzone/*"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "route53:ListHostedZones",
        "route53:ListResourceRecordSets"
      ],
      "Resource": [
        "*"
      ]
    }
  ]
}
```
- Make a note of Policy ARN which we will use in next step
```
arn:aws:iam::411686525067:policy/AllowExternalDNSUpdates
```  


## Step-02: Create IAM Role
```
# Template
eksctl create iamserviceaccount \
    --name service_account_name \
    --namespace service_account_namespace \
    --cluster cluster_name \
    --attach-policy-arn IAM_policy_ARN \
    --approve \
    --override-existing-serviceaccounts

# Replaced name, namespace, cluster, arn 
eksctl create iamserviceaccount \
    --name external-dns \
    --namespace default \
    --cluster eksdemo1 \
    --attach-policy-arn arn:aws:iam::411686525067:policy/AllowExternalDNSUpdates \
    --approve \
    --override-existing-serviceaccounts
```
- Verify the Service Account
```
kubectl get sa external-dns
```
- Make a note of IAM Role ARN Name created in IAM
  - Go to Services -> IAM -> Roles
  - Search for `eksctl-`
  - We should find a role as listed below 
  - Also check in **Permissions** tab and you should find the policy named **AllowExternalDNSUpdates**
```
eksctl-demo1-addon-iamserviceaccount-default-Role1-M7IEPRHZYLPB
eksctl-<clustername>-addon-iamserviceaccount-default-Role1-<SomeValue>
```
  - Open that Role and verify **Permissions**
  - We should have our **AllowExternalDNSUpdates** policy associated to it. 
  - Now make a note of that Role ARN
```
arn:aws:iam::411686525067:role/eksctl-eksdemo1-addon-iamserviceaccount-defa-Role1-1O3H7ZLUED5H4
```
## Step-03: Update External DNS Kubernetes manifest
- Original Template you can find in https://github.com/kubernetes-sigs/external-dns/blob/master/docs/tutorials/aws.md
- You will see `SS-COMMENTED` which we commented from original file.
- You will see `SS-REPLACED` where we replaced from original file. 
- **File Location:** V1-Deploy-ExternalDNS/01-Deploy-ExternalDNS.yml
### Change-1: Line number 9: IAM Role update
  - Copy the role-arn you have made a note at the end of step-02.
```yml
    eks.amazonaws.com/role-arn: arn:aws:iam::411686525067:role/eksctl-demo1-addon-iamserviceaccount-default-Role1-M7IEPRHZYLPB   
```
### Chnage-2: Line 55, 56: Commented them
- We used eksctl to create IAM role and attached the `AllowExternalDNSUpdates` policy
- We didnt use KIAM or Kube2IAM so we don't need these two lines, so commented
```yml
      #annotations:  
        #iam.amazonaws.com/role: arn:aws:iam::ACCOUNT-ID:role/IAM-SERVICE-ROLE-NAME    
```
### Change-3: Line 65, 67: Commented them
```yml
        # - --domain-filter=external-dns-test.my-org.com # will make ExternalDNS see only the hosted zones matching provided domain, omit to process all available hosted zones
       # - --policy=upsert-only # would prevent ExternalDNS from deleting any records, omit to enable full synchronization
```

## Step-04: Deploy ExternalDNS
- Deploy the manifest
```
# Deploy external DNS
kubectl apply -f V1-Deploy-ExternalDNS/

# Verify Deployment by checking logs
kubectl logs -f $(kubectl get po | egrep -o 'external-dns[A-Za-z0-9-]+')

# List pods (external-dns pod should be in running state)
kubectl get pods
```

# Module-2: Use External DNS for our Application
## Step-01: Update Ingress manifest by adding External DNS Annotation
- Added annotation with two DNS Names
  - dnstest1.stacksimplify.com
  - dnstest2.stacksimplify.com
- Once we deploy the application, we should be able to access our Applications with both DNS Names.   
- **07-ALB-Ingress-SSL-Redirect-ExternalDNS.yml**
```yml
    # External DNS - For creating a Record Set in Route53
    external-dns.alpha.kubernetes.io/hostname: dnstest1.stacksimplify.com, dnstest2.stacksimplify.com    
```
- In your case it is going to be, replace `yourdomain` with your domain name
  - dnstest1.yourdoamin.com
  - dnstest2.yourdoamin.com

## Step-02: Deploy all Application Kubernetes Manifests
### Deploy
```
# Deploy
kubectl apply -f V5-ALB-Ingress-ExternalDNS/
```
### Verify Load Balancer & Target Groups
    - Load Balancer -  Listeneres (Verify both 80 & 443) 
    - Load Balancer - Rules (Verify both 80 & 443 listeners) 
    - Target Groups - Group Details (Verify Health check path)
    - Target Groups - Targets (Verify all 3 targets are healthy)
    - Verify ingress controller from kubectl

### Verify External DNS Log
```
# Verify External DNS logs
kubectl logs -f $(kubectl get po | egrep -o 'external-dns[A-Za-z0-9-]+')
```
- **External DNS Log**
```log
time="2020-05-29T04:25:55Z" level=info msg="Desired change: CREATE dnstest1.zetaoptdemo.com A [Id: /hostedzone/Z29P9D94N7I5H5]"
time="2020-05-29T04:25:55Z" level=info msg="Desired change: CREATE dnstest2.zetaoptdemo.com A [Id: /hostedzone/Z29P9D94N7I5H5]"
time="2020-05-29T04:25:55Z" level=info msg="Desired change: CREATE dnstest1.zetaoptdemo.com TXT [Id: /hostedzone/Z29P9D94N7I5H5]"
time="2020-05-29T04:25:55Z" level=info msg="Desired change: CREATE dnstest2.zetaoptdemo.com TXT [Id: /hostedzone/Z29P9D94N7I5H5]"
time="2020-05-29T04:25:55Z" level=info msg="4 record(s) in zone zetaoptdemo.com. [Id: /hostedzone/Z29P9D94N7I5H5] were successfully updated"
time="2020-05-29T04:26:55Z" level=info msg="All records are already up to date"
time="2020-05-29T04:27:55Z" level=info msg="All records are already up to date"
time="2020-05-29T04:28:55Z" level=info msg="All records are already up to date"
```
### Verify Route53
- Go to Services -> Route53
- You should see **Record Sets** added for `dnstest1.stacksimplify.com`, `dnstest2.stacksimplify.com`

## Step-04: Access Application using newly registered DNS Name
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
kubectl delete -f V5-ALB-Ingress-ExternalDNS/
```

## Step-07: Delete the Public Node Group in EKS Cluster
```
# Template
eksctl delete nodegroup <NodeGroup-Name> --cluster <Cluster-Name>

# Replace nodegroup name and cluster name
eksctl delete nodegroup eksdemo1-ng1-public --cluster eksdemo1
```

## References
- https://github.com/kubernetes-sigs/external-dns/blob/master/docs/tutorials/alb-ingress.md
- https://github.com/kubernetes-sigs/external-dns/blob/master/docs/tutorials/aws.md


