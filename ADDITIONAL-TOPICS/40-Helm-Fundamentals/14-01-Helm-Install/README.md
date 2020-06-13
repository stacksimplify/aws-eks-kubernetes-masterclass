# Helm Basics

## Step-01: Helm Install
```
curl -sSL https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3 | bash
helm version --short
```

## Step-02: Configure our first chart Repository & Update it
- Chart repositories change frequently due to updates and new additions. 
- To keep Helm’s local list updated with all these changes, we need to regularly run the repository update command.
```
helm repo add stable https://kubernetes-charts.storage.googleapis.com/
helm repo update
```

## Step-03: Search Repo
```
helm search repo stable
```

## Step-04: Helm Bash Completion


- Reference: https://helm.sh/docs/helm/helm_completion/