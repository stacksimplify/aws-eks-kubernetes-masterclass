# Troubleshooting


## DNS UTILs

```
kubectl apply -f https://k8s.io/examples/admin/dns/dnsutils.yaml
kubectl get pods dnsutils

kubectl exec -ti dnsutils -- nslookup kubernetes.default

```

- https://kubernetes.io/docs/tasks/administer-cluster/dns-debugging-resolution/

## Service Troubleshooting
- https://kubernetes.io/docs/tasks/debug-application-cluster/debug-service/
