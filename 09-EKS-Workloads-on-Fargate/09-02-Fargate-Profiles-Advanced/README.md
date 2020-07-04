# Create 3 environments using Namespaces

## Step-01: What are we going to learn?
- We are going to learn about writing Fargate Profiles using YAML wherein with YAML we can create multiple fargate profiles at a time. 
- Understand about `namespaces and labels` in `fargate profiles`

## Step-02: Create Advanced Fargate Profile with yml

### Create Fargate Profile manifest
```yml
apiVersion: eksctl.io/v1alpha5
kind: ClusterConfig

metadata:
  name: eksdemo1
  region: us-east-1

fargateProfiles:
  - name: fp-stage-profile
    selectors:
      - namespace: fp-stage
  - name: fp-prod-profile
    selectors:
      - namespace: fp-prod
        labels:
          runon: fargate     
```

## Step-03: Create Fargate Profiles
```
eksctl create fargateprofile -f kube-manifests/01-fargate-profiles.yml
```

## Step-04:  Get list of Fargate profiles
```
# List Fargate profiles
eksctl get fargateprofile --cluster eksdemo1

# View in yaml format
eksctl get fargateprofile --cluster eksdemo1 -o yaml
```
