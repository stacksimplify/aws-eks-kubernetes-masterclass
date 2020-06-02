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

## Step-02: Create IAM Policy
- Go to Services -> IAM -> Policies -> Create Policy
- Policy Name: cw-kube-worker-node-logs
- Policy Description: Push Kubernetes worker node logs to CloudWatch using Fluentd
- **kube-worker-node-logs.json**
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Action": [
                "logs:DescribeLogGroups",
                "logs:DescribeLogStreams",
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ],
            "Resource": "*",
            "Effect": "Allow"
        }
    ]
}
```

## Step-03: Associate the policy to EKS Cluster Worker Node Role
- Associate the above newly creatd policy `cw-kube-worker-node-logs` policy to EKS Cluster Worker Node Role. 
- Go to Services -> IAM -> Roles -> Search for `eksctl-eksdemo1-nodegroup` (eksctl-clustername-nodegroup)
- Open the Role -> Attach Policies
- Associate newly created policy `cw-kube-worker-node-logs`

## Step-04: Create a Security Group allowing all ports inbound
- Go to Services -> EC2 -> Security Groups -> Create Security Group
- Security Group Name: eks-eksdemo1-allow-all
  - Inbound Rules
    - Type: All Traffic
    - Source: 0.0.0./0

## Step-05: Provision AWS Elasticsearch Cluster
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

## Step-06: Deploy Fluentd
- Update REGION and CLUSTER_NAME environment variables in `fluentd.yml` to the one what you are using. 
  - REGION: us-east-1
  - CLUSTER_NAME: eksdemo1
  - Line 200 & 201 in `fluentd.yml` file. 
```yml
        env:
          - name: REGION
            value: us-east-1
          - name: CLUSTER_NAME
            value: eksdemo1
```  
- If you didn't change anything when creating EKS cluster setup as part of this course then we are good. 
```
kubectl apply -f fluentd.yml
kubectl get pods -w --namespace=kube-system
```

## Step-07: Verify logs in CloudWatch
- Go to Services -> CloudWatch -> Logs -> Log Groups
```
# Search for 
Log Group: /eks/<cluster-name>/containers

# In our case it is going to be
Log Group: /eks/ekdemo1/containers
```
- You can find log streams for each container in our EKS Cluster: eksdemo1

## Step-08: Verify Elastichseach domain is Active
- Go to Services -> Elasticsearch -> My Domains -> eks-kube-logs
- It should be **Active**

## Step-09: Create an IAM role for Lambda function with full access to CloudWatch and Elasticsearch
- Go to Services -> Roles -> Create new Role -> 
  - AWS Service: Lambda
  - Policy Names:
    -  CloudWatchFullAccess
    - AmazonESFullAccess
  - Role Name: Lambda_full_access_to_CW_ES_for_EKS_logging
  - Role Description: Full access to Lambda function to pull logs from CW and push to ES.     

## Step-10: Create Subscription Filter in CloudWatch
- Go to Services -> CloudWatch -> Logs -> Log Groups
- Search for  Log Group name: `/eks/eksdemo1/containers` and click on that
- Click on Actions -> Create Elasticsearch subscription filter
  - Account: This Account
  - Amazon ES Cluster: eks-kube-logs
  - Lambda IAM Execution Role: Lambda_full_access_to_CW_ES_for_EKS_logging
  - Logformat: Common Log Format
  - Test pattern: Select container and click on Test pattern, we should see 50/50 patterns matched
  - Click on **Start Streaming**

## Step-11: Verify Lambda Function
- Go to Services -> Lambda
- Open Lamda function `LogsToElasticsearch_kubernetes-logs`
- Go to Monitoring Tab and keep refereshing for statistics

## Step-11: Access Kibana Dashboard
- Go to Services -> Elasticsearch -> Overview tab
- Click on **Kibana** url
- In Kibana, Go to -> Settings -> Index Patterns -> Create Index Pattern
  - Index Pattern: cw-*
  - Select @timestamp from the dropdown list and select Create index pattern
- Finally, click on Discover  


## Step-12: Clean-Up
1. Undeploy Fluentd from EKS Cluster
```
kubectl delete -f fluentd.yml
```
2. Delete Elasticsearch domain
```
aws es delete-elasticsearch-domain --domain-name eks-kube-logs
```
3. Remove ES Subscription in CloudWatch
4. Delete Log Group
```
aws logs delete-log-group --log-group-name /eks/eksdemo1/containers
```
5. Delete Lambda function

## References
-  https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CWL_ES_Stream.html


