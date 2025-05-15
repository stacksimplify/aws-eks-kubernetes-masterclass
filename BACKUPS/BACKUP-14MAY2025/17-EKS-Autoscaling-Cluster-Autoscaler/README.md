# EKS - Cluster Autoscaler

## Step-01: Introduction
- The Kubernetes Cluster Autoscaler automatically adjusts the number of nodes in your cluster when pods fail to launch due to lack of resources or when nodes in the cluster are underutilized and their pods can be rescheduled onto other nodes in the cluster.

## Step-02: Verify if our NodeGroup as --asg-access
- We need to ensure that we have a parameter named `--asg-access` present during the cluster or nodegroup creation.
- Verify the same when we created our cluster node group

### What will happen if we use --asg-access tag?
- It enables IAM policy for cluster-autoscaler
- Lets review our nodegroup IAM role for the same. 
- Go to Services -> IAM -> Roles -> eksctl-eksdemo1-nodegroup-XXXXXX
- Click on **Permissions** tab
- You should see a inline policy named `eksctl-eksdemo1-nodegroup-eksdemo1-ng-private1-PolicyAutoScaling` in the list of policies associated to this role.

## Step-03: Deploy Cluster Autoscaler
```
# Deploy the Cluster Autoscaler to your cluster
kubectl apply -f https://raw.githubusercontent.com/kubernetes/autoscaler/master/cluster-autoscaler/cloudprovider/aws/examples/cluster-autoscaler-autodiscover.yaml

# Add the cluster-autoscaler.kubernetes.io/safe-to-evict annotation to the deployment
kubectl -n kube-system annotate deployment.apps/cluster-autoscaler cluster-autoscaler.kubernetes.io/safe-to-evict="false"
```
## Step-04: Edit Cluster Autoscaler Deployment to add Cluster name and two more parameters
```
kubectl -n kube-system edit deployment.apps/cluster-autoscaler
```
- **Add cluster name**
```yml
# Before Change
        - --node-group-auto-discovery=asg:tag=k8s.io/cluster-autoscaler/enabled,k8s.io/cluster-autoscaler/<YOUR CLUSTER NAME>

# After Change
        - --node-group-auto-discovery=asg:tag=k8s.io/cluster-autoscaler/enabled,k8s.io/cluster-autoscaler/eksdemo1
```

- **Add two more parameters**
```yml
        - --balance-similar-node-groups
        - --skip-nodes-with-system-pods=false
```
- **Sample for reference**
```yml
    spec:
      containers:
      - command:
        - ./cluster-autoscaler
        - --v=4
        - --stderrthreshold=info
        - --cloud-provider=aws
        - --skip-nodes-with-local-storage=false
        - --expander=least-waste
        - --node-group-auto-discovery=asg:tag=k8s.io/cluster-autoscaler/enabled,k8s.io/cluster-autoscaler/eksdemo1
        - --balance-similar-node-groups
        - --skip-nodes-with-system-pods=false
```

## Step-05: Set the Cluster Autoscaler Image related to our current EKS Cluster version
- Open https://github.com/kubernetes/autoscaler/releases
- Find our release version (example: 1.16.n) and update the same. 
- Our Cluster version is 1.16 and our cluster autoscaler version is 1.16.5 as per above releases link 
```
# Template
# Update Cluster Autoscaler Image Version
kubectl -n kube-system set image deployment.apps/cluster-autoscaler cluster-autoscaler=us.gcr.io/k8s-artifacts-prod/autoscaling/cluster-autoscaler:v1.XY.Z


# Update Cluster Autoscaler Image Version
kubectl -n kube-system set image deployment.apps/cluster-autoscaler cluster-autoscaler=us.gcr.io/k8s-artifacts-prod/autoscaling/cluster-autoscaler:v1.16.5
```

## Step-06: Verify Image version got updated
```
kubectl -n kube-system get deployment.apps/cluster-autoscaler -o yaml
```
- **Sample partial output**
```yml
    spec:
      containers:
      - command:
        - ./cluster-autoscaler
        - --v=4
        - --stderrthreshold=info
        - --cloud-provider=aws
        - --skip-nodes-with-local-storage=false
        - --expander=least-waste
        - --node-group-auto-discovery=asg:tag=k8s.io/cluster-autoscaler/enabled,k8s.io/cluster-autoscaler/eksdemo1
        - --balance-similar-node-groups
        - --skip-nodes-with-system-pods=false
        image: us.gcr.io/k8s-artifacts-prod/autoscaling/cluster-autoscaler:v1.16.5
```

