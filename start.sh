
#!/bin/sh
export BACKEND_PATH='/home/yashwanth/Flask-SokcetIO-Kafka-DockerCompose'

if [ "$1" = "-u" ]; then
  docker network create kafka-network
  docker-compose -f ${BACKEND_PATH}/docker-compose.yml up -d
  docker-compose -f ${BACKEND_PATH}/prod-consumer-docker/docker-compose.yml up 

elif [ "$1" = "-d" ]; then
  docker network rm kafka-network
  docker-compose -f ${BACKEND_PATH}/docker-compose.yml down -v
  docker-compose -f ${BACKEND_PATH}/prod-consumer-docker/docker-compose.yml down -v
  
  #Pulling fresh image from hub and won't use the cache version that is prebuild
elif [ "$1" = "-r" ]; then
  docker-compose -f ${BACKEND_PATH}/docker-compose.yml down -v
  docker-compose -f ${BACKEND_PATH}/prod-consumer-docker/docker-compose.yml down -v
  docker network rm kafka-network
  docker network create kafka-network
  docker-compose -f ${BACKEND_PATH}/docker-compose.yml build --no-cache
  docker-compose -f ${BACKEND_PATH}/prod-consumer-docker/docker-compose.yml build --no-cache
  docker-compose -f ${BACKEND_PATH}/docker-compose.yml up -d
  docker-compose -f ${BACKEND_PATH}/prod-consumer-docker/docker-compose.yml up 
  
#Rebuilding only python docker server
elif [ "$1" = "-p" ]; then
  docker-compose -f ${BACKEND_PATH}/prod-consumer-docker/docker-compose.yml down -v
  docker-compose -f ${BACKEND_PATH}/prod-consumer-docker/docker-compose.yml build --no-cache
  docker-compose -f ${BACKEND_PATH}/prod-consumer-docker/docker-compose.yml up 
fi
