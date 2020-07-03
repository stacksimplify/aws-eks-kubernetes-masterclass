# External DNS - Use it for our Applications

## Step-01: Update Ingress manifest by adding External DNS Annotation
- Added annotation with two DNS Names
  - dnstest1.kubeoncloud.com
  - dnstest2.kubeoncloud.com
- Once we deploy the application, we should be able to access our Applications with both DNS Names.   
- **07-ALB-Ingress-SSL-Redirect-ExternalDNS.yml**
```yml
    # External DNS - For creating a Record Set in Route53
    external-dns.alpha.kubernetes.io/hostname: dnstest1.kubeoncloud.com, dnstest2.kubeoncloud.com    
```
- In your case it is going to be, replace `yourdomain` with your domain name
  - dnstest1.yourdoamin.com
  - dnstest2.yourdoamin.com

## Step-02: Deploy all Application Kubernetes Manifests
### Deploy
```
# Deploy
kubectl apply -f kube-manifests/
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
time="2020-05-29T04:25:55Z" level=info msg="Desired change: CREATE dnstest1.kubeoncloud.com A [Id: /hostedzone/Z29P9D94N7I5H5]"
time="2020-05-29T04:25:55Z" level=info msg="Desired change: CREATE dnstest2.kubeoncloud.com A [Id: /hostedzone/Z29P9D94N7I5H5]"
time="2020-05-29T04:25:55Z" level=info msg="Desired change: CREATE dnstest1.kubeoncloud.com TXT [Id: /hostedzone/Z29P9D94N7I5H5]"
time="2020-05-29T04:25:55Z" level=info msg="Desired change: CREATE dnstest2.kubeoncloud.com TXT [Id: /hostedzone/Z29P9D94N7I5H5]"
time="2020-05-29T04:25:55Z" level=info msg="4 record(s) in zone zetaoptdemo.com. [Id: /hostedzone/Z29P9D94N7I5H5] were successfully updated"
time="2020-05-29T04:26:55Z" level=info msg="All records are already up to date"
time="2020-05-29T04:27:55Z" level=info msg="All records are already up to date"
time="2020-05-29T04:28:55Z" level=info msg="All records are already up to date"
```
### Verify Route53
- Go to Services -> Route53
- You should see **Record Sets** added for `dnstest1.kubeoncloud.com`, `dnstest2.kubeoncloud.com`

## Step-04: Access Application using newly registered DNS Name
### Perform nslookup tests before accessing Application
- Test if our new DNS entries registered and resolving to an IP Address
```
# nslookup commands
nslookup dnstest1.kubeoncloud.com
nslookup dnstest2.kubeoncloud.com
```
### Access Application using dnstest1 domain
```
# HTTP URLs (Should Redirect to HTTPS)
http://dnstest1.kubeoncloud.com/app1/index.html
http://dnstest1.kubeoncloud.com/app2/index.html
http://dnstest1.kubeoncloud.com/usermgmt/health-status
```

### Access Application using dnstest2 domain
```
# HTTP URLs (Should Redirect to HTTPS)
http://dnstest2.kubeoncloud.com/app1/index.html
http://dnstest2.kubeoncloud.com/app2/index.html
http://dnstest2.kubeoncloud.com/usermgmt/health-status
```


## Step-05: Clean Up
```
kubectl delete -f kube-manifests/
```


## References
- https://github.com/kubernetes-sigs/external-dns/blob/master/docs/tutorials/alb-ingress.md
- https://github.com/kubernetes-sigs/external-dns/blob/master/docs/tutorials/aws.md


