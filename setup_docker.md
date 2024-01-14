Either use docker compose to setup the project which will also create the image or manually create the image using the following line of code:

```bash
docker build --pull -t kubernetes-test-server:1.0 ./src/server
```

running docker compose directly:

```bash
docker compose -f docker-compose.yml -p kubernetes-test up -d
```
