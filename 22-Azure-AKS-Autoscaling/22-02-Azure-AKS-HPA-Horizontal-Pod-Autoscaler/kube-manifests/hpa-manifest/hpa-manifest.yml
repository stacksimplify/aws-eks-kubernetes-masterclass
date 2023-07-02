apiVersion: autoscaling/v1
kind: HorizontalPodAutoscaler
metadata:
  name: hpa-demo-declarative
spec:
  maxReplicas: 10 # define max replica count
  minReplicas: 1  # define min replica count
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: hpa-demo-deployment
  targetCPUUtilizationPercentage: 20 # target CPU utilization