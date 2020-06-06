# Microservices with AWS AppMesh

## AppMesh
```
Mesh: microservices
```
## Tried with CloudMap - failed
```
VN: notification-vnode
notification-service.zetaoptdev.com
VS: notification-service.zetaoptdev.com
```
```
VN: usermgmt-vnode
usermanagement-service.zetaoptdev.com
BACKEND: notification-service.zetaoptdev.com
VS: usermanagement-service.zetaoptdev.com
```
## Trying with Route 53 DNS A Record
```
VN: notification-vnode
notification.appmesh.microdev.com
VS: notification.appmesh.microdev.com
```
```
VN: usermgmt-vnode
usermgmt.appmesh.microdev.com
BACKEND: notification.appmesh.microdev.com
VS:usermgmt.appmesh.microdev.com
```

## Mesh naming
```
VN: notification-vnode
notification.mesh1.local
VS: notification.mesh1.local
```
```
VN: usermgmt-vnode
usermgmt.mesh1.local
BACKEND: notification.mesh1.local
VS:usermgmt.mesh1.local
```


## Trying with CloudMap & Services  - Failed with Unknown Host
```
VN: notification-vnode
notification.microserv.com
VS: notification.microserv.com
```
```
VN: usermgmt-vnode
usermgmt.microserv.com
BACKEND: notification.microserv.com
VS:usermgmt.microserv.com
```
 
 ## Trying with Route 53 DNS A Record - Failed but not Unknown Host
```
VN: notification-vnode
notification.microdev.com
VS: notification.microdev.com
```
```
VN: usermgmt-vnode
usermgmt.microdev.com
BACKEND: notification.microdev.com
VS:usermgmt.microdev.com
```

## Trying with EKS cluster pod names

```
VN: notification-vnode
notification.default.svc.cluster.local
VS: notification.default.svc.cluster.local
```
```
VN: usermgmt-vnode
usermgmt.default.svc.cluster.local
BACKEND: notification.default.svc.cluster.local
VS:usermgmt.default.svc.cluster.local
```

