## Step-09: Scaling our Application
- Scaling our Application
```
# Scale Up 
kubectl scale deployments/kubenginx --replicas=4
kubectl get deployment
kubectl get po
kubectl get po -o wide
kubectl describe deployment kubenginx

# Scale Down
kubectl scale deployments/kubenginx --replicas=4
kubectl get po -o wide
kubectl describe deployment kubenginx
```
## Step-10: Rolling Updates
- **Update the version of the App**
```
kubectl set image deployments/kubernetes-bootcamp kubernetes-bootcamp=jocatalin/kubernetes-bootcamp:v2
kubectl get deployments
kubectl get pods
```
- **Rollback an Update to previous version**
```
kubectl rollout undo deployments/kubernetes-bootcamp
kubectl get deployments
```
