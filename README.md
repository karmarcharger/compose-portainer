
[![Docker Image Size](https://badgen.net/docker/size/karmarcharger/docker-compose-to-portainer-json?icon=docker&label=image%20size)](https://hub.docker.com/r/karmarcharger/docker-compose-to-portainer-json-march)
# compose-portainer
Python Flask app to convert compose to portainer.json
![image](https://github.com/karmarcharger/compose-portainer/assets/10364143/ed014c63-bd84-4c51-8dfe-c3e83f2fd4a8)


you can use https://www.composerize.com/ to convert your docker run commands to docker compose before throwing it into the text box

WIP
```
#docker run command if you want to just run it on docker instead of installing python
docker run -p 8082:8082 karmarcharger/docker-compose-to-portainer-json-march:latest
```
Docker compose
```
version: '3.3'
services:
    docker-compose-to-portainer-json:
        ports:
            - '8082:8082'
        image: 'karmarcharger/docker-compose-to-portainer-json-march:latest'
```
