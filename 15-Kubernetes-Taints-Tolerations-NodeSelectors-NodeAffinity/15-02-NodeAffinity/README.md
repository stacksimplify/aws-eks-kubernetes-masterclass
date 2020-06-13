# Kubernetes - Node Affinity

## Step-01: Introduction
- To get pods to be scheduled to specific nodes Kubernetes provides `nodeSelectors` and `nodeAffinity`. 
- As `nodeAffinity` is a superset of `nodeSelectors`, `nodeSelectors` will be deprecated in Kubernetes.
- With that said we will focus on `nodeAffinity`
- With node affinity we can tell Kubernetes which nodes to schedule to a pod using the **labels** on each node.

## Step-02: Label a Node
- Labelling a node with our custom label which we can use during our Pod Affinity configuration
```
# List Nodes
kubectl get nodes

# Label Node
kubectl label nodes <node-name> <label-key>=<label-value>
kubectl label nodes ip-192-168-28-109.ec2.internal node-used-for=webservers

# List nodes with specific lable
kubectl get nodes -l <label-key>=<label-value>, <label-key>=<label-value>
kubectl get nodes -l node-used-for=webservers
```

## Step-03: Update Node Affinity in our Application Pod Spec
- Add the below `affinity` to pod `spec` in a deployment
```yml
  affinity:
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
        - matchExpressions:
          - key: node-used-for
            operator: In
            values:
            - webservers
```

## Step-04: Deploy the updated deployment manifest and Test
```
# Deploy updated deployment manifest
kubectl apply -f 03-app1-nginx-NodeSelector.yml 

# List Pods
kubectl get pods -o wide
```
- **Observations:** 
  - Every pod of our app1 will be scheduled now on the tainted and labelled node. 
  - Node we tainted and labelled is `ip-192-168-28-109.ec2.internal` and all app1 pods now present on the same node. 

## Step-05: Clean-Up
```
# Undeploy Application
kubectl delete -f 03-app1-nginx-NodeSelector.yml 

# Untaint a node
# Template
kubectl taint nodes <node-name> <key>:NoSchedule-

# Replae Node Name & key
kubectl taint nodes ip-192-168-28-109.ec2.internal app:NoSchedule-
kubectl taint nodes ip-192-168-28-109.ec2.internal app:NoExecute-
```

## References
- For complete and detailed understanding of Node Affinity features refer the below documentation link
- https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/