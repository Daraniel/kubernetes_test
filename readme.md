# Kubernetes Test

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
![Kubernetes](https://img.shields.io/badge/kubernetes-%23326ce5.svg?style=for-the-badge&logo=kubernetes&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![MySQL](https://img.shields.io/badge/mysql-%2300f.svg?style=for-the-badge&logo=mysql&logoColor=white)
[![UnitTest](https://github.com/Daraniel/kubernetes_test/actions/workflows/python-package.yml/badge.svg)](https://github.com/Daraniel/kubernetes_test/actions/workflows/python-package.yml)
[![Publish Docker image](https://github.com/Daraniel/kubernetes_test/actions/workflows/docker-publish.yml/badge.svg)](https://github.com/Daraniel/kubernetes_test/actions/workflows/docker-publish.yml)

A sample Python FastAPI application that has user management system and user inventory and can be deployed with Docker
or Kubernetes. It uses SQLAlchemy to work with both SQLLite (direct execution and execution with docker compose) and
MYSQL (In Kubernetes) databases. The repository contains an auto formatter using Black and will run the tests on pull
request and push.

## Docker setup

Create the image with and push it to the repo (replace daraniel with your repo name when needed/applicable, it includes
replacing it in the commands, in the [docker-compose.yml](docker-compose.yml)
file, [deploy_and_serve.yaml](kubernetes_resources/deploy_and_serve.yaml), [deployment.yaml](kubernetes_resources/deployment.yaml),
and [service.yaml](service.yaml) Kubernetes
deployment config files)

```bash
docker build --pull -t daraniel/kubernetes-test-server:master ./src/server --push
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

> [!IMPORTANT]  
> If Ingress isn't setup, please refer to the instruction
> in [the Ingress section of setup_minikube.md file](setup_minikube.md#ingress) on how to set it up, incorrect setup and
> be troublesome and lead to strange behavior.


After starting Minikube, set up the Deployment and Server for MYSQL server and Deployment, Service, and Ingress for the
code by running the following line of code:

```bash
kubectl apply -k ./kubernetes_resources
```

```bash
kubectl delete deployment fastapi-server
```

Then it can be accessed by creating a tunnel:

```bash
minikube tunnel --cleanup
```

If needed, the services can be deleted using the following command:

```bash
kubectl delete ingress fastapi-server
kubectl delete service fastapi-server
kubectl delete service fastapi-mysql
kubectl delete deployment fastapi-server
kubectl delete deployment fastapi-mysql
#kubectl delete pvc fastapi-server-claim
kubectl delete pvc mysql-pv-claim
```
