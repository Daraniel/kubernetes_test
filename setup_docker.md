Either use docker compose to setup the project which will also create the image or manually create the image using the
following line of code:

```bash
docker build --pull -t daraniel/kubernetes-test-server:master ./src/server
```

or by running docker compose directly:

```bash
docker compose -f docker-compose.yml -p kubernetes-test up -d
```

you should log in to docker if you haven't already:

```bash
docker login
```

then push the image (it's needed for using the image in kubernetes):

```bash
docker image push daraniel/kubernetes-test-server 
```

then if needed, you can pull the image as follows:

```bash
docker compose pull 
```

or

```bash
docker pull daraniel/kubernetes-test-server
```
