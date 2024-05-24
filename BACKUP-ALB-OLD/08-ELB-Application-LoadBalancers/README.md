# Load Balancing workloads on EKS using AWS Application Load Balancer

## Topics
- We will be looking in to this topic very extensively in a step by step and module by module model. 
- The below will be the list of topics covered as part of AWS ALB Ingress Controller


| S.No  | Topic Name |
| ------------- | ------------- |
| 1.  | ALB Ingress Controller Installation  |
| 2.  | ALB Ingress Basics  |
| 3.  | ALB Ingress Context Path based Routing  |
| 4.  | ALB Ingress SSL  |
| 5.  | ALB Ingress SSL Redirect (HTTP to HTTPS) |
| 6.  | ALB Ingress External DNS |


## References: 
- Good to refer all the below for additional understanding.

### ALB Pre-requisite Setup - References: 
- https://github.com/kubernetes-sigs/aws-alb-ingress-controller
- Examples:
  - https://github.com/kubernetes-sigs/aws-alb-ingress-controller/tree/master/docs/examples/2048

### AWS ALB Ingress Annotations Reference
- https://kubernetes-sigs.github.io/aws-alb-ingress-controller/guide/ingress/annotation/

### eksctl getting started
- https://eksctl.io/introduction/#getting-started

### External DNS
- https://github.com/kubernetes-sigs/external-dns
- https://github.com/kubernetes-sigs/external-dns/blob/master/docs/tutorials/alb-ingress.md
- https://github.com/kubernetes-sigs/external-dns/blob/master/docs/tutorials/aws.md