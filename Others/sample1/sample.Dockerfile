FROM ubuntu:latest

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        python \
        git && \
    rm -rf /var/lib/apt/list/*

RUN u