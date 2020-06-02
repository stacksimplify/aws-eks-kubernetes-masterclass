# Monitoring EKS using CloudWatch Container Insigths

## Step-01: Deploy our Apps
```
cd aws-fargate-eks-masterclass/09-ELB-Application-LoadBalancers/09-06-ALB-Ingress-ExternalDNS/kube-manifests
kubectl apply -f V2-ALB-Ingress-ExternalDNS/
```

## Step-02: Associate CloudWatch Policy to our EKS Worker Nodes Role
```
Role Name: arn:aws:iam::411686525067:role/eksctl-eksdemo1-nodegroup-eksdemo-NodeInstanceRole-1JRQ5M9E53CC3

Associate Policy: CloudWatchAgentServerPolicy
```

## Step-03: Install Container Insights
- This command will 
  - Create the Namespace amazon-cloudwatch.
  - Create all the necessary security objects for both DaemonSet:
    - SecurityAccount.
    - ClusterRole.
    - ClusterRoleBinding.
  - Deploy Cloudwatch-Agent (responsible for sending the metrics to CloudWatch) as a DaemonSet.
  - Deploy fluentd (responsible for sending the logs to Cloudwatch) as a DaemonSet.
  -  Deploy ConfigMap configurations for both DaemonSets.
```
# Template
curl -s https://raw.githubusercontent.com/aws-samples/amazon-cloudwatch-container-insights/latest/k8s-deployment-manifest-templates/deployment-mode/daemonset/container-insights-monitoring/quickstart/cwagent-fluentd-quickstart.yaml | sed "s/{{cluster_name}}/<REPLACE_CLUSTER_NAME>/;s/{{region_name}}/<REPLACE-AWS_REGION>/" | kubectl apply -f -

# Replaced Cluster Name and Region
curl -s https://raw.githubusercontent.com/aws-samples/amazon-cloudwatch-container-insights/latest/k8s-deployment-manifest-templates/deployment-mode/daemonset/container-insights-monitoring/quickstart/cwagent-fluentd-quickstart.yaml | sed "s/{{cluster_name}}/eksdemo1/;s/{{region_name}}/us-east-1/" | kubectl apply -f -
```

- Verify
```
kubectl -n amazon-cloudwatch get daemonsets
```


## Step-04: Access CloudWatch Dashboard & Generate Traffic using Postman Runner
- Access CloudWatch Container Insigths Dashboard
- Generate some traffic using Postman Runner

## Step-05: CloudWatch Log Insights
- View Container logs


## Step-06: CloudWatch Alarms from metrics
- Create Alarms

