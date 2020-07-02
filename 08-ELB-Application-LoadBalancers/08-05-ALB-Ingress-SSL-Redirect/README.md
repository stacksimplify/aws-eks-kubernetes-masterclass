# AWS ALB Ingress Controller - Implement HTTP to HTTPS Redirect

## Step-01: Add annotations related to SSL Redirect
- Redirect from HTTP to HTTPS
```yml
     # SSL Redirect Setting
    alb.ingress.kubernetes.io/actions.ssl-redirect: '{"Type": "redirect", "RedirectConfig": { "Protocol": "HTTPS", "Port": "443", "StatusCode": "HTTP_301"}}'   
```
## Step-02: Deploy all manifests and test
- **Deploy**
```
# Deploy
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
  
## Step-04: Access Application using newly registered DNS Name
- **Access Application**
```
# HTTP URLs (Should Redirect to HTTPS)
http://ssldemo.kubeoncloud.com/app1/index.html
http://ssldemo.kubeoncloud.com/app2/index.html
http://ssldemo.kubeoncloud.com/usermgmt/health-status

# HTTPS URLs
https://ssldemo.kubeoncloud.com/app1/index.html
https://ssldemo.kubeoncloud.com/app2/index.html
https://ssldemo.kubeoncloud.com/usermgmt/health-status
```

## Step-06: Clean Up
```
kubectl delete -f kube-manifests/
```



