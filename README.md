# up
INFS3208 Project

# Deployment

```bash
docker stack deploy -c docker-compose.yml -c docker-compose.override.yml up
```

Scaling celery workers:

```bash
docker service scale up_celery_worker=2
```