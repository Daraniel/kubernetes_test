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

