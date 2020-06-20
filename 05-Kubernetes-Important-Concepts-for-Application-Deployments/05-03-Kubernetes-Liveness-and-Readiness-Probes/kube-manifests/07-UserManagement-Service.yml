apiVersion: v1
kind: Service
metadata:
  name: usermgmt-restapp-service
  labels: 
    app: usermgmt-restapp
spec:
  type: NodePort
  selector:
    app: usermgmt-restapp
  ports: 
    - port: 8095
      targetPort: 8095
      nodePort: 31231
