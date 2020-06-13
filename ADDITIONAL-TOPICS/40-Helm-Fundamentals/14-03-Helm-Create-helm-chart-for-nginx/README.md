# Create Helm Chart for our Kube Nginx App1 Application

## Step-01: Generate Chart
```
helm create kube-nginxapp1
```

## Step-02: Understand Helm Chart Directory Structure

```
kube-nginxapp1
|-- Chart.yaml
|-- charts
|-- templates
|   |-- NOTES.txt
|   |-- _helpers.tpl
|   |-- deployment.yaml
|   |-- ingress.yaml
|   `-- service.yaml
`-- values.yaml
```

## Step-03: Update Chart.yaml
- This will be our container image tag
- We are going to use the Container Image: https://hub.docker.com/repository/docker/stacksimplify/kube-nginxapp1
- Update `appVersion` value  in `Chart.yaml`
```
# Update appVersion to 1.0.0
appVersion: 1.0.0   
```

## Step-04: Update values.yaml
- Update `repository` value  in values.yaml
```
  repository: stacksimplify/kube-nginxapp1
```
- Discuss other settings on a high level

## Step-05: Dry run the chart
- Dry run and review the output templates
```
helm install mychartv1 --dry-run --debug ./kube-nginxapp1
```

## Step-06: Install our new chart
- Default it creates a service of type clusterIP, lets override that using `--set service.type=NodePort`
```
# Install Chart
helm install mychartv1 ./kube-nginxapp1 --set service.type=NodePort

# Helm list
helm ls
helm list

# Verify
kubectl get po,svc,deploy

# Access Application
kubectl get nodes -o wide
kubectl get svc
http://<Worker-Node-Public-IP>:Port/app1/index.html
```
- **Important Note:** If application not accessible in browser, mostly a security group issue, add a rule in security group startting wiht `eks-remoteAccess-*` (All Traffic, All Ports, Anywhere)

## Step-07: Uninstall our chart
```
# Helm List
helm list
helm ls

# Helm uninstall chart
helm uninstall mychartv1 
```

## Step-08: Packaging
- Helm will create a  `kube-nginxapp1-0.1.0.tgz` in our working directory using the name and version from the metadata defined in Chart.yaml
```
# Package using Helm
helm package ./kube-nginxapp1
```
- Install from package
```
# Helm Install
helm install mychartv1 kube-nginxapp1-0.1.0.tgz --set service.type=NodePort

# Helm uninstall chart
helm uninstall mychartv1 
```

