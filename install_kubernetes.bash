# install docker
winget install -e --id Docker.DockerDesktop --accept-source-agreements --accept-package-agreements

# install Kubernetes
winget install -e --id Kubernetes.kubectl
kubectl version --client

# Enable shell autocompletion
kubectl completion powershell | Out-String | Invoke-Expression
kubectl completion powershell >> $PROFILE

cd ~
mkdir .kube
cd .kube
New-Item config -type file

# install minikube
winget install minikube

## verify installation
#kubectl cluster-info
#kubectl cluster-info dump
