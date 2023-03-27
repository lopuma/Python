#!/bin/bash
#docker run -it -v /var/run/docker.sock:/var/run/docker.sock lbctl-container "$@"
docker run -it lbctl-container "$@"
