# Monitoring EKS using CloudWatch Container Insigths

## Step-01: Deploy our Sample to generate Load
```
# Deploy
kubectl apply -f kube-manifests

# Access Application
http://<Network-Load-Balancer-URL>/app1/index.html
```

## Step-02: Associate CloudWatch Policy to our EKS Worker Nodes Role
- Go to Services -> EC2 -> Worker Node EC2 Instance -> IAM Role -> Click on that role
```
# Sample Role ARN
arn:aws:iam::180789647333:role/eksctl-eksdemo1-nodegroup-eksdemo-NodeInstanceRole-1FVWZ2H3TMQ2M

# Policy to be associated
Associate Policy: CloudWatchAgentServerPolicy
```

## Step-03: Install Container Insights

### Deploy CloudWatch Agent and Fluentd as DaemonSets
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

## Verify
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


## Step-07: Clean-Up Container Insights
```
# Template
curl https://raw.githubusercontent.com/aws-samples/amazon-cloudwatch-container-insights/latest/k8s-deployment-manifest-templates/deployment-mode/daemonset/container-insights-monitoring/quickstart/cwagent-fluentd-quickstart.yaml | sed "s/{{cluster_name}}/cluster-name/;s/{{region_name}}/cluster-region/" | kubectl delete -f -

# Replace Cluster Name & Region Name
curl https://raw.githubusercontent.com/aws-samples/amazon-cloudwatch-container-insights/latest/k8s-deployment-manifest-templates/deployment-mode/daemonset/container-insights-monitoring/quickstart/cwagent-fluentd-quickstart.yaml | sed "s/{{cluster_name}}/eksdemo1/;s/{{region_name}}/us-east-1/" | kubectl delete -f -
```

## References
- https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/deploy-container-insights-EKS.html