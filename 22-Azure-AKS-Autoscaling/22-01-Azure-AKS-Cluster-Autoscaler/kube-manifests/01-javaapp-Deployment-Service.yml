apiVersion: apps/v1
kind: Deployment
metadata:
  name: cluster-autoscaler-demoapp-deployment
  labels:
    app: ca-java-app
spec:
  replicas: 1
  selector:
    matchLabels:
      app: ca-java-app
  template:
    metadata:
      labels:
        app: ca-java-app
    spec:
      containers:
      - name: ca-java-app
        #image: stacksimplify/kubenginx:1.0.0
        image: stacksimplify/kube-helloworld:1.0.0
        ports:
        - containerPort: 8080
        resources:
          requests:
            memory: "200Mi"
            cpu: "250m"
          limits:
            memory: "500Mi"
            cpu: "500m"                  
---
apiVersion: v1
kind: Service
metadata:
  name: cluster-autoscaler-demoservice-java-app
  labels:
    app: ca-java-app
spec:
  type: LoadBalancer
  selector:
    app: ca-java-app
  ports:
  - port: 80
    targetPort: 8080   