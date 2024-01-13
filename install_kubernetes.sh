sudo apt-get update

# install docker
sudo apt-get install docker.io -y
docker --version
# setup docker
sudo systemctl --user start docker
sudo systemctl --user enable docker

# install kubernetes depencandies
sudo apt-get install -y apt-transport-https ca-certificates curl

# get kubernetes public key (v1.29)
curl -fsSL https://pkgs.k8s.io/core:/stable:/v1.29/deb/Release.key | sudo gpg --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg
# add kubernetes apt repository (v1.29)
echo 'deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.29/deb/ /' | sudo tee /etc/apt/sources.list.d/kubernetes.list
sudo apt-get update

# install kubernetes
# sudo apt-get install -y kubectl
# alternatively install other kubernetes tools
sudo apt-get install -y kubeadm kubelet kubectl
kubeadm version

# install minikube
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube
