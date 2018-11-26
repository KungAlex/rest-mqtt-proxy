.. rest-mqtt-proxy documentation master file, created by
   sphinx-quickstart on Fri Nov 16 00:53:16 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.



=========
Getting-Started
=========

This section contains installation instructions and numerous tutorials that cover basic use cases of rest-mqtt-proxy.


Install
--------

You can use prebuild Docker image or clone this Repo and build from source build:

   clone
   make build

   to see all available commands type: make help

Docker
--------

docker pull kungalex/rest-mqtt-proxy
docker run -it -p 5000:5000 kungalex/rest-mqtt-proxy

Kubernetes
----------

kubectl apply -f k8s-example/

