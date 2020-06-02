# Deploy Workloads to Fargate Serverless

## Step-01: Introduction
- Fargate profiles are immutable by design, to change something we need to create new profile.

## Step-02: Create EKS Cluster with Fargate profile
```
eksctl create cluster -f V1-Fargate-Profiles/01-cluster-fargate.yml
```
```yml
apiVersion: eksctl.io/v1alpha5
kind: ClusterConfig

metadata:
  name: eksdemo-fargate
  region: us-east-1

fargateProfiles:
  - name: fp-default
    selectors:
      # All workloads in the "default" Kubernetes namespace will be
      # scheduled onto Fargate:
      - namespace: default
      # All workloads in the "kube-system" Kubernetes namespace will be
      # scheduled onto Fargate:
      - namespace: kube-system
  - name: fp-dev
    selectors:
      # All workloads in the "dev" Kubernetes namespace matching the following
      # label selectors will be scheduled onto Fargate:
      - namespace: dev
        labels:
          env: dev     
```
### Get list of Fargate profiles
```
# List Fargate profiles
eksctl get fargateprofile --cluster eksdemo1

# View in yaml format
eksctl get fargateprofile --cluster eksdemo1 -o yaml
```

## Step-03: Deploy our Workloads
```
kubectl apply -f V1-ALB-Ingress-ExternalDNS-FargateProfile-Basic/ -namespace dev
```

### Delete Fargate Profile
```
eksctl delete fargateprofile --cluster eksdemo1 --name fp-dev --wait
```

```
Step-1
eksctl utils associate-iam-oidc-provider \
    --region us-east-1 \
    --cluster eksdemo-fargate \
    --approve

Step-2: IAM Poolicy ALB    
# Make a note of Policy ARN    
Policy ARN:  arn:aws:iam::411686525067:policy/ALBIngressControllerIAMPolicy

Step-3: RBAC Role
kubectl apply -f https://raw.githubusercontent.com/kubernetes-sigs/aws-alb-ingress-controller/master/docs/examples/rbac-role.yaml

Step-4: IAM Role to Service Account Mapping
eksctl create iamserviceaccount \
    --region us-east-1 \
    --name alb-ingress-controller \
    --namespace kube-system \
    --cluster eksdemo-fargate \
    --attach-policy-arn arn:aws:iam::411686525067:policy/ALBIngressControllerIAMPolicy \
    --override-existing-serviceaccounts \
    --approve


Step-5: Install ingress
kubectl apply -f https://raw.githubusercontent.com/kubernetes-sigs/aws-alb-ingress-controller/master/docs/examples/alb-ingress-controller.yaml

Step-6: Edit Ingress to add cluster name
kubectl edit deployment.apps/alb-ingress-controller -n kube-system
# Replaced cluster-name with our cluster-name
    spec:
      containers:
      - args:
        - --ingress-class=alb
        - --cluster-name=eksdemo-fargate
        - --aws-vpc-id=vpc-08eb32dba47f7f24f
        - --aws-region=us-east-1        

Step-7: 
kubectl get pods -n kube-system
kubectl logs -f $(kubectl get po -n kube-system | egrep -o 'alb-ingress-controller-[A-Za-z0-9-]+') -n kube-system     


## External DNS
Step-01: Make a note of Policy ARN
arn:aws:iam::411686525067:policy/AllowExternalDNSUpdates

Step-02: Create IAM Role 
eksctl create iamserviceaccount \
    --name external-dns \
    --namespace default \
    --cluster eksdemo-fargate \
    --attach-policy-arn arn:aws:iam::411686525067:policy/AllowExternalDNSUpdates \
    --approve \
    --override-existing-serviceaccounts

Step-03: Make a note of Role ARN created and update in 

Step-04: Update ExternalDNS Deployment file with Role ARN and Deploy External DNS
01-Deploy-ExternalDNS.yml

kubectl apply -f V2-Deploy-ExternalDNS/01-Deploy-ExternalDNS.yml
kubectl logs -f $(kubectl get po | egrep -o 'external-dns[A-Za-z0-9-]+')

## Update Application Templates and Deploy
Step-01: Update Ingress yaml file
alb.ingress.kubernetes.io/target-type: ip (Under internet-facging annotation)

Step-02: Deploy
kubectl apply -f V3-ALB-Ingress-ExternalDNS-FargateProfile-fp-default/

Step-03: Access Applications
```