## Step-07: View Cluster Autoscaler logs to verify that it is monitoring your cluster load.
```
kubectl -n kube-system logs -f deployment.apps/cluster-autoscaler
```
- Sample log reference
```log
I0607 09:14:37.793323       1 pre_filtering_processor.go:66] Skipping ip-192-168-60-30.ec2.internal - node group min size reached
I0607 09:14:37.793332       1 pre_filtering_processor.go:66] Skipping ip-192-168-27-213.ec2.internal - node group min size reached
I0607 09:14:37.793408       1 static_autoscaler.go:440] Scale down status: unneededOnly=true lastScaleUpTime=2020-06-07 09:12:27.367461648 +0000 UTC m=+37.138078060 lastScaleDownDeleteTime=2020-06-07 09:12:27.367461724 +0000 UTC m=+37.138078135 lastScaleDownFailTime=2020-06-07 09:12:27.367461801 +0000 UTC m=+37.138078213 scaleDownForbidden=false isDeleteInProgress=false scaleDownInCooldown=true
I0607 09:14:47.803891       1 static_autoscaler.go:192] Starting main loop
I0607 09:14:47.804234       1 utils.go:590] No pod using affinity / antiaffinity found in cluster, disabling affinity predicate for this loop
I0607 09:14:47.804251       1 filter_out_schedulable.go:65] Filtering out schedulables
I0607 09:14:47.804319       1 filter_out_schedulable.go:130] 0 other pods marked as unschedulable can be scheduled.
I0607 09:14:47.804343       1 filter_out_schedulable.go:130] 0 other pods marked as unschedulable can be scheduled.
I0607 09:14:47.804351       1 filter_out_schedulable.go:90] No schedulable pods
I0607 09:14:47.804366       1 static_autoscaler.go:334] No unschedulable pods
I0607 09:14:47.804376       1 static_autoscaler.go:381] Calculating unneeded nodes
I0607 09:14:47.804392       1 pre_filtering_processor.go:66] Skipping ip-192-168-60-30.ec2.internal - node group min size reached
I0607 09:14:47.804401       1 pre_filtering_processor.go:66] Skipping ip-192-168-27-213.ec2.internal - node group min size reached
I0607 09:14:47.804460       1 static_autoscaler.go:440] Scale down status: unneededOnly=true lastScaleUpTime=2020-06-07 09:12:27.367461648 +0000 UTC m=+37.138078060 lastScaleDownDeleteTime=2020-06-07 09:12:27.367461724 +0000 UTC m=+37.138078135 lastScaleDownFailTime=2020-06-07 09:12:27.367461801 +0000 UTC m=+37.138078213 scaleDownForbidden=false isDeleteInProgress=false scaleDownInCooldown=true

```

## Step-08: Deploy simple Application
```
# Deploy Application
kubectl apply -f kube-manifests/
```

## Step-09: Cluster Scale UP: Scale our application to 30 pods
- In 2 to 3 minutes, one after the other new nodes will added and pods will be scheduled on them. 
- Our max number of nodes will be 4 which we provided during nodegroup creation.
```
# Terminal - 1: Keep monitoring cluster autoscaler logs
kubectl -n kube-system logs -f deployment.apps/cluster-autoscaler

# Terminal - 2: Scale UP the demo application to 30 pods
kubectl get pods
kubectl get nodes 
kubectl scale --replicas=30 deploy ca-demo-deployment 
kubectl get pods

# Terminal - 2: Verify nodes
kubectl get nodes -o wide
```
## Step-10: Cluster Scale DOWN: Scale our application to 1 pod
- It might take 5 to 20 minutes to cool down and come down to minimum nodes which will be 2 which we configured during nodegroup creation
```
# Terminal - 1: Keep monitoring cluster autoscaler logs
kubectl -n kube-system logs -f deployment.apps/cluster-autoscaler

# Terminal - 2: Scale down the demo application to 1 pod
kubectl scale --replicas=1 deploy ca-demo-deployment 

# Terminal - 2: Verify nodes
kubectl get nodes -o wide
```

## Step-11: Clean-Up
- We will leave cluster autoscaler and undeploy only application
```
kubectl delete -f kube-manifests/
```
