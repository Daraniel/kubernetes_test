# Kubernetes Test

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A sample Python FastAPI application that can be deployed with Docker or Kubernetes. The repository contains an auto
formatter using Black and will run the tests on pull request and push.

## Docker setup

Create the image with and push it to the repo (replace daraniel with your repo name when needed/applicable, it includes
replacing it in the commands, in the [docker-compose.yml](docker-compose.yml)
file, [deploy_and_serve.yaml](deploy_and_serve.yaml), [deployment.yaml](deployment.yaml),
and [service.yaml](service.yaml) Kubernetes
deployment config files)

```bash
docker build --pull -t daraniel/kubernetes-test-server:latest ./src/server --push
```

If you want, you can serve the app with docker compose as follows:

```bash
docker compose -f docker-compose.yml -p kubernetes-test up -d
```

## Kubernetes setup

First setup and start Minikube/Kubernetes, you can refer to install Kubernetes.bash/sh files to check for commands to
install Kubernetes. Also, [setup_minikube.md](setup_minikube.md) file contains more info about how to set up and use
Minikube to run Kubernetes locally.

After installing Minikube, it can be started with

```bash
minikube start
```

and stopped by:

```bash
minikube stop
```

After starting Minikube, setup Ingress and then deploy the code using:

> [!IMPORTANT]  
> If Ingress isn't setup, please refer to the instruction
> in [the Ingress section of setup_minikube.md file](setup_minikube.md#ingress) on how to set it up, incorrect setup and
> be troublesome and lead to strange behavior.

```bash
kubectl apply -f ./deploy_and_serve.yaml
```

Then it can be accessed by creating a tunnel:

```bash
minikube tunnel --cleanup
```
