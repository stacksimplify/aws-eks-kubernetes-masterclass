# DevOps for Applications

## Step-01: Get Cluster Certificate Authority Data
```
# Export Cluster Name
export EKS_CLUSTER_NAME=eksdemo1
echo $EKS_CLUSTER_NAME

# Get Cluster Certificate Authority Data
aws eks describe-cluster --region us-east-1 --name $EKS_CLUSTER_NAME --query cluster.certificateAuthority.data
```

## Step-02: Get Cluster Host Address
```
# Get Cluster Host Host Address
aws eks describe-cluster --region us-east-1 --name $EKS_CLUSTER_NAME --query cluster.endpoint
```

## Step-03: Get Secrets Name & Authorization Token
```
# Get Secrets
kubect get secrets

# Export Secret Name
export SECRET_NAME=default-token-ghwjn
echo $SECRET_NAME

# Get Authorization Token
kubectl get secret $SECRET_NAME -o json | jq -r '.data["token"]' | base64 -d
```