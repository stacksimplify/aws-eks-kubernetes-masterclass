# ALB Install Ingress Controller

## Step-01: Introduction
- Create k8s rbac role & Service Account for ALB Ingress Controller, for that we will create three  objects in k8s. Refer file `ALBIngress-rbac-roles.yml` for more details.
  - ClusterRole
  - ServiceAccount
  - ClusterRoleBinding
- Create IAM Policy with access to AWS Services (EC2, ELB, IAM, Cognito, WAF, Shield, Certificate Manager etc - All AWS Services in relation with AWS Application Load Balancer)  
- Associate the k8s service account, AWS IAM Policy by creating a AWS IAM Role
- Finally deploy ALB Ingress Controller and Test if that respective POD is finally running


## Step-02: Create a Kubernetes service account named alb-ingress-controller in the kube-system namespace
- We are using master branch instead of v1.1.4 
```
# List Service Accounts
kubectl get sa -n kube-system

# Create ClusterRole, ClusterRoleBinding & ServiceAccount
kubectl apply -f https://raw.githubusercontent.com/kubernetes-sigs/aws-alb-ingress-controller/master/docs/examples/rbac-role.yaml

# List Service Accounts
kubectl get sa -n kube-system

# Describe Service Account alb-ingress-controller 
kubectl describe sa alb-ingress-controller -n kube-system
```
- **Output**
```log
Kalyans-MacBook-Pro:aws-fargate-eks-masterclass kdaida$ kubectl describe sa alb-ingress-controller -n kube-system
Name:                alb-ingress-controller
Namespace:           kube-system
Labels:              app.kubernetes.io/name=alb-ingress-controller
Annotations:         kubectl.kubernetes.io/last-applied-configuration:
                       {"apiVersion":"v1","kind":"ServiceAccount","metadata":{"annotations":{},"labels":{"app.kubernetes.io/name":"alb-ingress-controller"},"name...
Image pull secrets:  <none>
Mountable secrets:   alb-ingress-controller-token-rs8c6
Tokens:              alb-ingress-controller-token-rs8c6
Events:              <none>
```

## Step-03: Create IAM Policy for ALB Ingress Controller

### Create IAM Policy
- **Why this policy:** This IAM policy will allow our ALB Ingress Controller pod to make calls to AWS APIs
- **ISSUE:** With `iam-policy.json` aws provided we have an issue, so created manually using AWS Management Console. 
- **IAM Policy Creation:** Create manually using AWS management console and give full access to ELB
- Go to Services -> IAM -> Policies -> Create Policy
- Click on **JSON** tab and paste the content from `https://raw.githubusercontent.com/kubernetes-sigs/aws-alb-ingress-controller/master/docs/examples/iam-policy.json`
- Come back to **Visual Editor**
- Add ELB full access  
  - Click on **Add Additional Permissions**
    - **Service:** ELB
    - **Actions:** All ELB actions (elasticloadbalancing:*)
    - **Resources:** All Resources
- Remove ELB which has warnings
  - Click on **Remove**
- Click on **Review Policy**
  - **Name:**  ALBIngressControllerIAMPolicy
  - **Description:** This IAM policy will allow our ALB Ingress Controller pod to make calls to AWS APIs
- Click on **Create Policy**

```
# NOT WORKING AS ON TODAY DUE TO ERRORS IN iam-policy.json 
# Create IAM Policy
aws iam create-policy \
    --policy-name ALBIngressControllerIAMPolicy \
    --policy-document https://raw.githubusercontent.com/kubernetes-sigs/aws-alb-ingress-controller/master/docs/examples/iam-policy.json
```
### Make a note of Policy ARN    
- Make a note of Policy ARN as we are going to use that in next step when creating IAM Role.
```
Policy ARN:  arn:aws:iam::180789647333:policy/ALBIngressControllerIAMPolicy
```

## Step-04: Create an IAM role for the ALB Ingress Controller and attach the role to the service account 
- Applicable only with `eksctl` managed clusters
- This command will create an AWS IAM role and bounds that to Kubernetes service account

