# Kubernetes Test

A sample Python FastAPI application that can be deployed with Docker or Kubernetes.

## Docker setup

Create the image with

```bash
docker build --pull -t daraniel/kubernetes-test-server:latest ./src/server
```

then push it to the repo (replace daraniel with your repo name when needed/applicable, it includes replacing it in the commands, in the docker-compose.yml file, deploy_and_serve.yaml and deployment.yaml Kubernetes deployment config files)

```bash
docker image push daraniel/kubernetes-test-server 
```

If you want, you can serve the app with docker compose as follows:


```bash
docker compose -f docker-compose.yml -p kubernetes-test up -d
```

## Kubernetes setup

First setup and start Minikube/Kubernetes, you can refer to install Kubernetes.bash/sh files to check for commands to install Kubernetes. Also, setup_minikube.md file contains more info about how to set up and use Minikube to run Kubernetes locally.

After installing Minikube, it can be started with

```bash
minikube start
```

and stopped by :

```bash
minikube stop
```

After starting Minikube, deploy the code using:

```bash
kubectl apply -f ./deploy_and_serve.yaml
```

Then it can be explored with proxy:

```bash
kubectl proxy
```

