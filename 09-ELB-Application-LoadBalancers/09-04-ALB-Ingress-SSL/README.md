# Learn ALB Ingress Controller - SSL

## PENDING - Step-01: Register a Domain in Route53

## Step-02: Create a SSL Certificate in Certificate Manager
- Pre-requisite: You should have a registered domain in Route53 b
- Go to Service -> Create a Certificate
- Click on **Request a Certificate**
  - Choose the type of certificate for ACM to provide: Request a public certificate
  - Add domain names: *.yourdomain.com (in my case it is going to be `*.stacksimplify.com`)
  - Select a Validation Method: DNS Validation
  - Click on **Confirm & Request**    
- **Validation**
  - Click on **Create record in Route 53**  
- Wait for 5 to 10 minutes and check the **Validation Status**  

## Step-02: Add annotations related to SSL
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
## Step-03: Deploy all manifests and test
- **Deploy**
```
kubectl apply -f V3-ALB-Ingress-SSL/
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
## Step-04: Add DNS in Route53   
- Go to **Services -> Route 53**
- Go to **Hosted Zones**
  - Click on **yourdomain.com** (in my case stacksimplify.com)
- Create a **Record Set**
  - **Name:** kubedemo.stacksimplify.com
  - **Alias:** yes
  - **Alias Target:** Copy our ALB DNS Name here (Sample: 55dc0e80-default-ingressus-ea9e-551932098.us-east-1.elb.amazonaws.com)
  - Click on **Create**
  
## Step-05: Access Application using newly registered DNS Name
- **Access Application**
```
# HTTP URLs
http://kubedemo.yourdoamin.com/app1/
http://kubedemo.yourdoamin.com/app2/
http://kubedemo.yourdoamin.com/usermgmt/health-status

# HTTPS URLs
https://kubedemo.yourdoamin.com/app1/
https://kubedemo.yourdoamin.com/app2/
https://kubedemo.yourdoamin.com/usermgmt/health-status
```




