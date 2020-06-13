# Microservices Distributed Tracing using AWS X-Ray
## X_RAY NOT WORKING

## Step-01: IAM Role
- Ensure that the IAM role that is attached to the EC2 instance, or the Kubernetes worker node, has the CloudWatchAgentServerPolicy and AWSXRayDaemonWriteAccess policies attached.

## Step-02: Daemonset
```
curl https://raw.githubusercontent.com/aws-samples/amazon-cloudwatch-container-insights/master/k8s-deployment-manifest-templates/deployment-mode/daemonset/cwagent-fluentd-xray/cwagent-fluentd-xray-quickstart.yaml | sed "s/{{cluster_name}}/cluster-name/;s/{{region_name}}/region/" | kubectl apply -f -


curl https://raw.githubusercontent.com/aws-samples/amazon-cloudwatch-container-insights/master/k8s-deployment-manifest-templates/deployment-mode/daemonset/cwagent-fluentd-xray/cwagent-fluentd-xray-quickstart.yaml | sed "s/{{cluster_name}}/appmesh/;s/{{region_name}}/us-east-1/" | kubectl apply -f -
```

## Step-03: Update usermgmt.yml
```
AWS_XRAY_DAEMON_ADDRESS
```


## References
### Nice PPT 
-  https://www.slideshare.net/AmazonWebServices/instrumenting-kubernetes-for-observability-using-aws-xray-and-amazon-cloudwatch-dev303r2-aws-reinvent-2018
- VERY NICE MICROSERVICES OBSERVABILITY: https://www.slideshare.net/AmazonWebServices/aws-app-mesh-service-mesh-magic-aws-container-day-2019-barcelona

### Nice Article on SpringBoot and X-Ray
- https://medium.com/@avijitsarkar123/so-what-is-distributed-tracing-and-why-its-so-relevant-in-the-current-world-e496a1e1a75c

### X-Ray Spring
- https://docs.aws.amazon.com/xray/latest/devguide/xray-sdk-java-aop-spring.html

```log

com.amazonaws.SdkClientException: Unable to execute HTTP request: Connect to 127.0.0.1:2000 [/127.0.0.1] failed: Connection refused (Connection refused)
	at com.amazonaws.http.AmazonHttpClient$RequestExecutor.handleRetryableException(AmazonHttpClient.java:1134) ~[aws-java-sdk-core-1.11.398.jar!/:na]
	at com.amazonaws.http.AmazonHttpClient$RequestExecutor.executeHelper(AmazonHttpClient.java:1080) ~[aws-java-sdk-core-1.11.398.jar!/:na]
	at com.amazonaws.http.AmazonHttpClient$RequestExecutor.doExecute(AmazonHttpClient.java:745) ~[aws-java-sdk-core-1.11.398.jar!/:na]
	at com.amazonaws.http.AmazonHttpClient$RequestExecutor.executeWithTimer(AmazonHttpClient.java:719) ~[aws-java-sdk-core-1.11.398.jar!/:na]
	at com.amazonaws.http.AmazonHttpClient$RequestExecutor.execute(AmazonHttpClient.java:701) ~[aws-java-sdk-core-1.11.398.jar!/:na]
	at com.amazonaws.http.AmazonHttpClient$RequestExecutor.access$500(AmazonHttpClient.java:669) ~[aws-java-sdk-core-1.11.398.jar!/:na]
	at com.amazonaws.http.AmazonHttpClient$RequestExecutionBuilderImpl.execute(AmazonHttpClient.java:651) ~[aws-java-sdk-core-1.11.398.jar!/:na]
	at com.amazonaws.http.AmazonHttpClient.execute(AmazonHttpClient.java:515) ~[aws-java-sdk-core-1.11.398.jar!/:na]
	at com.amazonaws.services.xray.AWSXRayClient.doInvoke(AWSXRayClient.java:1257) ~[aws-java-sdk-xray-1.11.398.jar!/:na]
	at com.amazonaws.services.xray.AWSXRayClient.invoke(AWSXRayClient.java:1226) ~[aws-java-sdk-xray-1.11.398.jar!/:na]
	at com.amazonaws.services.xray.AWSXRayClient.invoke(AWSXRayClient.java:1215) ~[aws-java-sdk-xray-1.11.398.jar!/:na]
	at com.amazonaws.services.xray.AWSXRayClient.executeGetSamplingRules(AWSXRayClient.java:568) ~[aws-java-sdk-xray-1.11.398.jar!/:na]
	at com.amazonaws.services.xray.AWSXRayClient.getSamplingRules(AWSXRayClient.java:539) ~[aws-java-sdk-xray-1.11.398.jar!/:na]
	at com.amazonaws.xray.strategy.sampling.pollers.RulePoller.pollRule(RulePoller.java:65) ~[aws-xray-recorder-sdk-core-2.5.0.jar!/:na]
	at com.amazonaws.xray.strategy.sampling.pollers.RulePoller.lambda$start$0(RulePoller.java:46) ~[aws-xray-recorder-sdk-core-2.5.0.jar!/:na]

```