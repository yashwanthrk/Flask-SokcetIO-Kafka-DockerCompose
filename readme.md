# Radar Kafka

## Horizontal scaling of websockets using KAFKA

- Tech Stack : Flask, Kafka and Socket.IO

```bash
$ First change the path in start.sh file
```

### To start the Kafka and Python server

```bash
$ ./start.sh -u
```

### To stop the Kafka and Python server

```bash
$ ./start.sh -d
```

Good to go!

## Optional (Not neccessary) - For educatiional purpose :p

To add the Docker network:
 - this is need for kafka broker to communicate with python servers
```bash
$ docker network rm kafka-network
```


- Spin up the local single-node Kafka cluster (will run in the background):

```bash
$ docker-compose -f docker-compose.yml up -d
```

- Check the cluster is up and running (wait for "started" to show up):

```bash
$ docker-compose -f docker-compose.yml logs -f broker | grep "started"
```

- Start the Python Producer and Consumer server (will run in the background):

```bash
$ docker-compose -f prod-consumer-docker/docker-compose.yml up -d
```

## Stopping

To stop the Python Producer and Consumer server:

```bash
$ docker-compose -f prod-consumer-docker/docker-compose.yml down -v
```

To stop the Kafka cluster:

```bash
$ docker-compose -f docker-compose.yml down -v
```

To remove the Docker network:

```bash
$ docker network rm kafka-network
```
