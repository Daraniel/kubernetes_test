# Kubernetes Test

![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![MySQL](https://img.shields.io/badge/mysql-%2300f.svg?style=for-the-badge&logo=mysql&logoColor=white)
![Kubernetes](https://img.shields.io/badge/kubernetes-%23326ce5.svg?style=for-the-badge&logo=kubernetes&logoColor=white)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![UnitTest](https://github.com/Daraniel/kubernetes_test/actions/workflows/unittest.yml/badge.svg)](https://github.com/Daraniel/kubernetes_test/actions/workflows/unittest.yml)
[![Publish Docker image](https://github.com/Daraniel/kubernetes_test/actions/workflows/docker-publish.yml/badge.svg)](https://github.com/Daraniel/kubernetes_test/actions/workflows/docker-publish.yml)

A sample Python FastAPI application that has user management system and user inventory and can be deployed with Docker
or Kubernetes. It uses SQLAlchemy to work with both SQLLite (direct execution and execution with docker compose) and
MYSQL (In Kubernetes) databases. The repository contains an auto formatter using Black and will run the tests on pull
request and push. The code also uses persistent volumes for its logs.

This project uses pre-commit hooks to make sure code is formatted correctly, to set it up, install pre-commit (either
run `pip/conda install pre-commit` or install the project dependencies `src/server/requirements.txt` file). After
installing pre-commit, install it on the current project by running `pre-commit install`. It will then run the
pre-commit script everytime something gets committed. If wanted, pre-commit can also be executed against all files by
running the `pre-commit run --all-files` command. Please note that the first run of pre-commit might take some time as
it needs to setup some codes.

## Project Parameters

The following environment variables can be set to configure the project:

| Name                        | Description                                                                             | Default Value           |
|-----------------------------|-----------------------------------------------------------------------------------------|-------------------------|
| ACCESS_TOKEN_EXPIRE_MINUTES | The number of minutes before an access token expires.                                   | 30                      |
| SECRET_KEY                  | A secret key used for encrypting and decrypting data.                                   | a random value          |
| DATABASE_CONNECTION_STRING  | The connection string for the MySQL database.                                           | sqlite:///./database.db |
| LOG_CFG                     | The path to the log configuration file.                                                 | ./configs/log_conf.yaml |
| LOG_PATH                    | The path to the directory where log files will be stored, used in the default log_conf. | ./logs                  |

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

Then it can be accessed by creating a tunnel:

```bash
minikube tunnel --cleanup
```

Sometimes the tunneling doesn't work, it this case, make sure no other app is using the same port (8000) and try
restarting Minikube and recreating the services.
Alternatively, the following command can be used to directly tunnel the service:

```bash
minikube service fastapi-server
```

If needed, the services can be deleted using the following command:

```bash
kubectl delete ingress fastapi-server
kubectl delete service fastapi-server
kubectl delete service fastapi-mysql
kubectl delete deployment fastapi-server
kubectl delete deployment fastapi-mysql
kubectl delete pvc fastapi-server-claim
kubectl delete pvc mysql-pv-claim
```

### Logging

When executed with Kubernetes, the code uses persistent storage for logging, this means that the logs won't get deleted
when the pod is deleted. To access the logs folder, first ssh into Minikube and then check the persistent storage folder
in it. This can be done as follows:

```bash
minikube ssh
cd ../../var/hostpath-provisioner/default/fastapi-server-claim/logs
```

in this folder each pod will have a folder named after it that will contain its logs.

Furthermore, the logging config file supports using environment variables.

While using docker-compose, the logs will be written to the `src/server/logs` folder in the host system.

### Development tips:

Set the image type in the Kubernetes config file to `IfNotPresent` (instead of `Always`) to make it use the local Docker
images (instead of pulling the image from Docker hub).
