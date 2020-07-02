# AWS ALB Ingress Controller - SSL 

## Step-01: Introduction
- We are going to register a new DNS in AWS Route53
- We are going to create a SSL certificate 
- Add Annotations related to SSL Certificate in Ingress manifest
- Deploy the manifests and test
- Clean-Up

## Step-02: Pre-requisite - Register a Domain in Route53 (if not exists)
- Goto Services -> Route53 -> Registered Domains
- Click on **Register Domain**
- Provide **desired domain: somedomain.com** and click on **check** (In my case its going to be `kubeoncloud.com`)
- Click on **Add to cart** and click on **Continue**
- Provide your **Contact Details** and click on **Continue**
- Enable Automatic Renewal
- Accept **Terms and Conditions**
- Click on **Complete Order**

## Step-03: Create a SSL Certificate in Certificate Manager
- Pre-requisite: You should have a registered domain in Route53 
- Go to Services -> Certificate Manager -> Create a Certificate
- Click on **Request a Certificate**
  - Choose the type of certificate for ACM to provide: Request a public certificate
  - Add domain names: *.yourdomain.com (in my case it is going to be `*.kubeoncloud.com`)
  - Select a Validation Method: **DNS Validation**
  - Click on **Confirm & Request**    
- **Validation**
  - Click on **Create record in Route 53**  
- Wait for 5 to 10 minutes and check the **Validation Status**  

## Step-04: Add annotations related to SSL
- **07-ALB-Ingress-SSL.yml**
```yml
# SSL Setting - 1
    ## SSL Settings
    alb.ingress.kubernetes.io/listen-ports: '[{"HTTPS":443}, {"HTTP":80}]'
    alb.ingress.kubernetes.io/certificate-arn: arn:aws:acm:us-east-1:411686525067:certificate/8adf7812-a1af-4eae-af1b-ea425a238a67
    #alb.ingress.kubernetes.io/ssl-policy: ELBSecurityPolicy-TLS-1-1-2017-01 #Optional (Picks default if not used)    
# SSL Setting - 2
spec:
  rules:
    #- host: kubedemo.stacksimplify.com    # SSL Setting (Optional only if we are not using certificate-arn annotation)
```
## Step-05: Deploy all manifests and test
- **Deploy**
```
kubectl apply -f kube-manifests/
```
- **Verify**
    - Load Balancer -  Listeneres (Verify both 80 & 443) 
    - Load Balancer - Rules (Verify both 80 & 443 listeners) 
    - Target Groups - Group Details (Verify Health check path)
    - Target Groups - Targets (Verify all 3 targets are healthy)
    - Verify ingress controller from kubectl
```
kubectl get ingress 
```
## Step-06: Add DNS in Route53   
- Go to **Services -> Route 53**
- Go to **Hosted Zones**
  - Click on **yourdomain.com** (in my case stacksimplify.com)
- Create a **Record Set**
  - **Name:** ssldemo.kubeoncloud.com
  - **Alias:** yes
  - **Alias Target:** Copy our ALB DNS Name here (Sample: 55dc0e80-default-ingressus-ea9e-551932098.us-east-1.elb.amazonaws.com)
  - Click on **Create**
  
## Step-07: Access Application using newly registered DNS Name
- **Access Application**
- **Important Note:** Instead of `kubeoncloud.com` you need to replace with your registered Route53 domain (Refer pre-requisite Step-02)
```
# HTTP URLs
http://ssldemo.kubeoncloud.com/app1/index.html
http://ssldemo.kubeoncloud.com/app2/index.html
http://ssldemo.kubeoncloud.com/usermgmt/health-status

# HTTPS URLs
https://ssldemo.kubeoncloud.com/app1/index.html
https://ssldemo.kubeoncloud.com/app2/index.html
https://ssldemo.kubeoncloud.com/usermgmt/health-status
```


