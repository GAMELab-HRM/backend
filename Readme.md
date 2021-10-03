# Backend 
this project is out Backend system(using docker-compose)

## Requirements
- [docker](https://docs.docker.com/get-docker/)
- [docker-compose](https://docs.docker.com/compose/install/)

## Build enviroment
```shell
# start
CURRENT_UID=$(id -u):$(id -g) docker-compose up
```

* restful-server (fastAPI)
    * address `127.0.0.1:8080`
* HTTP service(Nginx)
    * address `0.0.0.0:80`

---
## Github container registry
> After changing your code, please use following commands to **build & upload your docker images to github registry.**
```shell
cd /your/project/folder
docker build -t $IMAGE_NAME . 
docker tag $IMAGE_ID docker.pkg.github.com/gamelab-hrm/backend/$PROJECT_NAME:$VERSION
docker push docker.pkg.github.com/gamelab-hrm/backend/$PROJECT_NAME:$VERSION
```

## Vscode docker extension (great~!)
https://code.visualstudio.com/docs/remote/containers
