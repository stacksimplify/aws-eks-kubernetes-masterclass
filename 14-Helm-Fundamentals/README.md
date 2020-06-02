## Step-01: Install the Helm CLI
```
curl -sSL https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3 | bash
helm version --short
```

## Step-02: 

```
helm repo add stable https://kubernetes-charts.storage.googleapis.com/
helm repo update
```

## Step-03:  NOT CLEAR ABOUT THIS STEP
```
helm completion bash >> ~/.bash_completion
. /etc/profile.d/bash_completion.sh
. ~/.bash_completion
source <(helm completion bash)
```