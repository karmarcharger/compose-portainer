
[![Docker Image Size](https://badgen.net/docker/size/karmarcharger/docker-compose-to-portainer-json?icon=docker&label=image%20size)](https://hub.docker.com/r/karmarcharger/docker-compose-to-portainer-json-march)
# compose-portainer
Python Flask app to convert compose to portainer.json
![image](https://github.com/karmarcharger/compose-portainer/assets/10364143/d957519c-9953-4dcb-abed-74ebf661c0bc)



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
