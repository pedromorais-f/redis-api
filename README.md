# Redis PUB/SUB Application using MNIST Dataset

Docker Hub Images Repository: <a href="https://hub.docker.com/repository/docker/pmoraisf/redis-api/general" >Docker Repository<a/>

## ABOUT Images

MAIN IMAGE: A Subscriber that will receive an image, pre-process this image and in the final, will be an input
to the model and then will generate the prediction.After all this pipeline, this will be a Publisher and will
publish the image prediction in other channel

SUBSCRIBER IMAGE: A Subscriber that will receive the prediction

PUBLISHER IMAGE: Only for test, this publisher have some images that can be send and then receive a
prediction

## Env Variables
<ul>
    <li>REDIS_HOST</li>
    <li>REDIS_PASSWORD (If your Redis-Server don`t have a password, let that env variable empty)</li>
    <li>USER (Only for publishers image test)</li>
</ul>

## Execution

Start a Redis Server, the port that is defined in this project is <strong>PORT=6379</strong>

Run the <strong>compose.yml</strong> to see the project running and after that execute the publisher file
with REDIS_HOST=localhost and REDIS_PASSWORD=""

CMD: docker compose up