```
# Template
eksctl create iamserviceaccount \
    --region region-code \
    --name alb-ingress-controller \  #Note:  K8S Service Account Name that need to be bound to newly created IAM Role
    --namespace kube-system \
    --cluster prod \
    --attach-policy-arn arn:aws:iam::111122223333:policy/ALBIngressControllerIAMPolicy \
    --override-existing-serviceaccounts \
    --approve

# Replaced region, name, cluster and policy arn (Policy arn we took note in step-03)
eksctl create iamserviceaccount \
    --region us-east-1 \
    --name alb-ingress-controller \
    --namespace kube-system \
    --cluster eksdemo1 \
    --attach-policy-arn arn:aws:iam::180789647333:policy/ALBIngressControllerIAMPolicy \
    --override-existing-serviceaccounts \
    --approve
```

### Verify using eksctl cli
```
# Get IAM Service Account
eksctl  get iamserviceaccount --cluster eksdemo1
```

### Verify CloudFormation Template eksctl created & IAM Role
- Goto Services -> CloudFormation
- **CFN Template Name:** eksctl-eksdemo1-addon-iamserviceaccount-kube-system-alb-ingress-controller
- Click on **Resources** tab
- Click on link in **Physical Id** to open the IAM Role
- Verify it has **ALBIngressControllerIAMPolicy** associated

### Verify k8s Service Account
```
# Describe Service Account alb-ingress-controller 
kubectl describe sa alb-ingress-controller -n kube-system
```
- **Observation:** You can see that newly created Role ARN is added in `Annotations` confirming that **AWS IAM role bound to a Kubernetes service account**
- **Output**
```log
Kalyans-MacBook-Pro:aws-fargate-eks-masterclass kdaida$ kubectl describe sa alb-ingress-controller -n kube-system
Name:                alb-ingress-controller
Namespace:           kube-system
Labels:              app.kubernetes.io/name=alb-ingress-controller
Annotations:         eks.amazonaws.com/role-arn: arn:aws:iam::180789647333:role/eksctl-eksdemo1-addon-iamserviceaccount-kube-Role1-1Y1T391CKSSR1
                     kubectl.kubernetes.io/last-applied-configuration:
                       {"apiVersion":"v1","kind":"ServiceAccount","metadata":{"annotations":{},"labels":{"app.kubernetes.io/name":"alb-ingress-controller"},"name...
Image pull secrets:  <none>
Mountable secrets:   alb-ingress-controller-token-rs8c6
Tokens:              alb-ingress-controller-token-rs8c6
Events:              <none>
```

## Step-05: Deploy ALB Ingress Controller
- We are using Master branch file instead of 1.1.4, so that we can use latest ALB Ingress Controller
```
# Deploy ALB Ingress Controller
kubectl apply -f https://raw.githubusercontent.com/kubernetes-sigs/aws-alb-ingress-controller/master/docs/examples/alb-ingress-controller.yaml

# Verify Deployment
kubectl get deploy -n kube-system
```

## Step-06: Edit ALB Ingress Controller Manifest
- Edit ALB Ingress Controller manifest and add clustername field `- --cluster-name=eksdemo1`
```
# Edit Deployment
kubectl edit deployment.apps/alb-ingress-controller -n kube-system

# Template file  
    spec:
      containers:
      - args:
        - --ingress-class=alb
        - --cluster-name=cluster-name

# Replaced cluster-name with our cluster-name eksdemo1
    spec:
      containers:
      - args:
        - --ingress-class=alb
        - --cluster-name=eksdemo1
```

## Step-07: Verify our ALB Ingress Controller is running. 
- Verify for the pod starting with `alb-ingress-controller`
- We will know if all our above steps are working or not in our next section **08-02-ALB-Ingress-Basic**, if ALB not created then we something is wrong.
```
# Verify if alb-ingress-controller pod is running
kubectl get pods -n kube-system

# Verify logs
kubectl logs -f $(kubectl get po -n kube-system | egrep -o 'alb-ingress-controller-[A-Za-z0-9-]+') -n kube-system
```
