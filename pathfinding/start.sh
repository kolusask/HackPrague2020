#!/bin/bash
app="pathfinding"
docker build -t ${app} .
docker run -p 5000:8080 \
  --name=${app} \
  -v $PWD:/app \
  --env-file ./env.txt \
  ${app}
