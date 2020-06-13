# EKS - Logging with EFK AWS Elasticsearch, Fluentd and Kibana

## Step-01: Introduction
- Kubernetes Daemonsets
-  EFK Stack
  - E - Elasticsearch
  - F - Fluentd
  - K -Kibana
- Fluentd is an open source data collector providing a unified logging layer, supported by 500+ plugins connecting to many types of systems.
- AWS Elasticsearch is a distributed, RESTful search and analytics engine.
- Kibana lets you visualize your Elasticsearch data.
- Together, Fluentd, Elasticsearch and Kibana is also known as “EFK stack”. 
- Fluentd will forward logs from the individual instances in the cluster to a centralized logging backend (CloudWatch Logs) where they are combined for higher-level reporting using ElasticSearch and Kibana.
- We will be deploying Fluentd as a DaemonSet, or one pod per worker node. 
- The fluentd log daemon will collect logs and forward to CloudWatch Logs. 
- This will require the nodes to have permissions to send logs and create log groups and log streams. 
- This can be accomplished with an IAM user and IAM role



## Step-02: Create Elasticsearch Domain
```
aws es create-elasticsearch-domain \
  --domain-name eks-kube-logs \
  --elasticsearch-version 7.4 \
  --elasticsearch-cluster-config \
  InstanceType=m5.large.elasticsearch,InstanceCount=1 \
  --ebs-options EBSEnabled=true,VolumeType=standard,VolumeSize=100 \
  --access-policies '{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Principal":{"AWS":["*"]},"Action":["es:*"],"Resource":"*"}]}'
```
- Go to Services -> Elasticsearch -> Verify the new domain.
- **Important Note:**  It will take 10 to 15 minutes to create the Elasticsearch domain.  Continue with other steps below and come back and check it, it should be in Active status. 


## Step-03: Verify logs in CloudWatch
- Go to Services -> CloudWatch -> Logs -> Log Groups
```
# Search for 
Log Group: /aws/containerinsights/<ClusterName>

# We will find the log groups as below.  We will be interested in application logs
/aws/containerinsights/eksdemo1/application
/aws/containerinsights/eksdemo1/dataplane
/aws/containerinsights/eksdemo1/host
/aws/containerinsights/eksdemo1/performance
```
- We will find equivalent log stream for each application container present in our EKS Cluster: eksdemo1

## Step-04: Verify Elastichseach domain is Active
- Go to Services -> Elasticsearch -> My Domains -> eks-kube-logs
- It should be **Active**

## Step-05: Create an IAM role for Lambda function with full access to CloudWatch and Elasticsearch
- Go to Services -> Roles -> Create new Role -> 
  - AWS Service: Lambda
  - Policy Names:
    -  CloudWatchFullAccess
    - AmazonESFullAccess
  - Role Name: Lambda_full_access_to_CW_ES_for_EKS_logging
  - Role Description: Full access to Lambda function to pull logs from CW and push to ES.     

## Step-06: Create Subscription Filter in CloudWatch
- Go to Services -> CloudWatch -> Logs -> Log Groups
- Search for  Log Group name: `/aws/containerinsights/eksdemo1/application` and click on that
- Click on Actions -> Create Elasticsearch subscription filter
  - Account: This Account
  - Amazon ES Cluster: eks-kube-logs
  - Lambda IAM Execution Role: Lambda_full_access_to_CW_ES_for_EKS_logging
  - Logformat: Common Log Format 
  - Subscription filter pattern:  `[host, ident, authuser, date, request, status, bytes]`
  - Test pattern: Select container and click on Test pattern, we should see 50/50 patterns matched
  - Click on **Start Streaming**

## Step-07: Verify Lambda Function
- Go to Services -> Lambda
- Open Lamda function `LogsToElasticsearch_kubernetes-logs`
- Go to Monitoring Tab and keep refereshing for statistics

## Step-08: Access Kibana Dashboard
- Go to Services -> Elasticsearch -> Overview tab
- Click on **Kibana** url
- In Kibana, Go to -> Settings -> Index Patterns -> Create Index Pattern
  - Index Pattern: cw-*
  - Select @timestamp from the dropdown list and select Create index pattern
- Finally, click on Discover  

## Step-09: Generate some traffic using postman for App1
- Generate some traffic using postman for App1
- Watch live logs on Kibana Dashboard 

## Step-12: Clean-Up
1. Delete Elasticsearch domain
```
aws es delete-elasticsearch-domain --domain-name eks-kube-logs
```
2. Remove ES Subscription in CloudWatch
3. Delete Lambda function

## References
-  https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CWL_ES_Stream.html
- https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/Container-Insights-setup-EKS-quickstart.html
- https://www.kimsereylam.com/aws/cloudwatch/metrics/2018/11/09/monitor-nginx-access-log-in-cloudwatch.html

