# Instructions on how to use Minikube


## How to setup Minikube

Start minikube with

```bash
minikube start
```

The first run might take some time as it will pull the base image for docker, and then it will create a docker container
using it.

After it finishes, start a new terminal and leave this running:

```bash
minikube dashboard
```

It will launch the minikube dashboard in a browser window. It can alternatively be used with `--url` flag which will
only show the dashboard url and won't open the browser.

It is better to enable the metrics-server addon to have more features in the dashboard using the following command:

```bash
minikube addons enable metrics-server
```

If minikube is complaining about not finding the default docker context, The current active docker context can be set to be the default context with the following command:

```bash
docker context use default
```

Minikube can be paused with the following command:

```bash
minikube pause
```

And it can be unpaused with the following command:

```bash
minikube unpause
```

Minikube can then be stopped by running the following command:

```bash
minikube stop
```

Also, the minikube VM can be deleted using the following command:

```bash
minikube delete
```

or it can be used with the `--all` flag


## How to deploy an image   

### Create a Deployment
Run a test container image that includes a webserver

```bash
#kubectl create deployment fastapi-server --image=registry.k8s.io/e2e-test-images/agnhost:2.39 -- /agnhost netexec --http-port=8080
kubectl create deployment fastapi-server --image=daraniel/kubernetes-test-server:1.0 --http-port=8080
```

or use the following command to deploy using a deployment.yaml file:

```bash
kubectl apply -f ./deployment.yaml
```

Alternatively, the following command can be used to deploy and serve the image:

```bash
kubectl apply -f ./deploy_and_serve.yaml
```

View the Deployment:

```bash
kubectl get deployments
```

Display info about the Deployment:

```bash
kubectl describe deployment fastapi-server
```

View the Pod:

```bash
kubectl get pods
```

Display info about the Pod, note that the pod id changes in each execution:

```bash
kubectl describe pod fastapi-server-5bc57bd589-dqgmr
```

View cluster events:

```bash
kubectl get events
```

View the kubectl configuration:

```bash
kubectl config view
```

View application logs for a container in a pod:

```bash
kubectl logs fastapi-server-5bc57bd589-dqgmr
```

### Create a Service

Expose the Pod to the public internet:

```bash
kubectl expose deployment fastapi-server --type=LoadBalancer --port=8080
```

or alternatively run the following command:

```bash
kubectl apply -f ./service.yaml
```

View the Service:

```bash
kubectl get services
```

Run the server using the following command:

```bash
minikube service fastapi-server
```

It will list the app 

### Cleanup

Delete the service and deployment with:

```bash
kubectl delete service fastapi-server
kubectl delete deployment fastapi-server
# kubectl delete pod fastapi-server-5bc57bd589-dqgmr
```
