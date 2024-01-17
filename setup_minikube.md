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

If minikube is complaining about not finding the default docker context, The current active docker context can be set to
be the default context with the following command:

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

> [!IMPORTANT]  
> If deploying Ingress is intended, please fully read this file before trying it. Incorrect setup and be troublesome and
> lead to strange behavior. Alternatively, please first install [Ingress](#installing-ingress) first and then check the
> other sections.

### Create a Deployment

Run a test container image that includes a webserver

```bash
#kubectl create deployment fastapi-server --image=registry.k8s.io/e2e-test-images/agnhost:2.39 -- /agnhost netexec --http-port=8080
kubectl create deployment fastapi-server --image=daraniel/kubernetes-test-server:1.0 --http-port=8080
```

or use the following command to deploy using a deployment.yaml file:

```bash
kubectl apply -f ./kubernetes_resources/deployment.yaml
```

Alternatively, the following command can be used to deploy and serve the image:

```bash
kubectl apply -f ./kubernetes_resources/deploy_and_serve.yaml
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

SSH into a pod:

```bash
kubectl exec -it  fastapi-server-5bc57bd589-dqgmr -- bash  
```

### Create a Service

Expose the Pod to the public internet:

```bash
kubectl expose deployment fastapi-server --type=LoadBalancer --port=8080
```

or alternatively run the following command:

```bash
kubectl apply -f ./kubernetes_resources/service.yaml
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

### Ingress

> [!IMPORTANT]  
> Please fully read this section before trying it out. Incorrect setup and be troublesome and lead to strange behavior.

#### Installing Ingress

First enable Ingress in Minikube. To do so first ssh into minikube and set up ip link:

```bash
minikube ssh 
sudo ip link set docker0 promisc on 
```

Then enable ingress and ingress-dns addons:

```bash
minikube addons enable ingress
minikube addons enable ingress-dns
```

If on Windows, update openssh (to a version equal or newer than 8.1) by running the following command as admin:

```bash
choco install openssh
 ```

At the time of writing this file, the latest non-beta version on choco is 8.0 so install a beta version as follows:

```bash
choco install openssh --pre 
 ```

Or install a specific version as (recommended way IMO):

```bash
choco install openssh --version=8.6.0-beta1 --pre 
```

#### Using Ingress

Now the code can be deployed using Ingress, in this case, run the following command:

```bash
kubectl apply -f ./kubernetes_resources/deploy_and_serve.yaml
```

Please note that in this file, we are using the LoadBalancer service type instead of the NodePort used in the
stand-alone service file.

Now you can get Ingresses, please note that it might take some time for the Ingress instance to start and get an
address:

```bash
kubectl get ingress
```

Tunnel to Minikube to get access to Ingress:

```bash
minikube tunnel
```

or with the `--cleanup` flag:

```bash
minikube tunnel --cleanup
```

Now the app should be accessible, in Linux, the ip can be found using

```bash
minikube ip
```

but in Windows it doesn't seem to work, and it would use the ip address that's printed when running
the `minikube tunnel` command (in my case, 127.0.0.1).

Then the app can be accessed in the browser with the following link (replace ip with your ip) http://127.0.0.1:8000/docs

If wanted, the host name `fastapi-host.com` can be assigned to this ip address in the host file of your os.

Getting things to work might be troublesome and error prone, one way to get it to work would be to delete minikube and
then setup ingress first then start deploying things. It can be done with the following command:

> [!CAUTION]  
> RUNNING THIS LINE WILL DELETE EVERYTHING IN MINIKUBE AND WILL RESET IT

```bash
minikube delete  
```

Ingress, service and deployment can all be deployed together by running the following command:

```bash
kubectl apply -f ./kubernetes_resources/deploy_and_serve.yaml
```

### Port forwarding

Ports can be forwarded to a deployment using the following line:

```bash
kubectl port-forward deployment/fastapi-server 8000:8000
```

Or to a service using:

```bash
kubectl port-forward service/fastapi-server 8000:8000
```

Or to a specific pod using:

```bash
 kubectl port-forward fastapi-server-5bc57bd589-dqgmr 8000:8000 
```

Then the forwarded thing can be accessed on that port.

Another method to access things is using porxy as below but this use case is not explored in this app.

```bash
kubectl proxy
```

### Cleanup

Delete the service and deployment with:

```bash
kubectl delete service fastapi-server
kubectl delete deployment fastapi-server
```

Delete the ingress, service and deployment with:

```bash
kubectl delete ingress fastapi-server
kubectl delete service fastapi-server
kubectl delete deployment fastapi-server
```

Also pods can be deleted as below but it isn't needed as pods are managed internally by the deployment and get
automatically deleted when the deployment gets deleted:

```bash
kubectl delete pod fastapi-server-5bc57bd589-dqgmr
```
