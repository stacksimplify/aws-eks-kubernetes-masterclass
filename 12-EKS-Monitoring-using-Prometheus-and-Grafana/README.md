# Monitoring using Prometheus and Grafana

## Step-01: Verify if HELM installed
```
helm version --short
```

## Step-02: Install Prometheus on EKS Cluster
```
kubectl create namespace prometheus
helm install prometheus stable/prometheus \
    --namespace prometheus \
    --set alertmanager.persistentVolume.storageClass="gp2" \
    --set server.persistentVolume.storageClass="gp2"
```

```
Kalyans-MacBook-Pro:BINARY-DOWNLOADS kdaida$ helm install prometheus stable/prometheus \
>     --namespace prometheus \
>     --set alertmanager.persistentVolume.storageClass="gp2" \
>     --set server.persistentVolume.storageClass="gp2"

NAME: prometheus
LAST DEPLOYED: Mon Jun  1 16:54:34 2020
NAMESPACE: prometheus
STATUS: deployed
REVISION: 1
TEST SUITE: None
NOTES:
The Prometheus server can be accessed via port 80 on the following DNS name from within your cluster:
prometheus-server.prometheus.svc.cluster.local


Get the Prometheus server URL by running these commands in the same shell:
  export POD_NAME=$(kubectl get pods --namespace prometheus -l "app=prometheus,component=server" -o jsonpath="{.items[0].metadata.name}")
  kubectl --namespace prometheus port-forward $POD_NAME 9090


The Prometheus alertmanager can be accessed via port 80 on the following DNS name from within your cluster:
prometheus-alertmanager.prometheus.svc.cluster.local


Get the Alertmanager URL by running these commands in the same shell:
  export POD_NAME=$(kubectl get pods --namespace prometheus -l "app=prometheus,component=alertmanager" -o jsonpath="{.items[0].metadata.name}")
  kubectl --namespace prometheus port-forward $POD_NAME 9093
#################################################################################
######   WARNING: Pod Security Policy has been moved to a global property.  #####
######            use .Values.podSecurityPolicy.enabled with pod-based      #####
######            annotations                                               #####
######            (e.g. .Values.nodeExporter.podSecurityPolicy.annotations) #####
#################################################################################


The Prometheus PushGateway can be accessed via port 9091 on the following DNS name from within your cluster:
prometheus-pushgateway.prometheus.svc.cluster.local


Get the PushGateway URL by running these commands in the same shell:
  export POD_NAME=$(kubectl get pods --namespace prometheus -l "app=prometheus,component=pushgateway" -o jsonpath="{.items[0].metadata.name}")
  kubectl --namespace prometheus port-forward $POD_NAME 9091

For more information on running Prometheus, visit:
https://prometheus.io/

```

## Step-03: Access Prometheus server URL locally
- To access Prometheus server URL, we are going to use the `kubectl port-forward` command 
```
kubectl get all -n prometheus
kubectl --namespace=prometheus port-forward deploy/prometheus-server 9090

# Access URLs
http://localhost:9090
http://localhost:9090/targets
```

## Step-04: Create grafana.yml
- Replace url with url we have from Step-02 output when we installed Prometheus helm chart
```yml
datasources:
  datasources.yaml:
    apiVersion: 1
    datasources:
    - name: Prometheus
      type: prometheus
      url: http://prometheus-server.prometheus.svc.cluster.local
      access: proxy
      isDefault: true
```

## Step-05: Install grafana
```
# Create Namespace grafana
kubectl create namespace grafana

# Install Grafana Helm chart
helm install grafana stable/grafana \
    --namespace grafana \
    --set persistence.storageClassName="gp2" \
    --set persistence.enabled=true \
    --set adminPassword='EKS!Admin' \
    --values grafana.yml \
    --set service.type=LoadBalancer

# Verify all objects in grafana namespace
kubectl get all -n grafana    
```
- Grafana Output
```
Kalyans-MacBook-Pro:15-EKS-Monitoring-using-Prometheus-and-Grafana kdaida$ helm install grafana stable/grafana \
>     --namespace grafana \
>     --set persistence.storageClassName="gp2" \
>     --set persistence.enabled=true \
>     --set adminPassword='EKS!Admin' \
>     --values grafana.yml \
>     --set service.type=LoadBalancer
NAME: grafana
LAST DEPLOYED: Mon Jun  1 17:04:04 2020
NAMESPACE: grafana
STATUS: deployed
REVISION: 1
NOTES:
1. Get your 'admin' user password by running:

   kubectl get secret --namespace grafana grafana -o jsonpath="{.data.admin-password}" | base64 --decode ; echo

2. The Grafana server can be accessed via port 80 on the following DNS name from within your cluster:

   grafana.grafana.svc.cluster.local

   Get the Grafana URL to visit by running these commands in the same shell:
NOTE: It may take a few minutes for the LoadBalancer IP to be available.
        You can watch the status of by running 'kubectl get svc --namespace grafana -w grafana'
     export SERVICE_IP=$(kubectl get svc --namespace grafana grafana -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
     http://$SERVICE_IP:80

3. Login with the password from step 1 and the username: admin
Kalyans-MacBook-Pro:15-EKS-Monitoring-using-Prometheus-and-Grafana kdaida$ 

```

## Step-06: Get Load Balancer URL
```
# To get Grafana Load Balancer URL
kubectl get svc -n grafana grafana -o jsonpath='{.status.loadBalancer.ingress[0].hostname}'

# Sample
a64c99cb4e3b24531ace5679b0932a16-1861416249.us-east-1.elb.amazonaws.com

# URL
http://a64c99cb4e3b24531ace5679b0932a16-1861416249.us-east-1.elb.amazonaws.com
Username: admin
Password: EKS!Admin
```

## Step-07: Cluster Monitoring Dashboard
- Click ’+’ button on left panel and select ‘Import’.
- Enter 3119 dashboard id under Grafana.com Dashboard.
- Click ‘Load’.
- Select ‘Prometheus’ as the endpoint under prometheus data sources drop down.
- Click ‘Import’.


## Step-08: POD Monitoring Dashboard
- Click ’+’ button on left panel and select ‘Import’.
- Enter 6417 dashboard id under Grafana.com Dashboard.
- Click ‘Load’.
- Enter Kubernetes Pods Monitoring as the Dashboard name.
- Click change to set the Unique identifier (uid).
- Select ‘Prometheus’ as the endpoint under prometheus data sources drop down.s
- Click ‘Import’.

## Step-09: Clean-Up
```
helm uninstall prometheus --namespace prometheus
helm uninstall grafana --namespace grafana
```

