# Kubernetes - Taints & Tolerations

## Step-01: Introduction

## Step-02: Deploy a simple Application
```
# Deploy Application
kubectl apply -f 01-app1-nginx.yml

# Get Nodes
kubectl get nodes

# List Pods
kubectl get pods -o wide
```
- **Observation:** Kubernetes scheduled two pods per node automatically based on system resources available.

## Step-03: Taint a node with Effect as NoSchedule
### Effect
- **NoSchedule:** Instructs Kubernetes scheduler not to schedule any new pods to the node unless the pod tolerates the taint.
- **NoExecute:** Instructs Kubernetes scheduler to evict pods already running on the node that don't tolerate the taint.
```
# Get Nodes
kubectl get nodes

# Describe Node
kubectl describe  node <Node-Name>
kubectl describe  node ip-192-168-28-109.ec2.internal

# Taint Node with Effect:NoSchedule
kubectl taint nodes <Node-Name> <key>=<value>:<effect>
kubectl taint nodes ip-192-168-28-109.ec2.internal app=webservers:NoSchedule

# Describe Node
kubectl describe  node <Node-Name>
kubectl describe  node ip-192-168-28-109.ec2.internal
```
- **Observation:** No changes to any pods already present in tainted node, because we used `effect:NoSchedule`

## Step-04: Taint a node with Effect as NoExecute
```
# Taint Node with Effect:NoExecute
kubectl taint nodes <Node-Name> <key>=<value>:<effect>
kubectl taint nodes ip-192-168-28-109.ec2.internal app=webservers:NoExecute

# Get all pods from all namespaces
kubectl get pods -o wide

# Describe Node
kubectl describe  node <Node-Name>
kubectl describe  node ip-192-168-28-109.ec2.internal
```
- **Observation-1:** Our app1 pods re-scheduled on other node which is not tainted.
- **Observation-2:** We have also notice that pod with name `core-dns` also re-scheduled on non-tainted node. 
```
# Get pods from namespace kube-system
kubectl get pods -o wide -n kube-system
```
- **Observation-3:** We have also seen system pods: `aws-node` and `kube-proxy` running on every single node (Daemonsets) 
  - System pods are created with toleration settings that tolerate all taints so that they can be scheduled onto any node. 
  - By design, system pods are required by the Kubernetes infrastructure (e.g. `kube-proxy`) 
  - In the sameway, `aws-node` which is specific to managed Kubernetes for EKS and considered as system pod.

## Step-05: Add Toleration to our Sample App Deployment
-  By adding toleration we are telling the tainted node to allow scheduling that respective pod which matches toleration.
- Add the below toleration to pod `spec` in a deployment
```yml
      tolerations:
      - key: "app"
        operator: Equal
        value: "webservers"    
```
- Deploy updated manifest
```
kubectl apply -f 02-app1-nginx-tolerations-added.yml
```
- **Observations**: 
  - We can see that now `app1` pods are allowed in tainted node, but in addition you also see that `app1` pods on non-tainted node.
  - This is expected as the toleration allows the pod to be scheduled to a tainted node (it tolerates it) but doesn't guarantee that the pod will actually be scheduled there.
  - In order to get all the `app1` pods scheduled to a specific node (in our case `the tainted node`) we need to jump in to our next topic named **Node Selectors & Node Affinity**

## Step-06: Untaint Nodes

```
# Template
kubectl taint nodes <node-name> <key>:NoSchedule-

# Replae Node Name & key
kubectl taint nodes ip-192-168-28-109.ec2.internal app:NoSchedule-
kubectl taint nodes ip-192-168-28-109.ec2.internal app:NoExecute-
```